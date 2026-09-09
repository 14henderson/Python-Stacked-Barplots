import stackedbarplots

#Example Basic Plot
results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

basic_plot = stackedbarplots.basic(results, series_labels)
basic_plot.render()
basic_plot.show()


#Example Centered Plot
results_2 = {"Category 1": [10, 5, 3, 11, 5], "Category 2": [4, 2, 9, 12, 3], "Category 3": [11, 12, 3, 4, 2]}
series_labels_2 = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]
center_plot = stackedbarplots.centered(results_2, series_labels_2)
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