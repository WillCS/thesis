from typing import Callable

import networkx as nx
import scipy.special as sc

from common import strength, degree, integrate

"""
An implementation of the Polya Filter proposed by Marcaccioli et al. in
'A parametric approach to information filtering in complex networks: The Pólya Filter'
"""

def pmf(G, v, w, a) -> float:
    k = degree(G, v)
    s = strength(G, v)
    coef = sc.comb(s, w, exact = True)
    return coef * (sc.beta(1 / a + w, (k - 1) / a + s - w)) / (sc.beta(1 / a, (k - 1) / a))

def polya(G, p: float, a: float):
    p_values = {}
    if nx.is_directed(G):
        for (v, u) in G.edges():
            p_values[v, u] = pmf(G, v, G[v][u]["weight"], a)
    else:
        for (v, u) in G.edges():
            p_values[v, u] = pmf(G, v, G[v][u]["weight"], a)
            p_values[u, v] = pmf(G, u, G[v][u]["weight"], a)

    corrected_p = p / len(p_values)

    significant_adjacencies = {
        v: [u for u in G[v] if p_values[v, u] < corrected_p] for v in G
    }

    significant_edges = [
        (v, u, G[u][v]["weight"]) 
        for v in G if len(significant_adjacencies[v]) > 0
        for u in significant_adjacencies[v]
    ]

    backbone = nx.Graph()
    backbone.add_nodes_from(G)
    backbone.add_weighted_edges_from(significant_edges)

    return backbone
