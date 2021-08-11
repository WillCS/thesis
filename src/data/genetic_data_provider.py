from __future__ import annotations
from typing import Any, Tuple, Dict, List, Optional
from math import cos, sin, pi, atan2
from csv import DictReader

import networkx as nx

from common import Clustering, strength
from plot.label import Label

from .csv_adjacency import get_graph_from_csv_adjacency_matrix
from .data_provider import DataProvider

ADJACENCY_MATRIX_FILE = "./resources/plant_genetics/ATvAC_contrast6_ATcorr_matrix.csv"
FAMILY_FILE           = "./resources/plant_genetics/AT_gene_family_2021-08-04.csv"

def filtered_strength(v, graph: nx.Graph, edges: List) -> float:
    if edges is None:
        return strength(graph, v)
    else:
        return sum([
            graph[x][y]["weight"] for (x, y) in edges if x == v or x == y
        ])

def get_vertex_names() -> Dict[str, str]:
    names = {}
    with open(FAMILY_FILE) as csvfile:
        reader = DictReader(csvfile)

        for row in reader:
            names[row["gene_num"]] = row["Gene_Id"]

    return names

class GeneticDataProvider(DataProvider):
    def __init__(self) -> GeneticDataProvider:
        self.graph = get_graph_from_csv_adjacency_matrix(ADJACENCY_MATRIX_FILE, absolute = True)

        self.names = get_vertex_names()

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
