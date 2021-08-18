from __future__ import annotations
from typing import Any, Tuple, Dict, List, Optional
from math import cos, sin, pi, atan2
from os import listdir

import networkx as nx

from backbones import BackboneStrategy
from common import Clustering, strength, print_progress_bar

from .csv_edge_list import get_graph_from_csv_edge_list
from .data_provider import DataProvider, Label

DATA_FOLDER = "./resources/comms_test"

def filtered_strength(v, graph: nx.Graph, edges: List) -> float:
    if edges is None:
        return strength(graph, v)
    else:
        return sum([
            graph[x][y]["weight"] for (x, y) in edges if x == v and x in graph and y in graph[x]
        ])

class CommunicationsDataProvider(DataProvider):
    def __init__(self) -> CommunicationsDataProvider:
        self.graphs = []

        for file in listdir(DATA_FOLDER):
            graph = get_graph_from_csv_edge_list(f"{DATA_FOLDER}/{file}", directed = True)
            self.graphs.append(graph)

        self.current_graph = 0

    def get_graph(self) -> nx.Graph:
        return self.graphs[self.current_graph]

    def get_num_graphs(self) -> int:
        return len(self.graphs)

    def set_current_graph(self, index: int) -> None:
        self.current_graph = index

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

        print(vertex_positions)

        for i, v in enumerate(self.get_graph().nodes):
            text  = f"{v}"
            x, y  = vertex_positions[v]
            pos   = (x * 1.2, y * 1.2)
            angle = atan2(y, x) * (180 / pi)

            labels[v] = Label(text, pos, angle)

        return labels

    def apply_backbone_strategy(self, backbone: BackboneStrategy) -> None:
        for i, graph in enumerate(self.graphs):
            backbone.extract_backbone(graph)
            print_progress_bar("Computed backbone", i + 1, len(self.graphs))
    