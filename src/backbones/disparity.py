from typing import Callable

import networkx as nx

from common import strength, degree, integrate

"""
An implementation of the Disparity Filter proposed by Serrano et al. in
'Extracting the multiscale backbone of complex weighted networks'

Linear time, Linear space.
"""

def disparity(G, p: float):
    for (u, v) in G.edges():
        G[u][v]["p"] = 1

    for v in G:
        v_strength = strength(G, v)
        v_deg      = degree(G, v)
        for u in G[v]:
            w = G[v][u]["weight"] / v_strength
            p_value = integrate(
                w, 1,
                lambda x: -(1 - x) ** (v_deg - 1),
                indefinite = True
            )

            G[v][u]["p"] = min([p_value, G[v][u]["p"]])

    # backbone = nx.Graph()
    # backbone.add_nodes_from(G)
    # for (v, u) in G.edges():
    #     if G[v][u]["p"] < p:
    #         backbone.add_edge(v, u, weight = G[v][u]["weight"])

    return G
