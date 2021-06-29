import networkx as nx

from common import map_graph
from .threshold import threshold

def proximity(weight) -> float:
    if weight != 0:
        return 1 / weight
    else:
        return float("inf")

def high_salience_skeleton(G, t: float = 0.5):
    proximity_graph = map_graph(G, proximity)

    shortest_paths = dict(nx.all_pairs_dijkstra_path(proximity_graph))

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

    salience = [
        (v, u, inverse_order * len(list(t for t in shortest_path_trees.values() if v in t and u in t[v])))
        for v in proximity_graph
        for u in proximity_graph[v]
    ]

    salience_graph = nx.Graph()
    salience_graph.add_weighted_edges_from(salience)

    hss = threshold(salience_graph, t)

    return hss
