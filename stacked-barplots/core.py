# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,line-too-long
"""Core module pertaining to stacked-barplots Python library.

Core module contains definition for class StackedBarplot, which defines
the properties and behaviours of plots created from stacked-barplots.py, and 
the class StackedPlotStyle, which holds specific style properties for each 
StackedBarplot object. The StackedBarplot and StackedPlotStyle classes maintain
a one-to-one relationship.
"""

import os
import warnings
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.artist import Artist


from tools import *
from defaults import *


__all__ = [
    "StackedBarplot"
]

type results_type = dict[str, list[float]]
type series_labels_type = list[str]

class StackedBarplot:
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
        style: Instance of class StackedPlotStyle, containing chart style settings.
        bar_colours: Instance of class ColourGradient, containing chart bar colours.
    """
    def __init__(self, data:results_type, series_labels:series_labels_type):
        """Initializes the instance based on chart data and series labels.

        Args:
            data: Dictionary of chart data.
            series_labels: List of string headings for series used in chart.
            
        """
        self.data = list(data.values())
        self.series_labels = series_labels
        self.category_headings = list(data.keys())

        self.textbarvarartists = [] #Now redundant

        self.fig = None
        self.ax = None

        self.unrendered_changes = True

        self.style = StackedPlotStyle()

        self.bar_colours = ColourGradient()
        self.bar_colours.grayscale_gradient(len(self.series_labels))

        self._init_legend_markers()


    def set_style(self, style:StackedPlotStyle):
        """Applies a given StackedPlotStyle object to the current StackedBarplot plot.
        
        Args:
            style: Given StackedBarplot object that should be applied to the StackedBarplot plot.
        """
        self.style = style

        #Bar colours must be generated after the data is provided, as the number of colours must match the number of categories
        self.bar_colours.gradient(len(self.series_labels), DEFAULT_BAR_STYLE.startcolour, DEFAULT_BAR_STYLE.endcolour, DEFAULT_BAR_STYLE.midcolour)
        self._init_legend_markers()


    def _plot_bars(self):
        """Internal method. Renders bars and category headings according to stored style configuration."""
        self.fig, self.ax = plt.subplots(figsize=(
            self.style.figstored["size"][0],
            self.style.figstored["size"][1]
            ))

        middle_index = len(self.data[0]) // 2

        if self.style.figstored.get("ordered") != "unordered":
            if self.style.figstored.get("ordered") == "ascending": toreverse = True
            elif self.style.figstored.get("ordered") == "descending": toreverse = False
            else: toreverse = False
            if self.style.barstored.get("align") == "left":
                self.category_headings, self.data = zip(*sorted(zip(self.category_headings, self.data), key=lambda category: sum(category[1]), reverse=toreverse)) #Making sure the labels get ordered with the data
            elif self.style.barstored.get("align") == "center":
                if len(self.data[0]) % 2 == 0:
                    self.category_headings, self.data = zip(*sorted(zip(self.category_headings, self.data),key=lambda category: sum(category[1][:middle_index]),reverse=toreverse))
                else:
                    self.category_headings, self.data = zip(*sorted(zip(self.category_headings, self.data),key=lambda category: sum(category[1][:middle_index]) + category[1][middle_index]/2,reverse=toreverse))
        data_cum = cumu2d(self.data)

        offsets = [0]*len(self.data)
        if self.style.barstored.get("align") == "center":
            offsets = []
            for(row_index, row) in enumerate(self.data):
                if len(self.data[0]) % 2 == 0:
                    offsets.append(sum(self.data[row_index][0:middle_index]))
                else:
                    offsets.append(sum(self.data[row_index][0:middle_index]) + self.data[row_index][middle_index]/2)

        for col_index, (colname, colour) in enumerate(zip(self.series_labels, self.bar_colours.get_normalised_gradient_list())):
            widths = [bar_data[col_index] for bar_data in self.data]
            starts = [bar_data[col_index] for bar_data in data_cum]

            for bar_index, width in enumerate(widths):
                if self.style.barstored.get("align") == "left":
                    starts[bar_index] = starts[bar_index]-widths[bar_index]
                elif self.style.barstored.get("align") == "center":
                    starts[bar_index] = starts[bar_index]-widths[bar_index]-offsets[bar_index]
                elif self.style.barstored.get("align") == "right":
                    raise NotImplementedError("Right-aligned bars not yet implemented")
                else:
                    raise ValueError("Invalid alignment value, must be 'left', 'center', or 'right'")
            rects = self.ax.barh(self.category_headings,
                                 widths,
                                 left=starts,
                                 height=self.style.barstored.get("height"),
                                 color = colour,
                                 label=colname,
                                 zorder=1)

        for tick in self.ax.get_yticklabels(): tick.set_fontfamily(self.style.figstored.get("fontfamily"))
        self.fig.set_facecolor(self.style.figstored.get("backgroundcolour"))
        self.ax.set_facecolor(self.style.figstored.get("backgroundcolour"))

        if self.style.figstored.get("verline"): self.ax.axvline(0, linestyle="--", color="black", alpha=0.25, zorder=0)


    def _plot_bar_labels(self):
        """Internal method. Renders plot bar value annotations according to stored style configuration."""

        for col_index, c in enumerate(self.ax.containers):
            bar_labels = []

            #Formatting bar value labels
            for val in c.datavalues:
                display = True
                if self.style.barfontstored.get("fontdisplaythresh")[0] is not None: #Threshold for displaying labels, if value is below or above given threshold, don't display label
                    if val <= self.style.barfontstored.get("fontdisplaythresh")[0]: display = False
                if self.style.barfontstored.get("fontdisplaythresh")[1] is not None:
                    if val >= self.style.barfontstored.get("fontdisplaythresh")[1]: display = False
                if display: bar_labels.append(str.format(self.style.barfontstored.get("fontformat"), val))
                else: bar_labels.append("")

            #Positioning bar value labels
            for row_index, (rect, text) in enumerate(zip(c.patches, bar_labels)):
                ha, va = "center", "center" #Where the coords refer to on the text
                y = rect.get_y() + rect.get_height() / 2 #Y coordinate is usually the same no matter the alignment, but this can be changed later
                x = None #X coordinate will be set based on alignment

                #Threshold for first and last bar on a row, if value is below threshold, move label to outside of bar
                topadd = False
                if col_index == 0 and self.style.barfontstored.get("fontpaddthresh") is not None and self.style.barfontstored.get("fontendthreshpadd"): #Leftmost bar label
                    if c.datavalues[row_index] <= self.style.barfontstored.get("fontpaddthresh"):
                        topadd = True
                        ha = "right"
                        x = rect.get_x() - self.style.barfontstored.get("fontpadd")
                elif col_index == len(self.data[0])-1 and self.style.barfontstored.get("fontpaddthresh") is not None and self.style.barfontstored.get("fontendthreshpadd"): #Rightmost bar label
                    if c.datavalues[row_index] <= self.style.barfontstored.get("fontpaddthresh"):
                        topadd = True
                        ha = "left"
                        x = rect.get_x() + rect.get_width() + self.style.barfontstored.get("fontpadd")

                if not topadd: #Normal alignment for all other bars, or if no outside-of-bar threshold is set
                    if self.style.barfontstored.get("fontalign") == "center":
                        x = rect.get_x() + rect.get_width() / 2
                    elif self.style.barfontstored.get("fontalign") == "left":
                        x = rect.get_x() + self.style.barfontstored.get("fontpadd")
                        ha = "left"
                    elif self.style.barfontstored.get("fontalign") == "right":
                        x = rect.get_x() + rect.get_width() - self.style.barfontstored.get("fontpadd")
                        ha = "right"

                #TODO if(rect.get_width() <= 3): y -= ((rect.get_height() / 2) +0.07) #raising labels above the bar if the bar is too small, so that it doesn't overlap with the bar boundary
                #TODO if text is made white and shifted outside of bar, it becomes white text on white background.
                #TODO also, this should invert the colour rather than force white or black?
                if self.style.barfontstored.get("fontcolourinvert"):
                    luminence = 0.2126*rect.get_facecolor()[0] + 0.7152*rect.get_facecolor()[1] + 0.0722*rect.get_facecolor()[2]
                    print(luminence)
                    if luminence < 0.4: fontcolour = "white"
                    else: fontcolour = "black"
                else: fontcolour = self.style.barfontstored.get("fontcolour")

                textartist = self.ax.annotate(
                    text,
                    (x, y),
                    textcoords="offset points",
                    xytext=(0, 0),
                    ha=ha, va=va,
                    fontsize=self.style.barfontstored.get("fontsize"),
                    color=fontcolour,
                    fontfamily=self.style.figstored.get("fontfamily")
                    )
                self.textbarvarartists.append(textartist)

        self.ax.invert_yaxis() #Required for some reason?

    def _plot_axes(self):
        """Internal method. Renders and applies plot labels/title and axes settings according to stored style configuration."""
        if self.style.axisstored.get("xlim") is not None and self.style.axisstored.get("step") is not None:
            self.ax.set_xlim(self.style.axisstored.get("xlim")[0], self.style.axisstored.get("xlim")[1])
            self.ax.set_xticks([i for i in range(self.style.axisstored.get("xlim")[0], self.style.axisstored.get("xlim")[1]+1, self.style.axisstored.get("step"))])

        self.ax.xaxis.set_major_formatter(lambda x, pos: self.style.axisstored.get("xaxisformat").format(x))

        self.ax.tick_params(axis='x', labelsize=int(self.style.axisstored.get("xfontsize")), labelfontfamily=self.style.figstored.get("fontfamily"))
        self.ax.tick_params(axis='y', labelsize=int(self.style.axisstored.get("yfontsize")), labelfontfamily=self.style.figstored.get("fontfamily"))

        if not self.style.figstored.get("spinedisplay")[0]: self.ax.spines['left'].set_visible(False)
        if not self.style.figstored.get("spinedisplay")[1]: self.ax.spines['top'].set_visible(False)
        if not self.style.figstored.get("spinedisplay")[2]: self.ax.spines['right'].set_visible(False)
        if not self.style.figstored.get("spinedisplay")[3]: self.ax.spines['bottom'].set_visible(False)

        if self.style.figstored.get("title") is not None:
            self.ax.set_title(self.style.figstored.get("title"),
                              fontsize=self.style.figstored.get("titlefontsize"),
                              color=self.style.figstored.get("titlecolour"),
                              fontfamily=self.style.figstored.get("fontfamily"))
        if self.style.axistitlestored.get("xlabel") is not None:
            self.ax.set_xlabel(self.style.axistitlestored.get("xlabel"),
                               fontsize=self.style.axistitlestored.get("axislabelfontsize"),
                               color=self.style.axistitlestored.get("axislabelfontcolour"),
                               fontfamily=self.style.figstored.get("fontfamily"))
        if self.style.axistitlestored.get("ylabel") is not None:
            self.ax.set_ylabel(self.style.axistitlestored.get("ylabel"),
                               fontsize=self.style.axistitlestored.get("axislabelfontsize"),
                               color=self.style.axistitlestored.get("axislabelfontcolour"),
                               fontfamily=self.style.figstored.get("fontfamily"))

    def _plot_legend(self):
        """Internal method. Renders a plot legend according to stored style configuration."""
        if"horizontal" in self.style.legendstored.get("placement"): ncol = len(self.series_labels)
        else: ncol = 1

        bbox_to_anchor = list(DEFAULT_LEGEND_STYLE.placementoptions[self.style.legendstored.get("placement")][1])
        bbox_to_anchor[0] += self.style.legendstored.get("transform")[0]
        bbox_to_anchor[1] += self.style.legendstored.get("transform")[1]

        print(self.style.legendstored.get("bordercolour"))

        leg = self.ax.legend(handles=self.style.legendstored["markers"],
                       ncol=ncol,
                       bbox_to_anchor=bbox_to_anchor,
                       loc=DEFAULT_LEGEND_STYLE.placementoptions[self.style.legendstored.get("placement")][0],
                       fontsize=self.style.legendstored.get("fontsize"),
                       labelspacing = self.style.legendstored.get("spacing"),
                       labelcolor=self.style.legendstored.get("fontcolour"),
                       facecolor=self.style.legendstored.get("backgroundcolour"),
                       edgecolor = self.style.legendstored.get("bordercolour"),
                       framealpha=1,
                       shadow=False
        )

    def _plot_vert_line(self):
        """Internal method. Renders a vertical plot line according to stored style configuration."""
        if len(self.series_labels) %2 == 0: z = 2
        else: z = 0
        self.ax.axvline(0,
                        linestyle=self.style.vertlinestored.get("linestyle"),
                        color=self.style.vertlinestored.get("colour"),
                        alpha=self.style.vertlinestored.get("alpha"),
                        zorder=z)




    def _render(self):
        """Internal method. Internal method for rendering plot following render pipeline."""
        self._plot_bars()
        self._plot_bar_labels()
        self._plot_axes()
        if self.style.legendstored.get("show"): self._plot_legend()
        if self.style.vertlinestored.get("show"): self._plot_vert_line()

        self.fig.tight_layout()


    def get_bar_labels_style(self) -> dict:
        """Returns dictionary containing style configuration for chart bar labels."""
        return self.style.barfontstored

    #TODO: Start and end bar data label movement is implicit in whether paddthresh is None, thus endthreshpadd is redundant. 
    def set_bar_labels_style(self,
                fontsize:int=None,
                fontcolour:str = None,
                fontcolourinvert:bool = False,
                barvalueformat:str = None,
                displaythresh:tuple[float, float] = (None, None),
                paddthresh:float = None,
                endthreshpadd:bool = None,
                align:str=None,
                padding:float = None):
        """Update StackedBarplot bar text style configuration.

        Args:
            fontsize: Data label font size in points or as a string (e.g., 'large').
            fontcolour: The colour of data labels.
            fontcolourinvert: Boolean flag for if font colour should be inverted for
                data labels displayed on bars with low luminence.
            barvalueformat: format()-style format string for data labels. Default '{0}'. Format
                string can also round to (e.g., 1) decimal place(s) with '{0:.1}'. A suffix can
                be added using (for example) '{0}%'. See Python documentation for more inforamtion 
                (https://docs.python.org/3/library/string.html#format-specification-mini-language).
            displaythresh: Tuple of floats representing optional minimum and maximum display
                thresholds. Data labels below minimum or above maximum thresholds will not be displayed.
            paddthresh: Threshold for whether data labels on start or end bars of categories should
                be moved for better clarity (see parameter endthreshpadd).
            endthreshpadd: Boolean value indicating whether, for data values for start or end bars, 
                if the data value is below paddthresh, is should be moved outside of the bar for better
                clarity. 
            align: Alignment of data labels within bars. Can be 'left', 'center', or 'right'. 
            padding: Padding for data labels moved.
        """
        if fontsize is not None: self.style.barfontstored["fontsize"] = fontsize
        if fontcolour is not None: self.style.barfontstored["fontcolour"] = fontcolour
        if fontcolourinvert is not None: self.style.barfontstored["fontcolourinvert"] = fontcolourinvert
        if barvalueformat is not None: self.style.barfontstored["fontformat"] = barvalueformat
        if displaythresh is not None: self.style.barfontstored["fontdisplaythresh"] = displaythresh
        if paddthresh is not None: self.style.barfontstored["fontpaddthresh"] = paddthresh
        if endthreshpadd is not None: self.style.barfontstored["fontendthreshpadd"] = endthreshpadd
        if align is not None: self.style.barfontstored["fontalign"] = align
        if padding is not None: self.style.barfontstored["fontpadd"] = padding
        self.unrendered_changes = True


    def get_bar_style(self) -> dict:
        """Returns dictionary containing style configuration for chart bars."""
        return self.style.barstored

    def set_bar_style(self,
                    bar_height:int = None,
                    align:str = None,
                    ordered:str = None,
                    bar_gradient:ColourGradient = None
                    ):
        """Update StackedBarplot bar style configuration.

        Args:
            barheight: The height of each bar as a fraction. Selection 1 results on 
                no whitespace between displayed categories.
            align: The alignment of bars. Must be either 'left' or 'center'.
            ordered: Whether the displayed categories should be ordered. Must be either 
                None, 'ascending', or 'descending'. Categories are ordered based on sum of 
                leftmost bars.
            bar_gradient: ColourGradient object, containing colours matching the number of 
                series in each category.
        """
        #TODO: Improve method argument barcolours docstring to signpost colour methods.
        if bar_height is not None: self.style.barstored["barheight"] = bar_height
        if align is not None: self.style.barstored["align"] = align
        if ordered is not None: self.style.figstored["ordered"] = ordered
        if bar_gradient is not None: self.bar_colours = bar_gradient
        self.unrendered_changes = True


    def get_axis_title_style(self) -> dict:
        """Returns dictionary containing style configuration for chart axis labels."""
        return self.style.axistitlestored

    def set_axis_title_style(self,
                          xlabel:str = None,
                          ylabel:str = None,
                          axislabelfontsize:int = None,
                          axislabelfontcolour:str = None):
        """Update StackedBarplot axis title style configuration.

        Args:
            xlabel: X axis label. None (default) will result in no label being displayed.
            ylabel: Y axis label. None (default) will result in no label being displayed.
            axislabelfontsize: Axes label font size in points or as a string (e.g., 'large').
            axislabelfontcolour: Axes font colour.
        """
        if xlabel is not None: self.style.axistitlestored["xlabel"] = xlabel
        if ylabel is not None: self.style.axistitlestored["ylabel"] = ylabel
        if axislabelfontsize is not None:
            self.style.axistitlestored["axislabelfontsize"] = axislabelfontsize
        if axislabelfontcolour is not None:
            self.style.axistitlestored["axislabelfontcolour"] = axislabelfontcolour
        self.unrendered_changes = True


    def get_fig_style(self) -> dict:
        """Returns dictionary containing general style configuration for chart figure."""
        return self.style.figstored

    def set_fig_style(self,
                    title:str = None,
                    titlefontsize:int = None,
                    titlecolour:str = None,
                    fontfamily:str = None,
                    figsize:tuple[int, int] = None
                    ):
        """Update StackedBarplot general figure style configuration.

        Args:
            title: The title of the plot.
            titlefontsize: Plot title font size in points or as a string (e.g., 'large').
            titlecolour: The colour of the plot title.
            fontfamily: The font family for all text used in the plot. User must select from
                a list of font families (installed on user's machine).
            figsize: Tuple of integers representing the width and height of the figure.
        """
        if title is not None: self.style.figstored["title"] = title
        if titlefontsize is not None: self.style.figstored["titlefontsize"] = titlefontsize
        if titlecolour is not None: self.style.figstored["titlecolour"] = titlecolour
        if fontfamily is not None: self.style.figstored["fontfamily"] = fontfamily
        if figsize is not None: self.style.figstored["size"] = figsize
        self.unrendered_changes = True

    def get_vert_line_style(self) -> dict:
        """Returns dictionary containing style configuration for chart vertical line."""
        return self.style.vertlinestored

    def set_vert_line_style(self,
                    show:bool = None,
                    linestyle:str = None,
                    colour:str = None,
                    alpha:float = None):
        """Update StackedBarplot central vertical line style configuration.

        Args:
            show: A boolean flag for whether the vertical line should be shown,
                irrespectiev of other vertical line style configurations.
            linestyle: Set the linestyle of the line. Is {'-', '--', '-.', ':', '', ...}.
            colour: The colour of the line.
            alpha: The alpha value of the line.
        """
        if show is not None: self.style.vertlinestored["show"] = show
        if linestyle is not None: self.style.vertlinestored["linestyle"] = linestyle
        if colour is not None: self.style.vertlinestored["colour"] = colour
        if alpha is not None: self.style.vertlinestored["alpha"] = alpha
        self.unrendered_changes = True

    def get_legend_style(self) -> dict:
        """Returns dictionary containing style configuration for chart legend."""
        return self.style.legendstored

    def set_legend_style(self,
                       show:bool = None,
                       fontsize:int = None,
                       location:str = None,
                       spacing:float = None,
                       fontcolour:str = None,
                       backgroundcolour:str = None,
                       bordercolour:str = None,
                       placement:str = None,
                       markershape:str = None,
                       transform:tuple[float, float] = None
                       ):
        """Update StackedBarplot legend style configuration.

        Args:
            show: A boolean flag for whether the legend should be shown, irrespective
                of other legend style configurations. 
            fontsize: Series headings' font size in points or as a string (e.g., 'large').
            location: WORK IN PROGRESS
            spacing: Spacing between series headings, in font-size units.
            fontcolour: The color of the text in the legend.
            backgroundcolour: The legend's background color.
            bordercolour: The legend's background patch edge color.
            placement: WORK IN PROGRESS
            markershape: Marker style string. {'*': 'star', '+': 'plus', 's':'square', 
                'o':circle'}. For a full list of marker styles see https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html.
            transform: Allows the user to make minor adjustments to the legend's placement
                after placement choice.  
        """
        #TODO: finalise method argument documentation relating to legend placement.
        if show is not None: self.style.legendstored["show"] = show
        if fontsize is not None: self.style.legendstored["fontsize"] = fontsize
        if location is not None: self.style.legendstored["location"] = location
        if spacing is not None: self.style.legendstored["spacing"] = spacing
        if fontcolour is not None: self.style.legendstored["fontcolour"] = fontcolour
        if backgroundcolour is not None: self.style.legendstored["backgroundcolour"] = backgroundcolour
        if bordercolour is not None: self.style.legendstored["bordercolour"] = bordercolour
        if placement is not None: self.style.legendstored["placement"] = placement
        if markershape is not None:
            self.style.legendstored["markershape"] = markershape
            self._init_legend_markers()
        if transform is not None: self.style.legendstored["transform"] = transform
        self.unrendered_changes = True

    def get_axis_style(self) -> dict:
        """Returns dictionary containing style configuration for chart axis."""
        return self.style.axisstored

    def set_axis_style(self,
                       xlim:tuple[int, int] = None,
                       step:int = None,
                       xfontsize:int = None,
                       yfontsize:int = None,
                       xaxisformat:str = None):
        """Update StackedBarplot axis style configuration.

        Args:
            xlim: Left and right xlim in data coordinates, as a tuple.
            step: Intevals at which x axis ticks should be displayed.
            xfontsize: X axis tick label font size in points or as a string (e.g., 'large').
            yfontsize: Y axis tick label font size in points or as a string (e.g., 'large').
            xaxisformat: format()-style format string for x axis ticks. Default '{0}'. Format
                string can also round to (e.g., 1) decimal place(s) with '{0:.1}'. A suffix can
                be added using (for example) '{0}%'. See Python documentation for more inforamtion 
                (https://docs.python.org/3/library/string.html#format-specification-mini-language).
        """
        if xlim is not None: self.style.axisstored["xlim"] = xlim
        if step is not None: self.style.axisstored["step"] = step
        if xfontsize is not None: self.style.axisstored["xfontsize"] = xfontsize
        if yfontsize is not None: self.style.axisstored["yfontsize"] = yfontsize
        if xaxisformat is not None: self.style.axisstored["xaxisformat"] = xaxisformat
        self.unrendered_changes = True




    def render(self):
        """Renders the figure given current data and style configuration."""
        self._destroy_fig()
        self._render()
        self.unrendered_changes = False

    def show(self):
        """Displays the current figure."""

        if self.unrendered_changes:
            warnings.warn("You are attempting to display the figure before style changes " \
            "have been rendered. Beware that render() must be called on the StackedBarplot" \
            "object for any style changes to be displayed.")
        plt.show()

    def _destroy_fig(self):
        """Destroys the current figure."""
        if self.fig is not None:
            if len(self.textbarvarartists) != 0:
                self.clear_bar_text()
            #self._destroyAxes()
            self.fig.clear()
            plt.close(self.fig)


    def save(self, filename:str, transparent:bool=None, dpi='figure', bbox_inches='tight', pad_inches=0.1, fig_format:str="png"):
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
            format: The file format, e.g. 'png', 'pdf', 'svg', ... The behavior when this is 
                unset is documented under fname.

        """
        if self.unrendered_changes:
            warnings.warn("You are attempting to save the figure before style changes " \
            "have been rendered. Beware that render() must be called on the StackedBarplot" \
            "object for any style changes to be displayed.")
        path = os.path.dirname(os.path.abspath(__file__))
        self.fig.savefig(os.path.join(path, filename), transparent=transparent, dpi=dpi, bbox_inches=bbox_inches, pad_inches=pad_inches, format=fig_format)


    #def _init_fig_colours(self, colours:list[tuple[int, int, int]]):
    #    """Defines figure colours, converting to float."""
    #    self.style.barstored["barcolours"]  = [(col[0]/255.0, col[1]/255.0, col[2]/255.0) for col in colours]


    def _init_legend_markers(self):
        """Defines and stores legend markers.
        
        Method defines legend marker colours according to (previously) 
        initialised bar colours. Called by _render()."""

        self.style.legendstored["markers"] = []
        for i, cat in enumerate(self.series_labels):
            self.style.legendstored["markers"].append(
                mlines.Line2D([],
                [],
                color=self.bar_colours.get_normalised_gradient_list()[i],
                marker=self.style.legendstored.get("markershape"),
                linestyle='None',
                markersize=10,
                label=cat
            ))

    #TODO: Assess necessity of clear_bar_text() method.
    def clear_bar_text(self):
        """"""
        for artist in self.textbarvarartists:
            Artist.remove(artist)
            #del self.textbarvarartists[i]
        self.fig.canvas.draw()
        self.textbarvarartists = []


#TODO: Convert class attributes and dictionary keys to snake_case.
class StackedPlotStyle:
    """StackedPlotStyle objects represent the style configuration for a StackedBarplot plot.

    This class categorises plot style configuration variables into different dictionary
    variables which are stored as attributes. 

    Attributes:
        barfontstored: Style configurations for bar textual annotations.
        barstored: Style configurations for bar design and alignment.
        legendstored: Style configurations for plot legend.
        figstored: Style configurations for general figure style.
        axistitlestored: Style configurations for axis labels.
        vertlinestored: Style configurations for central vertical line.
        axisstored: Style configurations for axis scale font and values
    """
    def __init__(self):
        """Initializes the instance based on default values loaded from defaults.py."""

        self.barfontstored = {
            "fontsize": DEFAULT_BAR_FONT.size,
            "fontcolour": DEFAULT_BAR_FONT.colour,
            "fontformat": DEFAULT_BAR_FONT.format,
            "fontalign": DEFAULT_BAR_FONT.align,
            "fontpadd": DEFAULT_BAR_FONT.padding,
            "fontcolourinvert": DEFAULT_BAR_FONT.colourinvert,
            "fontdisplaythresh": DEFAULT_BAR_FONT.displaythresh,
            "fontpaddthresh": DEFAULT_BAR_FONT.paddingthresh,
            "fontendthreshpadd": DEFAULT_BAR_FONT.endthreshpadd
        }

        self.barstored = {
            "height": DEFAULT_BAR_STYLE.height,
            "align": DEFAULT_BAR_STYLE.align,
            "startcolour": DEFAULT_BAR_STYLE.startcolour,
            "endcolour": DEFAULT_BAR_STYLE.endcolour,
            "midcolour": DEFAULT_BAR_STYLE.midcolour
        }

        self.legendstored = {
            "show": DEFAULT_LEGEND_STYLE.show,
            "fontsize": DEFAULT_LEGEND_STYLE.fontsize,
            "location": DEFAULT_LEGEND_STYLE.location,
            "spacing": DEFAULT_LEGEND_STYLE.labelspacing,
            "fontcolour": DEFAULT_LEGEND_STYLE.fontcolour,
            "backgroundcolour": DEFAULT_LEGEND_STYLE.backgroundcolour,
            "bordercolour": DEFAULT_LEGEND_STYLE.bordercolour,
            "placement": DEFAULT_LEGEND_STYLE.placement,
            "markershape": DEFAULT_LEGEND_STYLE.markershape,
            "markers": [],
            "transform": DEFAULT_LEGEND_STYLE.placementtransform
        }

        self.figstored = {
            "title": DEFAULT_FIG_STYLE.title,
            "titlefontsize": DEFAULT_FIG_STYLE.titlefontsize,
            "titlecolour": DEFAULT_FIG_STYLE.titlecolour,
            "fontfamily": DEFAULT_FIG_STYLE.fontfamily,
            "size": DEFAULT_FIG_STYLE.size,
            "backgroundcolour": DEFAULT_FIG_STYLE.backgroundcolour,
            "ordered": DEFAULT_FIG_STYLE.ordered,
            "spinedisplay": DEFAULT_FIG_STYLE.spinedisplay
        }

        self.axistitlestored = {
            "xlabel": DEFAULT_AXIS_TITLE_STYLE.xlabel,
            "ylabel": DEFAULT_AXIS_TITLE_STYLE.ylabel,
            "axislabelfontsize": DEFAULT_AXIS_TITLE_STYLE.axislabelfontsize,
            "axislabelfontcolour": DEFAULT_AXIS_TITLE_STYLE.axislabelfontcolour
        }

        self.vertlinestored = {
            "show": DEFAULT_VERTLINE_STYLE.show,
            "linestyle": DEFAULT_VERTLINE_STYLE.linestyle,
            "colour": DEFAULT_VERTLINE_STYLE.colour,
            "alpha": DEFAULT_VERTLINE_STYLE.alpha
        }

        self.axisstored = {
            "xlim": DEFAULT_AXIS_STYLE.xlim,
            "step": DEFAULT_AXIS_STYLE.step,
            "xfontsize": DEFAULT_AXIS_STYLE.xfontsize,
            "yfontsize": DEFAULT_AXIS_STYLE.yfontsize,
            "xaxisformat": DEFAULT_AXIS_STYLE.xaxisformat,
        }
