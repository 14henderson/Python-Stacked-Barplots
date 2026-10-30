# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,line-too-long,invalid-name

"""Defaults module pertaining to stacked-barplots Python library.

defaults.py contains classes which store the default values for
all plot style elements covered in this project. Plot styles are 
separated into bars, bar text, overall axes and figure styles, and 
style settings relating to the plot legend and (where appropriate)
the vertical line.

defaults.py also contains the class StackedPlotStyle, of which each 
StackedBarplot object has an instance. The StackedBarplot and 
ColourGradient classes maintain a one-to-one relationship. Each
StackedPlotStyle hold style attributes related to a plot, as well 
as getter and setter functions which check argument value type and
values. Delegation means that StackedPlotStyle methods can be called
directly from a StackedBarplot object (see example below).

Typical usage example:
    results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
    series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

    #Style object can be created manually rather than through free methods in plots.py.
    local_style = StackedPlotStyle() 
    plot = StackedBarplot(data, series_labels)
    plot.set_style(local_style)

    plot.set_bar_labels_style(font_size=12,
                            bar_value_format="{0:.1f}%",
                            align="left",
                            expel_squeezed_ends=True)
    plot.render()
    plot.show()
"""

import warnings
import matplotlib.lines as mlines

from .tools import ColourGradient

__all__ = [
    "StackedPlotStyle", "DEFAULT_BAR_VAL_LABEL_STYLE", "DEFAULT_BAR_STYLE", "DEFAULT_FIG_STYLE", 
    "DEFAULT_AXIS_STYLE", "DEFAULT_AXIS_TITLE_STYLE", "DEFAULT_LEGEND_STYLE", 
    "DEFAULT_VERTLINE_STYLE", "Auto_Style_Calculations"
]


#TODO: Calculate in pixels rather than cm.
#TODO: Re-calculate as these are now estimated axes sizes not figure sizes.
class Auto_Style_Calculations:
    """Class holding static methods relating to calculations for default 
    style values. In particular, where the style value is contingent on
    chart data (e.g., figure height calculate from number of categories)"""

    #Padding around figure (in pixels)
    fig_left_pad = 10
    fig_top_pad = 10
    fig_right_pad = 10
    fig_bottom_pad = 10

    @staticmethod
    def calc_axis_width(num_series:int) -> int:
        """Calculate axis width (in cm) from number of series in plot.
        Args:
            num_series: The number of series in each category inthe plot."""
        if num_series > 10: return 24
        else: return (-0.198*num_series**2) + 4.23*num_series


    @staticmethod
    def calc_axis_height(num_categories:int) -> float:
        """Calculate axis height (in cm) from number of categories in plot.
        Args:
            num_categories: The number of categories in the plot."""
        if num_categories > 25: return 31.5
        else: return (-0.025*num_categories**2) + 1.2557*num_categories



class DEFAULT_AXIS_STYLE:
    """Default style class for axis scale font and values
    
    Default style settings for stacked barchart relating to the
    style of axis font and format are defined here. This includes
    axis min and max limits, font size, and format.
    
    xlim is stored as tuple of two integers representing the minimum
    and maximum values to be displayed on the X axis (None indicates 
    no limit). Font format is str.format() type, default as "{0}"."""

    x_axis_show:bool = True
    y_axis_show:bool = True
    x_lim:tuple[int, int] = None
    step:int = None
    x_font_size:int = 10
    y_font_size:int = 12
    x_font_colour = "#7E7D7D"
    y_font_colour = "#2c2c2c"
    x_axis_format:str = "{0:.0f}"
    x_axis_abs:bool = False


class DEFAULT_AXIS_TITLE_STYLE:
    """Default style class for axis labels.

    Default style settings for stacked barchart relating to the 
    style of X and Y axis labels. None value indicates no label."""
    x_label:str = None
    y_label:str = None
    axis_label_font_size:int = 12
    axis_label_font_colour = "#2c2c2c"


