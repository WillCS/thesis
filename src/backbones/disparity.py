from __future__ import annotations

import networkx as nx

from common import strength, degree, integrate

from .backbone import BackboneStrategy

"""
An implementation of the Disparity Filter proposed by Serrano et al. in
'Extracting the multiscale backbone of complex weighted networks'

Linear time, Linear space.
"""

class DisparityBackboneStrategy(BackboneStrategy):
    def __init__(self, graph: nx.Graph) -> DisparityBackboneStrategy:
        self.graph = graph

    def extract_backbone(self) -> nx.Graph:
        # Initialise the p values for all edges to be 1.
        for (v, u) in self.graph.edges():
            self.graph[v][u]["p"] = 1
            
        # Compute the p value for every edge.
        for v in self.graph:
            v_strength = strength(self.graph, v)
            v_deg      = degree(self.graph,   v)

            for u in self.graph[v]:
                w = self.graph[v][u]["weight"] / v_strength
                p_value = integrate(
                    w, 1,
                    lambda x: -(1 - x) ** (v_deg - 1),
                    indefinite = True
                )

                # If the p value we found for this edge is less than the
                # one we already had for it, udpate its p value to be the
                # new one.
                self.graph[v][u]["p"] = min([
                    p_value,
                    self.graph[v][u]["p"]
                ])

        return self.graph

    def correct_p_value(self, p: float) -> float:
        return p
