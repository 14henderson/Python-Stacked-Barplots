# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate,invalid-name

import inspect
import unittest

import matplotlib.pyplot as plt
from matplotlib import font_manager

from stackedbarplots.plots import basic, centred
from stackedbarplots.defaults import *


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


class Test_Default_Axis_Style(unittest.TestCase):
    """Unit tests for DEFAULT_AXIS_STYLE class in defaults.py. 
    Style settings that are set None by default are not tested."""

    def setUp(self): #TODO: Should this also test the other plot types? Or just stick to basic as this doesn't override any default style settings
        results = {"Category 1": [10, 5, 2, 3, 11], "Category 2": [4, 2, 2, 9, 12], "Category 3": [11, 12, 2, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]

        self.basic_plot = basic(results, series_labels)
        self.basic_plot.render()

    def test_x_axis_show(self):
        self.assertEqual(self.basic_plot.ax.get_xaxis().get_visible(), DEFAULT_AXIS_STYLE.x_axis_show)

    def test_y_axis_show(self):
        self.assertEqual(self.basic_plot.ax.get_yaxis().get_visible(), DEFAULT_AXIS_STYLE.y_axis_show)

    def test_x_font_size(self):
        self.assertEqual(self.basic_plot.ax.xaxis.get_majorticklabels()[0].get_fontsize(), DEFAULT_AXIS_STYLE.x_font_size)

    def test_y_font_size(self):
        self.assertEqual(self.basic_plot.ax.yaxis.get_majorticklabels()[0].get_fontsize(), DEFAULT_AXIS_STYLE.y_font_size)

    def test_y_font_color(self):
        self.assertEqual(self.basic_plot.ax.yaxis.get_majorticklabels()[0].get_color(), DEFAULT_AXIS_STYLE.y_font_colour)

    def test_x_font_color(self):
        self.assertEqual(self.basic_plot.ax.xaxis.get_majorticklabels()[0].get_color(), DEFAULT_AXIS_STYLE.x_font_colour)

    def test_x_axis_format(self):
        self.assertEqual(self.basic_plot.ax.xaxis.get_major_formatter().format_data(1.0), DEFAULT_AXIS_STYLE.x_axis_format.format(1.0))

    def test_x_axis_abs(self):
        results_2 = {"Category 1": [10, 5, 3, 11, 5], "Category 2": [4, 2, 9, 12, 3], "Category 3": [11, 12, 3, 4, 2]}
        series_labels_2 = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]
        centre_plot = centred(results_2, series_labels_2)
        centre_plot.render()
        self.assertLessEqual(float(centre_plot.ax.xaxis.get_ticklabels(which='major')[0].get_text()), 0)

    def test_x_axis_gridlines(self):
        self.assertEqual(self.basic_plot.ax.get_xgridlines()[0].get_visible(), DEFAULT_AXIS_STYLE.x_axis_gridlines)

    def test_x_axis_gridlines_colour(self):
        self.assertEqual(self.basic_plot.ax.get_xgridlines()[0].get_color(), DEFAULT_AXIS_STYLE.x_axis_gridlines_colour)


