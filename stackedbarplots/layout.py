# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,line-too-long,arguments-differ, wrong-import-position, unnecessary-pass, protected-access
"""Module contains LayoutEngine class for arranging figure and axis elements.

LayoutEngine child class is called at draw time for the plot, and aims
to rearrange the Axis/Axes on the Figure (as well as Axis elements) to
produce a "pleasing layout" (see https://matplotlib.org/stable/api/layout_engine_api.html).
A custom LayoutEngine is defined to allow more control of plot elements
(as the structure of BarPlots do not need the flexibility required from
matplotlib tight/constrained LayoutEngines), and to move layout code
out of core.py.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

import warnings
import matplotlib.layout_engine
from matplotlib.figure import Figure
import matplotlib.transforms as mtransforms

if TYPE_CHECKING: from .core import StackedBarplot
from .defaults import Auto_Style_Calculations, DEFAULT_LEGEND_STYLE


__all__ = [
    "StackedBarLayoutEngine"
]

#TODO: Stop using self.plot.fig/ax and use fig param instead.


class StackedBarLayoutEngine(matplotlib.layout_engine.LayoutEngine):
    """
    Matplotlib layout engine for figures created by the StackedBarplot library.

    Once this layout enging is attached to the StackedBarplot library, the layout
    engine ``execute`` function is called at draw time, providing a special draw-time
    hook (see https://matplotlib.org/stable/api/layout_engine_api.html). The 
    execution of this layout engine follows a specific pipeline:

    1. Align bar value annotations,
    2. align the plot legend with the rest of the figure decorations,
    3. align the plot's paratext (i.e., title and subtitle), and
    4. calculate the margins and overall size of the figure.
    """
    def __init__(self, plot:StackedBarplot) -> None:
        super().__init__()
        self.plot = plot
        self.fig_size_settings = {}

        self._adjust_compatible = True
        self._colorbar_gridspec = False


    def execute(self, fig:Figure) -> None:
        """Perform layout algorithm and move and resize axis and axis elements accordingly."""
        self.layout_bar_labels(fig)
        if self.plot.get_legend_style()["show"]: self.layout_legend(fig)
        if self.plot.get_fig_style()["title"] is not None or self.plot.get_fig_style()["subtitle"]: self.layout_paratext(fig)
        self.size_figure(fig)


    def set(self) -> None:
        """Required override, but redundant in this context."""

        warnings.warn("You are attempting to set or configure elements of" \
        "the plot's LayoutEngine. This LayoutEngine does not support such" \
        "customisation and acts only as a codespace for a rigid layout " \
        "algorithm. Calling this method is redundant.")
        raise NotImplementedError


    def layout_bar_labels(self, fig:Figure):
        """Layout figure bar value annotations."""
        x_pixels_per_unit = self.plot.ax.transData.get_matrix()[0, 0]
        padding_data_coords = self.plot.get_bar_val_label_style()["padding"]/x_pixels_per_unit

        for series_index, c in enumerate(self.plot.ax.containers):

            #Positioning bar value labels
            for category_index, (rect, val) in enumerate(zip(c.patches, c.datavalues)):

                y = rect.get_y() + rect.get_height() / 2 #Center annotation object to the bar vertically
                an = self.plot.ax._bar_labels[series_index][category_index]

                #Set general purpose bar value annotation padding
                if self.plot.get_bar_val_label_style()["align"] == "centre":
                    x = rect.get_x() + rect.get_width() / 2
                elif self.plot.get_bar_val_label_style()["align"] == "left":
                    x = rect.get_x() + padding_data_coords
                elif self.plot.get_bar_val_label_style()["align"] == "right":
                    x = rect.get_x() + rect.get_width() - padding_data_coords
                else: raise ValueError("Incompatible value for bar value label alignment.")
                an.xy = (x, y)

                #3 of padding added to font. If font isn't centered, font padding also needs to be to font width when calculating overlap with bar.
                if self.plot.get_bar_val_label_style()["align"] != "centre": 
                    font_width = abs(an.get_window_extent().width) + self.plot.get_bar_val_label_style()["padding"] + 3
                else: 
                    font_width = abs(an.get_window_extent().width) + 3
                bar_width = abs(rect.get_window_extent().width)

                #Threshold for first and last bar on a row; if value is below threshold, move label to outside of bar
                if self.plot.get_bar_val_label_style()["expelsqueezedends"] is True:
                    if series_index == 0 and font_width > bar_width:
                        an.set_ha("right")
                        an.xy = (rect.get_x() - padding_data_coords, y)
                        an.set_color(self.plot.get_bar_val_label_style()["fontcolour"])

                        #If the annotation has been placed overlapping with category ticks, the category ticks are padded by the required amount.
                        if an.get_window_extent().x0 < self.plot.ax.get_window_extent().x0:
                            shift_px = self.plot.ax.get_window_extent().x0 - an.get_window_extent().x0
                            self.plot.ax.tick_params(axis="y", pad=shift_px)

                    elif series_index == len(self.plot.series_labels)-1 and font_width > bar_width:
                        an.set_ha("left")
                        an.xy = (rect.get_x() + rect.get_width() + padding_data_coords, y)
                        an.set_color(self.plot.get_bar_val_label_style()["fontcolour"])

                #Hide bar data annotation if squeezed and style dictates it is to be hidden.
                if self.plot.get_bar_val_label_style()["hidesqueezed"] is not None:
                    if self.plot.get_bar_val_label_style()["hidesqueezed"] == "all" and font_width > bar_width:
                        an.set_visible(False)
                    elif self.plot.get_bar_val_label_style()["hidesqueezed"] == "inner-only" and (series_index not in (0, len(self.plot.series_labels)-1)) and font_width > bar_width:
                        an.set_visible(False)
                    else:
                        an.set_visible(True)
                else:
                    an.set_visible(True)


    def layout_legend(self, fig:Figure) -> None:
        """Layout plot legend to not overlap with plot peritext."""

        x_transform = self.plot.get_legend_style()["transform"][0]
        y_transform = self.plot.get_legend_style()["transform"][1]

        if "above-horizontal" in self.plot.get_legend_style()["placement"]:
            self.plot.ax.get_legend().set_bbox_to_anchor(
                list(DEFAULT_LEGEND_STYLE.placement_options[self.plot.get_legend_style()["placement"]][1]),
                transform=mtransforms.offset_copy(self.plot.ax.transAxes, fig=fig, y=y_transform + 5, x=x_transform, units="dots"),
            )
        elif "below-horizontal" in self.plot.get_legend_style()["placement"]:
            m_bottom_padd = 0
            if self.plot.get_axis_title_style()["xlabel"] is not None:
                m_bottom_padd += self.plot.ax.get_window_extent().y0 - self.plot.ax.xaxis.label.get_window_extent().y0
            else:
                labels = [label for label in self.plot.ax.get_xticklabels() if label.get_visible()]
                min_y0 = min(label.get_window_extent().y0 for label in labels)
                m_bottom_padd += self.plot.ax.get_window_extent().y0 - min_y0

            m_bottom_padd += 15

            self.plot.ax.get_legend().set_bbox_to_anchor(
                list(DEFAULT_LEGEND_STYLE.placement_options[self.plot.get_legend_style()["placement"]][1]),
                transform=mtransforms.offset_copy(self.plot.ax.transAxes, fig=fig, y=y_transform + (m_bottom_padd*-1), x = x_transform, units="dots"),
            )
        elif "right-vertical" in self.plot.get_legend_style()["placement"]:
            self.plot.ax.get_legend().set_bbox_to_anchor(
                list(DEFAULT_LEGEND_STYLE.placement_options[self.plot.get_legend_style()["placement"]][1]),
                transform=mtransforms.offset_copy(self.plot.ax.transAxes, fig=fig, x=x_transform + 15, y=y_transform, units="dots"),
            )


    def layout_paratext(self, fig:Figure) -> None:
        """Layout paratext around the figure (i.e., (sub)title)."""

        if self.plot.get_fig_style()["subtitle"] is not None:
            subtitle_pad = 0
            if self.plot.get_legend_style()["show"] and "above-horizontal" in self.plot.get_legend_style()["placement"]:
                subtitle_pad += self.plot.ax.get_legend().get_window_extent().y1 - self.plot.ax.get_window_extent().y1
                subtitle_pad += 10 #Add extra padding between legend and subtitle

            fig._subtitle.set_transform(mtransforms.IdentityTransform())
            fig._subtitle.set_position((fig.get_window_extent().width/2,
                                                self.plot.ax.get_window_extent().y1+subtitle_pad))

        if self.plot.get_fig_style()["title"] is not None:
            title_pad = 0
            if fig._subtitle is not None:
                title_pad += fig._subtitle.get_window_extent().y1 - self.plot.ax.get_window_extent().y1
                title_pad += 10 #Add extra padding between subtitle and title
            elif self.plot.get_legend_style()["show"] and "above-horizontal" in self.plot.get_legend_style()["placement"]:
                title_pad += self.plot.ax.get_legend().get_window_extent().y1 - self.plot.ax.get_window_extent().y1

            fig._suptitle.set_transform(mtransforms.IdentityTransform())
            fig._suptitle.set_position((fig.get_window_extent().width/2,
                                                   self.plot.ax.get_window_extent().y1+title_pad))


    def size_figure(self, fig:Figure):
        """Sets the size of the figure.
        
        Method will calculate the margins around the plot axes by, for
        each edge, subtracting the axes edge to the furthest Artist on
        that edge (e.g., subtracting the category heading y0 coordinate
        from the axes y0 coordinate). A padding is applied (defined in
        defaults.py) and the figure size is set."""

        if self.plot.get_fig_style()["size"] is None:
            desired_ax_width = Auto_Style_Calculations.calc_axis_width(len(self.plot.series_labels))*fig.dpi/2.54
            desired_ax_height = Auto_Style_Calculations.calc_axis_height(len(self.plot.category_headings))*fig.dpi/2.54
        else:
            desired_ax_width = self.plot.get_fig_style()["size"][0]
            desired_ax_height = self.plot.get_fig_style()["size"][1]

        m_left_px, m_right_px, m_top_px, m_bottom_px = 0, 0, 0, 0

        #Calculate left margin
        if self.plot.get_axis_title_style()["ylabel"] is not None:
            m_left_px += self.plot.ax.get_window_extent().x0 - self.plot.ax.yaxis.label.get_tightbbox().x0
        else:
            labels = [label for label in self.plot.ax.get_yticklabels() if label.get_visible()]
            min_x0 = min(label.get_window_extent().x0 for label in labels)
            m_left_px += self.plot.ax.get_window_extent().x0 - min_x0

        #Calculate right margin
        if self.plot.get_legend_style()["show"] and self.plot.get_legend_style()["placement"] == "right-vertical":
            m_right_px += self.plot.ax.get_legend().get_window_extent().x1 - self.plot.ax.get_window_extent().x1

        #Calculate top margin
        if self.plot.get_fig_style()["title"] is not None:
            m_top_px += self.plot.fig._suptitle.get_window_extent().y1 - self.plot.ax.get_window_extent().y1
        elif self.plot.get_fig_style()["subtitle"] is not None:
            m_top_px += self.plot.fig._subtitle.get_window_extent().y1 - self.plot.ax.get_window_extent().y1
        elif self.plot.get_legend_style()["show"] and self.plot.get_legend_style()["placement"] == "above-horizontal":
            m_top_px += self.plot.ax.get_legend().get_window_extent().y1 - self.plot.ax.get_window_extent().y1

        #Calculate bottom margin
        if self.plot.get_legend_style()["show"] and self.plot.get_legend_style()["placement"] == "below-horizontal":
            m_bottom_px += self.plot.ax.get_window_extent().y0 - self.plot.ax.get_legend().get_window_extent().y0
        elif self.plot.get_axis_title_style()["xlabel"] is not None:
            m_bottom_px += self.plot.ax.get_window_extent().y0 - self.plot.ax.xaxis.label.get_window_extent().y0
        else:
            labels = [label for label in self.plot.ax.get_xticklabels() if label.get_visible()]
            min_y0 = min(label.get_window_extent().y0 for label in labels)
            m_bottom_px += self.plot.ax.get_window_extent().y0 - min_y0

        #print(f"Axis bounds: {self.plot.ax.get_window_extent().bounds}")
        #print(f"Bottom margin: {m_bottom_px}, Left m: {m_left_px}, Top m: {m_top_px}, Right m: {m_right_px}")

        m_left_px += Auto_Style_Calculations.fig_left_pad
        m_right_px += Auto_Style_Calculations.fig_right_pad
        m_top_px += Auto_Style_Calculations.fig_top_pad
        m_bottom_px += Auto_Style_Calculations.fig_bottom_pad

        self.fig_size_settings["fig_width_px"] = m_left_px + desired_ax_width + m_right_px
        self.fig_size_settings["fig_height_px"] = m_top_px + desired_ax_height + m_bottom_px

        #See https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots_adjust.html
        self.fig_size_settings["left"] = m_left_px/self.fig_size_settings["fig_width_px"]
        self.fig_size_settings["right"] = (m_left_px+desired_ax_width)/self.fig_size_settings["fig_width_px"]
        self.fig_size_settings["bottom"] = m_bottom_px/self.fig_size_settings["fig_height_px"]
        self.fig_size_settings["top"] = (m_bottom_px + desired_ax_height)/self.fig_size_settings["fig_height_px"]

        fig.subplots_adjust(left=self.fig_size_settings["left"],
                            bottom=self.fig_size_settings["bottom"],
                            right=self.fig_size_settings["right"],
                            top=self.fig_size_settings["top"])

        fig.set_size_inches(self.fig_size_settings["fig_width_px"]/fig.dpi,
                            self.fig_size_settings["fig_height_px"]/fig.dpi)
