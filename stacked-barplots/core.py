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


    def set_style(self, style:StackedPlotStyle):
        """Applies a given StackedPlotStyle object to the current StackedBarplot plot.
        
        Args:
            style: Given StackedBarplot object that should be applied to the StackedBarplot plot.
        """
        self.style = style

        #Bar colours must be generated after the data is provided, as the number of colours must match the number of categories
        self.bar_colours.gradient(len(self.series_labels), DEFAULT_BAR_STYLE.start_colour, DEFAULT_BAR_STYLE.end_colour, DEFAULT_BAR_STYLE.mid_colour)


    def _plot_bars(self):
        """Internal method. Renders bars and category headings according to stored style configuration."""
        self.fig, self.ax = plt.subplots(figsize=(
            self.style.fig["size"][0],
            self.style.fig["size"][1]
            ))

        middle_index = len(self.data[0]) // 2

        if self.style.fig.get("ordered") != "unordered":
            if self.style.fig.get("ordered") == "ascending": toreverse = True
            elif self.style.fig.get("ordered") == "descending": toreverse = False
            else: toreverse = False
            if self.style.bar.get("align") == "left":
                self.category_headings, self.data = zip(*sorted(zip(self.category_headings, self.data), key=lambda category: sum(category[1]), reverse=toreverse)) #Making sure the labels get ordered with the data
            elif self.style.bar.get("align") == "center":
                if len(self.data[0]) % 2 == 0:
                    self.category_headings, self.data = zip(*sorted(zip(self.category_headings, self.data),key=lambda category: sum(category[1][:middle_index]),reverse=toreverse))
                else:
                    self.category_headings, self.data = zip(*sorted(zip(self.category_headings, self.data),key=lambda category: sum(category[1][:middle_index]) + category[1][middle_index]/2,reverse=toreverse))
        data_cum = cumu2d(self.data)

        offsets = [0]*len(self.data)
        if self.style.bar.get("align") == "center":
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
                if self.style.bar.get("align") == "left":
                    starts[bar_index] = starts[bar_index]-widths[bar_index]
                elif self.style.bar.get("align") == "center":
                    starts[bar_index] = starts[bar_index]-widths[bar_index]-offsets[bar_index]
                elif self.style.bar.get("align") == "right":
                    raise NotImplementedError("Right-aligned bars not yet implemented")
                else:
                    raise ValueError("Invalid alignment value, must be 'left', 'center', or 'right'")
            rects = self.ax.barh(self.category_headings,
                                 widths,
                                 left=starts,
                                 height=self.style.bar.get("height"),
                                 color = colour,
                                 label=colname,
                                 zorder=1)

        for tick in self.ax.get_yticklabels(): tick.set_fontfamily(self.style.fig.get("fontfamily"))
        self.fig.set_facecolor(self.style.fig.get("backgroundcolour"))
        self.ax.set_facecolor(self.style.fig.get("backgroundcolour"))

        if self.style.fig.get("verline"): self.ax.axvline(0, linestyle="--", color="black", alpha=0.25, zorder=0)


    def _plot_bar_labels(self):
        """Internal method. Renders plot bar value annotations according to stored style configuration."""

        for col_index, c in enumerate(self.ax.containers):
            bar_labels = []

            #Formatting bar value labels
            for val in c.datavalues:
                display = True
                if self.style.bar_font.get("fontdisplaythresh")[0] is not None: #Threshold for displaying labels, if value is below or above given threshold, don't display label
                    if val <= self.style.bar_font.get("fontdisplaythresh")[0]: display = False
                if self.style.bar_font.get("fontdisplaythresh")[1] is not None:
                    if val >= self.style.bar_font.get("fontdisplaythresh")[1]: display = False
                if display: bar_labels.append(str.format(self.style.bar_font.get("fontformat"), val))
                else: bar_labels.append("")

            #Positioning bar value labels
            for row_index, (rect, text) in enumerate(zip(c.patches, bar_labels)):
                ha, va = "center", "center" #Where the coords refer to on the text
                y = rect.get_y() + rect.get_height() / 2 #Y coordinate is usually the same no matter the alignment, but this can be changed later
                x = None #X coordinate will be set based on alignment

                #Threshold for first and last bar on a row, if value is below threshold, move label to outside of bar
                topadd = False
                if col_index == 0 and self.style.bar_font.get("fontpaddthresh") is not None and self.style.bar_font.get("fontendthreshpadd"): #Leftmost bar label
                    if c.datavalues[row_index] <= self.style.bar_font.get("fontpaddthresh"):
                        topadd = True
                        ha = "right"
                        x = rect.get_x() - self.style.bar_font.get("fontpadd")
                elif col_index == len(self.data[0])-1 and self.style.bar_font.get("fontpaddthresh") is not None and self.style.bar_font.get("fontendthreshpadd"): #Rightmost bar label
                    if c.datavalues[row_index] <= self.style.bar_font.get("fontpaddthresh"):
                        topadd = True
                        ha = "left"
                        x = rect.get_x() + rect.get_width() + self.style.bar_font.get("fontpadd")

                if not topadd: #Normal alignment for all other bars, or if no outside-of-bar threshold is set
                    if self.style.bar_font.get("fontalign") == "center":
                        x = rect.get_x() + rect.get_width() / 2
                    elif self.style.bar_font.get("fontalign") == "left":
                        x = rect.get_x() + self.style.bar_font.get("fontpadd")
                        ha = "left"
                    elif self.style.bar_font.get("fontalign") == "right":
                        x = rect.get_x() + rect.get_width() - self.style.bar_font.get("fontpadd")
                        ha = "right"

                #TODO if(rect.get_width() <= 3): y -= ((rect.get_height() / 2) +0.07) #raising labels above the bar if the bar is too small, so that it doesn't overlap with the bar boundary
                #TODO if text is made white and shifted outside of bar, it becomes white text on white background.
                #TODO also, this should invert the colour rather than force white or black?
                if self.style.bar_font.get("fontcolourinvert"):
                    luminence = 0.2126*rect.get_facecolor()[0] + 0.7152*rect.get_facecolor()[1] + 0.0722*rect.get_facecolor()[2]
                    if luminence < 0.4: fontcolour = "white"
                    else: fontcolour = "black"
                else: fontcolour = self.style.bar_font.get("fontcolour")

                textartist = self.ax.annotate(
                    text,
                    (x, y),
                    textcoords="offset points",
                    xytext=(0, 0),
                    ha=ha, va=va,
                    fontsize=self.style.bar_font.get("fontsize"),
                    color=fontcolour,
                    fontfamily=self.style.bar_font.get("fontfamily")
                    )
                self.textbarvarartists.append(textartist)

        self.ax.invert_yaxis() #Required for some reason?

    def _plot_axes(self):
        """Internal method. Renders and applies plot labels/title and axes settings according to stored style configuration."""
        if self.style.axis.get("xlim") is not None and self.style.axis.get("step") is not None:
            self.ax.set_xlim(self.style.axis.get("xlim")[0], self.style.axis.get("xlim")[1])
            self.ax.set_xticks([i for i in range(self.style.axis.get("xlim")[0], self.style.axis.get("xlim")[1]+1, self.style.axis.get("step"))])

        self.ax.xaxis.set_major_formatter(lambda x, pos: self.style.axis.get("xaxisformat").format(x))

        self.ax.tick_params(axis='x', labelsize=int(self.style.axis.get("xfontsize")), labelfontfamily=self.style.fig.get("fontfamily"))
        self.ax.tick_params(axis='y', labelsize=int(self.style.axis.get("yfontsize")), labelfontfamily=self.style.fig.get("fontfamily"))

        if not self.style.fig.get("spinedisplay")[0]: self.ax.spines['left'].set_visible(False)
        if not self.style.fig.get("spinedisplay")[1]: self.ax.spines['top'].set_visible(False)
        if not self.style.fig.get("spinedisplay")[2]: self.ax.spines['right'].set_visible(False)
        if not self.style.fig.get("spinedisplay")[3]: self.ax.spines['bottom'].set_visible(False)

        if self.style.fig.get("title") is not None:
            self.ax.set_title(self.style.fig.get("title"),
                              fontsize=self.style.fig.get("titlefontsize"),
                              color=self.style.fig.get("titlecolour"),
                              fontfamily=self.style.fig.get("fontfamily"))
        if self.style.axis_title.get("xlabel") is not None:
            self.ax.set_xlabel(self.style.axis_title.get("xlabel"),
                               fontsize=self.style.axis_title.get("axislabelfontsize"),
                               color=self.style.axis_title.get("axislabelfontcolour"),
                               fontfamily=self.style.fig.get("fontfamily"))
        if self.style.axis_title.get("ylabel") is not None:
            self.ax.set_ylabel(self.style.axis_title.get("ylabel"),
                               fontsize=self.style.axis_title.get("axislabelfontsize"),
                               color=self.style.axis_title.get("axislabelfontcolour"),
                               fontfamily=self.style.fig.get("fontfamily"))

    def _plot_legend(self):
        """Internal method. Renders a plot legend according to stored style configuration."""
        if"horizontal" in self.style.legend.get("placement"): ncol = len(self.series_labels)
        else: ncol = 1

        bbox_to_anchor = list(DEFAULT_LEGEND_STYLE.placement_options[self.style.legend.get("placement")][1])
        bbox_to_anchor[0] += self.style.legend.get("transform")[0]
        bbox_to_anchor[1] += self.style.legend.get("transform")[1]

        leg = self.ax.legend(handles=self.style.legend["markers"],
                       ncol=ncol,
                       bbox_to_anchor=bbox_to_anchor,
                       loc=DEFAULT_LEGEND_STYLE.placement_options[self.style.legend.get("placement")][0],
                       fontsize=self.style.legend.get("fontsize"),
                       labelspacing = self.style.legend.get("spacing"),
                       labelcolor=self.style.legend.get("fontcolour"),
                       facecolor=self.style.legend.get("backgroundcolour"),
                       edgecolor = self.style.legend.get("bordercolour"),
                       framealpha=1,
                       shadow=False
        )

    def _plot_vert_line(self):
        """Internal method. Renders a vertical plot line according to stored style configuration."""
        if len(self.series_labels) %2 == 0: z = 2
        else: z = 0
        self.ax.axvline(0,
                        linestyle=self.style.vert_line.get("linestyle"),
                        color=self.style.vert_line.get("colour"),
                        alpha=self.style.vert_line.get("alpha"),
                        zorder=z)



    def _render(self):
        """Internal method. Internal method for rendering plot following render pipeline."""
        self._plot_bars()
        self._plot_bar_labels()
        self._plot_axes()
        if self.style.legend.get("show"):
            self._init_legend_markers()
            self._plot_legend()
        if self.style.vert_line.get("show"): self._plot_vert_line()

        self.fig.tight_layout()


    def get_bar_labels_style(self) -> dict:
        """Returns dictionary containing style configuration for chart bar labels."""
        return self.style.bar_font

    #TODO: Start and end bar data label movement is implicit in whether paddthresh is None, thus endthreshpadd is redundant. 
    def set_bar_labels_style(self,
                font_size:int=None,
                font_colour:str = None,
                font_colour_invert:bool = False,
                bar_value_format:str = None,
                display_thresh:tuple[float, float] = (None, None),
                padd_thresh:float = None,
                end_thresh_padd:bool = None,
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
        if font_size is not None: self.style.bar_font["fontsize"] = font_size
        if font_colour is not None: self.style.bar_font["fontcolour"] = font_colour
        if font_colour_invert is not None: self.style.bar_font["fontcolourinvert"] = font_colour_invert
        if bar_value_format is not None: self.style.bar_font["fontformat"] = bar_value_format
        if display_thresh is not None: self.style.bar_font["fontdisplaythresh"] = display_thresh
        if padd_thresh is not None: self.style.bar_font["fontpaddthresh"] = padd_thresh
        if end_thresh_padd is not None: self.style.bar_font["fontendthreshpadd"] = end_thresh_padd
        if align is not None: self.style.bar_font["fontalign"] = align
        if padding is not None: self.style.bar_font["fontpadd"] = padding
        self.unrendered_changes = True


    def get_bar_style(self) -> dict:
        """Returns dictionary containing style configuration for chart bars."""
        return self.style.bar

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
        if bar_height is not None: self.style.bar["barheight"] = bar_height
        if align is not None: self.style.bar["align"] = align
        if ordered is not None: self.style.fig["ordered"] = ordered
        if bar_gradient is not None: self.bar_colours = bar_gradient
        self.unrendered_changes = True


    def get_axis_title_style(self) -> dict:
        """Returns dictionary containing style configuration for chart axis labels."""
        return self.style.axis_title

    def set_axis_title_style(self,
                          x_label:str = None,
                          y_label:str = None,
                          axis_label_font_size:int = None,
                          axis_label_font_colour:str = None):
        """Update StackedBarplot axis title style configuration.

        Args:
            xlabel: X axis label. None (default) will result in no label being displayed.
            ylabel: Y axis label. None (default) will result in no label being displayed.
            axislabelfontsize: Axes label font size in points or as a string (e.g., 'large').
            axislabelfontcolour: Axes font colour.
        """
        if x_label is not None: self.style.axis_title["xlabel"] = x_label
        if y_label is not None: self.style.axis_title["ylabel"] = y_label
        if axis_label_font_size is not None:
            self.style.axis_title["axislabelfontsize"] = axis_label_font_size
        if axis_label_font_colour is not None:
            self.style.axis_title["axislabelfontcolour"] = axis_label_font_colour
        self.unrendered_changes = True


    def get_fig_style(self) -> dict:
        """Returns dictionary containing general style configuration for chart figure."""
        return self.style.fig

    def set_fig_style(self,
                    title:str = None,
                    title_font_size:int = None,
                    title_colour:str = None,
                    font_family:str = None,
                    fig_size:tuple[int, int] = None,
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
        if title is not None: self.style.fig["title"] = title
        if title_font_size is not None: self.style.fig["titlefontsize"] = title_font_size
        if title_colour is not None: self.style.fig["titlecolour"] = title_colour
        if font_family is not None: self.style.fig["fontfamily"] = font_family
        if fig_size is not None: self.style.fig["size"] = fig_size
        self.unrendered_changes = True

    def get_vert_line_style(self) -> dict:
        """Returns dictionary containing style configuration for chart vertical line."""
        return self.style.vert_line

    def set_vert_line_style(self,
                    show:bool = None,
                    line_style:str = None,
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
        if show is not None: self.style.vert_line["show"] = show
        if line_style is not None: self.style.vert_line["linestyle"] = line_style
        if colour is not None: self.style.vert_line["colour"] = colour
        if alpha is not None: self.style.vert_line["alpha"] = alpha
        self.unrendered_changes = True

    def get_legend_style(self) -> dict:
        """Returns dictionary containing style configuration for chart legend."""
        return self.style.legend

    def set_legend_style(self,
                       show:bool = None,
                       font_size:int = None,
                       location:str = None,
                       spacing:float = None,
                       font_colour:str = None,
                       background_colour:str = None,
                       border_colour:str = None,
                       placement:str = None,
                       marker_shape:str = None,
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
        if show is not None: self.style.legend["show"] = show
        if font_size is not None: self.style.legend["fontsize"] = font_size
        if location is not None: self.style.legend["location"] = location
        if spacing is not None: self.style.legend["spacing"] = spacing
        if font_colour is not None: self.style.legend["fontcolour"] = font_colour
        if background_colour is not None: self.style.legend["backgroundcolour"] = background_colour
        if border_colour is not None: self.style.legend["bordercolour"] = border_colour
        if placement is not None: self.style.legend["placement"] = placement
        if marker_shape is not None: self.style.legend["markershape"] = marker_shape
        if transform is not None: self.style.legend["transform"] = transform
        self.unrendered_changes = True

    def get_axis_style(self) -> dict:
        """Returns dictionary containing style configuration for chart axis."""
        return self.style.axis

    def set_axis_style(self,
                       x_lim:tuple[int, int] = None,
                       step:int = None,
                       x_font_size:int = None,
                       y_font_size:int = None,
                       x_axis_format:str = None):
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
        if x_lim is not None: self.style.axis["xlim"] = x_lim
        if step is not None: self.style.axis["step"] = step
        if x_font_size is not None: self.style.axis["xfontsize"] = x_font_size
        if y_font_size is not None: self.style.axis["yfontsize"] = y_font_size
        if x_axis_format is not None: self.style.axis["xaxisformat"] = x_axis_format
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
        self.fig.savefig(os.path.join(path, filename),
                         transparent=transparent,
                         dpi=dpi, 
                         bbox_inches=bbox_inches,
                         pad_inches=pad_inches,
                         format=fig_format)


    def _init_legend_markers(self):
        """Defines and stores legend markers.
        
        Method defines legend marker colours according to (previously) 
        initialised bar colours. Called by _render()."""

        self.style.legend["markers"] = []
        for i, cat in enumerate(self.series_labels):
            self.style.legend["markers"].append(
                mlines.Line2D([],
                [],
                color=self.bar_colours.get_normalised_gradient_list()[i],
                marker=self.style.legend.get("markershape"),
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
        bar_font: Style configurations for bar textual annotations.
        bar: Style configurations for bar design and alignment.
        legend: Style configurations for plot legend.
        fig: Style configurations for general figure style.
        axis_title: Style configurations for axis labels.
        vert_line: Style configurations for central vertical line.
        axis: Style configurations for axis scale font and values
    """
    def __init__(self):
        """Initializes the instance based on default values loaded from defaults.py."""

        self.bar_font = {
            "fontsize": DEFAULT_BAR_FONT.size,
            "fontcolour": DEFAULT_BAR_FONT.colour,
            "fontformat": DEFAULT_BAR_FONT.format,
            "fontalign": DEFAULT_BAR_FONT.align,
            "fontpadd": DEFAULT_BAR_FONT.padding,
            "fontcolourinvert": DEFAULT_BAR_FONT.colour_invert,
            "fontdisplaythresh": DEFAULT_BAR_FONT.display_thresh,
            "fontpaddthresh": DEFAULT_BAR_FONT.padding_thresh,
            "fontendthreshpadd": DEFAULT_BAR_FONT.end_thresh_padd
        }

        self.bar = {
            "height": DEFAULT_BAR_STYLE.height,
            "align": DEFAULT_BAR_STYLE.align,
            "startcolour": DEFAULT_BAR_STYLE.start_colour,
            "endcolour": DEFAULT_BAR_STYLE.end_colour,
            "midcolour": DEFAULT_BAR_STYLE.mid_colour
        }

        self.legend = {
            "show": DEFAULT_LEGEND_STYLE.show,
            "fontsize": DEFAULT_LEGEND_STYLE.font_size,
            "location": DEFAULT_LEGEND_STYLE.location,
            "spacing": DEFAULT_LEGEND_STYLE.label_spacing,
            "fontcolour": DEFAULT_LEGEND_STYLE.font_colour,
            "backgroundcolour": DEFAULT_LEGEND_STYLE.background_colour,
            "bordercolour": DEFAULT_LEGEND_STYLE.border_colour,
            "placement": DEFAULT_LEGEND_STYLE.placement,
            "markershape": DEFAULT_LEGEND_STYLE.marker_shape,
            "markers": [],
            "transform": DEFAULT_LEGEND_STYLE.placement_transform
        }

        self.fig = {
            "title": DEFAULT_FIG_STYLE.title,
            "titlefontsize": DEFAULT_FIG_STYLE.title_font_size,
            "titlecolour": DEFAULT_FIG_STYLE.title_colour,
            "fontfamily": DEFAULT_FIG_STYLE.font_family,
            "size": DEFAULT_FIG_STYLE.size,
            "backgroundcolour": DEFAULT_FIG_STYLE.background_colour,
            "ordered": DEFAULT_FIG_STYLE.ordered,
            "spinedisplay": DEFAULT_FIG_STYLE.spine_display
        }

        self.axis_title = {
            "xlabel": DEFAULT_AXIS_TITLE_STYLE.x_label,
            "ylabel": DEFAULT_AXIS_TITLE_STYLE.y_label,
            "axislabelfontsize": DEFAULT_AXIS_TITLE_STYLE.axis_label_font_size,
            "axislabelfontcolour": DEFAULT_AXIS_TITLE_STYLE.axis_label_font_colour
        }

        self.vert_line = {
            "show": DEFAULT_VERTLINE_STYLE.show,
            "linestyle": DEFAULT_VERTLINE_STYLE.line_style,
            "colour": DEFAULT_VERTLINE_STYLE.colour,
            "alpha": DEFAULT_VERTLINE_STYLE.alpha
        }

        self.axis = {
            "xlim": DEFAULT_AXIS_STYLE.x_lim,
            "step": DEFAULT_AXIS_STYLE.step,
            "xfontsize": DEFAULT_AXIS_STYLE.x_font_size,
            "yfontsize": DEFAULT_AXIS_STYLE.y_font_size,
            "xaxisformat": DEFAULT_AXIS_STYLE.x_axis_format,
        }
