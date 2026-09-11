# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate

import unittest, inspect

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

    def test_attribute_length(self):
        """Count whether the number of default attributes defined in the 
        DEFAULT_ class matches the numner of attributes stored in the 
        StackedPlotStyle object. assertLessEqual() is used, as StackedPlotStyle
        may require additional attributes for functionality."""
        style_obj = StackedPlotStyle()

        self.assertLessEqual(self.get_attributes_len(DEFAULT_BAR_FONT_STYLE), len(style_obj.bar_font.keys()))
        self.assertLessEqual(self.get_attributes_len(DEFAULT_BAR_STYLE), len(style_obj.bar.keys()))
        self.assertLessEqual(self.get_attributes_len(DEFAULT_FIG_STYLE), len(style_obj.fig.keys()))
        self.assertLessEqual(self.get_attributes_len(DEFAULT_AXIS_STYLE), len(style_obj.axis.keys()))
        self.assertLessEqual(self.get_attributes_len(DEFAULT_AXIS_TITLE_STYLE), len(style_obj.axis_title.keys()))
        self.assertLessEqual(self.get_attributes_len(DEFAULT_LEGEND_STYLE), len(style_obj.legend.keys()))
        self.assertLessEqual(self.get_attributes_len(DEFAULT_VERTLINE_STYLE), len(style_obj.vert_line.keys()))
