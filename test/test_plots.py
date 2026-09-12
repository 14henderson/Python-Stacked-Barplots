# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate

import unittest
import matplotlib.pyplot as plt

from stackedbarplots.plots import basic, centered

class PlotsMethodTest(unittest.TestCase):
    """Very basic unit tests for basic() and centered()
    methods in plots.py. Unit tests in this class focus
    on general functionality, rather than asserting that
    style settings are correctly implemented."""

    def test_basic(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

        basic_plot = basic(results, series_labels)
        basic_plot.render()
        plt.close(basic_plot.fig)
        del basic_plot

    def test_centered(self):
        results_2 = {"Category 1": [10, 5, 3, 11, 5], "Category 2": [4, 2, 9, 12, 3], "Category 3": [11, 12, 3, 4, 2]}
        series_labels_2 = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]
        center_plot = centered(results_2, series_labels_2)
        center_plot.render()
        plt.close(center_plot.fig)
        del center_plot


