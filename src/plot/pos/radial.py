from __future__ import annotations
from typing import Dict, Any, List, Optional
from math import cos, sin

import numpy as np
import networkx as nx

from common import Clustering, strength

from .position import PositionStrategy

class UndirectedRadialPositionStrategy(PositionStrategy):
    def __init__(self,
        by_cluster:  bool = False,
        by_strength: bool = False
    ) -> UndirectedRadialPositionStrategy:
        self.by_cluster  = by_cluster
        self.by_strength = by_strength

    def filtered_strength(self, v,
        graph: nx.Graph,
        edges: Optional[List] = None
    ) -> float:
        if edges is None:
            return strength(graph, v)
        else:
            return sum([
                graph[x][y]["weight"] for (x, y) in edges if x == v or x == y
            ])

    def generate_positions(self, 
        graph:    nx.Graph,
        edges:    Optional[List]       = None,
        clusters: Optional[Clustering] = None
    ) -> Dict[Any, np.ndarray]:
        n_vertices   = graph.order()
        vertex_order = [
            sorted(c, key = lambda v: self.filtered_strength(v, graph, edges))
            for c in clusters.get_cluster_list()
        ]
        
        # flatten the list
        vertex_order = [v for c in vertex_order for v in c]

        return { vertex_order[i]: 
            (cos(2 * np.pi * i / n_vertices), sin(2 * np.pi * i / n_vertices))
            for i in range(n_vertices)
        }
