# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,line-too-long
"""User-facing module pertaining to the stacked-barplots Python library.

Module contains a number of non-member methods which users may call to 
create horizontal stacked bar charts. Methods return StackedBarplot objects
(from module core.py) from which specific style configurations may be made,
plot rendered, and saved or displayed to the user. Barplots are created with
default values defined in the module defaults.py.

Typical usage example:

    results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
    series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

    basic_plot = basic(results, series_labels)
    basic_plot.render()
    basic_plot.show()

    center_plot = centered(results, series_labels)
    center_plot.render()
    center_plot.show()

    custom_plot = basic(results, series_labels, title="Custom Plot")
    custom_plot.set_legend_style(show=True, fontsize=8)
    custom_plot.set_bar_labels_style(barvalueformat="{0}%", align="left", padding=.5)
    custom_plot.set_axis_style(step=5)
    custom_plot.set_bar_style(barheight=.5)
    custom_plot.render()
    custom_plot.show()
"""


from defaults import DEFAULT_BAR_FONT
from tools import *
import core


def basic(
        data:core.results_type,
        series_labels:core.series_labels_type,
        title:str = None,
        figsize:list[int, int] = [10, 5],
        fontsize:int = DEFAULT_BAR_FONT.size,
        fontcolour:str = DEFAULT_BAR_FONT.colour,
        barvalueformat:str = DEFAULT_BAR_FONT.format,
        barvaluealign:str = DEFAULT_BAR_FONT.align,
        barcolours:core.colour_type = None,
        legendloc:str = None,
        xaxislim:tuple[int, int] = None,
        xaxisstep:int = None,
        barheight:float = 0.8
        ) -> core.StackedBarplot:
    """
    Draw a simple left-aligned horizontal stacked bar chart.

    Args:
        data: Dictionary of category headings and associated category integer or float 
            data. For example, {"Ages": [12, 3, 4, 1], ...}. Order of data list must follow
            order of series labels. 
        series_labels: Required list of string headings for chart series, to be (optionally) be 
            displayed on legend.
        title: The title of the plot.
        figsize: Tuple of integers representing the width and height of the figure.
        fontsize: Figure font size in points or as a string (e.g., 'large'). Font size for 
            individual figure elemetns may be changed with set_style_ methods.
        fontcolour: Figure font colour. Font colour for individual plot elements may be changed 
            with set_style_ methods.
        barvalueformat: format()-style format string for data labels. Default '{0}'. Format
                string can also round to (e.g., 1) decimal place(s) with '{0:.1}'. A suffix can
                be added using (for example) '{0}%'. See Python documentation for more inforamtion 
                (https://docs.python.org/3/library/string.html#format-specification-mini-language).
        barvaluealign: Alignment of data labels within bars. Can be 'left', 'center', or 'right'. 
        barcolours: List of colour tuples, matching the number of series in each category.
        legendloc: WORK IN PROGRESS
        xaxislim:Left and right xlim in data coordinates, as a tuple.
        xaxisstep: Intevals at which x axis ticks should be displayed.
        barheight: The height of each bar as a fraction. Selection 1 results on 
                no whitespace between displayed categories.

    Returns:
        StackedBarplot: User must call .render() on returned object to render figure. The 
            figure can be saved or displayed with .save() or .show().
    
    """
    #TODO: Improve method argument barcolours docstring to signpost colour methods.

    local_style = core.StackedPlotStyle()
    local_style.figstored["title"] = title
    local_style.barfontstored["fontsize"] = fontsize
    local_style.barfontstored["fontcolour"] = fontcolour
    local_style.barfontstored["fontformat"] = barvalueformat
    local_style.barfontstored["fontalign"] = barvaluealign
    local_style.barfontstored["endthreshpadd"] = True
    local_style.barfontstored["paddthresh"] = 4

    if xaxislim is not None: local_style.axisstored["xlim"] = xaxislim
    if xaxisstep is not None: local_style.axisstored["step"] = xaxisstep
    if barcolours is not None: local_style.barstored["barcolours"] = barcolours
    if legendloc is not None: local_style.legendstored["location"] = legendloc

    local_style.legendstored["fontsize"] = fontsize
    local_style.figstored["size"] = figsize
    local_style.barstored["align"] = "left"
    local_style.barstored["barheight"] = barheight
    local_style.figstored["spinedisplay"] = (False, False, False, True)

    plot = core.StackedBarplot(data, series_labels)
    plot.set_style(local_style)

    return plot

