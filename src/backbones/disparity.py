from typing import Callable

import networkx as nx

from common import transform_incident_edge_weights, strength, degree, integrate

def get_normalise_fn(G, v):
    v_strength = strength(G, v)
    return lambda weight: weight / v_strength

def get_indefinite_pdf(deg: int) -> Callable[[float], float]:
    return lambda x: -(1 - x) ** (deg - 1)

def disparity(G, p: float):
    normalise_fns   = { v: get_normalise_fn(G, v) for v in G }
    indefinite_pdfs = { v: get_indefinite_pdf(degree(G, v)) for v in G }

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
        v: [u for u in G[v] if p_values[v, u] > p] for v in G
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
