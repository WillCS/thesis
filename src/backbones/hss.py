from __future__ import annotations

import networkx as nx

from common import map_graph

from .threshold import threshold
from .backbone import BackboneStrategy

def proximity(weight) -> float:
    if weight != 0:
        return 1 / weight
    else:
        return float("inf")

class HighSalienceSkeletonBackboneStrategy(BackboneStrategy):
    def extract_backbone(self, graph: nx.Graph) -> nx.Graph:
        proximity_graph = map_graph(graph, proximity)
        shortest_paths  = dict(nx.all_pairs_dijkstra_path(proximity_graph))

        shortest_path_trees = {}

        for v in proximity_graph:
            paths_from_v = shortest_paths[v]
            shortest_path_trees[v] = nx.Graph()

            for u in proximity_graph:
                if u in paths_from_v.keys() and len(paths_from_v[u]) > 1:
                    path = paths_from_v[u]
                    for i in range(len(path) - 1):
                        shortest_path_trees[v].add_edge(path[i], path[i + 1])

        inverse_order = 1 / proximity_graph.order()

        salience = {
            (v, u): inverse_order * len(
                list(t for t in shortest_path_trees.values() if v in t and u in t[v]))
            for v in proximity_graph
            for u in proximity_graph[v]
        }

        for (v, u) in graph:
            graph[v][u]["salience"] = salience[v,u]["weight"]

        return graph

    def correct_p_value(self, graph: nx.Graph, p: float) -> float:
        return p
