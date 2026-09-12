# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate

import unittest
import matplotlib.pyplot as plt

from stackedbarplots.core import StackedBarplot
from stackedbarplots.defaults import StackedPlotStyle

class CoreClassTest(unittest.TestCase):
    """Unit tests for StackedBarplot class in core.py.
    Unit tests in this class focus on the general
    functionality of StackedBarplot, including pipeline
    plotting operations."""

    def test_set_style(self):
        style_obj = StackedPlotStyle()
        style_obj.bar_font["fontsize"] = 20
        style_obj.bar["height"] = .5
        style_obj.legend["show"] = True
        style_obj.fig["title"] = "Test Figure Title"
        style_obj.axis_title["xlabel"] = "Test axis title"
        style_obj.vert_line["show"] = True
        style_obj.axis["step"] = 5

        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

        test_plot = StackedBarplot(data=results, series_labels=series_labels)
        test_plot.set_style(style_obj)

        self.assertEqual(style_obj.bar_font["fontsize"], test_plot.style.bar_font["fontsize"])
        self.assertEqual(style_obj.bar["height"], test_plot.style.bar["height"])
        self.assertEqual(style_obj.legend["show"], test_plot.style.legend["show"])
        self.assertEqual(style_obj.fig["title"], test_plot.style.fig["title"])
        self.assertEqual(style_obj.axis_title["xlabel"], test_plot.style.axis_title["xlabel"])
        self.assertEqual(style_obj.vert_line["show"], test_plot.style.vert_line["show"])
        self.assertEqual(style_obj.axis["step"], test_plot.style.axis["step"])

        #Make sure gradient has been generated and doesn't throw an error when called
        test_plot.bar_colours.get_gradient_list()
        test_plot.bar_colours.get_normalised_gradient_list()

    def test_plot_bars(self):
        #With even number of series
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        for alignment in ["left", "center"]:
            for order in ["unordered", "ascending", "descending"]:
                test_plot.style.bar["align"] = alignment
                test_plot.style.fig["ordered"] = order
                test_plot.render()

        #With odd number of series
        results = {"Category 1": [10, 5, 3, 11, 5], "Category 2": [4, 2, 9, 12, 4], "Category 3": [11, 12, 3, 4, 3]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4", "New Series 5"]

        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        for alignment in ["left", "center"]:
            for order in ["unordered", "ascending", "descending"]:
                test_plot.style.bar["align"] = alignment
                test_plot.style.fig["ordered"] = order
                test_plot.render()

        #Test other misc settings
        test_plot.style.fig["fontfamily"] = "Arial"
        test_plot.render()

        test_plot.style.fig["backgroundcolour"] = "Green"
        test_plot.render()

        test_plot.style.vert_line["show"] = True
        test_plot.render()

        plt.close(test_plot.fig)
        del test_plot

    def test_plot_bar_labels(self):
        pass

    def test_plot_axes(self):
        pass

    def test_plot_legend(self):
        pass

    def test_plot_vert_line(self):
        pass



class CoreStyleTest(unittest.TestCase):
    """Unit tests for StackedBarplot class in core.py.
    Unit tests in this class focus on the functional 
    plotting of different figure elements that the 
    user is able to modify."""

    def test_style_bar_font(self):
        pass

    def test_style_bar(self):
        pass

    def test_style_fig(self):
        pass

    def test_style_axis(self):
        pass

    def test_style_axis_title(self):
        pass

    def test_style_legend(self):
        pass

    def test_style_vertline(self):
        pass