class DEFAULT_BAR_STYLE:
    """Default style class for bar design and alignment.
    
    Default style settings for stacked barchart relating to
    the design of bars themselves. Align defines how to align the
    figure: [left] stacks bars from 0 on X axis, and [centre] aligns bars 
    centrally on X axis. The start, mid, and end colour are also defined
    here for a colour gradient to be generated."""

    align:str = "left"
    height:float = .8
    start_colour:tuple[int, int, int] = (227, 108, 85)
    end_colour:tuple[int, int, int] = (106, 139, 239)
    mid_colour:tuple[int, int, int] = (220, 221, 221)


class DEFAULT_BAR_VAL_LABEL_STYLE:
    """Default style class for bar data value annotations.
    
    Default style settings for stacked barchart relating to 
    textual annotations made on data bars containing bar values. 
    Default values are stored on font size, colour, format, 
    alignment in bar, and a what to do if the bar is thinner 
    than the label itself (if a start or end bar in a category,
    the label can be moved to outside the bar). The user can 
    also specify if the text colour should be inverted when
    displayed on a dark-coloured bar; this is set to False by 
    default."""

    font_size:int = 10
    font_colour = "#2c2c2c"
    format:str = "{0:.1f}"
    align:str = "centre"
    colour_invert:bool = False
    padding:float = 5 #In display coordinates
    hide_squeezed:str = "all" #Can be None, "all", "inner-only"
    expel_squeezed_ends:bool = False


class DEFAULT_FIG_STYLE:
    """Default style class for general figure style.

    Default style settings for stacked barchart relating to the
    style of the figure itself. Default values on figure size, title (and
    related settings), figure font family, background colour, spine display, 
    and whether the categories should be ordererd based on an aggregate
    function of each category."""

    size:tuple[int, int] = None #Can be None (auto scaling), or an integer tuple. In pixels. #TODO: Move to axis style as this is now the desired axis size?
    title:str = None
    title_font_size:int = 20
    title_colour = "#2c2c2c"
    subtitle:str = None
    subtitle_font_size:int = 11
    subtitle_colour = "#7E7D7D"
    font_family:str = "Liberation Sans"
    font_weight:int = 400
    title_weight:int = 700
    background_colour = "#ffffff"
    sorted:str = None #Can be None, "sum-asc", "sum-desc", "avg-asc", "avg-desc", "lhlf-asc", "lhlf-desc", "rhlf-asc", "rhlf-desc"
    spine_display:tuple[bool, bool, bool, bool] = (False, False, False, False) #left, top, right, bottom


class DEFAULT_LEGEND_STYLE:
    """Default style class for plot legend.
    
    Default style settings for stacked barchart relating to the
    style of the plot legend. The visibility, font size, legend marker
    shape, and padding between legend items is defined here. 

    Default positioning for the legend is also defined here, which
    is managed through a legend anchor location combined with a figure anchor.
    Users are expected to choose one of the given placement options for
    accessibility. A 'placementtransform' is also given to adjust placement."""

    show:bool = False
    font_size:int = 8
    font_colour = "black"
    label_padding:float = 0.8
    marker_shape:str = "s" #see for different marker shapes https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html
    border_colour = DEFAULT_FIG_STYLE.background_colour
    background_colour = DEFAULT_FIG_STYLE.background_colour
    placement:str = "right-vertical"
    placement_options = {
        "right-vertical": ["upper left", (1, 1)],
        "left-vertical": ["upper right", (0, 1)],
        "below-horizontal": ["upper center", (0.5, 0)],
        "above-horizontal": ["lower center", (0.5, 1)]
    }
    placement_transform:tuple[float, float] = (0, 0) #In dots/pixels


class DEFAULT_VERTLINE_STYLE:
    """Default style class for central vertical line.
    
    Default style settings for stacked barchart relating
    to the style of the vertically plotted line for centred
    charts. Linestyle follows the matplotlib standard 
    (see https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html)."""
    show:bool = False
    line_style:str = "-"
    colour = "black"
    alpha:float = 1
    z_order:str = "front" #Can be "front" or "behind"




