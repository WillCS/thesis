from __future__ import annotations
from typing import Any, Tuple, Dict, List, Optional
from math import cos, sin, pi, atan2
from csv import DictReader

import networkx as nx

from backbones import BackboneStrategy
from common import Clustering, strength

from .csv_adjacency import get_graph_from_csv_adjacency_matrix
from .data_provider import DataProvider, Label

def filtered_strength(v, graph: nx.Graph, edges: List) -> float:
    if edges is None:
        return strength(graph, v)
    else:
        return sum([
            graph[x][y]["weight"] for (x, y) in edges if x == v or x == y
        ])

def get_vertex_names(source: str) -> Dict[str, str]:
    names = {}
    with open(source) as csvfile:
        reader = DictReader(csvfile)

        for row in reader:
            names[row["gene_num"]] = row["Gene_Id"]

    return names

class GeneticDataProvider(DataProvider):
    def __init__(self, sourcefile: str, namefile: Optional[str] = None) -> GeneticDataProvider:
        self.graph = get_graph_from_csv_adjacency_matrix(sourcefile, absolute = True)

        if namefile:
            self.names = get_vertex_names(namefile)
        else:
            self.names = {v: n for (n, v) in enumerate(self.graph.nodes)}

    def get_graph(self) -> nx.Graph:
        return self.graph

    def get_vertex_positions(self,
        visible_edges: Optional[List]       = None,
        clustering:    Optional[Clustering] = None,
    ) -> Dict[Any, Tuple(float, float)]:
        n_vertices   = self.get_graph().order()
        vertex_order = [
            sorted(c, key = lambda v: filtered_strength(v, self.get_graph(), visible_edges))
            for c in clustering.get_cluster_list()
        ]
        
        # flatten the list
        vertex_order = [v for c in vertex_order for v in c]

        return { vertex_order[i]: 
            (cos(2 * pi * i / n_vertices), sin(2 * pi * i / n_vertices))
            for i in range(n_vertices)
        }

    def get_vertex_labels(self,
        visible_edges: Optional[List]       = None,
        clustering:    Optional[Clustering] = None,
    ) -> Dict[Any, Label]:
        labels = {}
        vertex_positions = self.get_vertex_positions(visible_edges, clustering)

        for i, v in enumerate(self.get_graph().nodes):
            text  = f"{self.names[v]}({clustering.get_cluster_of(v)})"
            x, y  = vertex_positions[v]
            pos   = (x * 1.2, y * 1.2)
            angle = atan2(y, x) * (180 / pi)

            labels[v] = Label(text, pos, angle)

        return labels

    def apply_backbone_strategy(self, backbone: BackboneStrategy) -> None:
        backbone.extract_backbone(self.graph)
    