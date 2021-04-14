from typing import Callable, Optional, Iterable

import networkx as nx
import numpy    as np
import pandas   as pd

from scipy.integrate import quad

def integrand(k):
    return lambda x: (k - 1) * (1 - x) ** (k - 2)

def indefinite(k):
    return lambda x: -(1 - x) ** (k - 1)

def integrate(l: float, u: float,
    fn:         Callable[[float], float],
    indefinite: bool = False
) -> float:
    if indefinite:
        return fn(u) - fn(l)
    else:
        return quad(fn, l, u)

def transform_incident_edge_weights(G, v, f) -> Iterable:
    return {v2: f(G[v][v2]["weight"]) for v2 in G[v]}

def strength(G, v) -> float:
    return sum(G[v][v2]["weight"] for v2 in G[v])

# print(integrate(0.5, 1, integrand(10)))
# print(integrate(0.5, 1, indefinite(10), indefinite = True))

graph = nx.Graph()
graph.add_nodes_from(["a", "b", "c", "d"])
graph.add_edge("a", "b", weight = 1)
graph.add_edge("a", "c", weight = 0.5)

print(nx.edges(graph, "a"))
print(graph["a"])

print(strength(graph, "a"))

print(transform_incident_edge_weights(graph, "a", lambda a: a / (strength(graph, "a"))))
