# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate

import unittest
import matplotlib.pyplot as plt

from stackedbarplots.plots import basic, centred, normalised, normalised_centred
from stackedbarplots.tools import ColourGradient
from .test_tools import compare_figs




class GraphicalPlotsTest(unittest.TestCase):
    """Unit tests for plot method functionality.
    Unit tests are designed not to be comprehensive
    but ensure that changes to codebase do not break
    core visual output of plotted figures. These 
    plots are also used in the project's README file."""

    def setUp(self):
        self.show_plots = False
        self.override_expected_plots = False


    def test_vis_basic(self):
        results = {
            "1980": [26.42, 33, 47.39], 
            "1990": [39.61, 28.53, 43.60], 
            "2000": [47.90, 29.87, 43.98],
            "2010": [51.14, 28.10, 38.8],
            "2020": [57.29, 29.88, 37.07]
            }
        series_labels = ["Poultry", "Pork", "Beef"]
        custom_colours = ColourGradient()
        custom_colours.set_colour_gradient_list([
            (92, 128, 186),
            (241, 137, 87),
            (213, 81, 83)
        ])
        meat_plot = basic(results, series_labels, bar_colours=custom_colours)
        meat_plot.render()

        meat_plot.set_fig_style(title="Per capita meat consumption in the United States", subtitle="Average per capita meat availability, measured in kilograms per year. This data does not account for consumption-level waste, and therefore actual per capita intake will be slightly lower than meat availability. See https://ourworldindata.org/grapher/per-capita-meat-usa.")
        meat_plot.set_legend_style(show=True)
        meat_plot.set_bar_val_label_style(format="{0:.2f} kg")
        meat_plot.set_axis_style(x_axis_format="{0:.0f} kg")
        meat_plot.render()

        compare_figs(meat_plot, "GraphPlots_basic.png", override=self.override_expected_plots)

        if self.show_plots: meat_plot.show()
        plt.close(meat_plot.fig)
        del meat_plot


    def test_vis_centred(self):
        results = {
            "United Kingdom": [14.9, 7.2, 10.7, 13.0, 10.8, 16.2, 12.1, 7.9, 4.9, 1.3, 1.0],
            "France":         [13.8, 3.8,  9.4, 11.8, 10.6, 22.6, 10.9, 9.3, 5.6, 0.8, 1.5],
            "Germany":        [11.3, 4.5,  6.4, 10.5,  9.8, 16.2, 11.6,12.7,11.5,3.5,2.3],
            "Italy":          [10.4, 5.0,  8.1, 11.3, 14.4, 17.5, 14.8,10.6,5.9,1.0,1.2],
            "Spain":          [14.9, 4.3,  6.4,  9.3, 10.8, 20.9, 12.4,10.4,7.5,1.3,1.7]
        }

        series_labels = [
            "No trust at all",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "Complete trust"
        ]
        centre_plot = centred(results, series_labels, title="Trust in Country's Parliament", subtitle="European Social Survey Round 11. Respondent counts derived from published percentages and sample sizes. ESS round 11 - 2023. Social inequalities in health, Gender in contemporary Europe.")
        centre_plot.set_legend_style(show=True)
        centre_plot.set_bar_val_label_style(format="{0:.0f}%")
        centre_plot.set_axis_style(x_axis_format="{0:.0f}%")
        centre_plot.set_fig_style(sorted="lhlf-asc")
        centre_plot.render()

        compare_figs(centre_plot, "GraphPlots_centred.png", override=self.override_expected_plots)

        if self.show_plots: centre_plot.show()
        plt.close(centre_plot.fig)
        del centre_plot


    def test_vis_normalised(self):
        pov_results = {"Sub-Saharan Africa": [43.3, 48.4, 7.5, 0.8],
                          "MENA, Afghanistan and Pakistan": [14.5, 52.6, 24.1, 8.8],
                          "World": [9.8, 41.7, 28.6, 19.9],
                          "Latin America and Caribbean": [4, 26.7, 48.2, 21.1],
                          "South Asia": [1.7, 81.9, 16, 0.4],
                          "East Asia and Pacific": [1.6, 30.1, 47.9, 20.4],
                          "North America": [0.9, 1, 10.1, 88],
                          "Europe and Central Asia": [0.5, 5.7, 30.6, 63.2]}
        pov_series = ["Below $3 a day", "\$3-\$10 a day", "\$10-\$30 a day", "Above $30 a day"]
        custom_colours = ColourGradient()
        custom_colours.set_colour_gradient_list([
            (223, 71, 73),
            (253, 190, 129),
            (188, 225, 237),
            (86, 149, 197)
        ])

        poverty_plot = normalised(pov_results, pov_series, bar_colours=custom_colours)
        poverty_plot.set_legend_style(show=True)
        poverty_plot.set_fig_style(title="Distribution of population between different poverty lines",
                                   subtitle="This data is adjusted for inflation and differences in living costs between countries. See https://ourworldindata.org/grapher/distribution-of-population-between-different-poverty-thresholds-stacked-bar.")
        poverty_plot.render()
        compare_figs(poverty_plot, "GraphPlots_normalised.png", override=self.override_expected_plots)

        if self.show_plots: poverty_plot.show()
        plt.close(poverty_plot.fig)
        del poverty_plot


    def test_vis_normalised_centred(self):
        results = {"Quality of care":[476, 233, 224],
                   "Range of treatments": [448, 233, 252],
                   "Time to GP appointment": [215, 140, 578],
                   "Time to hospital appointment": [131, 205, 606],
                   "Time in A&E": [112, 168, 644]}
        series_labels = ["Very/quite satisfied", "Neither satisfied nor dissatisfied", "Very/quite dissatisfied"]

        custom_colours = ColourGradient()
        custom_colours.set_colour_gradient_list([
            (99, 179, 93),
            (224, 224, 224),
            (255, 110, 110)
        ])

        norm_plot_centre = normalised_centred(results, series_labels, bar_colours=custom_colours)
        norm_plot_centre.set_fig_style(title="Satisfaction with the quality of NHS care, the range of treatments, and time waiting for care",
                                       subtitle="Public satisfaction with the NHS and social care in 2024. Source: The King's Fund and Nuffield Trust analysis of NatCen's BSA survey data.")
        norm_plot_centre.set_bar_val_label_style(format="{0:.1f}%", expel_squeezed_ends=True, hide_squeezed="inner-only")
        norm_plot_centre.set_legend_style(show=True)
        norm_plot_centre.set_axis_title_style(x_label="Percentage of respondents")
        norm_plot_centre.set_axis_style(x_lim=(-80, 80), step=20)
        norm_plot_centre.render()

        compare_figs(norm_plot_centre, "GraphPlots_normalised_centred.png", override=self.override_expected_plots)

        if self.show_plots: norm_plot_centre.show()
        plt.close(norm_plot_centre.fig)
        del norm_plot_centre
