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

def strength(G, v) -> float:
    return sum(G[v][u]["weight"] for u in G[v])

def degree(G, v) -> int:
    return len(G[v])

# print(integrate(0.5, 1, integrand(10)))
# print(integrate(0.5, 1, indefinite(10), indefinite = True))
