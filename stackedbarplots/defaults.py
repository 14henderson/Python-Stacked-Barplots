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

#TODO: Convert variable names to snake_case

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
    align:str = "center"
    padding:float = 1.5
    display_thresh:tuple[float, float] = (0, None)
    colour_invert:bool = False
    padding_thresh:float = 0 #The threshold for if a label should be moved
    end_thresh_padd:bool = False


class DEFAULT_BAR_STYLE:
    """Default style class for bar design and alignment.
    
    Default style settings for stacked barchart relating to
    the design of bars themselves. Align defines how to align the
    figure: [left] stacks bars from 0 on X axis, and [center] aligns bars 
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

    size:tuple[int, int] = None
    title:str = None
    title_font_size:int = 12
    title_colour = "black"
    font_family:str = "sans-serif"
    background_colour = "#ffffff"
    ordered:str = "unordered"
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
    to the style of the vertically plotted line for centered
    charts. Linestyle follows the matplotlib standard 
    (see https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html)."""
    show:bool = False
    line_style:str = "-"
    colour = "black"
    alpha:float = 1
    order:str = "front"




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
            "alpha": DEFAULT_VERTLINE_STYLE.alpha,
            "order": DEFAULT_VERTLINE_STYLE.order
        }

        self.axis = {
            "xlim": DEFAULT_AXIS_STYLE.x_lim,
            "step": DEFAULT_AXIS_STYLE.step,
            "xfontsize": DEFAULT_AXIS_STYLE.x_font_size,
            "yfontsize": DEFAULT_AXIS_STYLE.y_font_size,
            "xaxisformat": DEFAULT_AXIS_STYLE.x_axis_format,
            "xaxisshow": DEFAULT_AXIS_STYLE.x_axis_show
        }