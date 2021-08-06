from __future__ import annotations
from typing import Any, List, Optional, Tuple, Callable
import math

from matplotlib import pyplot as plot
from matplotlib.widgets import Slider, TextBox, Button
import networkx as nx
import numpy    as np
from common import Clustering

from plot.label.label import LabelStrategy
from plot.pos.position import PositionStrategy

class PlotBuilder():
    """
    A class to encapsulate the process of constructing a visualisation
    of a graph. This class manages things like making sure that edge widths
    are normalised when the list of edges to be drawn changes, handling
    the addition of widgets to the plot window, and colouring clusters.
    """

    def __init__(self, graph: nx.Graph, position_strategy: PositionStrategy) -> PlotBuilder:
        """
        A PlotBuilder needs a graph to visualise, and a strategy for positioning
        the vertices in the visualisation. 
        """
        self.graph        = graph
        self.set_position_strategy(position_strategy)
        self.set_edges(self.graph.edges)

        # By default we don't show vertex labels,
        # but by setting a label strategy we can
        # change what the labels will be and how
        # they will be displayed.
        self.node_label_strategy: Optional[LabelStrategy] = None

        # We use the rainbow colourmap because it contains every colour,
        # and we need as much difference as we can get between clusters
        self.colormap = plot.get_cmap("gist_rainbow")

        # By default we assume no clusters
        self.set_clusters(None)

        self.fig, self.ax = plot.subplots()
        self.widgets = {}

        # Prevent matplotlib from spitting errors into the console every time
        # I touch a textbox
        self.fig.canvas.mpl_disconnect(self.fig.canvas.manager.key_press_handler_id)

    def set_position_strategy(self, position_strategy: PositionStrategy) -> PlotBuilder:
        self.position_strategy = position_strategy

        return self

    def set_node_label_strategy(self, label_strategy: LabelStrategy) -> PlotBuilder:
        self.node_label_strategy = label_strategy

        return self

    def set_edges(self, edges) -> PlotBuilder:
        self.edges = edges

        max_weight = 1
        if len(edges) != 0:
            max_weight = max([self.graph[v][u]["weight"] for (v, u) in edges])

        self.edge_widths = list([self.graph[v][u]["weight"] / max_weight for (v, u) in edges])

        return self

    def set_clusters(self, clusters: Optional[Clustering]) -> PlotBuilder:
        """
        Set the clustering to be used when drawing the visualisation.
        The clustering can affect the colours of vertices, their positions,
        their labelling, and probably more features that are yet to be added.

        If no clustering is provided, we use a single cluster as though there
        were none at all.
        """
        if clusters is None:
            self.clusters = Clustering({"1": list(self.graph.nodes)})
        else:
            self.clusters = clusters

        # Sample from the colour map at evenly spaced intervals to get
        # colours for vertices according to their clusters
        colours = [self.colormap(i) for i in np.linspace(0, 0.9, self.clusters.get_num_clusters())]

        self.node_colours = []

        for node in list(self.graph.nodes):
            for i, c in enumerate(self.clusters.get_cluster_list()):
                if node in c:
                    self.node_colours.append(colours[i])
                    break

        return self

    def add_slider(self,
        label:       str,
        min_val:     float,
        max_val:     float,
        init_val:    float, 
        update_fn:   Callable[[Any, nx.Graph, Callable], None],
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

        slider.on_changed(lambda v: update_fn(v, self.graph, self.draw_plot))

        self.widgets[label] = (slider, axis)

        return self

    def add_textbox(self,
        label:       str,
        initial:     str, 
        update_fn:   Callable[[Any, nx.Graph, Callable], None],
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

        textbox.on_submit(lambda v: update_fn(v, self.graph, self.draw_plot))

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

        button.on_clicked(lambda event: fn(self.graph, self.edges, self.clusters))

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

    def draw_plot(self, **kwargs) -> None:
        """
        This draw method actually draws the visualisation, and
        should be called if it needs to be updated once the plot
        window is already opened.
        """
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        # By saving the canvas limits before we clear it,
        # we can set them again afterwards, keeping
        # any zooming in or out that might have been done

        self.ax.clear()

        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        
        # Generate the positions of the vertices according to
        # our position strategy
        positions = self.position_strategy.generate_positions(
            self.graph, self.edges, self.clusters)

        # Draw the graph
        nx.draw_networkx(self.graph, positions,
            width       = self.edge_widths,
            ax          = self.ax,
            edgelist    = self.edges,
            node_color  = self.node_colours,
            with_labels = False,
            **kwargs
        )

        # If we have a label strategy, we want to generate labels
        # and draw them too.
        if self.node_label_strategy is not None:
            labels = self.node_label_strategy.generate_labels(
                self.graph,
                positions,
                self.edges,
                self.clusters
            )
            
            label_text  = { n : labels[n].text  for n in labels.keys() }
            label_pos   = { n : labels[n].pos   for n in labels.keys() }
            label_angle = { n : labels[n].angle for n in labels.keys() }
            
            handles = nx.draw_networkx_labels(self.graph,
                ax        = self.ax,
                labels    = label_text,
                pos       = label_pos,
                font_size = 10
            )

            # We have to set the rotation of labels after
            # they've already been drawn
            for p, t in handles.items():
                t.set_rotation(label_angle[p])

    def draw(self, **kwargs) -> None:
        """
        This draw method should only be called once, when
        the visualisation is first shown. It sets up the
        initial limits of the canvas, draws the plot, and
        then shows the plot window.
        """
        self.ax.set_xlim((-1.1, 1.1))
        self.ax.set_ylim((-1.1, 1.1))

        self.draw_plot(**kwargs)

        plot.show()
