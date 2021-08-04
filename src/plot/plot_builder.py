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
    def __init__(self, graph: nx.Graph, position_strategy: PositionStrategy) -> PlotBuilder:
        self.graph        = graph
        self.set_position_strategy(position_strategy)
        self.set_edges(self.graph.edges)
        self.node_label_strategy: Optional[LabelStrategy] = None

        self.colormap = plot.get_cmap("gist_rainbow")
        self.set_clusters([self.graph.nodes])

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

    def set_clusters(self, clusters: List) -> PlotBuilder:
        self.clusters = Clustering(clusters)

        colours = [self.colormap(i) for i in np.linspace(0, 0.9, self.clusters.num_clusters())]

        self.node_colours = []

        for node in list(self.graph.nodes):
            for i, c in enumerate(self.clusters.get_clusters()):
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
        self.widgets[label][1].remove()
        del self.widgets[label]

        return self

    def draw_plot(self, **kwargs) -> None:
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        self.ax.clear()

        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)

        positions = self.position_strategy.generate_positions(
            self.graph, self.edges, self.clusters)

        nx.draw_networkx(self.graph, positions,
            width       = self.edge_widths,
            ax          = self.ax,
            edgelist    = self.edges,
            node_color  = self.node_colours,
            with_labels = False,
            **kwargs
        )

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

            for p, t in handles.items():
                t.set_rotation(label_angle[p])

    def draw(self, **kwargs) -> None:
        self.ax.set_xlim((-1.1, 1.1))
        self.ax.set_ylim((-1.1, 1.1))

        self.draw_plot(**kwargs)

        plot.show()
