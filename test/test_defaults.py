# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate,invalid-name

import inspect
import unittest

import matplotlib.pyplot as plt
from matplotlib import font_manager

from stackedbarplots.plots import basic


class Test_Default_Fields(unittest.TestCase):
    """Unit tests for DEFAULT_ classes in defaults.py."""

    def get_attributes_len(self, obj) -> int:
        total = 0
        for i in inspect.getmembers(obj):
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    total += 1
        return total

    def test_font_family(self):
        """Unit test to check that default font family is applied to all text elements."""

        results = {"Category 1": [10, 5, 2, 3, 11], "Category 2": [4, 2, 2, 9, 12], "Category 3": [11, 12, 2, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]

        basic_plot = basic(results, series_labels, title="Test title", subtitle="Test subtitle")
        basic_plot.set_axis_title_style(x_label = "Test x label", y_label = "Test y labels")

        basic_plot.render()

        dflt_font_name = font_manager.FontProperties(fname=str("stackedbarplots/fonts/LiberationSans-Regular.ttf")).get_name()

        self.assertEqual(dflt_font_name, basic_plot.fig._subtitle.get_fontfamily()[0])
        self.assertEqual(dflt_font_name, basic_plot.fig._suptitle.get_fontfamily()[0])

        self.assertEqual(dflt_font_name, basic_plot.ax.xaxis.label.get_fontfamily()[0])
        self.assertEqual(dflt_font_name, basic_plot.ax.yaxis.label.get_fontfamily()[0])

        self.assertEqual(dflt_font_name, basic_plot.ax.get_xticklabels()[0].get_fontfamily()[0])
        self.assertEqual(dflt_font_name, basic_plot.ax.get_yticklabels()[0].get_fontfamily()[0])

        plt.close(basic_plot.fig)
        del basic_plot




    # def test_attribute_length(self):
    #     """Count whether the number of default attributes defined in the 
    #     DEFAULT_ class matches the numner of attributes stored in the 
    #     StackedPlotStyle object. assertLessEqual() is used, as StackedPlotStyle
    #     may require additional attributes for functionality."""
    #     style_obj = StackedPlotStyle()

    #     self.assertLessEqual(self.get_attributes_len(DEFAULT_BAR_FONT_STYLE), len(style_obj.__bar_font_style.keys()),
    #                          "Error: Is StackedPlotStyle missing dict keys related to DEFAULT_BAR_FONT_STYLE?")
    #     self.assertLessEqual(self.get_attributes_len(DEFAULT_BAR_STYLE), len(style_obj.__bar_style.keys()),
    #                          "Error: Is StackedPlotStyle missing dict keys related to DEFAULT_BAR_STYLE?")
    #     self.assertLessEqual(self.get_attributes_len(DEFAULT_FIG_STYLE), len(style_obj.__fig_style.keys()),
    #                          "Error: Is StackedPlotStyle missing dict keys related to DEFAULT_FIG_STYLE?")
    #     self.assertLessEqual(self.get_attributes_len(DEFAULT_AXIS_STYLE), len(style_obj.__axis_style.keys()),
    #                          "Error: Is StackedPlotStyle missing dict keys related to DEFAULT_AXIS_STYLE?")
    #     self.assertLessEqual(self.get_attributes_len(DEFAULT_AXIS_TITLE_STYLE), len(style_obj.__axis_title_style.keys()),
    #                          "Error: Is StackedPlotStyle missing dict keys related to DEFAULT_AXIS_TITLE_STYLE?")
    #     self.assertLessEqual(self.get_attributes_len(DEFAULT_LEGEND_STYLE), len(style_obj.__legend_style.keys()),
    #                          "Error: Is StackedPlotStyle missing dict keys related to DEFAULT_LEGEND_STYLE?")
    #     self.assertLessEqual(self.get_attributes_len(DEFAULT_VERTLINE_STYLE), len(style_obj.__vert_line_style.keys()),
    #                          "Error: Is StackedPlotStyle missing dict keys related to DEFAULT_VERTLINE_STYLE?")
