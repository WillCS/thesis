from __future__ import annotations
from typing import Any, List, Optional, Tuple, Callable
import math

from matplotlib import pyplot as plot
from matplotlib.widgets import Slider, TextBox, Button
import networkx as nx
import numpy    as np

from common import Clustering

from .visualisation import Visualisation

class PlotBuilder():
    """
    A class to encapsulate the process of constructing a visualisation
    of a graph. This class manages things like making sure that edge widths
    are normalised when the list of edges to be drawn changes, handling
    the addition of widgets to the plot window, and colouring clusters.
    """

    def __init__(self, visualisation: Visualisation) -> PlotBuilder:
        """
        A PlotBuilder needs a graph to visualise, and a strategy for positioning
        the vertices in the visualisation. 
        """
        self.visualisation = visualisation
        self.graph = visualisation.get_graph()

        self.fig, self.ax = plot.subplots()
        self.widgets   = {}
        self.plot_args = {}

        # Prevent matplotlib from spitting errors into the console every time
        # I touch a textbox
        self.fig.canvas.mpl_disconnect(self.fig.canvas.manager.key_press_handler_id)

    def add_slider(self,
        label:       str,
        min_val:     float,
        max_val:     float,
        init_val:    float, 
        update_fn:   Callable[[Any], None],
        orientation: str = "horizontal",
        loc:         Tuple[float, float, float, float] = (0.25, 0.05, 0.5, 0.03),
        **kwargs
    ) -> PlotBuilder:
        axis = plot.axes(loc)

        slider = Slider(
            label       = label,
            valmin      = min_val,
            valmax      = max_val,
            valinit     = init_val,
            orientation = orientation,
            ax          = axis,
            **kwargs
        )

        slider.on_changed(update_fn)

        self.widgets[label] = (slider, axis)

        return self

    def add_textbox(self,
        label:       str,
        initial:     str, 
        update_fn:   Callable[[Any], None],
        loc:         Tuple[float, float, float, float] = (0.25, 0.05, 0.5, 0.03),
        **kwargs
    ) -> PlotBuilder:
        axis = plot.axes(loc)

        textbox = TextBox(
            label       = label,
            initial     = initial,
            ax          = axis,
            **kwargs
        )

        textbox.on_submit(update_fn)

        self.widgets[label] = (textbox, axis)

        return self

    def add_button(self,
        label: str,
        fn:    Callable,
        loc:   Tuple[float, float, float, float] = (0.25, 0.05, 0.5, 0.03),
        **kwargs
    ) -> PlotBuilder:
        axis = plot.axes(loc)

        button = Button(axis, label)

        button.on_clicked(fn)

        self.widgets[label] = (button, axis)

        return self

    def remove_widget(self, label: str) -> PlotBuilder:
        """
        Remove a widget (button, slider, textbox, etc) from
        the plot window.
        """
        self.widgets[label][1].remove()
        del self.widgets[label]

        return self

    def redraw(self, clear = True) -> None:
        """
        This draw method actually draws the visualisation, and
        should be called if it needs to be updated once the plot
        window is already opened.
        """
        if clear:
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            
            # By saving the canvas limits before we clear it,
            # we can set them again afterwards, keeping
            # any zooming in or out that might have been done
            
            self.ax.clear()

            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)

        self.visualisation.draw(self.ax, **self.plot_args)

    def draw(self,
        xlim: Tuple[float, float] = (-1, 1),
        ylim: Tuple[float, float] = (-1, 1),
        show  = True,
        clear = False,
        **kwargs
    ) -> None:
        """
        This draw method should only be called once, when
        the visualisation is first shown. It sets up the
        initial limits of the canvas, draws the plot, and
        then shows the plot window.
        """
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.plot_args = kwargs

        self.redraw(clear)

        if show:
            plot.show()
