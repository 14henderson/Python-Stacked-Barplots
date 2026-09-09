# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,line-too-long
"""User-facing module pertaining to the stacked-barplots Python library.

Module contains a number of non-member methods which users may call to 
create horizontal stacked bar charts. Methods return StackedBarplot objects
(from module core.py) from which specific style configurations may be made,
plot rendered, and saved or displayed to the user. Barplots are created with
default values defined in the module defaults.py.

Typical usage example:
    import stackedbarplots

    results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
    series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

    #Example Basic Plot
    basic_plot = stackedbarplots.basic(results, series_labels)
    basic_plot.render()
    basic_plot.show()

    #Example Centered Plot
    center_plot = stackedbarplots.centered(results, series_labels)
    center_plot.render()
    center_plot.show()

    #Example Custom Plot
    custom_colours = stackedbarplots.ColourGradient()
    custom_colours.gradient(len(series_labels), (200, 100, 150), (100, 150, 200))
    custom_plot = stackedbarplots.basic(results, series_labels, title="Custom Plot", bar_colours=custom_colours)
    custom_plot.set_legend_style(show=True, font_size=8)
    custom_plot.set_bar_labels_style(bar_value_format="{0}%", align="left", padding=.5)
    custom_plot.set_axis_style(step=5)
    custom_plot.set_bar_style(bar_height=.5)
    custom_plot.render()
    custom_plot.show()
"""


from .defaults import DEFAULT_BAR_FONT
from .tools import *
from .core import StackedBarplot, StackedPlotStyle


__all__ = [
    "basic", "centered"
]


def basic(
        data:dict[str, list[float]],
        series_labels:list[str],
        title:str = None,
        fig_size:tuple[int, int] = (10, 5),
        font_size:int = DEFAULT_BAR_FONT.size,
        font_colour:str = DEFAULT_BAR_FONT.colour,
        data_label_format:str = DEFAULT_BAR_FONT.format,
        data_label_align:str = DEFAULT_BAR_FONT.align,
        bar_colours:ColourGradient = None,
        legend_placement:str = None,
        x_axis_lim:tuple[int, int] = None,
        x_axis_step:int = None,
        bar_height:float = 0.8
        ) -> StackedBarplot:
    """
    Draw a simple left-aligned horizontal stacked bar chart.

    Args:
        data: Dictionary of category headings and associated category integer or float 
            data. For example, {"Ages": [12, 3, 4, 1], ...}. Order of data list must follow
            order of series labels. 
        series_labels: Required list of string headings for chart series, to be (optionally) be 
            displayed on legend.
        title: The title of the plot.
        fig_size: Tuple of integers representing the width and height of the figure.
        font_size: Figure font size in points or as a string (e.g., 'large'). Font size for 
            individual figure elemetns may be changed with set_style_ methods.
        font_colour: Figure font colour. Font colour for individual plot elements may be changed 
            with set_style_ methods.
        data_label_format: format()-style format string for data labels. Default '{0}'. Format
                string can also round to (e.g., 1) decimal place(s) with '{0:.1}'. A suffix can
                be added using (for example) '{0}%'. See Python documentation for more inforamtion 
                (https://docs.python.org/3/library/string.html#format-specification-mini-language).
        data_label_align: Alignment of data labels within bars. Can be 'left', 'center', or 'right'. 
        bar_colours: List of colour tuples, matching the number of series in each category.
        legend_placement: String representing where around the figure the legend should be
                        displayed. {"right-vertical", "left-vertical", "below-horizontal", "above-horizontal"}.
        x_axis_lim:Left and right xlim in data coordinates, as a tuple.
        x_axis_step: Intevals at which x axis ticks should be displayed.
        bar_height: The height of each bar as a fraction. Selection 1 results on 
                no whitespace between displayed categories.

    Returns:
        StackedBarplot: User must call .render() on returned object to render figure. The 
            figure can be saved or displayed with .save() or .show().
    
    """
    local_style = StackedPlotStyle()
    plot = StackedBarplot(data, series_labels)
    plot.set_style(local_style)

    plot.set_axis_style(x_lim=x_axis_lim, step=x_axis_step)
    plot.set_bar_style(align="left", bar_height=bar_height)
    if bar_colours is not None: plot.set_bar_style(bar_gradient=bar_colours)

    plot.set_fig_style(title=title,
                       fig_size=fig_size,
                       spine_display=(False, False, False, True))

    plot.set_bar_labels_style(font_size=font_size,
                              font_colour=font_colour,
                              bar_value_format=data_label_format,
                              align=data_label_align,
                              end_thresh_padd=True,
                              padd_thresh=4)

    if legend_placement is not None:
        plot.set_legend_style(show=True,
                              placement=legend_placement,
                              font_size=font_size)

    return plot

