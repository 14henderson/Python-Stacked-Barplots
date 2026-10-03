# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,line-too-long,invalid-name

"""Defaults module pertaining to stacked-barplots Python library.

defaults.py contains classes which store the default values for
all plot style elements covered in this project. Plot styles are 
separated into bars, bar text, overall axes and figure styles, and 
style settings relating to the plot legend and (where appropriate)
the vertical line. 

Typical usage example:

  foo = ClassFoo()
  bar = foo.function_bar()
"""

import matplotlib.lines as mlines
from .tools import ColourGradient

__all__ = [
    "StackedPlotStyle", "DEFAULT_BAR_FONT_STYLE", "DEFAULT_BAR_STYLE", "DEFAULT_FIG_STYLE", 
    "DEFAULT_AXIS_STYLE", "DEFAULT_AXIS_TITLE_STYLE", "DEFAULT_LEGEND_STYLE", 
    "DEFAULT_VERTLINE_STYLE"
]




class DEFAULT_BAR_FONT_STYLE:
    """Default style class for bar textual annotations.
    
    Default style settings for stacked barchart relating to 
    textual annotations made on data bars containing bar values. 
    Default values are stored on font size, colour, format, alignment in bar, and 
    a display threshold. The user can also specify if the text colour should be
    inverted when displayed on a dark-coloured bar; this is set to False by default.

    More advanced style settings allow the user to specify if, when the 
    bar value is below a certain value (and thus below a certain visual width), 
    whether (for first or last bars for a category) the value should be moved outside 
    of the bar."""

    size:int = 12
    colour = "black"
    format:str = "{0:.1f}"
    align:str = "centre"
    padding:float = 1.5
    display_thresh:tuple[float, float] = (0, None)
    colour_invert:bool = False
    padding_thresh:float = 0 #The threshold for if a label should be moved
    end_thresh_padd:bool = False


class DEFAULT_BAR_STYLE:
    """Default style class for bar design and alignment.
    
    Default style settings for stacked barchart relating to
    the design of bars themselves. Align defines how to align the
    figure: [left] stacks bars from 0 on X axis, and [centre] aligns bars 
    centrally on X axis. The start, mid, and end colour are also defined
    here for a colour gradient to be generated."""

    align:str = "left"
    height:float = 0.8
    start_colour:tuple[int, int, int] = (227, 108, 85)
    end_colour:tuple[int, int, int] = (106, 139, 239)
    mid_colour:tuple[int, int, int] = (220, 221, 221)


class DEFAULT_FIG_STYLE:
    """Default style class for general figure style.

    Default style settings for stacked barchart relating to the
    style of the figure itself. Default values on figure size, title (and
    related settings), figure font family, background colour, spine display, 
    and whether the bars are ordered are defined here."""

    size:tuple[int, int] = (10, 5)
    title:str = None
    title_font_size:int = 12
    title_colour = "black"
    font_family:str = "sans-serif"
    background_colour = "#ffffff"
    sorted:str = None
    spine_display:tuple[bool, bool, bool, bool] = (False, False, False, True) #left, top, right, bottom


class DEFAULT_AXIS_STYLE:
    """Default style class for axis scale font and values
    
    Default style settings for stacked barchart relating to the
    style of axis font and format are defined here. This includes
    axis min and max limits, font size, and format.
    
    xlim is stored as tuple of two integers representing the minimum
    and maximum values to be displayed on the X axis (None indicates 
    no limit). Font format is str.format() type, default as "{0}".
    """

    x_lim:tuple[int, int] = None
    step:int = None
    x_font_size:int = 12
    y_font_size:int = 12
    x_axis_format:str = "{0:.0f}"
    x_axis_show:bool = True
    y_axis_show:bool = True
    x_axis_abs:bool = False


class DEFAULT_AXIS_TITLE_STYLE:
    """Default style class for axis labels.

    Default style settings for stacked barchart relating to the 
    style of X and Y axis labels. None value indicates no label.
    """
    x_label:str = None
    y_label:str = None
    axis_label_font_size:int = 12
    axis_label_font_colour = "black"


