# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate

import unittest
import matplotlib.pyplot as plt

from stackedbarplots.plots import basic
from stackedbarplots.core import StackedBarplot
from stackedbarplots.tools import ColourGradient
from .test_tools import compare_figs




class GraphicalStylesTest(unittest.TestCase):
    """Unit tests for plot style functionality.
    Unit tests are designed not to be comprehensive
    but ensure that changes to codebase do not break
    core visual output of plotted figures."""

    def setUp(self):
        self.show_plots = False
        self.override_expected_plots = True


    def test_vis_bar_font(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [1, 2, 9, 12], "Category 3": [11, 12, 3, 2]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        bar_font_plot = StackedBarplot(data=results, series_labels=series_labels)

        hide_squeezed = "inner-only"
        font_colour="blue"
        padding = 4

        bar_font_plot.set_bar_val_label_style(font_size=15,
                                       font_colour=font_colour,
                                       colour_invert=True,
                                       format="{0:.1f} kg",
                                       hide_squeezed=hide_squeezed,
                                       expel_squeezed_ends=True,
                                       align="right",
                                       padding=padding)

        custom_colours = ColourGradient()
        custom_colours.set_colour_gradient_list([
            (10, 10, 10),
            (60, 60, 60),
            (150, 150, 150),
            (200, 200, 200)
        ])

        bar_font_plot.set_bar_style(bar_gradient=custom_colours)
        bar_font_plot.render()

        compare_figs(bar_font_plot, "GraphStyles_bar_font.png", override=self.override_expected_plots)

        if self.show_plots: bar_font_plot.show()
        plt.close(bar_font_plot.fig)
        del bar_font_plot


    def test_vis_bar(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        bar_plot = StackedBarplot(data=results, series_labels=series_labels)

        custom_colours = ColourGradient()
        custom_colours.gradient(len(series_labels), (200, 100, 150), (100, 150, 200))

        height = 1
        align = "left"

        bar_plot.set_bar_style(bar_height=height,
                                align=align,
                                bar_gradient=custom_colours)
        bar_plot.set_fig_style(sorted="sum-desc")
        bar_plot.render()

        compare_figs(bar_plot, "GraphStyles_bar.png", override=self.override_expected_plots)

        if self.show_plots: bar_plot.show()
        plt.close(bar_plot.fig)
        del bar_plot


    def test_vis_fig(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        fig_plot = StackedBarplot(data=results, series_labels=series_labels)

        title="Test Title"
        title_font_size=20
        title_colour="green"
        subtitle="Test subtitle"
        subtitle_font_size=10
        subtitle_colour="red"
        font_family="monospace"
        spine_display=(False, True, False, True)

        fig_plot.set_fig_style(title=title,
                                title_font_size=title_font_size,
                                title_colour=title_colour,
                                subtitle=subtitle,
                                subtitle_font_size=subtitle_font_size,
                                subtitle_colour=subtitle_colour,
                                font_family=font_family,
                                fig_size=(500, 800),
                                spine_display=spine_display)
        fig_plot.render()

        compare_figs(fig_plot, "GraphStyles_fig.png", override=self.override_expected_plots)

        if self.show_plots: fig_plot.show()
        plt.close(fig_plot.fig)
        del fig_plot


    def test_vis_axis(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        axis_plot = StackedBarplot(data=results, series_labels=series_labels)

        x_lim = (-30, 30)
        step = 5
        x_font_size = 10
        y_font_size=15
        x_axis_abs = True

        axis_plot.set_bar_style(align="centre")
        axis_plot.set_axis_style(x_lim=x_lim,
                                 step=step,
                                 x_font_size=x_font_size,
                                 y_font_size=y_font_size,
                                 x_axis_format="{0:.0f}%",
                                 x_axis_show=True,
                                 x_axis_abs=x_axis_abs)
        axis_plot.render()

        compare_figs(axis_plot, "GraphStyles_axis.png", override=self.override_expected_plots)

        if self.show_plots: axis_plot.show()
        plt.close(axis_plot.fig)
        del axis_plot


    def test_vis_axis_title(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        axis_title_plot = StackedBarplot(data=results, series_labels=series_labels)

        x_label = "Example x axis label"
        y_label = "Example y axis label"
        label_colour = "#4287f5"

        axis_title_plot.set_axis_title_style(x_label=x_label,
                                       y_label=y_label,
                                       axis_label_font_colour=label_colour)
        axis_title_plot.render()

        compare_figs(axis_title_plot, "GraphStyles_axis_title.png", override=self.override_expected_plots)

        if self.show_plots: axis_title_plot.show()
        plt.close(axis_title_plot.fig)
        del axis_title_plot


    def test_vis_legend(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

        for placement in ["above-horizontal", "right-vertical", "below-horizontal"]:
            legend_plot_placements = basic(results, series_labels)
            legend_plot_placements.set_legend_style(show=True, placement=placement)
            legend_plot_placements.set_fig_style(title="Example title.", subtitle="Example subtitle.")
            legend_plot_placements.set_axis_title_style(x_label="Example x axis title.")
            legend_plot_placements.render()

            compare_figs(legend_plot_placements, f"GraphStyles_legend_{placement}.png", override=self.override_expected_plots)
            if self.show_plots: legend_plot_placements.show()
            plt.close(legend_plot_placements.fig)
        del legend_plot_placements

        legend_plot = StackedBarplot(data=results, series_labels=series_labels)
        legend_plot.set_fig_style(title="Example title.", subtitle="Example subtitle.")
        legend_plot.set_legend_style(show=True,
                                   font_size=15,
                                   padding=.5,
                                   font_colour="blue",
                                   background_colour="#dbdbdb",
                                   border_colour="#8e8e8e",
                                   placement="below-horizontal",
                                   marker_shape="o",
                                   transform=(.1, -.1))
        legend_plot.render()
        compare_figs(legend_plot, "GraphStyles_legend.png", override=self.override_expected_plots)
        if self.show_plots: legend_plot.show()
        plt.close(legend_plot.fig)
        del legend_plot

        results_long = {"Category 1": [10, 5, 3, 11, 4, 5, 8], "Category 2": [4, 2, 9, 12, 2, 11, 6], "Category 3": [11, 12, 3, 4, 1, 2, 5, 4]}
        series_labels_long = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5", "Series 6", "Series 7"]

        legend_plot_series = basic(results_long, series_labels_long)
        legend_plot_series.set_legend_style(show=True, columns=3)
        legend_plot_series.set_fig_style(title="Example title.", subtitle="Example subtitle.")
        legend_plot_series.render()
        compare_figs(legend_plot_series, "GraphStyles_legend_lseries.png", override=self.override_expected_plots)
        if self.show_plots: legend_plot_series.show()
        plt.close(legend_plot_series.fig)
        del legend_plot_series


    def test_vis_vert_line(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        vert_line_plot = StackedBarplot(data=results, series_labels=series_labels)
        vert_line_plot.set_bar_style(align="centre")

        vert_line_plot.set_vert_line_style(show=True,
                                      line_style="--",
                                      colour="red",
                                      alpha=.5,
                                      z_order="front")
        vert_line_plot.render()

        compare_figs(vert_line_plot, "GraphStyles_vert_line.png", override=self.override_expected_plots)

        if self.show_plots: vert_line_plot.show()
        plt.close(vert_line_plot.fig)
        del vert_line_plot
