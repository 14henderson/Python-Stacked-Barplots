# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,line-too-long
"""Core module pertaining to stacked-barplots Python library.

Core module contains definition for class StackedBarplot, which defines
the properties and behaviours of plots created from stacked-barplots.py.
The StackedBarplot and StackedPlotStyle (defined in defaults.ph) classes 
maintain a one-to-one relationship.
"""

import os
import warnings
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

from .tools import cumu2d, ChartDataSorting
from .defaults import StackedPlotStyle, DEFAULT_LEGEND_STYLE, DEFAULT_BAR_STYLE


__all__ = [
    "StackedBarplot"
]




class StackedBarplot():
    """StackedBarplot object represents horizontal stacked barchart with given style.

    Each instance of StackedBarplot represents a single active plot. Class methods
    are categorised as methods setting style settings, drawing elemetns of the plot, 
    or relate to the plot as a whole (e.g., render(), show(), or save()). The intended
    pipeline of this class is instantiation -> configuration of chart style -> 
    calling of render() method -> calling of show() or save() method.

    Attributes:
        data: Dictionary of category headings and associated category integer or float 
            data. For example, {"Ages": [12, 3, 4, 1], ...}. Order of data list must follow
            order of series labels. 
        series_labels: List of string headings for series, to be (optionally) be displayed
            on legend.
        category_headings: List of string headings for data categories.
        fig: matplotlib.pyplot.figure object.
        ax: matplotlib.pyplot.axis object.
        style: StackedPlotStyle object representing the style of the current StackedBarplot instance.
    """

    def __init__(self, data:dict[str, list[float]], series_labels:list[str]):
        """Initializes the instance based on chart data and series labels.

        Args:
            data: Dictionary of chart data.
            series_labels: List of string headings for series used in chart.
            
        """

        if not isinstance(data, dict):
            raise ValueError("Argument data must be a dictionary of category headings and associated category integer or float data.")
        if not isinstance(series_labels, list):
            raise ValueError("Argument series_labels must be list of strings.")
        if len(list(data.values())[0]) != len(series_labels):
            raise ValueError("Length of data in each category must equal total number of series labels provided.")

        self.data = list(data.values())
        self.series_labels = series_labels
        self.category_headings = list(data.keys())

        self.fig = None
        self.ax = None

        self.style = StackedPlotStyle()
        #Method delegation setup, so that StackedBarplot object can call StackedPlotStyle methods directly
        self.style_methods = [f for f in dir(StackedPlotStyle) if not f.startswith("_")]
        self.style.bar_colours.grayscale_gradient(len(self.series_labels))


    def __getattr__(self, func_name):
        """Internal method; non-callable. Delegates method calls to StackedPlotStyle object if method is not defined in StackedBarplot."""
        def delegated_method(*args, **kwargs):
            if func_name in self.style_methods:
                return getattr(self.style, func_name)(*args, **kwargs)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{func_name}'")
        return delegated_method


    def set_style(self, style:StackedPlotStyle):
        """Applies a given StackedPlotStyle object to the current StackedBarplot plot.
        
        Args:
            style: Given StackedPlotStyle object that should be applied to the StackedBarplot plot.
        """
        if not isinstance(style, StackedPlotStyle): raise ValueError("Argument style must be of type StackedPlotStyle.")
        self.style = style

        #Bar colours must be generated after the data is provided, as the number of colours must match the number of categories
        self.style.bar_colours.gradient(len(self.series_labels), DEFAULT_BAR_STYLE.start_colour, DEFAULT_BAR_STYLE.end_colour, DEFAULT_BAR_STYLE.mid_colour)


    def render(self):
        """Renders the figure given current data and style configuration."""
        self._destroy_fig()
        self._render()
        self.style.unrendered_changes = False


    def show(self):
        """Displays all figures currently created in the plt environment."""

        if self.style.unrendered_changes:
            warnings.warn("You are attempting to display the figure before style changes " \
            "have been rendered. Beware that render() must be called on the StackedBarplot" \
            "object for any style changes to be displayed.")
        plt.show()


    def save(self,
             filename:str,
             transparent:bool=None,
             dpi='figure',
             bbox_inches='tight',
             pad_inches=0.1,
             fig_format:str="png"):
        """Saves rendered figure to file.

        See https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html for
        verbose detail of parameters. 

        Args:
            filename: The path and filename to save figure. Must be relative path.
            transparent: If True, the Axes patches will all be transparent. 
            dpi: The resolution in dots per inch. If 'figure', use the figure's dpi value.
            bbox_inches: Bounding box in inches: only the given portion of the figure is saved. 
                If 'tight', try to figure out the tight bbox of the figure.
            pad_inches: Amount of padding in inches around the figure when bbox_inches is 
                'tight'.
            fig_format: The file format, e.g. 'png', 'pdf', 'svg', ... The behavior when this is 
                unset is documented under fname.

        """
        if self.style.unrendered_changes:
            warnings.warn("You are attempting to save the figure before style changes " \
            "have been rendered. Beware that render() must be called on the StackedBarplot" \
            "object for any style changes to be displayed.")
        path = os.path.dirname(os.path.abspath(__file__))
        self.fig.savefig(os.path.join(path, filename),
                         transparent=transparent,
                         dpi=dpi,
                         bbox_inches=bbox_inches,
                         pad_inches=pad_inches,
                         format=fig_format)


    def _render(self):
        """Internal method. Internal method for rendering plot following render pipeline."""
        self._plot_bars()
        self._plot_bar_labels()
        self._plot_axes()
        if self.get_legend_style()["show"]:
            self._init_legend_markers()
            self._plot_legend()
        if self.get_vert_line_style()["show"]:
            self._plot_vert_line()
        self.fig.tight_layout()


    def _destroy_fig(self):
        """Destroys the current figure."""
        if self.fig is not None:
            #self.fig.clear()
            plt.close(self.fig)


    def _plot_bars(self):
        """Internal method. Renders bars and category headings according to stored style configuration."""
        self.fig, self.ax = plt.subplots(figsize=self.get_fig_style()["size"])

        middle_index = len(self.data[0]) // 2

        if self.get_fig_style()["sorted"] is not None:
            if self.get_fig_style()["sorted"] == "sum-asc":
                self.data, self.category_headings = ChartDataSorting.by_sum(self.data, self.category_headings, reverse=False)
            elif self.get_fig_style()["sorted"] == "sum-desc":
                self.data, self.category_headings = ChartDataSorting.by_sum(self.data, self.category_headings, reverse=True)
            elif self.get_fig_style()["sorted"] == "avg-asc":
                self.data, self.category_headings = ChartDataSorting.by_average(self.data, self.category_headings, reverse=False)
            elif self.get_fig_style()["sorted"] == "avg-desc":
                self.data, self.category_headings = ChartDataSorting.by_average(self.data, self.category_headings, reverse=True)
            elif self.get_fig_style()["sorted"] == "lhlf-asc":
                self.data, self.category_headings = ChartDataSorting.by_left_half(self.data, self.category_headings, reverse=False)
            elif self.get_fig_style()["sorted"] == "lhlf-desc":
                self.data, self.category_headings = ChartDataSorting.by_left_half(self.data, self.category_headings, reverse=True)
            elif self.get_fig_style()["sorted"] == "rhlf-asc":
                self.data, self.category_headings = ChartDataSorting.by_right_half(self.data, self.category_headings, reverse=False)
            elif self.get_fig_style()["sorted"] == "rhlf-desc":
                self.data, self.category_headings = ChartDataSorting.by_right_half(self.data, self.category_headings, reverse=True)

        data_cum = cumu2d(self.data)

        offsets = [0]*len(self.data)
        if self.get_bar_style()["align"] == "centre":
            offsets = []
            for(row_index, row) in enumerate(self.data):
                if len(self.data[0]) % 2 == 0:
                    offsets.append(sum(self.data[row_index][0:middle_index]))
                else:
                    offsets.append(sum(self.data[row_index][0:middle_index]) + self.data[row_index][middle_index]/2)

        for col_index, (colname, colour) in enumerate(zip(self.series_labels, self.style.bar_colours.get_normalised_gradient_list())):
            widths = [bar_data[col_index] for bar_data in self.data]
            starts = [bar_data[col_index] for bar_data in data_cum]

            for bar_index, width in enumerate(widths):
                if self.get_bar_style()["align"] == "left":
                    starts[bar_index] = starts[bar_index]-widths[bar_index]
                elif self.get_bar_style()["align"] == "centre":
                    starts[bar_index] = starts[bar_index]-widths[bar_index]-offsets[bar_index]
                elif self.get_bar_style()["align"] == "right":
                    raise NotImplementedError("Right-aligned bars not yet implemented")
                else:
                    raise ValueError("Invalid alignment value, must be 'left', 'centre', or 'right'")
            self.ax.barh(self.category_headings,
                                 widths,
                                 left=starts,
                                 height=self.get_bar_style()["height"],
                                 color = colour,
                                 label=colname,
                                 zorder=1)

        for tick in self.ax.get_yticklabels(): tick.set_fontfamily(self.style.get_fig_style()["fontfamily"])
        self.fig.set_facecolor(self.style.get_fig_style()["backgroundcolour"])
        self.ax.set_facecolor(self.style.get_fig_style()["backgroundcolour"])

        if self.style.get_vert_line_style()["show"]: self.ax.axvline(0, linestyle="--", color="black", alpha=0.25, zorder=0)


    def _plot_bar_labels(self):
        """Internal method. Renders plot bar value annotations according to stored style configuration."""

        for series_index, c in enumerate(self.ax.containers):

            #Positioning bar value labels
            for category_index, (rect, val) in enumerate(zip(c.patches, c.datavalues)):
                text = str.format(self.get_bar_val_label_style()["format"], val)

                ha = "center" #Point on the annotation object that is aligned to the given coordinates. Horizontal can change depending on whether annotations are left or right aligned.
                y = rect.get_y() + rect.get_height() / 2 #Center annotation object to the bar vertically
                x = None #To be set based on alignment and threshold settings

                #Transforming padding from display coordinate space to data space.
                x_pixels_per_unit = self.ax.transData.get_matrix()[0, 0]
                padding_data_coords = self.get_bar_val_label_style()["padding"]/x_pixels_per_unit

                #Normal alignment for all other bars, or if no outside-of-bar threshold is set
                if self.get_bar_val_label_style()["align"] == "centre":
                    x = rect.get_x() + rect.get_width() / 2
                elif self.get_bar_val_label_style()["align"] == "left":
                    x = rect.get_x() + padding_data_coords
                    ha = "left"
                elif self.get_bar_val_label_style()["align"] == "right":
                    x = rect.get_x() + rect.get_width() - padding_data_coords
                    ha = "right"

                #Set font colour and handle colour inverting (if style setting is set)
                font_colour = self.get_bar_val_label_style()["fontcolour"]
                if self.get_bar_val_label_style()["colourinvert"]:
                    luminence = 0.2126*rect.get_facecolor()[0] + 0.7152*rect.get_facecolor()[1] + 0.0722*rect.get_facecolor()[2]
                    if luminence < 0.2: font_colour = "white"
                    elif luminence > 0.8: font_colour = "black"

                #Create annotation object (needed for measuring width differences to bar)
                an = self.ax.annotate(
                    text,
                    (x, y),
                    textcoords="offset points",
                    xytext=(0, 0),
                    ha=ha, va="center",
                    fontsize=self.get_bar_val_label_style()["fontsize"],
                    color=font_colour,
                    fontfamily=self.get_fig_style()["fontfamily"],
                    annotation_clip=False
                    )

                #3 of padding added to font. If font isn't centered, font padding also needs to be to font width when calculating overlap with bar.
                if self.get_bar_val_label_style()["align"] != "centre": font_width = abs(an.get_window_extent().width) + self.get_bar_val_label_style()["padding"] + 3
                else: font_width = abs(an.get_window_extent().width) + 3
                bar_width = abs(rect.get_window_extent().width)

                #Threshold for first and last bar on a row; if value is below threshold, move label to outside of bar
                if self.get_bar_val_label_style()["expelsqueezedends"] is True:
                    if series_index == 0 and font_width > bar_width:
                        an.set_ha("right")
                        an.xy = (rect.get_x() - padding_data_coords, y)
                        an.set_color(self.get_bar_val_label_style()["fontcolour"])

                        #If the annotation has been placed overlapping with category ticks, the category ticks are padded by the required amount.
                        if an.get_window_extent().x0 < self.ax.get_window_extent().x0:
                            shift_px = self.ax.get_window_extent().x0 - an.get_window_extent().x0
                            self.ax.tick_params(axis="y", pad=shift_px)

                    elif series_index == len(self.data[0])-1 and font_width > bar_width:
                        an.set_ha("left")
                        an.xy = (rect.get_x() + rect.get_width() + padding_data_coords, y)
                        an.set_color(self.get_bar_val_label_style()["fontcolour"])

                #Hide bar data annotation if squeezed and style dictates it is to be hidden.
                if self.get_bar_val_label_style()["hidesqueezed"] is not None:
                    if self.get_bar_val_label_style()["hidesqueezed"] == "all" and font_width > bar_width:
                        an.set_visible(False)
                    elif self.get_bar_val_label_style()["hidesqueezed"] == "inner-only" and (series_index not in (0, len(self.data[0])-1)) and font_width > bar_width:
                        an.set_visible(False)

        self.ax.invert_yaxis() #Required for some reason?


    def _plot_axes(self):
        """Internal method. Renders and applies plot labels/title and axes settings according to stored style configuration."""
        if not self.get_axis_style()["yaxisshow"]: self.ax.yaxis.set_visible(False)
        if not self.get_axis_style()["xaxisshow"]: self.ax.xaxis.set_visible(False)
        else:
            if self.get_axis_style()["xlim"] is not None:
                self.ax.set_xlim(self.get_axis_style()["xlim"])
                if self.get_axis_style()["step"] is not None:
                    self.ax.set_xticks([i for i in range(self.get_axis_style()["xlim"][0], self.get_axis_style()["xlim"][1]+1, self.get_axis_style()["step"])])
            if self.get_axis_style()["xaxisabs"]:
                self.ax.xaxis.set_major_formatter(lambda x, pos: self.get_axis_style()["xaxisformat"].format(abs(x))) #Absolute x ticks
            else:
                self.ax.xaxis.set_major_formatter(lambda x, pos: self.get_axis_style()["xaxisformat"].format(x))
            self.ax.tick_params(axis='x', labelsize=int(self.get_axis_style()["xfontsize"]), labelfontfamily=self.get_fig_style()["fontfamily"])

        self.ax.tick_params(axis='y', labelsize=int(self.get_axis_style()["yfontsize"]), labelfontfamily=self.get_fig_style()["fontfamily"])

        if not self.get_fig_style()["spinedisplay"][0]: self.ax.spines['left'].set_visible(False)
        if not self.get_fig_style()["spinedisplay"][1]: self.ax.spines['top'].set_visible(False)
        if not self.get_fig_style()["spinedisplay"][2]: self.ax.spines['right'].set_visible(False)
        if not self.get_fig_style()["spinedisplay"][3]: self.ax.spines['bottom'].set_visible(False)

        if self.get_fig_style()["title"] is not None:
            self.ax.set_title(self.get_fig_style()["title"],
                              fontsize=self.get_fig_style()["titlefontsize"],
                              color=self.get_fig_style()["titlecolour"],
                              fontfamily=self.get_fig_style()["fontfamily"])
        if self.get_axis_title_style()["xlabel"] is not None:
            self.ax.set_xlabel(self.get_axis_title_style()["xlabel"],
                               fontsize=self.get_axis_title_style()["axislabelfontsize"],
                               color=self.get_axis_title_style()["axislabelfontcolour"],
                               fontfamily=self.get_fig_style()["fontfamily"])
        if self.get_axis_title_style()["ylabel"] is not None:
            self.ax.set_ylabel(self.get_axis_title_style()["ylabel"],
                               fontsize=self.get_axis_title_style()["axislabelfontsize"],
                               color=self.get_axis_title_style()["axislabelfontcolour"],
                               fontfamily=self.get_fig_style()["fontfamily"])

        self.ax.tick_params(axis='y', which='major', left=False, right=False)


    def _plot_legend(self):
        """Internal method. Renders a plot legend according to stored style configuration."""
        if "horizontal" in self.get_legend_style()["placement"]: ncol = len(self.series_labels)
        else: ncol = 1

        bbox_to_anchor = list(DEFAULT_LEGEND_STYLE.placement_options[self.get_legend_style()["placement"]][1])
        bbox_to_anchor[0] += self.get_legend_style()["transform"][0]
        bbox_to_anchor[1] += self.get_legend_style()["transform"][1]

        self.ax.legend(handles=self.get_legend_style()["markers"],
                       ncol=ncol,
                       bbox_to_anchor=bbox_to_anchor,
                       loc=DEFAULT_LEGEND_STYLE.placement_options[self.get_legend_style()["placement"]][0],
                       fontsize=self.get_legend_style()["fontsize"],
                       labelspacing = self.get_legend_style()["spacing"],
                       labelcolor=self.get_legend_style()["fontcolour"],
                       facecolor=self.get_legend_style()["backgroundcolour"],
                       edgecolor = self.get_legend_style()["bordercolour"],
                       framealpha=1,
                       shadow=False)


    def _plot_vert_line(self):
        """Internal method. Renders a vertical plot line according to stored style configuration."""
        if self.get_vert_line_style()["zorder"] == "front": z = 2
        elif self.get_vert_line_style()["zorder"] == "behind": z = 0
        else: raise ValueError("Vertical line zorder must be either 'front' or 'behind'.")

        self.ax.axvline(0,
                        linestyle=self.get_vert_line_style()["linestyle"],
                        color=self.get_vert_line_style()["colour"],
                        alpha=self.get_vert_line_style()["alpha"],
                        zorder=z)


    def _init_legend_markers(self):
        """Defines and stores legend markers.
        
        Method defines legend marker colours according to (previously) 
        initialised bar colours. Called by _render()."""

        self.set_legend_markers([])
        markers_temp = []
        for i, cat in enumerate(self.series_labels):
            markers_temp.append(
                mlines.Line2D([],
                [],
                color=self.style.bar_colours.get_normalised_gradient_list()[i],
                marker=self.get_legend_style()["markershape"],
                linestyle='None',
                markersize=10,
                label=cat))
        self.set_legend_markers(markers_temp)
