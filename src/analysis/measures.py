from typing import List, Optional, Tuple
from statistics import mean, stdev

import networkx as nx
import numpy    as np

from scipy.optimize.minpack import leastsq

def degree_sequence(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> List[int]:
    degrees = { v: 0 for v in graph.nodes }

    for (v, u) in graph.edges:
        if graph[v][u][attribute] < p:
            degrees[v] += 1
            degrees[u] += 1

    return [x for x in sorted(degrees.values(), reverse = True) if x > 0]

def strength_sequence(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> List[int]:
    weights = { v: 0 for v in graph.nodes }

    for (v, u) in graph.edges:
        if graph[v][u][attribute] < p:
            weight = graph[v][u]["weight"]
            weights[v] += weight
            weights[u] += weight

    return [x for x in sorted(weights.values(), reverse = True) if x > 0]

def size(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> int:
    size = 0
    for (v, u) in graph.edges:
        if graph[v][u][attribute] < p:
            size += 1

    return size

def order(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> int:
    order = 0
    for v in graph.nodes:
        if len(list(graph[v][u] for u in graph[v] if graph[v][u][attribute] < p)) > 0:
            order += 1

    return order

def total_strength(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> float:
    strength_sum = 0

    for v in graph.nodes:
        strength = 0
        for u in graph[v]:
            if graph[v][u][attribute] < p:
                strength += graph[v][u]["weight"]

        strength_sum += strength

    return strength_sum

def mean_maybe_empty(sample: List[float]) -> float:
    return 0 if len(sample) == 0 else mean(sample)

def strengths(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> List[float]:
    strengths = []

    for v in graph.nodes:
        strength = 0
        for u in graph[v]:
            if graph[v][u][attribute] < p:
                strength += graph[v][u]["weight"]

        if strength > 0:
            strengths.append(strength)

    return strengths

def average_strength(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> float:
    return mean_maybe_empty(strengths(graph, p, attribute))

def degrees(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> List[int]:
    degrees = []

    for v in graph.nodes:
        degree = 0
        for u in graph[v]:
            if graph[v][u][attribute] < p:
                degree += 1

        if degree > 0:
            degrees.append(degree)

    return degrees

def average_degree(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> float:
    return mean_maybe_empty(degrees(graph, p, attribute))

def edge_weights(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> List[float]:
    edge_weights = []

    for (v, u) in graph.edges:
        if graph[v][u][attribute] < p:
            edge_weights.append(graph[v][u]["weight"])

    return edge_weights

def average_edge_weight(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> float:
    return mean_maybe_empty(edge_weights(graph, p, attribute))

def p_values(graph: nx.Graph, attribute: str = "p") -> List[float]:
    p_values = []

    for (v, u) in graph.edges:
        p_values.append(graph[v][u][attribute])

    return p_values

def degree_sequence_power_law_exponent(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> Optional[float]:
    seq = np.array(degree_sequence(graph, p, attribute))
    return fit_power_law(seq)

def strength_sequence_power_law_exponent(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> Optional[float]:
    seq = np.array(strength_sequence(graph, p, attribute))
    return fit_power_law(seq)

def power_law(x, a, b):
    return a * np.power(x, b)

def fit_power_law(seq: np.ndarray) -> Optional[float]:
    xs  = np.array([x + 1 for x in range(len(seq))])

    logx    = np.log10(xs)
    logy    = np.log10(seq)
    y_error = (0.2 * seq) / seq

    fit_func = lambda p, x: p[0] + p[1] * x
    err_func = lambda p, x, y, err: (y - fit_func(p, x)) / err

    p_init = [1.0, -1.0]

    try:
        out = leastsq(err_func, p_init, args = (logx, logy, y_error), full_output = 1)
        return out[0][1]
    except:
        return None

def degree_sequence_exponents(
    graph:     nx.Graph,
    ps:        List[float],
    attribute: str = "p"
) -> Optional[float]:
    return [degree_sequence_power_law_exponent(graph, p, attribute) for p in ps]

def strength_sequence_exponents(
    graph:     nx.Graph,
    ps:        List[float],
    attribute: str = "p"
) -> Optional[float]:
    return [strength_sequence_power_law_exponent(graph, p, attribute) for p in ps]
