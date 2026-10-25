# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,line-too-long,arguments-differ, wrong-import-position, unnecessary-pass
"""Module contains LayoutEngine class for arranging figure and axis elements.

LayoutEngine child class is called at draw time for the plot, and aims
to rearrange the Axis/Axes on the Figure (as well as Axis elements) to
produce a "pleasing layout" (see https://matplotlib.org/stable/api/layout_engine_api.html).
A custom LayoutEngine is defined to allow more control of plot elements
(as the structure of BarPlots do not need the flexibility required from
matplotlib tight/constrained LayoutEngines), and to move layout code
out of core.py.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from .core import StackedBarplot

import warnings
import matplotlib.layout_engine


__all__ = [
    "StackedBarLayoutEngine"
]




class StackedBarLayoutEngine(matplotlib.layout_engine.LayoutEngine):
    """
    Matplotlib layout engine for figures created by the StackedBarplot library.

    Once this layout enging is attached to the StackedBarplot library, the layout
    engine ``execute`` function is called at draw time, providing a special draw-time
    hook (see https://matplotlib.org/stable/api/layout_engine_api.html). The 
    execution of this layout engine follows a specific pipeline, padding figure
    decorations outward from the axes. The order is as follows.

    1. The plot's axes
    2. x and y axes ticks (including category labels)
    3. Peritext (i.e., axis labels if shown)
    4. Plot legend (if shown)
    5. Paratext (i.e., subtitle then title if shown)
    6. Resizing of the figure itself
    """
    def __init__(self, plot:StackedBarplot) -> None:
        super().__init__()

        self.plot = plot


    def execute(self, fig) -> None:
        """Perform layout algorithm and move and resize axis and axis elements accordingly."""
        pass


    def set(self) -> None:
        """Required override, but redundant in this context."""
        warnings.warn("You are attempting to set or configure elements of" \
        "the plot's LayoutEngine. This LayoutEngine does not support such" \
        "customisation and acts only as a codespace for a rigid layout " \
        "algorithm. Calling this method is redundant.")
        raise NotImplementedError
