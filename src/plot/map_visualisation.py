from __future__ import annotations
from typing import Optional, List

import networkx as nx
from matplotlib import pyplot as plot


from backbones import BackboneStrategy
from common    import Clustering
from data      import DataProvider

from .visualisation import Visualisation

class MapVisualisation(Visualisation):
    def __init__(self,
        data_provider:     DataProvider,
        backbone_strategy: BackboneStrategy
    ) -> MapVisualisation:
        self.data_provider     = data_provider
        self.backbone_strategy = backbone_strategy

        self.data_provider.apply_backbone_strategy(self.backbone_strategy)

        self.vertex_positions        = {}
        self.normalised_edge_weights = []

        self.set_clusters(None)
        self.set_edges_to_display(None)

    def get_graph(self) -> nx.Graph:
        return self.data_provider.get_graph()
    
    def set_clusters(self, clusters: Optional[Clustering]) -> None:
        if clusters is None:
            self.clusters = Clustering({"1": list(self.get_graph().nodes)})
        else:
            self.clusters = clusters

    def set_edges_to_display(self, edges: Optional[List]) -> None:
        if edges is None:
            self.edges = list(self.get_graph().edges)
        else:
            self.edges = edges

    def get_edges_to_display(self) -> List:
        return self.edges

    def update(self) -> None:
        # Generate Vertex Locations
        self.vertex_positions = self.data_provider.get_vertex_positions(
            self.edges,
            self.clusters
        )
        
        # Generate Edge Widths
        max_weight = 1
        if len(self.edges) != 0:
            max_weight = max([self.get_graph()[v][u]["weight"] for (v, u) in self.edges])

        self.normalised_edge_weights = list([self.get_graph()[v][u]["weight"] / max_weight for (v, u) in self.edges])

    def draw(self, ax: plot.Axes, **kwargs) -> None:
        self.update()

        positions = self.vertex_positions
        edges     = self.edges
        widths    = self.normalised_edge_weights

        graph     = self.get_graph()

        # Draw the graph
        nx.draw_networkx(graph,
            pos         = positions,
            width       = widths,
            ax          = ax,
            edgelist    = edges,
            with_labels = False,
            **kwargs
        )
