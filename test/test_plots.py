# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate

import unittest
import matplotlib
import matplotlib.pyplot as plt

from stackedbarplots.plots import basic, centred, normalised, normalised_centred




class PlotsMethodTest(unittest.TestCase):
    """Very basic unit tests for basic(), centred(),
    normalised(), and normalised_centred() methods in 
    plots.py. Unit tests in this class focus on general 
    functionality, rather than asserting that style 
    settings are correctly implemented."""

    def setUp(self):
        self.show_plots = False
        self.override_expected_plots = True


    def test_custom(self):
        """Custom unit test to allow developers to quickly test the plotting methods with their own data and settings."""
        debug = False

        if debug:
            results = {"Category 1": [10, 5, 2, 3, 11], "Category 2": [4, 2, 2, 9, 12], "Category 3": [11, 12, 2, 3, 4]}
            series_labels = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]

            legend_plot_placements = basic(results, series_labels)
            legend_plot_placements.set_legend_style(show=True, placement="above-horizontal")
            legend_plot_placements.set_fig_style(title="Example title.", subtitle="Example subtitle.")
            legend_plot_placements.set_axis_title_style(x_label="Example x axis title.")
            legend_plot_placements.set_axis_title_style(x_label="Example x axis title.")
            legend_plot_placements.render()
            legend_plot_placements.save("test.png")
            legend_plot_placements.save("test1.png")
            legend_plot_placements.save("test2.png")
            legend_plot_placements.save("test3.png")
            plt.close(legend_plot_placements.fig)


    def test_basic(self):
        results = {"Category 1": [10, 5, 2, 3, 11], "Category 2": [4, 2, 2, 9, 12], "Category 3": [11, 12, 2, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]

        meat_plot = basic(results, series_labels)
        meat_plot.render()

        meat_plot.set_fig_style(title="Per capita meat consumption in the United States", subtitle="Average per capita meat availability, measured in kilograms per year. This data does not account for consumption-level waste, and therefore actual per capita intake will be slightly lower than meat availability. See https://ourworldindata.org/grapher/per-capita-meat-usa.")
        meat_plot.set_legend_style(show=True)
        meat_plot.set_bar_val_label_style(format="{0:.2f} kg")
        meat_plot.set_axis_style(x_axis_format="{0:.0f} kg")

        #Check correct number of rects
        axis_objs = meat_plot.ax.get_children()
        axis_rects = list(filter(lambda actor: isinstance(actor, matplotlib.patches.Rectangle), axis_objs))
        self.assertGreaterEqual(len(axis_rects), len(series_labels)*len(results.keys()),
                                "Error in bar plotting. Stacked barchart figure as more rects than data requires.")
        meat_plot.render()

        if self.show_plots: meat_plot.show()
        plt.close(meat_plot.fig)
        del meat_plot


    def test_centred(self):
        results_2 = {"Category 1": [10, 5, 3, 11, 5], "Category 2": [4, 2, 9, 12, 3], "Category 3": [11, 12, 3, 4, 2]}
        series_labels_2 = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]
        centre_plot = centred(results_2, series_labels_2)
        centre_plot.render()

        #Check correct number of rects
        axis_objs = centre_plot.ax.get_children()
        axis_rects = list(filter(lambda actor: isinstance(actor, matplotlib.patches.Rectangle), axis_objs))
        self.assertGreaterEqual(len(axis_rects), len(series_labels_2)*len(results_2.keys()),
                                "Error in bar plotting. Stacked barchart figure as more rects than data requires.")

        if self.show_plots: centre_plot.show()
        plt.close(centre_plot.fig)
        del centre_plot


    def test_normalised(self):
        norm_results_1 = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12]}
        norm_results_2 = {"Category 1": [10, 5], "Category 2": [4, 2], "Category 3": [11, 12]}
        norm_results_3 = {"Category 1": [10, 5, 3, 11, 5, 1, 3], "Category 2": [4, 2, 9, 12, 4, 4, 2], "Category 3": [11, 12, 3, 4, 5, 10, 2]}
        norm_series_labels_1 = ["Series 1", "Series 2", "Series 3", "Series 4"]
        norm_series_labels_2 = ["Series 1", "Series 2"]
        norm_series_labels_3 = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5", "Series 6", "Series 7"]

        for data, labels in zip([norm_results_1, norm_results_2, norm_results_3], [norm_series_labels_1, norm_series_labels_2, norm_series_labels_3]):
            norm_plot = normalised(data, labels)

            #Check data has been correctly normalised
            for (cat_lab, cat_data), norm_data in zip(data.items(), norm_plot.data):
                cat_total = sum(cat_data)
                for ser_val, norm_val in zip(cat_data, norm_data):
                    self.assertAlmostEqual(norm_val, (ser_val/cat_total)*100, 5) #Check normalisation to 5 decimal places.

        plt.close(norm_plot.fig)
        del norm_plot


    def test_normalised_centred(self):
        norm_results_1 = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12]}
        norm_results_2 = {"Category 1": [10, 5], "Category 2": [4, 2], "Category 3": [11, 12]}
        norm_results_3 = {"Category 1": [10, 5, 3, 11, 5, 1, 3], "Category 2": [4, 2, 9, 12, 4, 4, 2], "Category 3": [11, 12, 3, 4, 5, 10, 2]}
        norm_series_labels_1 = ["Series 1", "Series 2", "Series 3", "Series 4"]
        norm_series_labels_2 = ["Series 1", "Series 2"]
        norm_series_labels_3 = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5", "Series 6", "Series 7"]

        for data, labels in zip([norm_results_1, norm_results_2, norm_results_3], [norm_series_labels_1, norm_series_labels_2, norm_series_labels_3]):
            norm_plot_centre = normalised_centred(data, labels)

            #Check data has been correctly normalised
            for (cat_lab, cat_data), norm_data in zip(data.items(), norm_plot_centre.data):
                cat_total = sum(cat_data)
                for ser_val, norm_val in zip(cat_data, norm_data):
                    self.assertAlmostEqual(norm_val, (ser_val/cat_total)*100, 5) #Check normalisation to 5 decimal places.
        norm_plot_centre.render()

        if self.show_plots: norm_plot_centre.show()
        plt.close(norm_plot_centre.fig)
        del norm_plot_centre
