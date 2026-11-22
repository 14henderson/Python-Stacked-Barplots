# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,line-too-long,disable=consider-using-enumerate
"""Tools module pertaining to graphical unit tests of stacked-barplots Python library."""

import os
from matplotlib.testing.compare import compare_images
from stackedbarplots.core import StackedBarplot

EXPECTED_PLOTS_DIR = "expected_plots"
TEST_PLOTS_DIR = "test_plots"

def compare_figs(plot:StackedBarplot, filename:str, override=False) -> None:
    """Method used to graphically compare two plots.
        
    Args:
        plot: StackedBarplot object to be tested.
        filename: Filename for saved test plot.
        override: Boolean flag if expected plot file should be overwritten (default False)
    """

    expected_plot_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), EXPECTED_PLOTS_DIR)
    test_plot_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), TEST_PLOTS_DIR)

    if not os.path.isdir(expected_plot_dir):
        os.mkdir(expected_plot_dir)

    if not os.path.isdir(test_plot_dir):
        os.mkdir(test_plot_dir)

    expected_plot_uri = os.path.join(expected_plot_dir, filename)
    test_plot_uri = os.path.join(test_plot_dir, filename)

    if override: plot.save(expected_plot_uri)
    plot.save(test_plot_uri)
    if compare_images(expected_plot_uri, test_plot_uri, tol=30) is not None:
        raise RuntimeError(f"Unit test error: {filename} has changed from expected plot layout.")
