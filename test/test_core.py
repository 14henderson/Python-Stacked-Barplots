# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate

import unittest
import matplotlib.pyplot as plt

from stackedbarplots.core import StackedBarplot
from stackedbarplots.defaults import StackedPlotStyle
from stackedbarplots.tools import ColourGradient

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
        test_plot.style.fig["fontfamily"] = "monospace"
        test_plot.render()

        test_plot.style.fig["backgroundcolour"] = "Green"
        test_plot.render()

        test_plot.style.vert_line["show"] = True
        test_plot.render()

        test_plot.style.fig["size"] = (10, 5)
        test_plot.render()
        test_plot.style.fig["size"] = (10, 10)
        test_plot.render()
        test_plot.style.fig["size"] = (5, 10)
        test_plot.render()

        plt.close(test_plot.fig)
        del test_plot

    def test_plot_bar_labels(self):
        #Mostly testing for crashes rather than unit testing assert statements.
        #TODO: Test if these style settings are actually changing the figure

        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        for alignment in ["left", "center", "right"]:
            for endpadd in [True, False]:
                test_plot.style.bar_font["align"] = alignment
                test_plot.style.bar_font["end_thresh_padd"] = endpadd
                test_plot.render()

        test_plot.style.bar_font["fontformat"] = "{0}"
        test_plot.render()
        test_plot.style.bar_font["fontformat"] = "{0:.0f}"
        test_plot.render()
        test_plot.style.bar_font["fontformat"] = "{0:.4f}%"
        test_plot.render()
        test_plot.style.bar_font["fontfamily"] = "monospace"
        test_plot.render()

        for fontsize in [0, 10, 30]:
            test_plot.style.bar_font["fontsize"] = fontsize
            test_plot.render()
        for paddthresh in [0, 5, 10]:
            test_plot.style.bar_font["fontpaddthresh"] = paddthresh
            test_plot.render()
        for padd in [0, 5, 10]:
            test_plot.style.bar_font["padding"] = padd
            test_plot.render()
        for thresh in [(None, None), (5, None), (None, 10), (3, 11)]:
            test_plot.style.bar_font["fontdisplaythresh"] = thresh
            test_plot.render()
        for flag in [True, False]:
            test_plot.style.bar_font["fontcolourinvert"] = flag
            test_plot.render()

        plt.close(test_plot.fig)
        del test_plot


    def test_plot_axes(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        test_plot.style.axis["xaxisformat"] = "{0}"
        test_plot.render()
        test_plot.style.axis["xaxisformat"] = "{0:.0f}"
        test_plot.render()
        test_plot.style.axis["xaxisformat"] = "{0:.4f}%"
        test_plot.render()

        for show in [True, False]:
            for lim_tup in [(-20, 0), (-20, 20), (0, 20)]:
                test_plot.style.axis["xaxisshow"] = show
                test_plot.style.axis["xlim"] = lim_tup
                test_plot.render()

        for x_show in [True, False]:
            for y_show in [True, False]:
                test_plot.style.axis_title["xlabel"] = x_show
                test_plot.style.axis_title["ylabel"] = y_show
                test_plot.render()

        test_plot.style.fig["title"] = "Test Title"
        test_plot.render()

        for spinedisplay in [(False, False, False, False),
                             (True, True, False, False),
                             (False, False, True, True),
                             (True, True, True, True)]:
            test_plot.style.fig["spinedisplay"] = spinedisplay
            test_plot.render()
        plt.close(test_plot.fig)
        del test_plot

    def test_plot_legend(self):
        #fontsize; fontcolour; backgroundcolour; bordercolour;
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        for show in [True, False]:
            test_plot.style.legend["show"] = show

            for placement in ["right-vertical", "left-vertical", "below-horizontal", "above-horizontal"]:
                test_plot.style.legend["placement"] = placement
                test_plot.render()

            for marker in ["s", "o", "v", "^", "<", ">"]:
                test_plot.style.legend["markershape"] = marker
                test_plot.render()

            for padd in [0, .1, .25, .5, 1]:
                test_plot.style.legend["spacing"] = padd
                test_plot.render()

            for trans in [(0, 0), (.1, 0), (0, .1), (.1, .1)]:
                test_plot.style.legend["transform"] = trans
                test_plot.render()
        plt.close(test_plot.fig)
        del test_plot

    def test_plot_vert_line(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        for show in [True, False]:
            test_plot.style.vert_line["show"] = show

            for line_style in ["-", ":" , "--", "-.", ""]:
                test_plot.style.vert_line["linestyle"] = line_style
                test_plot.render()

            for alpha in [0, .5, 1]:
                test_plot.style.vert_line["alpha"] = alpha
                test_plot.render()

            for order in ["front", "behind"]:
                test_plot.style.vert_line["order"] = order
                test_plot.render()

        plt.close(test_plot.fig)
        del test_plot

class CoreStyleTest(unittest.TestCase):
    """Unit tests for StackedBarplot class in core.py.
    Unit tests in this class focus on the functional 
    plotting of different figure elements that the 
    user is able to modify. These are basic in nature
    and only call each set_style method with example
    data."""

    def test_style_bar_font(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        test_plot.set_bar_labels_style(font_size=20, 
                                       font_colour="red", 
                                       font_colour_invert=True, 
                                       bar_value_format="{0:.1f}%", 
                                       display_thresh=(2, 10), 
                                       padd_thresh=4, 
                                       end_thresh_padd=True, 
                                       align="right", 
                                       padding=4)
        test_plot.render()
        plt.close(test_plot.fig)
        del test_plot

    def test_style_bar(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        custom_colours = ColourGradient()
        custom_colours.gradient(len(series_labels), (200, 100, 150), (100, 150, 200))
        test_plot.set_bar_style(bar_height=.5, align="left", ordered="ascending", bar_gradient=custom_colours)
        test_plot.render()
        plt.close(test_plot.fig)
        del test_plot

    def test_style_fig(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        test_plot.set_fig_style(title="Test Title",
                                title_font_size=20,
                                title_colour="green",
                                font_family="monospace",
                                fig_size=(20, 20),
                                spine_display=(False, True, False, True))
        test_plot.render()
        plt.close(test_plot.fig)
        del test_plot

    def test_style_axis(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        test_plot.set_axis_style(x_lim=(-10, 50),
                                 step=5,
                                 x_font_size=10,
                                 y_font_size=10,
                                 x_axis_format="{0:.0f}%",
                                 x_axis_show=True)
        test_plot.render()
        plt.close(test_plot.fig)
        del test_plot

    def test_style_axis_title(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        test_plot.set_axis_title_style(x_label="Example x axis label",
                                       y_label="Example y axis label",
                                       axis_label_font_colour="yellow")
        test_plot.render()
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
        plt.close(test_plot.fig)
        del test_plot

    def test_style_vertline(self):
        results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
        series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
        test_plot = StackedBarplot(data=results, series_labels=series_labels)

        test_plot.set_vert_line_style(show=True,
                                      line_style="--",
                                      colour="red",
                                      alpha=.5,
                                      order="front")
        test_plot.render()
        plt.close(test_plot.fig)
        del test_plot
