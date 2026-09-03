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
    "DEFAULT_BAR_FONT", "DEFAULT_BAR_STYLE", "DEFAULT_FIG_STYLE", 
    "DEFAULT_AXIS_STYLE", "DEFAULT_AXIS_TITLE_STYLE", "DEFAULT_LEGEND_STYLE", 
    "DEFAULT_VERTLINE_STYLE"
]



class DEFAULT_BAR_FONT:
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
    displaythresh:tuple[float, float] = (0, None)
    colourinvert:bool = False
    paddingthresh:float = 0 #The threshold for if a label should be moved
    endthreshpadd:bool = False


class DEFAULT_BAR_STYLE:
    """Default style class for bar design and alignment.
    
    Default style settings for stacked barchart relating to
    the design of bars themselves. Align defines how to align the
    figure: [left] stacks bars from 0 on X axis, and [center] aligns bars 
    centrally on X axis. The start, mid, and end colour are also defined
    here for a colour gradient to be generated."""

    align:str = "left"
    height:float = 0.8
    startcolour:tuple[int, int, int] = (227, 108, 85)
    endcolour:tuple[int, int, int] = (106, 139, 239)
    midcolour:tuple[int, int, int] = (220, 221, 221)


class DEFAULT_FIG_STYLE:
    """Default style class for general figure style.

    Default style settings for stacked barchart relating to the
    style of the figure itself. Default values on figure size, title (and
    related settings), figure font family, background colour, spine display, 
    and whether the bars are ordered are defined here."""

    size:tuple[int, int] = None
    title:str = None
    titlefontsize:int = 12
    titlecolour = "black"
    fontfamily:str = "sans-serif"
    backgroundcolour = "#ffffff"
    ordered:str = "unordered"
    spinedisplay:tuple[bool, bool, bool, bool] = (False, False, False, True) #left, top, right, bottom


class DEFAULT_AXIS_STYLE:
    """Default style class for axis scale font and values
    
    Default style settings for stacked barchart relating to the
    style of axis font and format are defined here. This includes
    axis min and max limits, font size, and format.
    
    xlim is stored as tuple of two integers representing the minimum
    and maximum values to be displayed on the X axis (None indicates 
    no limit). Font format is str.format() type, default as "{0}".
    """

    xlim:tuple[int, int] = None
    step:int = None
    xfontsize:int = 12
    yfontsize:int = 12
    xaxisformat:str = "{0}"


class DEFAULT_AXIS_TITLE_STYLE:
    """Default style class for axis labels.

    Default style settings for stacked barchart relating to the 
    style of X and Y axis labels. None value indicates no label.
    """
    xlabel:str = None
    ylabel:str = None
    axislabelfontsize:int = 12
    axislabelfontcolour = "black"


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
    fontsize:int = 12
    labelspacing:float = 0.5
    location:str = "upper left" #Which corner of the legend box is the anchor
    fontcolour = "black"
    markershape:str = "s" #see for different marker shapes https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html
    bordercolour = "#ededed"
    backgroundcolour = "#ededed"
    placement:str = "right-vertical" #TODO: tidy up the difference between placement and location
    placementoptions = {
        "right-vertical": ["upper left", (1.12, 1)],
        "left-vertical": ["upper right", (-0.12, 1)],
        "below-horizontal": ["upper center", (0.5, -0.12)],
        "above-horizontal": ["lower center", (0.5, 1.02)]
    }
    placementtransform:tuple[float, float] = (0, 0)


class DEFAULT_VERTLINE_STYLE:
    """Default style class for central vertical line.
    
    Default style settings for stacked barchart relating
    to the style of the vertically plotted line for centered
    charts. Linestyle follows the matplotlib standard 
    (see https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html)."""
    show:bool = False
    linestyle:str = "-"
    colour = "black"
    alpha:float = 1
