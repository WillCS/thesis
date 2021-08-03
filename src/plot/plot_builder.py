from __future__ import annotations
from typing import Any, Tuple, Callable

from matplotlib import pyplot as plot
from matplotlib.widgets import Slider
import networkx as nx
import numpy    as np

class PlotBuilder():
    def __init__(self, graph: nx.Graph, pos) -> PlotBuilder:
        self.graph        = graph
        self.set_vertex_positions(pos)
        self.set_edges(self.graph.edges)

        self.colormap = plot.get_cmap("gist_rainbow")
        self.set_clusters([self.graph.nodes])

        self.fig, self.ax = plot.subplots()
        self.sliders = {}

    def set_vertex_positions(self, pos) -> PlotBuilder:
        self.pos = pos

        return self

    def set_edges(self, edges) -> PlotBuilder:
        self.edges = edges

        max_weight = max([self.graph[v][u]["weight"] for (v, u) in edges])
        self.edge_widths = list([self.graph[v][u]["weight"] / max_weight for (v, u) in edges])

        return self

    def set_clusters(self, clusters) -> PlotBuilder:
        self.clusters = clusters

        colours = [self.colormap(i) for i in np.linspace(0, 0.9, len(clusters))]

        self.node_colours = []

        for node in range(self.graph.order()):
            for c in range(len(clusters)):
                if node in clusters[c]:
                    self.node_colours.append(colours[c])
                    break

        return self

    def add_slider(self,
        label:       str,
        min_val:     float,
        max_val:     float,
        init_val:    float, 
        update_fn:   Callable[[Any, Callable], None],
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

        self.sliders[label] = (slider, axis)

        return self

    def remove_slider(self, label: str) -> PlotBuilder:
        self.sliders[label][1].remove()
        del self.sliders[label]

        return self

    def draw_plot(self, **kwargs) -> None:
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        self.ax.clear()

        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)

        nx.draw_networkx(self.graph, self.pos,
            width      = self.edge_widths,
            ax         = self.ax,
            edgelist   = self.edges,
            node_color = self.node_colours,
            **kwargs
        )

    def draw(self, **kwargs) -> None:
        self.ax.set_xlim((-1.0, 1.0))
        self.ax.set_ylim((-1.0, 1.0))

        self.draw_plot(**kwargs)

        plot.show()