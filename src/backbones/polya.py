from typing import Callable

import networkx as nx

from common import strength, degree, integrate

"""
An implementation of the Polya Filter proposed by Marcaccioli et al. in
'A parametric approach to information filtering in complex networks: The Pólya Filter'
"""

# IT'S STILL THE DISPARITY FILTER

def get_normalise_fn(G, v) -> Callable[[float], float]:
    v_strength = strength(G, v)
    return lambda weight: weight / v_strength

def get_indefinite_pdf(G, v) -> Callable[[float], float]:
    v_deg = degree(G, v)
    return lambda x: -(1 - x) ** (v_deg - 1)

def disparity(G, p: float):
    # A normalisation function for each vertex
    normalise_fns   = { v: get_normalise_fn(G, v)   for v in G }

    # The indefinite integral of the probability density function
    # for each vertex
    indefinite_pdfs = { v: get_indefinite_pdf(G, v) for v in G }

    # The locally normalised edge weights.
    # Each edge appears twice in undirected graphs, each time normalised with
    # respect to the "starting" edge
    normalised_weights = {
        (v, u) : normalise_fns[v](G[v][u]["weight"])
            for v in G for u in G[v]
    }

    p_values = {
        (v, u): integrate(
            normalised_weights[v, u], 1,
            indefinite_pdfs[v],
            indefinite = True
        ) for v in G for u in G[v]
    }

    significant_adjacencies = {
        v: [u for u in G[v] if p_values[v, u] < p] for v in G
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
