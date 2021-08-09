from __future__ import annotations
from decimal import *
import math

import networkx as nx
import scipy.special as sc

from common import strength, degree
from common.common import integrate
from .backbone import BackboneStrategy

"""
An implementation of the Pólya Filter proposed by Marcaccioli et al. in
'A parametric approach to information filtering in complex networks: The Pólya Filter'
"""

class PolyaBackboneStrategy(BackboneStrategy):
    def __init__(self, graph: nx.Graph, a: float, integer_weights = True) -> PolyaBackboneStrategy:
        self.graph           = graph
        self.a               = a
        self.integer_weights = integer_weights

    def extract_backbone(self) -> nx.Graph:
        for (v, u) in self.graph.edges():
            w = self.graph[v][u]["weight"]
            ps = []
                
            ps.append(self._compute_p_value(v, w))
            if not self.graph.is_directed:
                ps.append(self._compute_p_value(u, w))

            self.graph[v][u]["p"] = min(ps)

        return self.graph

    def correct_p_value(self, p: float) -> float:
        return p

        num_tests = len(self.graph.edges())
        if not self.graph.is_directed:
            return p / (2 * num_tests)
        else:
            return p / num_tests

    def _pmf(self, v, w) -> float:
        k = degree(self.graph,   v)
        s = strength(self.graph, v)

        coef        = Decimal(sc.comb(s, w, exact = True))
        numerator   = Decimal(sc.beta((1 / self.a) + w, ((k - 1) / self.a) + s - w))
        denominator = Decimal(sc.beta(1 / self.a, (k - 1) / self.a))
        return float(coef * (numerator / denominator))

    def _p_approximation(self, v, w) -> float:
        """
        The Pólya filter was designed with integer-weighted graphs in mind.
        In order to apply it to graphs with non-integer weights, we use
        the approximation given in (A1) on page 11 of Marcaccioli et al.'s
        paper.
        """
        k = degree(self.graph,   v)
        s = strength(self.graph, v)
        
        t1 = (1 / sc.gamma(1 / self.a))
        t2 = math.pow(1 - (w / s), (k - 1) / self.a)
        t3 = math.pow((w * k) / (s * self.a), (1 / self.a) - 1)
        return t1 * t2 * t3


    def _compute_p_value(self, v, w) -> float:
        if self.integer_weights:
            return 1 - sum([self._pmf(v, x) for x in range(0, w - 1)])
        else:
            return self._p_approximation(v, w)
