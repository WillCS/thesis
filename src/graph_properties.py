from statistics import mean, stdev
from typing import List, Optional, Tuple
from math import pow, sqrt

from matplotlib import pyplot as plot
from matplotlib.widgets import Slider
import networkx as nx
import numpy    as np
from scipy.optimize import curve_fit
from scipy.optimize.minpack import leastsq
import scipy.stats

from backbones import DisparityBackboneStrategy
from backbones.backbone import BackboneStrategy
from common.progress_bar import print_progress_bar
from data      import GeneticDataProvider, RandomGeneticDataProvider

genetic_data_provider = GeneticDataProvider()
backbone_strategy = DisparityBackboneStrategy()

genetic_graph = backbone_strategy.extract_backbone(genetic_data_provider.get_graph())

def plot_weights(graph, p = 0.1):
    weights = [ graph[u][v]["weight"] for (u, v) in graph.edges if graph[u][v]["p"] < p]

    plot.hist(weights, 100)
    plot.show()

# plot_weights(genetic_graph)
# plot_weights(random_graph)

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
    strength = 0
    for (v, u) in graph.edges:
        if graph[v][u]["p"] < p:
            strength += graph[v][u]["weight"]

    return strength

def estimate_distribution(samples: List[float]) -> Tuple[float, float]:
    average = mean(samples)
    std_dev = stdev(samples, xbar = average)

    return (average, std_dev)

def plot_normal_distribution(average: float, std_dev: float) -> None:
    x = np.linspace(average - 5 * std_dev, average + 5 * std_dev, 100)
    y = scipy.stats.norm.pdf(x, average, std_dev)

    plot.plot(x, y)

def get_random_backbone(strategy: BackboneStrategy) -> nx.Graph:
    provider = RandomGeneticDataProvider()
    provider.apply_backbone_strategy(strategy)

    return provider.get_graph()

backbones = 100
random_backbones = []

ps = [p for p in np.linspace(0, 1, 100)]

r_sizes           = [size(genetic_graph, p) for p in ps]
r_orders          = [order(genetic_graph, p) for p in ps]
r_total_strengths = [total_strength(genetic_graph, p) for p in ps]

sizes           = [[] for _ in ps]
orders          = [[] for _ in ps]
total_strengths = [[] for _ in ps]

a_sizes           = []
a_orders          = []
a_total_strengths = []

size_std_devs           = []
order_std_devs          = []
total_strength_std_devs = []

for i in range(backbones):
    print_progress_bar(f"Computing backbone", i + 1, backbones)
    random_backbones.append(get_random_backbone(backbone_strategy))

for (i, p) in enumerate(ps):
    print_progress_bar(f"Computing graph properties", i + 1, len(ps))

    for backbone in random_backbones:
        sizes[i].append(size(backbone, p))
        orders[i].append(order(backbone, p))
        total_strengths[i].append(total_strength(backbone, p))

    m_size,           size_std_dev           = estimate_distribution(sizes[i])
    m_order,          order_std_dev          = estimate_distribution(orders[i])
    m_total_strength, total_strength_std_dev = estimate_distribution(total_strengths[i])

    a_sizes.append(m_size)
    a_orders.append(m_order)
    a_total_strengths.append(m_total_strength)

    size_std_devs.append(3 * size_std_dev)
    order_std_devs.append(3 * order_std_dev)
    total_strength_std_devs.append(3 * total_strength_std_dev)

plot.subplot(1, 3, 1)
plot.plot(ps, a_sizes)
plot.plot(ps, r_sizes)
plot.errorbar(ps, a_sizes, yerr = size_std_devs, fmt = "none")
plot.legend(["mean", "real"])

plot.subplot(1, 3, 2)
plot.plot(ps, a_orders)
plot.plot(ps, r_orders)
plot.errorbar(ps, a_orders, yerr = order_std_devs, fmt = "none")
plot.legend(["mean", "real"])

plot.subplot(1, 3, 3)
plot.plot(ps, a_total_strengths)
plot.plot(ps, r_total_strengths)
plot.errorbar(ps, a_total_strengths, yerr = total_strength_std_devs, fmt = "none")
plot.legend(["mean", "real"])

# plot.xticks(np.linspace(0, 1, 11))
# plot.grid()

plot.show()