def centered(
        data:dict[str, list[float]],
        series_labels:list[str],
        title:str = None,
        fig_size:tuple[int, int] = (10, 5),
        font_size:int = DEFAULT_BAR_FONT.size,
        font_colour:str = DEFAULT_BAR_FONT.colour,
        data_label_format:str = DEFAULT_BAR_FONT.format,
        data_label_align:str = DEFAULT_BAR_FONT.align,
        bar_colours:ColourGradient = None,
        legend_placement:str = None,
        x_axis_lim:tuple[int, int] = None,
        x_axis_step:int = None,
        bar_height:float = 0.8
        ) -> StackedBarplot:
    """
    Draw a simple center-aligned horizontal stacked bar chart with central dividing line.

    Args:
        data: Dictionary of category headings and associated category integer or float 
            data. For example, {"Ages": [12, 3, 4, 1], ...}. Order of data list must follow
            order of series labels. 
        series_labels: Required list of string headings for chart series, to be (optionally) be 
            displayed on legend.
        title: The title of the plot.
        fig_size: Tuple of integers representing the width and height of the figure.
        font_size: Figure font size in points or as a string (e.g., 'large'). Font size for 
            individual figure elemetns may be changed with set_style_ methods.
        font_colour: Figure font colour. Font colour for individual plot elements may be changed 
            with set_style_ methods.
        data_label_format: format()-style format string for data labels. Default '{0}'. Format
                string can also round to (e.g., 1) decimal place(s) with '{0:.1}'. A suffix can
                be added using (for example) '{0}%'. See Python documentation for more inforamtion 
                (https://docs.python.org/3/library/string.html#format-specification-mini-language).
        data_label_align: Alignment of data labels within bars. Can be 'left', 'center', or 'right'. 
        bar_colours: List of colour tuples, matching the number of series in each category.
        legend_placement: String representing where around the figure the legend should be
                        displayed. {"right-vertical", "left-vertical", "below-horizontal", "above-horizontal"}.
        x_axis_lim:Left and right xlim in data coordinates, as a tuple.
        x_axis_step: Intevals at which x axis ticks should be displayed.
        bar_height: The height of each bar as a fraction. Selection 1 results on 
                no whitespace between displayed categories.

    Returns:
        StackedBarplot: User must call .render() on returned object to render figure. The 
            figure can be saved or displayed with .save() or .show().
        
    """
    local_style = StackedPlotStyle()
    plot = StackedBarplot(data, series_labels)
    plot.set_style(local_style)

    plot.set_axis_style(x_lim=x_axis_lim, step=x_axis_step)
    plot.set_bar_style(align="center", bar_height=bar_height)
    if bar_colours is not None: plot.set_bar_style(bar_gradient=bar_colours)
    plot.set_vert_line_style(show=True)

    plot.set_fig_style(title=title,
                       fig_size=fig_size, 
                       spine_display=(False, False, False, True))

    plot.set_bar_labels_style(font_size=font_size,
                              font_colour=font_colour,
                              bar_value_format=data_label_format,
                              align=data_label_align,
                              end_thresh_padd=True,
                              padd_thresh=4)

    if legend_placement is not None:
        plot.set_legend_style(show=True,
                              placement=legend_placement,
                              font_size=font_size)

    return plot

#Not yet implemented
def normalised():
    """Not yet implemented."""
    pass

#Not yet implemented
def normcentered():
    """Not yet implemented."""
    pass