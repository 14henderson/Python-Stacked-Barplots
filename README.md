<p align="center">
    <img src="https://github.com/14henderson/Python-Stacked-Barplots/blob/main/stackedbarplots/tests/readmefigures/Likert-example-graph.png?raw=true" width=100% alt="Example Horizontal Stacked Barchart created using this library, showing Likert-scale data.">
</p>

## About

> Are you a social scientist working with Likert-scale data in Python? 
> Do you wish there was an easier way to create horizontal stacked barcharts without having to write 100s of lines of matplotlib code?
> Do you just need an easy way to create horizontal stacked barcharts in Python?
> Me too! **Python-Stacked-Barplots is here to help!**

Python-Stacked-Barplots is a Python library that makes it easy to create, customise, save, and diplay **horizontal stacked barcharts**. This library currently supports left-aligned and centered horizontal barplots, but there are future plans to expand this. This library has been written with the intention of being both easy to use, and support a lot of flexibility. 

## Simple Use

Python-Stacked-Barplots follows a simple pipeline for use. See code snippet below for simple example use.

1. Create a StackedBarplot object using one of the base plotting methods (i.e., basic or centered),
2. Apply style changes to the plot where appropriate,
3. Call render() on your StackedBarplot object to render the plot, and either save() or show() to save or display it (or both).

#### Basic Plot

```Python
results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

basic_plot = basic(results, series_labels)
basic_plot.render()
basic_plot.save("Example-Graph-1.png")
```

<p align="center">
    <img src="https://github.com/14henderson/Python-Stacked-Barplots/blob/main/stackedbarplots/tests/readmefigures/Example-Graph-1.png?raw=true" width=60% alt="Example 1 Horizontal Stacked Barchart created using this library.">
</p>

#### Centered Plot

A centered horizontal stacked bar chart can easily be drawn from the same data by calling centered(). See code snippet below for simple example use.

```Python
results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
center_plot = centered(results, series_labels)
center_plot.render()
center_plot.save("Example-Graph-2.png")
```

<p align="center">
    <img src="https://github.com/14henderson/Python-Stacked-Barplots/blob/main/stackedbarplots/tests/readmefigures/Example-Graph-2.png?raw=true" width=60% alt="Example 2 Horizontal Stacked Barchart created using this library.">
</p>

#### Simple Custom-Styled Plot

Custom style settings from the StackedBarplot object can easily be changed. See following code snippet below for simple example use.

```Python
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
```

<p align="center">
    <img src="https://github.com/14henderson/Python-Stacked-Barplots/blob/main/stackedbarplots/tests/readmefigures/Example-Graph-3.png?raw=true" width=60% alt="Example 3 Horizontal Stacked Barchart created using this library.">
</p>

#### Advanced Custom-Style Plot

```Python
#dataset taken from https://github.com/owid/covid-19-data
custom_colour = ColourGradient()
custom_colour.set_colour_gradient_list([(227, 108, 85), (101, 219, 133)])

basic_plot = centered(dataset, ["Total COVID-19 Deaths Per Million People in 2021", "Total COVID-19 Tests Per 1,000 People in 2021"], fig_size=(10, 8))

basic_plot.set_bar_style(bar_gradient=custom_colour)

basic_plot.set_axis_style(y_font_size=10, x_axis_show=False)
basic_plot.set_bar_style(ordered="descending")
basic_plot.set_fig_style(spine_display=(False, False, False, False))

basic_plot.set_bar_labels_style(bar_value_format="{0:.0f}", font_size=8, align="left", padd_thresh=1000, end_thresh_padd=True, padding=100)
basic_plot.set_legend_style(show=True, placement="above-horizontal", background_colour="white", border_colour="white", transform=[-.2, -.03], font_size=10)
basic_plot.set_vert_line_style(line_style="--", alpha=.9)

basic_plot.render()
basic_plot.save("COVID-Deaths-EU-Tests-Fig.png")
```

<p align="center">
    <img src="https://github.com/14henderson/Python-Stacked-Barplots/blob/main/stackedbarplots/tests/readmefigures/COVID-Deaths-Tests-Fig.png?raw=true" width=60% alt="Example 4 Horizontal Stacked Barchart created using this library.">
</p>


## Technical implementation
* Written in Python 3.14.
* Written in pure python and minimal dependencies.
* Open to collaboration: create new and accessible style configurations easily.
* Written with Pylint following (where sensible) the Google-style documentation.


Copyright (c) 2026 Niklas Henderson