def centered(
        data:core.results_type,
        series_labels:core.series_labels_type,
        title:str = None,
        figsize:list[int, int] = [10, 5],
        fontsize:int = DEFAULT_BAR_FONT.size,
        fontcolour:str = DEFAULT_BAR_FONT.colour,
        barvalueformat:str = DEFAULT_BAR_FONT.format,
        barvaluealign:str = DEFAULT_BAR_FONT.align,
        barcolours:list[tuple[float, float, float]] = None,
        legendloc:str = None,
        xaxislim:tuple[int, int] = None,
        xaxisstep:int = None,
        barheight:float = 0.8
        ) -> core.StackedBarplot:
    """
    Draw a simple center-aligned horizontal stacked bar chart with central dividing line.

    Args:
        data: Dictionary of category headings and associated category integer or float 
            data. For example, {"Ages": [12, 3, 4, 1], ...}. Order of data list must follow
            order of series labels. 
        series_labels: Required list of string headings for chart series, to be (optionally) be 
            displayed on legend.
        title: The title of the plot.
        figsize: Tuple of integers representing the width and height of the figure.
        fontsize: Figure font size in points or as a string (e.g., 'large'). Font size for 
            individual figure elemetns may be changed with set_style_ methods.
        fontcolour: Figure font colour. Font colour for individual plot elements may be changed 
            with set_style_ methods.
        barvalueformat: format()-style format string for data labels. Default '{0}'. Format
                string can also round to (e.g., 1) decimal place(s) with '{0:.1}'. A suffix can
                be added using (for example) '{0}%'. See Python documentation for more inforamtion 
                (https://docs.python.org/3/library/string.html#format-specification-mini-language).
        barvaluealign: Alignment of data labels within bars. Can be 'left', 'center', or 'right'. 
        barcolours: List of colour tuples, matching the number of series in each category.
        legendloc: WORK IN PROGRESS
        xaxislim:Left and right xlim in data coordinates, as a tuple.
        xaxisstep: Intevals at which x axis ticks should be displayed.
        barheight: The height of each bar as a fraction. Selection 1 results on 
                no whitespace between displayed categories.

    Returns:
        StackedBarplot: User must call .render() on returned object to render figure. The 
            figure can be saved or displayed with .save() or .show().
        
    """
    #TODO: Improve method argument barcolours docstring to signpost colour methods.

    local_style = core.StackedPlotStyle()
    local_style.figstored["title"] = title
    local_style.barfontstored["fontsize"] = fontsize
    local_style.barfontstored["fontcolour"] = fontcolour
    local_style.barfontstored["fontformat"] = barvalueformat
    local_style.barfontstored["fontalign"] = barvaluealign
    local_style.barfontstored["endthreshpadd"] = True
    local_style.barfontstored["paddthresh"] = 4

    if xaxislim is not None: local_style.axisstored["xlim"] = xaxislim
    if xaxisstep is not None: local_style.axisstored["step"] = xaxisstep
    if barcolours is not None: local_style.barstored["barcolours"] = barcolours
    if legendloc is not None: local_style.legendstored["location"] = legendloc

    local_style.legendstored["fontsize"] = fontsize
    local_style.figstored["size"] = figsize
    local_style.barstored["align"] = "center"
    local_style.barstored["barheight"] = barheight
    local_style.vertlinestored["show"] = True
    local_style.figstored["spinedisplay"] = (False, False, False, True)

    plot = core.StackedBarplot(data, series_labels)
    plot.set_style(local_style)

    return plot

#Not yet implemented
def normalised():
    """Not yet implemented."""
    pass

#Not yet implemented
def normcentered():
    """Not yet implemented."""
    pass

if __name__ == "__main__":
    results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
    series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

    basic_plot = basic(results, series_labels)
    basic_plot.render()
    basic_plot.show()

    center_plot = centered(results, series_labels)
    center_plot.render()
    center_plot.show()

    custom_plot = basic(results, series_labels, title="Custom Plot")
    custom_plot.set_legend_style(show=True, fontsize=8)
    custom_plot.set_bar_labels_style(barvalueformat="{0}%", align="left", padding=.5)
    custom_plot.set_axis_style(step=5)
    custom_plot.set_bar_style(barheight=.5)
    custom_plot.render()
    custom_plot.show()