class StackedPlotStyle:
    """Represent the style configuration for a StackedBarplot plot, and is inherited by StackedBarplot.

    This class categorises plot style configuration variables into different dictionary
    variables which are stored as attributes. This class also includes getter and setter
    methods to safely access these attributes.

    Attributes:
        unrendered_changes: Boolean flag for whether the plot has unrendered changes.
        bar_colours: Instance of class ColourGradient, containing chart bar colours.
        __bar_font_style: Style configurations for bar textual annotations.
        __bar_style: Style configurations for bar design and alignment.
        __legend_style: Style configurations for plot legend.
        __fig_style: Style configurations for general figure style.
        __axis_title_style: Style configurations for axis labels.
        __vert_line_style: Style configurations for central vertical line.
        __axis_style: Style configurations for axis scale font and values
    """
    def __init__(self):
        """Initializes the instance based on default values loaded from defaults.py."""

        self.unrendered_changes = True
        self.bar_colours = ColourGradient()

        self.__axis_style = {
            "xlim": DEFAULT_AXIS_STYLE.x_lim,
            "step": DEFAULT_AXIS_STYLE.step,
            "xfontsize": DEFAULT_AXIS_STYLE.x_font_size,
            "yfontsize": DEFAULT_AXIS_STYLE.y_font_size,
            "xfontcolour": DEFAULT_AXIS_STYLE.x_font_colour,
            "yfontcolour": DEFAULT_AXIS_STYLE.y_font_colour,
            "xaxisformat": DEFAULT_AXIS_STYLE.x_axis_format,
            "xaxisshow": DEFAULT_AXIS_STYLE.x_axis_show,
            "yaxisshow": DEFAULT_AXIS_STYLE.y_axis_show,
            "xaxisabs": DEFAULT_AXIS_STYLE.x_axis_abs
        }
        self.__axis_title_style = {
            "xlabel": DEFAULT_AXIS_TITLE_STYLE.x_label,
            "ylabel": DEFAULT_AXIS_TITLE_STYLE.y_label,
            "axislabelfontsize": DEFAULT_AXIS_TITLE_STYLE.axis_label_font_size,
            "axislabelfontcolour": DEFAULT_AXIS_TITLE_STYLE.axis_label_font_colour
        }
        self.__bar_style = {
            "height": DEFAULT_BAR_STYLE.height,
            "align": DEFAULT_BAR_STYLE.align,
            "startcolour": DEFAULT_BAR_STYLE.start_colour,
            "endcolour": DEFAULT_BAR_STYLE.end_colour,
            "midcolour": DEFAULT_BAR_STYLE.mid_colour
        }
        self.__bar_val_label_style = {
            "fontsize": DEFAULT_BAR_VAL_LABEL_STYLE.font_size,
            "fontcolour": DEFAULT_BAR_VAL_LABEL_STYLE.font_colour,
            "format": DEFAULT_BAR_VAL_LABEL_STYLE.format,
            "align": DEFAULT_BAR_VAL_LABEL_STYLE.align,
            "padding": DEFAULT_BAR_VAL_LABEL_STYLE.padding,
            "colourinvert": DEFAULT_BAR_VAL_LABEL_STYLE.colour_invert,
            "hidesqueezed": DEFAULT_BAR_VAL_LABEL_STYLE.hide_squeezed,
            "expelsqueezedends": DEFAULT_BAR_VAL_LABEL_STYLE.expel_squeezed_ends
        }
        self.__fig_style = {
            "title": DEFAULT_FIG_STYLE.title,
            "titlefontsize": DEFAULT_FIG_STYLE.title_font_size,
            "titlecolour": DEFAULT_FIG_STYLE.title_colour,
            "subtitle": DEFAULT_FIG_STYLE.subtitle,
            "subtitlefontsize": DEFAULT_FIG_STYLE.subtitle_font_size,
            "subtitlecolour": DEFAULT_FIG_STYLE.subtitle_colour,
            "fontfamily": DEFAULT_FIG_STYLE.font_family,
            "fontweight": DEFAULT_FIG_STYLE.font_weight,
            "titleweight": DEFAULT_FIG_STYLE.title_weight,
            "size": DEFAULT_FIG_STYLE.size,
            "backgroundcolour": DEFAULT_FIG_STYLE.background_colour,
            "sorted": DEFAULT_FIG_STYLE.sorted,
            "spinedisplay": DEFAULT_FIG_STYLE.spine_display
        }
        self.__legend_style = {
            "show": DEFAULT_LEGEND_STYLE.show,
            "fontsize": DEFAULT_LEGEND_STYLE.font_size,
            "padding": DEFAULT_LEGEND_STYLE.label_padding,
            "fontcolour": DEFAULT_LEGEND_STYLE.font_colour,
            "backgroundcolour": DEFAULT_LEGEND_STYLE.background_colour,
            "bordercolour": DEFAULT_LEGEND_STYLE.border_colour,
            "placement": DEFAULT_LEGEND_STYLE.placement,
            "markershape": DEFAULT_LEGEND_STYLE.marker_shape,
            "markers": [],
            "transform": DEFAULT_LEGEND_STYLE.placement_transform
        }
        self.__vert_line_style = {
            "show": DEFAULT_VERTLINE_STYLE.show,
            "linestyle": DEFAULT_VERTLINE_STYLE.line_style,
            "colour": DEFAULT_VERTLINE_STYLE.colour,
            "alpha": DEFAULT_VERTLINE_STYLE.alpha,
            "zorder": DEFAULT_VERTLINE_STYLE.z_order
        }


    def get_axis_style(self) -> dict:
        """Returns dictionary containing style configuration for chart axis."""
        return self.__axis_style


    def set_axis_style(self,
                        x_lim:tuple[int, int] = None,
                        step:int = None,
                        x_font_size:int = None,
                        y_font_size:int = None,
                        x_font_colour:str = None,
                        y_font_colour:str = None,
                        x_axis_format:str = None,
                        x_axis_show:bool = None,
                        y_axis_show:bool = None,
                        x_axis_abs:bool = None):
        """Update StackedBarplot axis style configuration.

        Args:
            x_lim: Left and right xlim in data coordinates, as a tuple.
            step: Intevals at which x axis ticks should be displayed. Custom x_lim definition
                is a requirement for step.
            x_font_size: X axis tick label font size in points or as a string (e.g., 'large').
            y_font_size: Y axis tick label font size in points or as a string (e.g., 'large').
            x_font_colour: X axis tick label font colour.
            y_font_colour: X axis tick label font colour.
            x_axis_format: format()-style format string for x axis ticks. Default '{0}'. Format
                string can also round to (e.g., 1) decimal place(s) with '{0:.1}'. A suffix can
                be added using (for example) '{0}%'. See Python documentation for more inforamtion 
                (https://docs.python.org/3/library/string.html#format-specification-mini-language).
            x_axis_show: Boolean flag for if the x axis should show (default True).
            y_axis_show: Boolean flag for if the y axis should show (default True).
            x_axis_abs: Boolean flag for if negative X axis ticks should remain positive (default False).
        """
        if x_lim is not None: self.__axis_style["xlim"] = x_lim
        if step is not None: self.__axis_style["step"] = step
        if x_font_size is not None: self.__axis_style["xfontsize"] = x_font_size
        if y_font_size is not None: self.__axis_style["yfontsize"] = y_font_size
        if x_font_colour is not None: self.__axis_style["xfontcolour"] = x_font_colour
        if y_font_colour is not None: self.__axis_style["yfontcolour"] = y_font_colour
        if x_axis_format is not None: self.__axis_style["xaxisformat"] = x_axis_format
        if x_axis_show is not None: self.__axis_style["xaxisshow"] = x_axis_show
        if y_axis_show is not None: self.__axis_style["yaxisshow"] = y_axis_show
        if x_axis_abs is not None: self.__axis_style["xaxisabs"] = x_axis_abs
        self.unrendered_changes = True


    def get_axis_title_style(self) -> dict:
        """Returns dictionary containing style configuration for chart axis labels."""
        return self.__axis_title_style


    def set_axis_title_style(self,
                            x_label:str = None,
                            y_label:str = None,
                            axis_label_font_size:int = None,
                            axis_label_font_colour:str = None):
        """Update StackedBarplot axis title style configuration.

        Args:
            x_label: X axis label. None (default) will result in no label being displayed.
            y_label: Y axis label. None (default) will result in no label being displayed.
            axis_label_font_size: Axes label font size in points or as a string (e.g., 'large').
            axis_label_font_colour: Axes font colour.
        """
        if x_label is not None: self.__axis_title_style["xlabel"] = x_label
        if y_label is not None: self.__axis_title_style["ylabel"] = y_label
        if axis_label_font_size is not None:
            self.__axis_title_style["axislabelfontsize"] = axis_label_font_size
        if axis_label_font_colour is not None:
            self.__axis_title_style["axislabelfontcolour"] = axis_label_font_colour
        self.unrendered_changes = True

    def get_bar_style(self) -> dict:
        """Returns dictionary containing style configuration for chart bars."""
        return self.__bar_style


    def set_bar_style(self,
                    bar_height:int = None,
                    align:str = None,
                    bar_gradient:ColourGradient = None):
        """Update StackedBarplot bar style configuration.

        Args:
            bar_height: The height of each bar as a fraction. Selection 1 results on 
                no whitespace between displayed categories.
            align: The alignment of bars. Must be either 'left' or 'centre'.
            bar_gradient: ColourGradient object, containing colours matching the number of 
                series in each category.
        """
        if bar_height is not None: self.__bar_style["height"] = bar_height
        if align is not None:
            if align not in ["left", "centre"]:
                raise ValueError("Argument align must be either None, \"left\", or \"centre\".")
            self.__bar_style["align"] = align
        if bar_gradient is not None:
            if not isinstance(bar_gradient, ColourGradient): raise ValueError("Argument bar_gradient must be of type ColourGradient.")
            self.bar_colours = bar_gradient
        self.unrendered_changes = True


    def get_bar_val_label_style(self) -> dict:
        """Returns dictionary containing style configuration for chart bar labels."""
        return self.__bar_val_label_style


    def set_bar_val_label_style(self,
                font_size:int=None,
                font_colour:str = None,
                colour_invert:bool = None,
                format:str = None,
                align:str=None,
                padding:float = None,
                hide_squeezed:str = None,
                expel_squeezed_ends:bool = None
                ):
        """Update StackedBarplot bar text style configuration.

        Args:
            font_size: Data label font size in points or as a string (e.g., 'large').
            font_colour: The colour of data labels.
            colour_invert: Boolean flag for if font colour should be inverted for
                data labels displayed on bars with low luminence.
            format: format()-style format string for data labels. Default '{0}'. Format
                string can also round to (e.g., 1) decimal place(s) with '{0:.1}'. A suffix can
                be added using (for example) '{0}%'. See Python documentation for more inforamtion 
                (https://docs.python.org/3/library/string.html#format-specification-mini-language).
            align: Alignment of data labels within bars. Can be 'left', 'centre', or 'right'. 
            padding: Padding for data labels moved. Given in display coordinate space. 
            hide_squeezed: Whether data labels that overlap their bar should be hidden (e.g., for
                very small bars). Can be None (default), "all" (hide all squeezed data labels), or 
                "inner-only", which ignores data labels for left-most or right-most bars in a category 
                (useful if these data labels are moved outside of the bar).
            expel_squeezed_ends: Boolean flag for whether data labels on start or end bars of categories
                should be moved outside the bar for better clarity (i.e., to the left or right of the
                while category bars) if the annotation is wider than its bar.
        """
        if font_size is not None: self.__bar_val_label_style["fontsize"] = font_size
        if font_colour is not None: self.__bar_val_label_style["fontcolour"] = font_colour
        if colour_invert is not None: self.__bar_val_label_style["colourinvert"] = colour_invert
        if format is not None: self.__bar_val_label_style["format"] = format
        if hide_squeezed not in [None, "all", "inner-only"]:
            raise ValueError("Argument hide-squeezed must be either None, \"all\", or \"inner-only\".")
        elif hide_squeezed is not None: self.__bar_val_label_style["hidesqueezed"] = hide_squeezed
        if expel_squeezed_ends is not None: self.__bar_val_label_style["expelsqueezedends"] = expel_squeezed_ends
        if align is not None:
            if align not in ["left", "centre", "right"]:
                raise ValueError("Argument align must be either \"left\", \"centre\", or \"right\".")
            self.__bar_val_label_style["align"] = align
        if padding is not None: self.__bar_val_label_style["padding"] = padding
        self.unrendered_changes = True


    def get_fig_style(self) -> dict:
        """Returns dictionary containing general style configuration for chart figure."""
        return self.__fig_style


    def set_fig_style(self,
                    title:str = None,
                    title_font_size:int = None,
                    title_colour:str = None,
                    subtitle:str = None,
                    subtitle_font_size:int = None,
                    subtitle_colour:str = None,
                    font_family:str = None,
                    font_weight:int = None,
                    title_weight:int = None,
                    fig_size:tuple[int, int] = None,
                    background_colour:str = None,
                    sorted:str = None,
                    spine_display:tuple[bool, bool, bool, bool] = None):
        """Update StackedBarplot general figure style configuration.

        Args:
            title: The title of the plot.
            title_font_size: Plot title font size in points.
            title_colour: The colour of the plot title.
            subttile: The subtitle of the plot.
            subtitle_font_size: Plot subtitle font size in points.
            subtitle_colour: The colour of the plot subtitle.
            font_family: The font family for all text used in the plot. User must select from
                a list of font families (installed on user's machine).
            font_weight: The font weight for all text used in the plot (excluding title).
            title_weight: The font weight for the figure title.
            fig_size: Tuple of integers representing the width and height of the figure in pixels.
            background_colour: The background colour of the figure.
            sorted: Whether the displayed categories should be ordered. Must be either 
                None, 'sum-asc', 'sum-desc', 'avg-asc', 'avg-desc', 'lhlf-asc', 'lhlf-desc', 'rhlf-asc', or 'rhlf-desc'. 
                Sum denotes the total value of the category, avg denotes the average value, lhlf denotes the sum of the left
                half of the category, and rhlf denotes the sum of the right half of the category.
                Each of these can be sorted in ascending or descending order. None (default) 
                indicates no sorting.
            spine_display: Tuple of booleans representing the four figure spines. Ordered as 
                (left, top, right, bottom).
        """
        if title is not None: self.__fig_style["title"] = title
        if title_font_size is not None: self.__fig_style["titlefontsize"] = title_font_size
        if title_colour is not None: self.__fig_style["titlecolour"] = title_colour
        if subtitle is not None: self.__fig_style["subtitle"] = subtitle
        if subtitle_font_size is not None: self.__fig_style["subtitlefontsize"] = subtitle_font_size
        if subtitle_colour is not None: self.__fig_style["subtitlecolour"] = subtitle_colour
        if font_family is not None: self.__fig_style["fontfamily"] = font_family
        if font_weight is not None: self.__fig_style["fontweight"] = font_weight
        if title_weight is not None: self.__fig_style["titleweight"] = title_weight
        if fig_size is not None:
            if not isinstance(fig_size, tuple) or len(fig_size) != 2:
                raise ValueError("Argument fig_size must be a tuple of two integers representing the width and height of the figure.")
            elif fig_size[0] < 500:
                warnings.warn("An axis width below 500px can result in a larger than expected margin at right of figure.")
            self.__fig_style["size"] = fig_size
        if background_colour is not None: self.__fig_style["backgroundcolour"] = background_colour
        if sorted is not None: #sum-asc, sum-desc, avg-asc, avg-desc, lhlf-asc, lhlf-desc, rhlf-asc, rhlf-desc
            if sorted not in [None, "sum-asc", "sum-desc", "avg-asc", "avg-desc", "lhlf-asc", "lhlf-desc", "rhlf-asc", "rhlf-desc"]:
                raise ValueError("Argument sorted must be either None, sum-asc, sum-desc, avg-asc, avg-desc, lhlf-asc, lhlf-desc, rhlf-asc, or rhlf-desc.")
            self.__fig_style["sorted"] = sorted
        if spine_display is not None:
            if not isinstance(spine_display, tuple) or len(spine_display) != 4:
                raise ValueError("Argument spine_display must be a tuple of four boolean values representing the four figure spines.")
            self.__fig_style["spinedisplay"] = spine_display
        self.unrendered_changes = True


    def get_legend_style(self) -> dict:
        """Returns dictionary containing style configuration for chart legend."""
        return self.__legend_style


    def set_legend_markers(self, markers):
        """Update StackedBarplot legend markers.

        Args:
            markers: List of matplotlib.lines.Line2D objects representing the legend markers.
        """
        if not isinstance(markers, list) or not all(isinstance(marker, mlines.Line2D) for marker in markers):
            raise ValueError("Argument markers must be a list of matplotlib.lines.Line2D objects.")
        self.__legend_style["markers"] = markers


    def set_legend_style(self,
                        show:bool = None,
                        font_size:int = None,
                        padding:float = None,
                        font_colour:str = None,
                        background_colour:str = None,
                        border_colour:str = None,
                        placement:str = None,
                        marker_shape:str = None,
                        transform:tuple[float, float] = None):
        """Update StackedBarplot legend style configuration.

        Args:
            show: A boolean flag for whether the legend should be shown, irrespective
                of other legend style configurations. 
            font_size: Series headings' font size in points or as a string (e.g., 'large').
            padding: Padding between series headings.
            font_colour: The color of the text in the legend.
            background_colour: The legend's background color.
            border_colour: The legend's background patch edge color.
            placement: String representing where around the figure the legend should be
                displayed. {"right-vertical", "below-horizontal", "above-horizontal"}.
            marker_shape: Marker style string. {'*': 'star', '+': 'plus', 's':'square', 
                'o':circle'}. For a full list of marker styles see https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html.
            transform: Allows the user to make minor adjustments to the legend's placement
                after placement choice. Must be tuple of length 2 representing a transform in X and Y axis in dots/pixels. 
        """
        #TODO: finalise method argument documentation relating to legend placement.
        if show is not None: self.__legend_style["show"] = show
        if font_size is not None: self.__legend_style["fontsize"] = font_size
        if padding is not None: self.__legend_style["padding"] = padding
        if font_colour is not None: self.__legend_style["fontcolour"] = font_colour
        if background_colour is not None: self.__legend_style["backgroundcolour"] = background_colour
        if border_colour is not None: self.__legend_style["bordercolour"] = border_colour
        if placement is not None:
            if placement not in ["right-vertical", "below-horizontal", "above-horizontal"]:
                raise ValueError("Placement must be either \"right-vertical\", \"below-horizontal\", \"above-horizontal\".")
            self.__legend_style["placement"] = placement
        if marker_shape is not None: self.__legend_style["markershape"] = marker_shape
        if transform is not None:
            if not isinstance(transform, tuple) and len(transform) != 2:
                raise ValueError("Argument transform must be tuple of length two representing transform in X and Y axis in dots/pixels.")
            self.__legend_style["transform"] = transform
        self.unrendered_changes = True


    def get_vert_line_style(self) -> dict:
        """Returns dictionary containing style configuration for chart vertical line."""
        return self.__vert_line_style


    def set_vert_line_style(self,
                    show:bool = None,
                    line_style:str = None,
                    colour:str = None,
                    alpha:float = None,
                    z_order:str = None):
        """Update StackedBarplot central vertical line style configuration.

        Args:
            show: A boolean flag for whether the vertical line should be shown,
                irrespectiev of other vertical line style configurations.
            line_style: Set the linestyle of the line. Is {'-', '--', '-.', ':', '', ...}.
            colour: The colour of the line.
            alpha: The alpha value of the line.
            z_order: Whether the vertical line is displayed in front or behind the plot. Is
                {"front", "behind"}.
        """
        if show is not None: self.__vert_line_style["show"] = show
        if line_style is not None: self.__vert_line_style["linestyle"] = line_style
        if colour is not None: self.__vert_line_style["colour"] = colour
        if alpha is not None:
            if alpha < 0 or alpha > 1:
                raise ValueError("Argument alpha must be a float between 0 and 1.")
            self.__vert_line_style["alpha"] = alpha
        if z_order is not None:
            if z_order not in ["front", "behind"]:
                raise ValueError("Argument z_order must be a string with value of either \"front\" or \"behind\".")
            self.__vert_line_style["zorder"] = z_order
        self.unrendered_changes = True
