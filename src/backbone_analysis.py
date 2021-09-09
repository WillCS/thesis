from statistics import mean, stdev
from typing import Callable, List, Optional
from math import pow, sqrt

from matplotlib import pyplot as plot
import networkx as nx
import numpy    as np

from backbones import BackboneStrategy, DisparityBackboneStrategy, PolyaBackboneStrategy
from data      import USAirportDataProvider

a_list = [0.1, 1, 10, 100, 1000]

data_providers      = [USAirportDataProvider() for _ in a_list]
# backbone_strategy = DisparityBackboneStrategy()
backbone_strategies = [PolyaBackboneStrategy(a, integer_weights = False) for a in a_list]
backbones           = [strategy.extract_backbone(data_providers[i].get_graph()) for i, strategy in enumerate(backbone_strategies)]

# backbone = backbone_strategy.extract_backbone(data_provider.get_graph())
ps       = [p for p in np.linspace(0, 1, 100)]

plot_xticks = np.linspace(0, 1, 11)

def plot_weights(graph, p = 0.1):
    weights = [ graph[u][v]["weight"] for (u, v) in graph.edges if graph[u][v]["p"] < p]

    plot.hist(weights, 100)
    plot.show()

def degree_sequence(graph: nx.Graph, p = 0.1) -> List[int]:
    degrees = { v: 0 for v in graph.nodes }

    for (v, u) in graph.edges:
        if graph[v][u]["p"] < p:
            degrees[v] += 1
            degrees[u] += 1

    return [x for x in sorted(degrees.values(), reverse = True) if x > 0]

def strength_sequence(graph: nx.Graph, p = 0.1) -> List[int]:
    weights = { v: 0 for v in graph.nodes }

    for (v, u) in graph.edges:
        if graph[v][u]["p"] < p:
            weight = graph[v][u]["weight"]
            weights[v] += weight
            weights[u] += weight

    return [x for x in sorted(weights.values(), reverse = True) if x > 0]

def size(graph: nx.Graph, p = 0.1) -> int:
    size = 0
    for (v, u) in graph.edges:
        if graph[v][u]["p"] < p:
            size += 1

    return size

def order(graph: nx.Graph, p = 0.1) -> int:
    order = 0
    for v in graph.nodes:
        if len(list(graph[v][u] for u in graph[v] if graph[v][u]["p"] < p)) > 0:
            order += 1

    return order

def total_strength(graph: nx.Graph, p = 0.1) -> float:
    strength_sum = 0

    for v in graph.nodes:
        strength = 0
        for u in graph[v]:
            if graph[v][u]["p"] < p:
                strength += graph[v][u]["weight"]

        strength_sum += strength

    return strength_sum

def mean_maybe_empty(sample: List[float]) -> float:
    return 0 if len(sample) == 0 else mean(sample)

def average_strength(graph: nx.Graph, p = 0.1) -> float:
    strengths = []

    for v in graph.nodes:
        strength = 0
        for u in graph[v]:
            if graph[v][u]["p"] < p:
                strength += graph[v][u]["weight"]

        strengths.append(strength)

    return mean_maybe_empty(strengths)

def average_degree(graph: nx.Graph, p = 0.1) -> float:
    degrees = []

    for v in graph.nodes:
        degree = 0
        for u in graph[v]:
            if graph[v][u]["p"] < p:
                degree += 1

        degrees.append(degree)

    return mean_maybe_empty(degrees)

def average_edge_weight(graph: nx.Graph, p = 0.1) -> float:
    edge_weights = []

    for (v, u) in graph.edges:
        if graph[v][u]["p"] < p:
            edge_weights.append(graph[v][u]["weight"])

    return mean_maybe_empty(edge_weights)

def plot_graph_property(
    prop:      Callable[[nx.Graph, float], float], 
    backbones: List[nx.Graph],
    name:      str,
    legend:    Optional[List[str]] = None,
) -> None:
    plot.clf()

    for backbone in backbones:
        plot.plot(ps, [prop(backbone, p) for p in ps])

    plot.title(f"{name} vs p-value")
    if legend:
        plot.legend(legend)

    plot.ylabel(name)
    plot.xlabel("p-value")

    plot.xticks(plot_xticks)
    plot.grid()

    plot.show()

legend = [f"a = {a}" for a in a_list]

plot_graph_property(size,                backbones, "Backbone Size",                legend = legend)
plot_graph_property(order,               backbones, "Backbone Order",               legend = legend)
plot_graph_property(total_strength,      backbones, "Backbone Total Strength",      legend = legend)
plot_graph_property(average_strength,    backbones, "Backbone Average Strength",    legend = legend)
plot_graph_property(average_degree,      backbones, "Backbone Average Degree",      legend = legend) 
plot_graph_property(average_edge_weight, backbones, "Backbone Average Edge Weight", legend = legend)
