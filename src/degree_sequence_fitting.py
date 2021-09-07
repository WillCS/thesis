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
from data      import GeneticDataProvider, RandomGeneticDataProvider, MiscDataProvider, genetic_data_provider

# genetic_data_provider = MiscDataProvider("resources/plant_genetics/ATvAC_collapsed_contrast6_ATcorr_matrix.csv")
genetic_data_provider = GeneticDataProvider()
graph_n = 71
backbone_strategy = DisparityBackboneStrategy()

genetic_graph = backbone_strategy.extract_backbone(genetic_data_provider.get_graph())

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
    strength = 0
    for (v, u) in graph.edges:
        if graph[v][u]["p"] < p:
            strength += graph[v][u]["weight"]

    return strength

def power_law(x, a, b):
    return a * np.power(x, b)

def fit_power_law(graph: nx.Graph, p: float = 0.1, should_plot = False, degree = True) -> Optional[float]:
    if degree:
        seq = np.array(degree_sequence(graph, p))
    else:
        seq = np.array(strength_sequence(graph, p))

    xs  = np.array([x + 1 for x in range(len(seq))])

    logx = np.log10(xs)
    logy = np.log10(seq)
    y_error = (0.2 * seq) / seq

    fit_func = lambda p, x: p[0] + p[1] * x
    err_func = lambda p, x, y, err: (y - fit_func(p, x)) / err

    p_init = [1.0, -1.0]
    out = None
    try:
        out = leastsq(err_func, p_init, args = (logx, logy, y_error), full_output = 1)
    except:
        return None

    exponent = out[0][1]
    amplitude = 10 ** out[0][0]

    if should_plot:
        plot.plot(xs, power_law(xs, amplitude, exponent))
        plot.scatter(xs, seq)
        plot.show()

    return exponent

ps = [p for p in np.linspace(0, 1, 100)]

def get_exponents(graph: nx.Graph, ps: List[float], degree = True) -> List[float]:
    return [fit_power_law(graph, p, degree = degree) for p in ps]

def estimate_distribution(samples: List[float]) -> Tuple[float, float]:
    average = mean(samples)
    std_dev = stdev(samples, xbar = average)

    return (average, std_dev)

def plot_normal_distribution(average: float, std_dev: float) -> None:
    x = np.linspace(average - 5 * std_dev, average + 5 * std_dev, 100)
    y = scipy.stats.norm.pdf(x, average, std_dev)

    plot.plot(x, y)

def get_random_backbone(strategy: BackboneStrategy) -> nx.Graph:
    provider = RandomGeneticDataProvider(n = graph_n)
    provider.apply_backbone_strategy(strategy)

    return provider.get_graph()

backbones = 1000
random_backbones = []

for i in range(backbones):
    print_progress_bar(f"Computing backbone", i + 1, backbones)
    random_backbones.append(get_random_backbone(backbone_strategy))

def plot_sequence(degree = True):
    real_exponents = get_exponents(genetic_graph, ps, degree)

    random_exponents = []
    for i in range(backbones):
        print_progress_bar(f"Fitting power laws", i + 1, backbones)
        
        random_exponents.append(get_exponents(random_backbones[i], ps, degree))

    mean_exponents = []
    for (i, p) in enumerate(ps):
        print_progress_bar(f"Averaging exponents", i + 1, len(ps))

        exps = [e[i] for e in random_exponents if e[i] is not None]
        if len(exps) > 0:
            mean_exponents.append(mean(exps))
        else:
            mean_exponents.append(None)

    diff = sum([1 for x in mean_exponents if x is None])

    yerr = []

    for slice in range(diff, len(random_exponents[0])):
        print_progress_bar(f"Estimating distributions", slice + 1 - diff, len(random_exponents[0]) - diff)

        samples = [random_exponents[i][slice] for i in range(len(random_exponents)) if random_exponents[i][slice] is not None]
        if len(samples) < 2:
            yerr.append(0)
        else:
            average, std_dev = estimate_distribution(samples)
            yerr.append(std_dev * 3)

    m_exps = np.array(mean_exponents[diff:])
    std_devs = np.array(yerr)

    plot.clf()
    # plot.subplot(2, 1, 1)
    plot.plot(ps[diff:], mean_exponents[diff:])
    plot.fill_between(ps[diff:], m_exps + std_devs, m_exps - std_devs, alpha = 0.2)
    plot.plot(ps, real_exponents)

    plot.title(f"Exponent of Power Law Fitted to {'Degree' if degree else'Strength'} Sequence")
    plot.legend(["Random data", "Real data", "3σ"])
    plot.ylabel("Exponent")
    plot.xlabel("p-value")

    plot.xticks(np.linspace(0, 1, 11))
    plot.grid()

    slice = 10

    plot.show()
    # plot.subplot(2, 1, 2)
    plot.clf()

    plot.hist([random_exponents[i][slice] for i in range(len(random_exponents))], 50)

    y_min, y_max = plot.ylim()

    plot.plot(np.linspace(real_exponents[slice], real_exponents[slice]), np.linspace(y_min, y_max))

    plot.ylim(y_min, y_max)

    plot.title(f"Exponents of {backbones} Power Laws Fitted to {'Degree' if degree else'Strength'} Sequences")
    plot.legend(["Random data", "Real data"])
    plot.ylabel("Occurrences")
    plot.xlabel("Exponent")

    plot.grid(axis = "y")

    plot.show()

def plot_graph_properties():
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

    np_ssd = np.array(size_std_devs)
    np_osd = np.array(order_std_devs)
    np_tsd = np.array(total_strength_std_devs)

    np_s = np.array(a_sizes)
    np_o = np.array(a_orders)
    np_t = np.array(a_total_strengths)

    plot.clf()

    # plot.subplot(1, 3, 1)
    plot.plot(ps, a_sizes)
    plot.plot(ps, r_sizes)
    plot.fill_between(ps, np_s + np_ssd, np_s - np_ssd, alpha = 0.2)

    plot.title("Backbone Size vs p-value")
    plot.legend(["Random data", "Real data", "3σ"])
    plot.ylabel("Graph Size")
    plot.xlabel("p-value")

    plot.xticks(np.linspace(0, 1, 11))
    plot.grid()

    plot.show()

    plot.clf()
    # plot.subplot(1, 3, 2)

    plot.plot(ps, a_orders)
    plot.plot(ps, r_orders)
    plot.fill_between(ps, np_o + np_osd, np_o - np_osd, alpha = 0.2)

    plot.title("Backbone Order vs p-value")
    plot.legend(["Random data", "Real data", "3σ"])
    plot.ylabel("Graph Order")
    plot.xlabel("p-value")

    plot.xticks(np.linspace(0, 1, 11))
    plot.grid()

    plot.show()

    plot.clf()
    # plot.subplot(1, 3, 3)

    plot.plot(ps, a_total_strengths)
    plot.plot(ps, r_total_strengths)
    plot.fill_between(ps, np_t + np_tsd, np_t - np_tsd, alpha = 0.2)

    plot.title("Backbone Total Strength vs p-value")
    plot.legend(["Random data", "Real data", "3σ"])
    plot.ylabel("Graph Total Strength")
    plot.xlabel("p-value")

    plot.xticks(np.linspace(0, 1, 11))
    plot.grid()

    # plot.xticks(np.linspace(0, 1, 11))
    # plot.grid()

    plot.show()

plot_sequence(True)
plot_sequence(False)
plot_graph_properties()
