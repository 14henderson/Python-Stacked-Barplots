# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,line-too-long,protected-access
"""Core module pertaining to stacked-barplots Python library.

Core module contains definition for class StackedBarplot, which defines
the properties and behaviours of plots created from stacked-barplots.py.
The StackedBarplot and StackedPlotStyle (defined in defaults.ph) classes 
maintain a one-to-one relationship.
"""

import os
import warnings
from pathlib import Path

import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.text
from matplotlib import font_manager


from .defaults import DEFAULT_BAR_STYLE, DEFAULT_LEGEND_STYLE, DEFAULT_AXIS_STYLE, StackedPlotStyle
from .layout import StackedBarLayoutEngine
from .tools import ChartDataSorting, cumu2d

__all__ = [
    "StackedBarplot"
]


font_manager.fontManager.addfont(str(Path(os.path.dirname(os.path.realpath(__file__)), "fonts/LiberationSans-Regular.ttf"))) #Can this be outside the class?
font_manager.fontManager.addfont(str(Path(os.path.dirname(os.path.realpath(__file__)), "fonts/LiberationSans-Bold.ttf")))
font_manager.fontManager.addfont(str(Path(os.path.dirname(os.path.realpath(__file__)), "fonts/LiberationSans-Italic.ttf")))




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
        """Applies a given StackedPlotStyle object to the current StackedBarplot plot, and sets plot default styles.
        
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
        self._set_font_style()

        self._plot_bars()
        self._plot_bar_labels()
        self._plot_axes()
        self._plot_peritext()

        if self.get_legend_style()["show"]:
            self._plot_legend()
        if self.get_vert_line_style()["show"]:
            self._plot_vert_line()

        self._plot_paratext()

        self.fig.canvas.draw()



    def _destroy_fig(self):
        """Destroys the current figure."""
        if self.fig is not None:
            #self.fig.clear()
            plt.close(self.fig)


    def _set_font_style(self):
        plt.rcParams["font.family"] = self.get_fig_style()["fontfamily"]
        plt.rcParams["font.weight"] = self.get_fig_style()["fontweight"]
        plt.rcParams["axes.labelweight"] = self.get_fig_style()["fontweight"]
        plt.rcParams["figure.titleweight"] = self.get_fig_style()["titleweight"]


    def _plot_bars(self):
        """Internal method. Renders bars and category headings according to stored style configuration."""
        self.fig, self.ax = plt.subplots()

        layout_engine = StackedBarLayoutEngine(self)
        self.fig.set_layout_engine(layout_engine)

        middle_index = len(self.series_labels) // 2

        if self.get_fig_style()["sorted"] is not None: #TODO: There has to be a better way to do this!
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
                if len(self.series_labels) % 2 == 0:
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

        self.fig.set_facecolor(self.style.get_fig_style()["backgroundcolour"])
        self.ax.set_facecolor(self.style.get_fig_style()["backgroundcolour"])

        if self.style.get_vert_line_style()["show"]: self.ax.axvline(0, linestyle="--", color="black", alpha=0.25, zorder=0)

        if self.get_axis_style()["xaxisgridlines"]:
            self.ax.tick_params(axis='x', which="major", tick1On=False, tick2On=False)
            self.ax.set_axisbelow(True)
            self.ax.grid(visible=True, axis="x", zorder=-1, which="major", color=DEFAULT_AXIS_STYLE.x_axis_gridlines_colour)
        else:
            self.ax.tick_params(axis='x', which="major", tick1On=True, tick2On=False)
            self.ax.grid(visible=False, axis="x")


    def _plot_bar_labels(self):
        """Internal method. Renders plot bar value annotations according to stored style configuration."""
        self.ax._bar_labels = []

        for series_index, c in enumerate(self.ax.containers):
            self.ax._bar_labels.append([])

            #Positioning bar value labels
            for category_index, (rect, val) in enumerate(zip(c.patches, c.datavalues)):
                text = str.format(self.get_bar_val_label_style()["format"], val)

                ha = "center" #Point on the annotation object that is aligned to the given coordinates. Horizontal can change depending on whether annotations are left or right aligned.
                y = rect.get_y() + rect.get_height() / 2 #Center annotation object to the bar vertically

                #This will be overwritten by StackedBarLayoutEngine
                if self.get_bar_val_label_style()["align"] == "centre":
                    x = rect.get_x() + rect.get_width() / 2
                elif self.get_bar_val_label_style()["align"] == "left":
                    x = rect.get_x()
                    ha = "left"
                elif self.get_bar_val_label_style()["align"] == "right":
                    x = rect.get_x() + rect.get_width()
                    ha = "right"
                else: raise ValueError("Incompatible value for bar value label alignment.")

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
                    annotation_clip=False
                    )
                self.ax._bar_labels[series_index].append(an)
        self.ax.invert_yaxis() #Required for some reason?


    def _plot_peritext(self):
        """Internal method. Draws peritext (i.e., text of the axis) including axes ticks and axes labels."""

        if self.get_axis_title_style()["xlabel"] is not None:
            self.ax.set_xlabel(self.get_axis_title_style()["xlabel"],
                               labelpad=5,
                               fontsize=self.get_axis_title_style()["axislabelfontsize"],
                               color=self.get_axis_title_style()["axislabelfontcolour"],
                               )

        if self.get_axis_title_style()["ylabel"] is not None:
            self.ax.set_ylabel(self.get_axis_title_style()["ylabel"],
                               labelpad=0,
                               fontsize=self.get_axis_title_style()["axislabelfontsize"],
                               color=self.get_axis_title_style()["axislabelfontcolour"],
                               )

        self.ax.tick_params(axis='y', which='major', left=False, right=False)

        if self.get_axis_style()["xfontcolour"] is not None:
            #Assumption made that bottom spine colour should match x axis tick colour?
            self.ax.spines["bottom"].set_color(self.get_axis_style()["xfontcolour"])
            self.ax.tick_params(axis='x', colors=self.get_axis_style()["xfontcolour"])
        if self.get_axis_style()["yfontcolour"] is not None:
            self.ax.tick_params(axis='y', colors=self.get_axis_style()["yfontcolour"])


    def _plot_paratext(self):
        """Internal method. Draws paratext (i.e., text around the axis) including title and subtitle."""

        self.fig._subtitle = None
        if self.get_fig_style()["title"] is not None:
            self.fig.suptitle(self.get_fig_style()["title"],
                              fontsize=self.get_fig_style()["titlefontsize"],
                              color=self.get_fig_style()["titlecolour"],
                              horizontalalignment="left",
                              verticalalignment="bottom",
                              )

        if self.get_fig_style()["subtitle"] is not None:
            self.fig._subtitle = matplotlib.text.Text(text=self.get_fig_style()["subtitle"],
                                                    fontsize=self.get_fig_style()["subtitlefontsize"],
                                                    color=self.get_fig_style()["subtitlecolour"],
                                                    horizontalalignment="left",
                                                    verticalalignment="bottom",
                                                    )
            self.fig.add_artist(self.fig._subtitle)


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
            self.ax.tick_params(axis='x', labelsize=int(self.get_axis_style()["xfontsize"]))

        self.ax.tick_params(axis='y', labelsize=int(self.get_axis_style()["yfontsize"]))

        if not self.get_fig_style()["spinedisplay"][0]: self.ax.spines['left'].set_visible(False)
        if not self.get_fig_style()["spinedisplay"][1]: self.ax.spines['top'].set_visible(False)
        if not self.get_fig_style()["spinedisplay"][2]: self.ax.spines['right'].set_visible(False)
        if not self.get_fig_style()["spinedisplay"][3]: self.ax.spines['bottom'].set_visible(False)


    def _plot_legend(self):
        """Internal method. Renders a plot legend according to stored style configuration."""
        self._init_legend_markers()
        if self.get_legend_style()["columns"] is not None:
            ncol = self.get_legend_style()["columns"]
        elif "horizontal" in self.get_legend_style()["placement"]:
            ncol = len(self.series_labels)
        else:
            ncol = 1

        self.ax.legend(handles=self.get_legend_style()["markers"],
                       ncol=ncol,
                       loc=DEFAULT_LEGEND_STYLE.placement_options[self.get_legend_style()["placement"]][0],
                       fontsize=self.get_legend_style()["fontsize"],
                       labelspacing = self.get_legend_style()["padding"], #Done twice so it is applied either vert or horiz
                       columnspacing = self.get_legend_style()["padding"], #Done twice so it is applied either vert or horiz
                       labelcolor=self.get_legend_style()["fontcolour"],
                       facecolor=self.get_legend_style()["backgroundcolour"],
                       edgecolor = self.get_legend_style()["bordercolour"],
                       framealpha=1,
                       shadow=False,
                       borderaxespad=0,
                       handletextpad=0.1 #Space between label and marker
                       )


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
