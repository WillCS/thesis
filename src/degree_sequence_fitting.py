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

collapsed = True

if collapsed:
    genetic_data_provider = MiscDataProvider("resources/plant_genetics/ATvAC_collapsed_contrast6_ATcorr_matrix.csv",
        vertex_name_row = False,
        directed        = False,
        absolute        = True
    )
    graph_n = 44
else:
    genetic_data_provider = GeneticDataProvider()
    graph_n = 71

backbone_strategy = DisparityBackboneStrategy()

genetic_graph = backbone_strategy.extract_backbone(genetic_data_provider.get_graph())

ps = [p for p in np.linspace(0, 0.2, 50)]

plot_xticks = np.linspace(0, 0.2, 11)

backbones = 1000
random_backbones = []

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

def average_strength(graph: nx.Graph, p = 0.1) -> float:
    strength_sum = 0
    vertices     = 0

    for v in graph.nodes:
        strength = 0
        for u in graph[v]:
            if graph[v][u]["p"] < p:
                strength += graph[v][u]["weight"]

        strength_sum += strength
        vertices     += 1

    return strength_sum / vertices

def average_degree(graph: nx.Graph, p = 0.1) -> float:
    degree_sum = 0
    vertices     = 0

    for v in graph.nodes:
        degree = 0
        for u in graph[v]:
            if graph[v][u]["p"] < p:
                degree += 1

        degree_sum += degree
        vertices   += 1

    return degree_sum / vertices

def average_edge_weight(graph: nx.Graph, p = 0.1) -> float:
    weight_sum = 0
    edges      = 0

    for (v, u) in graph.edges:
        if graph[v][u]["p"] < p:
            weight_sum += graph[v][u]["weight"]
            edges      += 1

    return 0 if edges == 0 else weight_sum / edges

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
        pw_law = np.array(power_law(xs, amplitude, exponent))
        np_seq  = np.array(seq)
        errorbars = pw_law - np_seq
        errorbars = np.array([[max(e, 0) for e in errorbars], [-min(e, 0) for e in errorbars]])

        plot.plot(xs, pw_law)
        plot.scatter(xs, seq)
        plot.errorbar(xs, pw_law, yerr = errorbars, fmt = "none")
        plot.xlabel("Position")
        plot.ylabel("Degree" if degree else "Strength")
        plot.title(f"{'Degree' if degree else 'Strength'} Sequence vs Fitted Power Law at p = {p}")
        plot.show()

    return exponent

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

    plot.title(f"Exponent of Power Law Fitted to {'Degree' if degree else 'Strength'} Sequence")
    plot.legend(["Random data", "Real data", "3σ"])
    plot.ylabel("Exponent")
    plot.xlabel("p-value")

    plot.xticks(plot_xticks)
    plot.grid()

    slice = 25

    plot.show()
    # plot.subplot(2, 1, 2)
    plot.clf()

    plot.hist([random_exponents[i][slice] for i in range(len(random_exponents))], 50)

    y_min, y_max = plot.ylim()

    plot.plot(np.linspace(real_exponents[slice], real_exponents[slice]), np.linspace(y_min, y_max))

    plot.ylim(y_min, y_max)

    plot.title(f"Exponents of {backbones} Power Laws Fitted to {'Degree' if degree else 'Strength'} Sequences - p = {ps[slice]:.2f}")
    plot.legend(["Random data", "Real data"])
    plot.ylabel("Occurrences")
    plot.xlabel("Exponent")

    plot.grid(axis = "y")

    plot.show()

def plot_graph_property(prop, name: str):
    real_values   = [prop(genetic_graph, p) for p in ps]
    random_values = [[] for _ in ps]
    mean_values   = []
    std_devs      = []

    for (i, p) in enumerate(ps):
        print_progress_bar(f"Computing {name}", i + 1, len(ps))

        for backbone in random_backbones:
            random_values[i].append(prop(backbone, p))

        mean_value, std_dev = estimate_distribution(random_values[i])
        mean_values.append(mean_value)
        std_devs.append(3 * std_dev)

    np_mean_values = np.array(mean_values)
    np_std_devs    = np.array(std_devs)

    plot.clf()

    plot.plot(ps, mean_values)
    plot.plot(ps, real_values)
    plot.fill_between(ps, np_mean_values + np_std_devs, np_mean_values - np_std_devs, alpha = 0.2)

    plot.title(f"{name} vs p-value")
    plot.legend(["Random data", "Real data", "3σ"])
    plot.ylabel(name)
    plot.xlabel("p-value")

    plot.xticks(plot_xticks)
    plot.grid()

    plot.show()

fit_power_law(genetic_graph, p = 0.1,  should_plot = True, degree = True)
fit_power_law(genetic_graph, p = 0.15, should_plot = True, degree = True)
fit_power_law(genetic_graph, p = 0.5,  should_plot = True, degree = True)

fit_power_law(genetic_graph, p = 0.1,  should_plot = True, degree = False)
fit_power_law(genetic_graph, p = 0.15, should_plot = True, degree = False)
fit_power_law(genetic_graph, p = 0.5,  should_plot = True, degree = False)

plot_sequence(degree = True)
plot_sequence(degree = False)

plot_graph_property(size,                "Backbone Size")
plot_graph_property(order,               "Backbone Order")
plot_graph_property(total_strength,      "Backbone Total Strength")
plot_graph_property(average_strength,    "Backbone Average Strength")
plot_graph_property(average_degree,      "Backbone Average Degree")
plot_graph_property(average_edge_weight, "Backbone Average Edge Weight")
