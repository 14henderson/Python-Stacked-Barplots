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

    custom_colours = ColourGradient()
    custom_colours.gradient(len(series_labels), (200, 100, 150), (100, 150, 200))
    custom_plot = basic(results, series_labels, title="Custom Plot", bar_colours=custom_colours)
    custom_plot.set_legend_style(show=True, fontsize=8)
    custom_plot.set_bar_labels_style(barvalueformat="{0}%", align="left", padding=.5)
    custom_plot.set_axis_style(step=5)
    custom_plot.set_bar_style(bar_height=.5)
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
        fig_size:list[int, int] = [10, 5],
        font_size:int = DEFAULT_BAR_FONT.size,
        font_colour:str = DEFAULT_BAR_FONT.colour,
        data_label_format:str = DEFAULT_BAR_FONT.format,
        data_label_align:str = DEFAULT_BAR_FONT.align,
        bar_colours:ColourGradient = None,
        legend_loc:str = None,
        x_axis_lim:tuple[int, int] = None,
        x_axis_step:int = None,
        bar_height:float = 0.8
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
    local_style = core.StackedPlotStyle()
    local_style.fig["title"] = title
    local_style.bar_font["fontsize"] = font_size
    local_style.bar_font["fontcolour"] = font_colour
    local_style.bar_font["fontformat"] = data_label_format
    local_style.bar_font["fontalign"] = data_label_align
    local_style.bar_font["endthreshpadd"] = True
    local_style.bar_font["paddthresh"] = 4

    if x_axis_lim is not None: local_style.axis["xlim"] = x_axis_lim
    if x_axis_step is not None: local_style.axis["step"] = x_axis_step
    if legend_loc is not None: local_style.legend["location"] = legend_loc

    local_style.legend["fontsize"] = font_size
    local_style.fig["size"] = fig_size
    local_style.bar["align"] = "left"
    local_style.bar["barheight"] = bar_height
    local_style.fig["spinedisplay"] = (False, False, False, True)

    plot = core.StackedBarplot(data, series_labels)
    plot.set_style(local_style)
    if bar_colours is not None: plot.set_bar_style(bar_gradient=bar_colours)

    return plot

def centered(
        data:core.results_type,
        series_labels:core.series_labels_type,
        title:str = None,
        fig_size:list[int, int] = [10, 5],
        font_size:int = DEFAULT_BAR_FONT.size,
        font_colour:str = DEFAULT_BAR_FONT.colour,
        data_label_format:str = DEFAULT_BAR_FONT.format,
        data_label_align:str = DEFAULT_BAR_FONT.align,
        bar_colours:ColourGradient = None,
        legend_loc:str = None,
        x_axis_lim:tuple[int, int] = None,
        x_axis_step:int = None,
        bar_height:float = 0.8
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
    local_style = core.StackedPlotStyle()
    local_style.fig["title"] = title
    local_style.bar_font["fontsize"] = font_size
    local_style.bar_font["fontcolour"] = font_colour
    local_style.bar_font["fontformat"] = data_label_format
    local_style.bar_font["fontalign"] = data_label_align
    local_style.bar_font["endthreshpadd"] = True
    local_style.bar_font["paddthresh"] = 4

    if x_axis_lim is not None: local_style.axis["xlim"] = x_axis_lim
    if x_axis_step is not None: local_style.axis["step"] = x_axis_step
    if legend_loc is not None: local_style.legend["location"] = legend_loc

    local_style.legend["fontsize"] = font_size
    local_style.fig["size"] = fig_size
    local_style.bar["align"] = "center"
    local_style.bar["barheight"] = bar_height
    local_style.vert_line["show"] = True
    local_style.fig["spinedisplay"] = (False, False, False, True)

    plot = core.StackedBarplot(data, series_labels)
    plot.set_style(local_style)
    if bar_colours is not None: plot.set_bar_style(bar_gradient=bar_colours)

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
    #Typical Example Usage
    # results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
    # series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

    # custom_colours = ColourGradient()
    # custom_colours.gradient(len(series_labels), (200, 100, 150), (100, 150, 200))

    # basic_plot = basic(results, series_labels, bar_colours=custom_colours)
    # basic_plot.render()
    # basic_plot.show()

    # center_plot = centered(results, series_labels)
    # center_plot.render()
    # center_plot.show()

    # custom_plot = basic(results, series_labels, title="Custom Plot")
    # custom_plot.set_legend_style(show=True, font_size=12, spacing=2, background_colour="white", border_colour="white", transform=[-0.16, -0.02])
    # custom_plot.set_bar_labels_style(bar_value_format="{0}%", align="left", padding=.5)
    # custom_plot.set_axis_style(step=5)

    # custom_colours = ColourGradient()
    # custom_colours.gradient(len(series_labels), (200, 100, 150), (100, 150, 200))

    # custom_plot.set_bar_style(bar_height=.5, bar_gradient=custom_colours)
    # custom_plot.render()
    # custom_plot.show()
    import pandas as pd
    import numpy as np

    firstcolumn = "total_deaths_per_million"
    secondcolumn = "total_tests_per_thousand"
 
    df = pd.read_csv("owid-covid-data.csv")[["location", firstcolumn, secondcolumn]].dropna()
    df[firstcolumn] = pd.to_numeric(df[firstcolumn], errors="coerce")
    df[secondcolumn] = pd.to_numeric(df[secondcolumn], errors="coerce")

    df[firstcolumn] = df[firstcolumn]/1000.0#np.log(df[firstcolumn])
    df[secondcolumn] = df[secondcolumn]/1000.0#np.log(df[secondcolumn])
    #df[secondcolumn] = np.log(df[secondcolumn])#np.log(df["human_development_index"])

    #print(df.head())

    # Depending on the OWID data version, this field may contain either
    # percentages (0-100) or fractions (0-1). Use the same percentage scale
    # for both columns before grouping and plotting.
    #if df[firstcolumn].max() <= 1: df[firstcolumn] *= 100
    #if df["people_vaccinated_per_hundred"].max() <= 1: df["people_vaccinated_per_hundred"] *= 100

    df = df.groupby("location")[[firstcolumn, secondcolumn]].max()
    #df["people_unvaccinated"] = 100 - df["people_fully_vaccinated_per_hundred"]
    print(df.head())
    
    result = df.apply(list, axis=1).to_dict()

    EUCountries = [
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
    "England"
]
    subset = {k: v for k, v in result.items() if k in EUCountries}


    custom_colour = ColourGradient()
    custom_colour.set_colour_gradient_list([(227, 108, 85), (101, 219, 133)])

    basic_plot = centered(subset, ["Total Deaths Per 100 People", "Total Tests Per Person"], fig_size=(10, 8))

    basic_plot.set_bar_style(bar_gradient=custom_colour)

    basic_plot.set_axis_style(y_font_size=10, x_axis_format="{0:.0f}")
    basic_plot.set_bar_style(ordered="descending")

    basic_plot.set_bar_labels_style(bar_value_format="{0:.1f}", font_size=8, align="left", padd_thresh=2, end_thresh_padd=True, padding=0.5)
    basic_plot.set_legend_style(show=True, placement="above-horizontal", background_colour="white", border_colour="white", transform=[-.3, -.03], font_size=10)
    basic_plot.render()
    basic_plot.show()


#https://github.com/owid/covid-19-data/tree/master/public/data
https://github.com/Opensourcefordatascience/Data-sets
https://github.com/mwaskom/seaborn-data/blob/master/mpg.csv