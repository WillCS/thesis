from math import sqrt
import random
from typing import Optional, List, Tuple
from statistics import mean

import networkx as nx

# By the central limit theorem, the sum of independent random variables
# approximates a normal distribution.
def get_random_normal(n: int = 3) -> float:
    return sum([random.uniform(0, 1 / n) for _ in range(n)])

def correlation(
    v: Tuple[float, float, float, float, float],
    u: Tuple[float, float, float, float, float]
) -> float:
    v_mean = mean(v)
    u_mean = mean(u)

    c_v = [v_i - v_mean for v_i in v]
    c_u = [u_i - u_mean for u_i in u]

    numerator   = sum([c_v[i] * c_u[i] for i in range(5)])
    denominator = sqrt(sum([pow(c_v_i, 2) for c_v_i in c_v]) * sum([pow(c_u_i, 2) for c_u_i in c_u]))

    return abs(numerator / denominator)

def generate_vertex() -> Tuple[float, float, float, float, float]:
    return tuple([get_random_normal() for _ in range(5)])

def generate_vertices(n: int) -> List[Tuple[float, float, float, float, float]]:
    return [generate_vertex() for v in range(n)]

def create_random_complete_graph(n: int, seed: Optional[int] = None) -> nx.Graph:
    if seed is not None:
        random.seed(seed)

    tuples = generate_vertices(n)

    graph = nx.Graph()
    graph.add_nodes_from([v for v in range(n)])

    i = 0
    for v in range(n):
        for u in range(v + 1, n):
            graph.add_edge(v, u, weight = correlation(tuples[v], tuples[u]))
            i = i + 1

    return graph
