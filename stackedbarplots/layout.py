# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,line-too-long,arguments-differ, wrong-import-position, unnecessary-pass
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

if TYPE_CHECKING: from .core import StackedBarplot
from .defaults import Auto_Style_Calculations


__all__ = [
    "StackedBarLayoutEngine"
]




class StackedBarLayoutEngine(matplotlib.layout_engine.LayoutEngine):
    """
    Matplotlib layout engine for figures created by the StackedBarplot library.

    Once this layout enging is attached to the StackedBarplot library, the layout
    engine ``execute`` function is called at draw time, providing a special draw-time
    hook (see https://matplotlib.org/stable/api/layout_engine_api.html). The 
    execution of this layout engine follows a specific pipeline, padding figure
    decorations outward from the axes. The order is as follows.

    1. The plot's axes
    2. x and y axes ticks (including category labels)
    3. Peritext (i.e., axis labels if shown)
    4. Plot legend (if shown)
    5. Paratext (i.e., subtitle then title if shown)
    6. Resizing of the figure itself
    """
    def __init__(self, plot:StackedBarplot) -> None:
        super().__init__()
        self.plot = plot
        self.fig_size_settings = {}

        self._adjust_compatible = True
        self._colorbar_gridspec = False


    def execute(self, fig:Figure) -> None:
        """Perform layout algorithm and move and resize axis and axis elements accordingly."""
        #Required to ensure the layout engine size_figure is only being called once.
        if len(self.fig_size_settings.keys()) == 0:
            self.layout_legend(fig)
            self.layout_paratext(fig)
            self.size_figure(fig)


    def set(self) -> None:
        """Required override, but redundant in this context."""

        warnings.warn("You are attempting to set or configure elements of" \
        "the plot's LayoutEngine. This LayoutEngine does not support such" \
        "customisation and acts only as a codespace for a rigid layout " \
        "algorithm. Calling this method is redundant.")
        raise NotImplementedError


    def layout_legend(self, fig:Figure) -> None:
        """Layout plot legend to not overlap with plot peritext."""
        pass


    def layout_paratext(self, fig:Figure) -> None:
        """Layout paratext around the figure (i.e., (sub)title)."""
        pass


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
        labels = [label for label in self.plot.ax.get_yticklabels() if label.get_visible()]
        min_x0 = min(label.get_window_extent().x0 for label in labels)
        m_left_px += self.plot.ax.get_window_extent().x0 - min_x0

        #Calculate right margin
        if self.plot.get_legend_style()["show"] and self.plot.get_legend_style()["placement"] == "vertical-right":
            m_right_px += self.plot.ax.get_legend().get_window_extent().x1 - self.plot.ax.get_window_extent().x1

        #Calculate top margin
        if self.plot.get_legend_style()["show"] and self.plot.get_legend_style()["placement"] == "horizontal-top":
            m_top_px += self.plot.ax.get_legend().get_window_extent().width
            #TODO: Take into account title and subtitle

        #Calculate bottom margin
        if self.plot.get_legend_style()["show"] and self.plot.get_legend_style()["placement"] == "horizontal-bottom":
            m_bottom_px += self.plot.ax.get_window_extent().x0 - self.plot.ax.get_legend().get_window_extent().x0
        else:
            m_bottom_px += self.plot.ax.get_window_extent().y0 - self.plot.ax.xaxis.get_window_extent().y0

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
