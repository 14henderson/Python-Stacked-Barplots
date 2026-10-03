# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate

import unittest
import matplotlib
import matplotlib.pyplot as plt

from stackedbarplots.core import StackedBarplot
from stackedbarplots.defaults import StackedPlotStyle
from stackedbarplots.tools import ColourGradient

class CoreClassTest(unittest.TestCase):
    """Unit tests for StackedBarplot class in core.py.
    Unit tests in this class focus on the general
    functionality of StackedBarplot, including pipeline
    plotting operations. Intended to test runtime errors
    (logic errors related to style tested in CoreStyleTest)."""
    show_plots = False


    def test_set_style(self):
        style_obj = StackedPlotStyle()
        style_obj.set_bar_labels_style(font_size=20)
        style_obj.set_bar_style(bar_height=.5)
        style_obj.set_legend_style(show=True)
        style_obj.set_fig_style(title="Test Figure Title")
        style_obj.set_axis_title_style(x_label="Test axis title")
        style_obj.set_vert_line_style(show=True)
        style_obj.set_axis_style(step=5)

        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

        test_plot = StackedBarplot(data=results, series_labels=series_labels)
        test_plot.set_style(style_obj)

        self.assertEqual(style_obj.get_bar_labels_style()["fontsize"], test_plot.style.get_bar_labels_style()["fontsize"],
                         "Error: Fontsize attribute from StackedPlotStyle object not applied to StackedBarplot on set_style().")
        self.assertEqual(style_obj.get_bar_style()["height"], test_plot.style.get_bar_style()["height"],
                         "Error: Height attribute from StackedPlotStyle object not applied to StackedBarplot on set_style().")
        self.assertEqual(style_obj.get_legend_style()["show"], test_plot.style.get_legend_style()["show"],
                         "Error: Legend show attribute from StackedPlotStyle object not applied to StackedBarplot on set_style().")
        self.assertEqual(style_obj.get_fig_style()["title"], test_plot.style.get_fig_style()["title"],
                         "Error: Title attribute from StackedPlotStyle object not applied to StackedBarplot on set_style().")
        self.assertEqual(style_obj.get_axis_title_style()["xlabel"], test_plot.style.get_axis_title_style()["xlabel"],
                         "Error: XLabel attribute from StackedPlotStyle object not applied to StackedBarplot on set_style().")
        self.assertEqual(style_obj.get_vert_line_style()["show"], test_plot.style.get_vert_line_style()["show"],
                         "Error: Verticle line show attribute from StackedPlotStyle object not applied to StackedBarplot on set_style().")
        self.assertEqual(style_obj.get_axis_style()["step"], test_plot.style.get_axis_style()["step"],
                         "Error: Step attribute from StackedPlotStyle object not applied to StackedBarplot on set_style().")

        #Make sure gradient has been generated and doesn't throw an error when called
        test_plot.style.bar_colours.get_gradient_list()
        test_plot.style.bar_colours.get_normalised_gradient_list()


    def test_plot_bars(self):
        #With even number of series
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]

        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        for alignment in ["left", "centre"]:
            for order in [None, "ascending", "descending"]:
                test_plot.set_bar_style(align=alignment)
                test_plot.set_fig_style(sorted=order)
                test_plot.render()

        #With odd number of series
        results = {"Category 1": [10, 5, 3, 11, 5], "Category 2": [4, 2, 9, 12, 4], "Category 3": [11, 12, 3, 4, 3]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4", "New Series 5"]

        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        for alignment in ["left", "centre"]:
            for order in [None, "ascending", "descending"]:
                test_plot.set_bar_style(align=alignment)
                test_plot.set_fig_style(sorted=order)
                test_plot.render()

        #Test other misc settings
        test_plot.set_fig_style(font_family="monospace")
        test_plot.render()

        test_plot.set_fig_style(background_colour="Green")
        test_plot.render()

        test_plot.set_vert_line_style(show=True)
        test_plot.render()

        test_plot.set_fig_style(fig_size=(10, 5))
        test_plot.render()
        test_plot.set_fig_style(fig_size=(10, 10))
        test_plot.render()
        test_plot.set_fig_style(fig_size=(5, 10))
        test_plot.render()

        if self.show_plots: test_plot.show()
        plt.close(test_plot.fig)
        del test_plot


    def test_plot_bar_labels(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        for alignment in ["left", "centre", "right"]:
            for endpadd in [True, False]:
                test_plot.set_bar_labels_style(align=alignment, end_thresh_padd=endpadd)
                test_plot.render()

        test_plot.set_bar_labels_style(bar_value_format="{0}")
        test_plot.render()
        test_plot.set_bar_labels_style(bar_value_format="{0:.0f}")
        test_plot.render()
        test_plot.set_bar_labels_style(bar_value_format="{0:.4f}%")
        test_plot.render()
        test_plot.set_fig_style(font_family="monospace")
        test_plot.render()

        for fontsize in [0, 10, 30]:
            test_plot.set_bar_labels_style(font_size=fontsize)
            test_plot.render()
        for paddthresh in [0, 5, 10]:
            test_plot.set_bar_labels_style(padd_thresh=paddthresh)
            test_plot.render()
        for padd in [0, 5, 10]:
            test_plot.set_bar_labels_style(padding=padd)
            test_plot.render()
        for thresh in [(None, None), (5, None), (None, 10), (3, 11)]:
            test_plot.set_bar_labels_style(display_thresh=thresh)
            test_plot.render()
        for flag in [True, False]:
            test_plot.set_bar_labels_style(font_colour_invert=flag)
            test_plot.render()

        if self.show_plots: test_plot.show()
        plt.close(test_plot.fig)
        del test_plot


    def test_plot_axes(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        test_plot.set_axis_style(x_axis_format="{0}")
        test_plot.render()
        test_plot.set_axis_style(x_axis_format="{0:.0f}")
        test_plot.render()
        test_plot.set_axis_style(x_axis_format="{0:.4f}%")
        test_plot.render()

        for show in [True, False]:
            for lim_tup in [(-20, 0), (-20, 20), (0, 20)]:
                test_plot.set_axis_style(x_axis_show=show, x_lim=lim_tup)
                test_plot.render()

        for x_show in [True, None]:
            for y_show in [True, None]:
                test_plot.set_axis_style(x_axis_show=x_show, y_axis_show=y_show)
                test_plot.render()

        test_plot.set_fig_style(title="Test Title")
        test_plot.render()

        for spine_display in [(False, False, False, False),
                             (True, True, False, False),
                             (False, False, True, True),
                             (True, True, True, True)]:
            test_plot.set_fig_style(spine_display=spine_display)
            test_plot.render()

        if self.show_plots: test_plot.show()
        plt.close(test_plot.fig)
        del test_plot


    def test_plot_legend(self):
        #fontsize; fontcolour; backgroundcolour; bordercolour;
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        for show in [True, False]:
            test_plot.set_legend_style(show=show)

            for placement in ["right-vertical", "left-vertical", "below-horizontal", "above-horizontal"]:
                test_plot.set_legend_style(placement=placement)
                test_plot.render()
                if self.show_plots and show: test_plot.show()

            for marker in ["s", "o", "v", "^", "<", ">"]:
                test_plot.set_legend_style(marker_shape=marker)
                test_plot.render()

            for padd in [0, .1, .25, .5, 1]:
                test_plot.set_legend_style(spacing=padd)
                test_plot.render()

            for trans in [(0, 0), (.1, 0), (0, .1), (.1, .1)]:
                test_plot.set_legend_style(transform=trans)
                test_plot.render()

        plt.close(test_plot.fig)
        del test_plot


    def test_plot_vert_line(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        for show in [True, False]:
            test_plot.set_vert_line_style(show=show)

            for line_style in ["-", ":" , "--", "-.", ""]:
                test_plot.set_vert_line_style(line_style=line_style)
                test_plot.render()

            for alpha in [0, .5, 1]:
                test_plot.set_vert_line_style(alpha=alpha)
                test_plot.render()

            for order in ["front", "behind"]:
                test_plot.set_vert_line_style(z_order=order)
                test_plot.render()

        if self.show_plots: test_plot.show()
        plt.close(test_plot.fig)
        del test_plot




class CoreStyleTest(unittest.TestCase):
    """Unit tests for StackedBarplot class in core.py.
    Unit tests in this class focus on the functional 
    plotting of different figure elements that the 
    user is able to modify, and whether they are plotted
    in the figure axis. Focusses on logic errors, rather
    than runtime errors."""

    def test_style_bar_font(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        display_thresh = (2, 10)
        font_colour="red"
        padding = 4

        test_plot.set_bar_labels_style(font_size=20,
                                       font_colour=font_colour,
                                       font_colour_invert=True,
                                       bar_value_format="{0:.1f}@",
                                       display_thresh=display_thresh,
                                       padd_thresh=4,
                                       end_thresh_padd=True,
                                       align="right",
                                       padding=padding)
        test_plot.render()

        #Filter to only showing Annotation actors
        axis_objs = test_plot.ax.get_children()
        def data_label_filter(x):
            if isinstance(x, matplotlib.text.Annotation) and x.get_text() != "": return True
            else: return False
        axis_data_labels = list(filter(data_label_filter, axis_objs))

        #Filter chart data by display threshold
        chart_data = []
        for cat_data in results.values(): chart_data += cat_data
        def filter_to_thresh(x): return not (x <= display_thresh[0] or x >= display_thresh[1])
        threshed_chart_data = list(filter(filter_to_thresh, chart_data))

        self.assertEqual(len(threshed_chart_data), len(axis_data_labels),
                         "Error in display_thresh for shart data labels. Some labels showing/not showing against set threshold.")
        self.assertEqual(axis_data_labels[0].get_text()[-1], "@",
                         "Error in data label format; format style not being followed")
        #TODO: unit test for fontcolour, fontsize, fontcolourinvert, paddthresh, align, padding

        plt.close(test_plot.fig)
        del test_plot


    def test_style_bar(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        custom_colours = ColourGradient()
        custom_colours.gradient(len(series_labels), (200, 100, 150), (100, 150, 200))

        height = .5
        align = "left"

        test_plot.set_bar_style(bar_height=height,
                                align=align,
                                bar_gradient=custom_colours)
        test_plot.set_fig_style(sorted="descending")
        test_plot.render()

        axis_objs = test_plot.ax.get_children()
        axis_rects = list(filter(lambda actor: isinstance(actor, matplotlib.patches.Rectangle), axis_objs))
        self.assertEqual(axis_rects[0].get_height(), height,
                         "Attribute bar_height not being applied.")
        self.assertEqual(axis_rects[0].get_x(), 0,
                         "Attribute align not being applied (rects not starting at x=0 on left-align).")

        plt.close(test_plot.fig)
        del test_plot


    def test_style_fig(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        title="Test Title"
        title_font_size=20
        title_colour="green"
        font_family="monospace"
        spine_display=(False, True, False, True)

        test_plot.set_fig_style(title=title,
                                title_font_size=title_font_size,
                                title_colour=title_colour,
                                font_family=font_family,
                                fig_size=(20, 20),
                                spine_display=spine_display)
        test_plot.render()
        self.assertEqual(test_plot.ax.title.get_text(), title,
                         "Attribute title not being applied.")
        self.assertEqual(test_plot.ax.title.get_fontsize(), title_font_size,
                         "Attribute font_size not being applied.")
        self.assertEqual(test_plot.ax.title.get_color(), title_colour,
                         "Attribute title_colour not being applied.")
        self.assertEqual(test_plot.ax.title.get_fontfamily()[0], font_family,
                         "Attribute font_family not being applied.")
        self.assertEqual(test_plot.ax.spines['left'].get_visible(), spine_display[0],
                         "Left spine showing/not showing against defined style.")
        self.assertEqual(test_plot.ax.spines['top'].get_visible(), spine_display[1],
                         "Left spine showing/not showing against defined style.")
        self.assertEqual(test_plot.ax.spines['right'].get_visible(), spine_display[2],
                         "Left spine showing/not showing against defined style.")
        self.assertEqual(test_plot.ax.spines['bottom'].get_visible(), spine_display[3],
                         "Left spine showing/not showing against defined style.")

        plt.close(test_plot.fig)
        del test_plot


    def test_style_axis(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        x_lim = (-10, 50)
        step = 5
        x_font_size = 10
        y_font_size=15
        x_axis_abs = True

        num_ticks = ((x_lim[1] - x_lim[0])/step) + 1 #1 added for end tick

        test_plot.set_axis_style(x_lim=x_lim,
                                 step=step,
                                 x_font_size=x_font_size,
                                 y_font_size=y_font_size,
                                 x_axis_format="{0:.0f}@",
                                 x_axis_show=True,
                                 x_axis_abs=x_axis_abs)
        test_plot.render()

        x_ticks = test_plot.ax.get_xticklabels()
        self.assertEqual(num_ticks, len(x_ticks), "Attributes x_lim and step not being applied.")
        self.assertEqual(x_ticks[0].get_text()[-1], "@", "Error in x_tick format; format not being followed.")
        self.assertNotEqual(x_ticks[0].get_text()[0], "-", "Absolute value of negative axis tick not being displayed.")
        self.assertEqual(x_ticks[0].get_fontsize(), x_font_size, "x_tick fontsize not being applied.")

        y_ticks = test_plot.ax.get_yticklabels()
        self.assertEqual(len(results.keys()), len(y_ticks), "Incongruent number of Y-axis ticks.")
        self.assertEqual(y_ticks[0].get_fontsize(), y_font_size, "y_tick fontsize not being applied.")

        plt.close(test_plot.fig)
        del test_plot


    def test_style_axis_title(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        x_label = "Example x axis label"
        y_label = "Example y axis label"
        label_colour = "yellow"

        test_plot.set_axis_title_style(x_label=x_label,
                                       y_label=y_label,
                                       axis_label_font_colour=label_colour)
        test_plot.render()

        axis_objs = test_plot.ax.get_children()
        for child in axis_objs:
            if isinstance(child, matplotlib.axis.XAxis):
                self.assertEqual(child.get_children()[0].get_text(), x_label, "X Axis title text not being applied.")
                self.assertEqual(child.get_children()[0].get_color(), label_colour, "X Axis title text colour not being applied.")
            elif isinstance(child, matplotlib.axis.YAxis):
                self.assertEqual(child.get_children()[0].get_text(), y_label, "Y Axis title text not being applied.")
                self.assertEqual(child.get_children()[0].get_color(), label_colour, "Y Axis title text colour not being applied.")

        plt.close(test_plot.fig)
        del test_plot


    def test_style_legend(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        test_plot.set_legend_style(show=True,
                                   font_size=15,
                                   spacing=.5,
                                   font_colour="blue",
                                   background_colour="yellow",
                                   border_colour="black",
                                   placement="below-horizontal",
                                   marker_shape="o",
                                   transform=(.1, -.1))
        test_plot.render()

        #Search for legend artist in figure axis
        axis_objs = test_plot.ax.get_children()
        legend_present = False
        for child in axis_objs:
            if isinstance(child, matplotlib.legend.Legend):
                legend_present = True
                legend_actor = child
                break
        self.assertEqual(legend_present, True, "Legend showing/not showing against set plot style.")

        #Check that legend config matches data
        self.assertEqual(len(series_labels), len(legend_actor.get_texts()), "Number of legend series labels inconsistent with supplied data.")
        for legend_text_actor, series_label in zip(legend_actor.get_texts(), series_labels):
            self.assertEqual(legend_text_actor.get_text(), series_label, "Legend series label inconsistent with supplied series label.")

        plt.close(test_plot.fig)
        del test_plot


    def test_style_vert_line(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        test_plot.set_vert_line_style(show=True,
                                      line_style="--",
                                      colour="red",
                                      alpha=.5,
                                      z_order="front")
        test_plot.render()

        #Search for Line2D artist in figure axis
        axis_objs = test_plot.ax.get_children()
        vert_line_present = False
        for child in axis_objs:
            if isinstance(child, matplotlib.lines.Line2D):
                vert_line_present = True
                break
        self.assertEqual(vert_line_present, True, "Vertical line showing/not showing against set style.")

        plt.close(test_plot.fig)
        del test_plot
