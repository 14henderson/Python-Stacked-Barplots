# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate

import unittest
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.testing.compare import compare_images

from stackedbarplots.plots import basic, centred, normalised, normalised_centred

class PlotsMethodTest(unittest.TestCase):
    """Very basic unit tests for basic(), centred(),
    normalised(), and normalised_centred() methods in 
    plots.py. Unit tests in this class focus on general 
    functionality, rather than asserting that style 
    settings are correctly implemented."""

    def setUp(self):
        self.show_plots = False
        self.override_expected_plots = False
        self.EXPECTED_PLOTS_DIR = "./test/expected_plots/"
        self.TEST_PLOTS_DIR = "./test/test_plots/"

    def test_custom(self):
        """Custom unit test to allow developers to quickly test the plotting methods with their own data and settings."""
        debug = False

        if debug:
            results = {"Category 1": [10, 5, 2, 3, 11], "Category 2": [4, 2, 2, 9, 12], "Category 3": [11, 12, 2, 3, 4]}
            series_labels = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]

            basic_plot = basic(results, series_labels)
            basic_plot.set_fig_style(title="Hello world")
            basic_plot.set_fig_style(title=None)

            basic_plot.render()
            basic_plot.show()

            plt.close(basic_plot.fig)
            del basic_plot

    def test_basic(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

        basic_plot = basic(results, series_labels)
        basic_plot.render()

        #Check correct number of rects
        axis_objs = basic_plot.ax.get_children()
        axis_rects = list(filter(lambda actor: isinstance(actor, matplotlib.patches.Rectangle), axis_objs))
        self.assertGreaterEqual(len(axis_rects), len(series_labels)*len(results.keys()),
                                "Error in bar plotting. Stacked barchart figure as more rects than data requires.")

        basic_plot.save("../test/test_plots/test_basic_plot.png")
        compare_images(self.TEST_PLOTS_DIR + "test_basic_plot.png",
                       self.EXPECTED_PLOTS_DIR + "test_basic_plot.png",
                       tol=0.1)

        if self.show_plots: basic_plot.show()
        if self.override_expected_plots: basic_plot.save(self.EXPECTED_PLOTS_DIR + "test_basic_plot.png")
        plt.close(basic_plot.fig)
        del basic_plot


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

        centre_plot.save("../test/test_plots/test_centred_plot.png")
        compare_images(self.TEST_PLOTS_DIR + "test_centred_plot.png",
                       self.EXPECTED_PLOTS_DIR + "test_centred_plot.png",
                       tol=0.1)


        if self.show_plots: centre_plot.show()
        if self.override_expected_plots: centre_plot.save(self.EXPECTED_PLOTS_DIR + "test_centred_plot.png")
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

        norm_plot.render()

        norm_plot.save("../test/test_plots/test_norm_plot.png")
        compare_images(self.TEST_PLOTS_DIR + "test_norm_plot.png",
                       self.EXPECTED_PLOTS_DIR + "test_norm_plot.png",
                       tol=0.1)

        if self.show_plots: norm_plot.show()
        if self.override_expected_plots: norm_plot.save(self.EXPECTED_PLOTS_DIR + "test_norm_plot.png")
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

        norm_plot_centre.save("../test/test_plots/test_norm_centre_plot.png")
        compare_images(self.TEST_PLOTS_DIR + "test_norm_centre_plot.png",
                       self.EXPECTED_PLOTS_DIR + "test_norm_centre_plot.png",
                       tol=0.1)

        if self.show_plots: norm_plot_centre.show()
        if self.override_expected_plots: norm_plot_centre.save(self.EXPECTED_PLOTS_DIR + "test_norm_centre_plot.png")
        plt.close(norm_plot_centre.fig)
        del norm_plot_centre
