from __future__ import annotations
from typing import Any, Optional, List, Tuple, Dict
from math import cos, sin, pi, atan2

import networkx as nx
import numpy    as np
from matplotlib import pyplot as plot
from backbones.backbone import BackboneStrategy

from common import Clustering, strength
from data import DataProvider

from .visualisation import Visualisation

class RadialVisualisation(Visualisation):
    def __init__(self,
        data_provider:     DataProvider,
        backbone_strategy: BackboneStrategy
    ) -> RadialVisualisation:
        self.data_provider     = data_provider
        self.backbone_strategy = backbone_strategy

        self.backbone = backbone_strategy.extract_backbone(data_provider.get_graph())

        self.vertex_positions       = {}
        self.vertex_colours         = []
        self.vertex_labels          = {}
        self.vertex_label_positions = {}
        self.vertex_label_rotations = {}

        self.normalised_edge_weights = []

        self.set_clusters(None)
        self.set_edges_to_display(None)

    def get_graph(self) -> nx.Graph:
        return self.backbone
    
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
        
        # Generate Vertex Labels
        self.vertex_labels          = {}
        self.vertex_label_positions = {}
        self.vertex_label_rotations = {}

        labels = self.data_provider.get_vertex_labels(
            self.edges,
            self.clusters
        )

        for v, l in labels.items():
            self.vertex_labels[v]          = l.text
            self.vertex_label_positions[v] = l.pos
            self.vertex_label_rotations[v] = l.angle

        # Generate Vertex Colours
        colormap = plot.get_cmap("gist_rainbow")

        colours = [colormap(i) for i in np.linspace(0, 0.9, self.clusters.get_num_clusters())]

        self.vertex_colours = []

        for v in list(self.get_graph().nodes):
            for i, c in enumerate(self.clusters.get_cluster_list()):
                if v in c:
                    self.vertex_colours.append(colours[i])
                    break
        
        # Generate Edge Widths
        max_weight = 1
        if len(self.edges) != 0:
            max_weight = max([self.get_graph()[v][u]["weight"] for (v, u) in self.edges])

        self.normalised_edge_weights = list([self.get_graph()[v][u]["weight"] / max_weight for (v, u) in self.edges])


    def draw(self, ax: plot.Axes, **kwargs) -> None:
        self.update()

        positions = self.vertex_positions
        colours   = self.vertex_colours
        edges     = self.edges
        widths    = self.normalised_edge_weights

        graph     = self.get_graph()

        # Draw the graph
        nx.draw_networkx(graph,
            pos         = positions,
            width       = widths,
            ax          = ax,
            edgelist    = edges,
            node_color  = colours,
            with_labels = False,
            **kwargs
        )

        label_text  = self.vertex_labels
        label_pos   = self.vertex_label_positions
        label_angle = self.vertex_label_rotations
        
        handles = nx.draw_networkx_labels(graph,
            ax        = ax,
            labels    = label_text,
            pos       = label_pos,
            font_size = 10
        )

        # We have to set the rotation of labels after
        # they've already been drawn
        for p, t in handles.items():
            t.set_rotation(label_angle[p])