class DEFAULT_LEGEND_STYLE:
    """Default style class for plot legend.
    
    Default style settings for stacked barchart relating to the
    style of the plot legend. The visibility, font size, legend marker
    shape, and spacing between legend items is defined here. 

    Default positioning for the legend is also defined here, which
    is managed through a legend anchor location combined with a figure anchor.
    Users are expected to choose one of the given placement options for
    accessibility. A 'placementtransform' is also given to adjust placement.
    """

    show:bool = False
    font_size:int = 12
    label_spacing:float = 0.5
    font_colour = "black"
    marker_shape:str = "s" #see for different marker shapes https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html
    border_colour = "#ededed"
    background_colour = "#ededed"
    placement:str = "right-vertical" #TODO: tidy up the difference between placement and location
    placement_options = {
        "right-vertical": ["upper left", (1.12, 1)],
        "left-vertical": ["upper right", (-0.12, 1)],
        "below-horizontal": ["upper center", (0.5, -0.12)],
        "above-horizontal": ["lower center", (0.5, 1.02)]
    }
    placement_transform:tuple[float, float] = (0, 0)


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
    z_order:str = "front"




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
        self.__bar_font_style = {
            "fontsize": DEFAULT_BAR_FONT_STYLE.size,
            "fontcolour": DEFAULT_BAR_FONT_STYLE.colour,
            "fontformat": DEFAULT_BAR_FONT_STYLE.format,
            "fontalign": DEFAULT_BAR_FONT_STYLE.align,
            "fontpadd": DEFAULT_BAR_FONT_STYLE.padding,
            "fontcolourinvert": DEFAULT_BAR_FONT_STYLE.colour_invert,
            "fontdisplaythresh": DEFAULT_BAR_FONT_STYLE.display_thresh,
            "fontpaddthresh": DEFAULT_BAR_FONT_STYLE.padding_thresh,
            "fontendthreshpadd": DEFAULT_BAR_FONT_STYLE.end_thresh_padd
        }
        self.__fig_style = {
            "title": DEFAULT_FIG_STYLE.title,
            "titlefontsize": DEFAULT_FIG_STYLE.title_font_size,
            "titlecolour": DEFAULT_FIG_STYLE.title_colour,
            "fontfamily": DEFAULT_FIG_STYLE.font_family,
            "size": DEFAULT_FIG_STYLE.size,
            "backgroundcolour": DEFAULT_FIG_STYLE.background_colour,
            "sorted": DEFAULT_FIG_STYLE.sorted,
            "spinedisplay": DEFAULT_FIG_STYLE.spine_display
        }
        self.__legend_style = {
            "show": DEFAULT_LEGEND_STYLE.show,
            "fontsize": DEFAULT_LEGEND_STYLE.font_size,
            "spacing": DEFAULT_LEGEND_STYLE.label_spacing,
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


    def get_bar_labels_style(self) -> dict:
        """Returns dictionary containing style configuration for chart bar labels."""
        return self.__bar_font_style


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
            font_size: Data label font size in points or as a string (e.g., 'large').
            font_colour: The colour of data labels.
            font_colour_invert: Boolean flag for if font colour should be inverted for
                data labels displayed on bars with low luminence.
            bar_value_format: format()-style format string for data labels. Default '{0}'. Format
                string can also round to (e.g., 1) decimal place(s) with '{0:.1}'. A suffix can
                be added using (for example) '{0}%'. See Python documentation for more inforamtion 
                (https://docs.python.org/3/library/string.html#format-specification-mini-language).
            display_thresh: Tuple of floats representing optional minimum and maximum display
                thresholds. Data labels below minimum or above maximum thresholds will not be displayed.
            padd_thresh: Threshold for whether data labels on start or end bars of categories should
                be moved for better clarity (see parameter endthreshpadd).
            end_thresh_padd: Boolean value indicating whether, for data values for start or end bars, 
                if the data value is below paddthresh, is should be moved outside of the bar for better
                clarity. 
            align: Alignment of data labels within bars. Can be 'left', 'centre', or 'right'. 
            padding: Padding for data labels moved.
        """
        if font_size is not None: self.__bar_font_style["fontsize"] = font_size
        if font_colour is not None: self.__bar_font_style["fontcolour"] = font_colour
        if font_colour_invert is not None: self.__bar_font_style["fontcolourinvert"] = font_colour_invert
        if bar_value_format is not None: self.__bar_font_style["fontformat"] = bar_value_format
        if display_thresh is not None: self.__bar_font_style["fontdisplaythresh"] = display_thresh
        if padd_thresh is not None: self.__bar_font_style["fontpaddthresh"] = padd_thresh
        if end_thresh_padd is not None: self.__bar_font_style["fontendthreshpadd"] = end_thresh_padd
        if align is not None:
            if align not in ["left", "centre", "right"]:
                raise ValueError("Argument align must be either \"left\", \"centre\", or \"right\".")
            self.__bar_font_style["fontalign"] = align
        if padding is not None: self.__bar_font_style["fontpadd"] = padding
        self.unrendered_changes = True


    def get_fig_style(self) -> dict:
        """Returns dictionary containing general style configuration for chart figure."""
        return self.__fig_style


    def set_fig_style(self,
                    title:str = None,
                    title_font_size:int = None,
                    title_colour:str = None,
                    font_family:str = None,
                    fig_size:tuple[int, int] = None,
                    background_colour:str = None,
                    sorted:str = None,
                    spine_display:tuple[bool, bool, bool, bool] = None):
        """Update StackedBarplot general figure style configuration.

        Args:
            title: The title of the plot.
            title_font_size: Plot title font size in points or as a string (e.g., 'large').
            title_colour: The colour of the plot title.
            font_family: The font family for all text used in the plot. User must select from
                a list of font families (installed on user's machine).
            fig_size: Tuple of integers representing the width and height of the figure.
            background_colour: The background colour of the figure.
            sorted: Whether the displayed categories should be ordered. Must be either 
                None, 'ascending', or 'descending'. Categories are ordered based on sum of
                leftmost bars.
            spine_display: Tuple of booleans representing the four figure spines. Ordered as (left, top, right, bottom).
        """
        if title is not None: self.__fig_style["title"] = title
        if title_font_size is not None: self.__fig_style["titlefontsize"] = title_font_size
        if title_colour is not None: self.__fig_style["titlecolour"] = title_colour
        if font_family is not None: self.__fig_style["fontfamily"] = font_family
        if fig_size is not None:
            if not isinstance(fig_size, tuple) or len(fig_size) != 2:
                raise ValueError("Argument fig_size must be a tuple of two integers representing the width and height of the figure.")
            self.__fig_style["size"] = fig_size
        if background_colour is not None: self.__fig_style["backgroundcolour"] = background_colour
        if sorted is not None:
            if sorted not in [None, "ascending", "descending"]:
                raise ValueError("Argument sorted must be either None, 'ascending', or 'descending'.")
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
                        spacing:float = None,
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
            spacing: Spacing between series headings, in font-size units.
            font_colour: The color of the text in the legend.
            background_colour: The legend's background color.
            border_colour: The legend's background patch edge color.
            placement: String representing where around the figure the legend should be
                displayed. {"right-vertical", "left-vertical", "below-horizontal", "above-horizontal"}.
            marker_shape: Marker style string. {'*': 'star', '+': 'plus', 's':'square', 
                'o':circle'}. For a full list of marker styles see https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html.
            transform: Allows the user to make minor adjustments to the legend's placement
                after placement choice. Must be tuple of length 2 representing a transform in X and Y axis. 
        """
        #TODO: finalise method argument documentation relating to legend placement.
        if show is not None: self.__legend_style["show"] = show
        if font_size is not None: self.__legend_style["fontsize"] = font_size
        if spacing is not None: self.__legend_style["spacing"] = spacing
        if font_colour is not None: self.__legend_style["fontcolour"] = font_colour
        if background_colour is not None: self.__legend_style["backgroundcolour"] = background_colour
        if border_colour is not None: self.__legend_style["bordercolour"] = border_colour
        if placement is not None:
            if placement not in ["right-vertical", "left-vertical", "below-horizontal", "above-horizontal"]:
                raise ValueError("Placement must be either \"right-vertical\", \"left-vertical\", \"below-horizontal\", \"above-horizontal\".")
            self.__legend_style["placement"] = placement
        if marker_shape is not None: self.__legend_style["markershape"] = marker_shape
        if transform is not None:
            if not isinstance(transform, tuple) and len(transform) != 2:
                raise ValueError("Argument transform must be tuple of length two representing transform in X and Y axis.")
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