class Test_Default_Axis_Title_Style(unittest.TestCase):
    """Unit tests for DEFAULT_AXIS_TITLE_STYLE class in defaults.py. 
    Style settings that are set None by default are not tested."""

    def setUp(self):
        results = {"Category 1": [10, 5, 2, 3, 11], "Category 2": [4, 2, 2, 9, 12], "Category 3": [11, 12, 2, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]

        self.basic_plot = basic(results, series_labels)
        self.basic_plot.set_axis_title_style(x_label = "Test x label", y_label = "Test y labels")
        self.basic_plot.render()

    def test_axis_label_font_size(self):
        self.assertEqual(self.basic_plot.ax.xaxis.label.get_fontsize(), DEFAULT_AXIS_TITLE_STYLE.axis_label_font_size)
        self.assertEqual(self.basic_plot.ax.yaxis.label.get_fontsize(), DEFAULT_AXIS_TITLE_STYLE.axis_label_font_size)

    def test_axis_label_font_colour(self):
        self.assertEqual(self.basic_plot.ax.xaxis.label.get_color(), DEFAULT_AXIS_TITLE_STYLE.axis_label_font_colour)
        self.assertEqual(self.basic_plot.ax.yaxis.label.get_color(), DEFAULT_AXIS_TITLE_STYLE.axis_label_font_colour)


class Test_Default_Bar_Style(unittest.TestCase):
    """Unit tests for DEFAULT_BAR_STYLE class in defaults.py. 
    Style settings that are set None by default are not tested."""

    def setUp(self):
        results = {"Category 1": [10, 5, 2, 3, 11], "Category 2": [4, 2, 2, 9, 12], "Category 3": [11, 12, 2, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]

        self.basic_plot = basic(results, series_labels)
        self.basic_plot.render()

    def test_align(self):
        self.assertEqual(self.basic_plot.ax.patches[0].get_x(), 0)

    def test_height(self):
        self.assertEqual(self.basic_plot.ax.patches[0].get_height(), DEFAULT_BAR_STYLE.height)

    def test_bar_colours(self):
        norm_start_col = list([col/255.0 for col in DEFAULT_BAR_STYLE.start_colour])
        norm_end_col = list([col/255.0 for col in DEFAULT_BAR_STYLE.end_colour])

        for col1, col2 in zip(self.basic_plot.ax.patches[0].get_facecolor(), norm_start_col):
            self.assertAlmostEqual(col1, col2, 2)

        for col1, col2 in zip(self.basic_plot.ax.patches[-1].get_facecolor(), norm_end_col):
            self.assertAlmostEqual(col1, col2, 2)


class Test_Default_Bar_Val_Label_Style(unittest.TestCase):
    """Unit tests for DEFAULT_BAR_VAL_LABEL_STYLE class in defaults.py. 
    Style settings that are set None by default are not tested."""

    def setUp(self):
        results = {"Category 1": [10, 5, 2, 3, 11], "Category 2": [4, 2, 2, 9, 12], "Category 3": [11, 12, 2, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]

        self.basic_plot = basic(results, series_labels)
        self.basic_plot.render()

    def test_font_size(self):
        self.assertEqual(self.basic_plot.ax.texts[0].get_fontsize(), DEFAULT_BAR_VAL_LABEL_STYLE.font_size)

    def test_font_colour(self):
        self.assertEqual(self.basic_plot.ax.texts[0].get_color(), DEFAULT_BAR_VAL_LABEL_STYLE.font_colour)

    def test_format(self):
        self.assertEqual(self.basic_plot.ax.texts[0].get_text(), DEFAULT_BAR_VAL_LABEL_STYLE.format.format(10))

    def test_align(self): #Anchor point on the text object changes depending on the alignment setting.
        default_align = "center" if DEFAULT_BAR_VAL_LABEL_STYLE.align == "centre" else DEFAULT_BAR_VAL_LABEL_STYLE.align
        self.assertEqual(self.basic_plot.ax.texts[0].get_horizontalalignment(), default_align)

    def test_padding(self):
        results = {"Category 1": [10, 5, 2, 3, 11], "Category 2": [4, 2, 2, 9, 12], "Category 3": [11, 12, 2, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4", "Series 5"]

        new_plot = basic(results, series_labels)
        new_plot.set_bar_val_label_style(align="left")
        new_plot.render()

        label_x_px = new_plot.ax.transData.transform(new_plot.ax.texts[0].xy)[0]
        bar_left_px = new_plot.ax.patches[0].get_window_extent().x0
        actual_padding = label_x_px - bar_left_px

        if DEFAULT_BAR_VAL_LABEL_STYLE.padding == 0:
            self.assertEqual(actual_padding, 0)
        else:
            self.assertGreater(actual_padding, 0)

    def test_hide_squeezed(self):
        results = {"Category": [60, 1.1, 25, 1.2]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = basic(results, series_labels)
        test_plot.render()

        labels = {label.get_text(): label for label in test_plot.ax.texts}

        if DEFAULT_BAR_VAL_LABEL_STYLE.hide_squeezed == "all":
            self.assertFalse(labels["1.1"].get_visible())
            self.assertFalse(labels["1.2"].get_visible())
            self.assertTrue(labels["25.0"].get_visible())
            self.assertTrue(labels["60.0"].get_visible())
        elif DEFAULT_BAR_VAL_LABEL_STYLE.hide_squeezed == "inner-only":
            self.assertFalse(labels["1.1"].get_visible())
            self.assertTrue(labels["1.2"].get_visible())
            self.assertTrue(labels["25.0"].get_visible())
            self.assertTrue(labels["60.0"].get_visible())
        elif DEFAULT_BAR_VAL_LABEL_STYLE.hide_squeezed is None:
            self.assertTrue(labels["1.1"].get_visible())
            self.assertTrue(labels["1.2"].get_visible())
            self.assertTrue(labels["25.0"].get_visible())
            self.assertTrue(labels["60.0"].get_visible())

    def test_expel_squeezed_ends(self):
        results = {"Category": [60, 1, 25, 1.2]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = basic(results, series_labels)
        test_plot.set_bar_val_label_style(hide_squeezed="inner-only", expel_squeezed_ends=True)
        test_plot.render()

        self.assertGreaterEqual(test_plot.ax.texts[-1].get_window_extent().x0, test_plot.ax.patches[0].get_window_extent().x1)





#TODO: Check if default vals are actually set


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
