from math import factorial, sqrt, pi, asin
import random
from typing import Optional, List

import networkx as nx
import numpy as np
from scipy.interpolate import interp1d

def generate_weights(n: int) -> List[float]:
    pdf = lambda x: (4 / pi) * sqrt(1 - pow(x, 2))

    xs = np.linspace(0, 1, 1000)
    c  = np.cumsum([pdf(x) for x in xs])
    c -= c.min()
    f  = interp1d(c / c.max(), xs)

    return f(np.random.random(n))

def create_random_complete_graph(n: int, seed: Optional[int] = None) -> nx.Graph:
    if seed is not None:
        random.seed(seed)

    weights = generate_weights(n * (n - 1) // 2)

    graph = nx.Graph()
    graph.add_nodes_from([v for v in range(n)])

    i = 0
    for v in range(n):
        for u in range(v + 1, n):
            graph.add_edge(v, u, weight = weights[i])
            i = i + 1

    return graph
