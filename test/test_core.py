# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate

import unittest

from stackedbarplots.core import StackedBarplot

class CoreClassTest(unittest.TestCase):
    """Unit tests for StackedBarplot class in core.py.
    Unit tests in this class focus on the general
    functionality of StackedBarplot, including pipeline
    plotting operations."""

    def test_set_style(self):
        pass

    def test_plot_bars(self):
        pass

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
