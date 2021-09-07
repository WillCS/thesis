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

def power_law(x, a, b):
    return a * np.power(x, b)

def fit_power_law(graph: nx.Graph, p: float = 0.1, should_plot = False) -> Optional[float]:
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

def get_exponents(graph: nx.Graph, ps: List[float]) -> List[float]:
    return [fit_power_law(graph, p) for p in ps]

def estimate_distribution(samples: List[float]) -> Tuple[float, float]:
    average = mean(samples)
    std_dev = stdev(samples, xbar = average)

    return (average, std_dev)

def plot_normal_distribution(average: float, std_dev: float) -> None:
    x = np.linspace(average - 5 * std_dev, average + 5 * std_dev, 100)
    y = scipy.stats.norm.pdf(x, average, std_dev)

    plot.plot(x, y)

real_exponents = get_exponents(genetic_graph, ps)

def get_random_backbone(strategy: BackboneStrategy) -> nx.Graph:
    provider = RandomGeneticDataProvider()
    provider.apply_backbone_strategy(strategy)

    return provider.get_graph()

backbones = 100

random_backbones = []

for i in range(backbones):
    print_progress_bar(f"Computing backbone", i + 1, backbones)
    random_backbones.append(get_random_backbone(backbone_strategy))

random_exponents = []
for i in range(backbones):
    print_progress_bar(f"Fitting power laws", i + 1, backbones)
    
    random_exponents.append(get_exponents(random_backbones[i], ps))

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

plot.subplot(2, 1, 1)
plot.plot(ps[diff:], mean_exponents[diff:])
plot.errorbar(ps[diff:], mean_exponents[diff:], yerr = yerr, fmt = 'none')
plot.plot(ps, real_exponents)
plot.legend(["mean", "real"])
plot.xticks(np.linspace(0, 1, 11))
plot.grid()

slice = 10

plot.subplot(2, 1, 2)
plot.hist([random_exponents[i][slice] for i in range(len(random_exponents))], 50)

y_min, y_max = plot.ylim()

plot.plot(np.linspace(real_exponents[slice], real_exponents[slice]), np.linspace(y_min, y_max))
average, std_dev = estimate_distribution([random_exponents[i][slice] for i in range(len(random_exponents))])
# plot_normal_distribution(average, std_dev)

plot.show()
