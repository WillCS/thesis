from statistics import mean
from typing import List, Optional

from matplotlib import pyplot as plot
import networkx as nx
import numpy    as np
from scipy.optimize import curve_fit
from scipy.optimize.minpack import leastsq

from backbones import DisparityBackboneStrategy
from backbones.backbone import BackboneStrategy
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

def size(graph: nx.Graph, p = 0.1) -> int:
    size = 0
    for (v, u) in graph.edges:
        if graph[v][u]["p"] < p:
            size += 1

    return size

def power_law(x, a, b):
    return a * np.power(x, b)

def fit_power_law(graph: nx.Graph, p: float = 0.1, should_plot = False) -> Optional[float]:
    seq = np.array(degree_sequence(graph, p))
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

real_exponents = get_exponents(genetic_graph, ps)

def get_random_backbone(strategy: BackboneStrategy) -> nx.Graph:
    provider = RandomGeneticDataProvider()
    provider.apply_backbone_strategy(strategy)
    return provider.get_graph()

random_backbones = [get_random_backbone(backbone_strategy) for i in range(100)]
random_exponents = [get_exponents(graph, ps) for graph in random_backbones]

mean_exponents = []
for (i, p) in enumerate(ps):
    exps = [e[i] for e in random_exponents if e[i] is not None]
    if len(exps) > 0:
        mean_exponents.append(mean(exps))
    else:
        mean_exponents.append(None)

diff = len(ps) - len(mean_exponents)
other_ps = ps[diff:]

plot.subplot(2, 1, 1)
plot.plot(other_ps, mean_exponents)
plot.plot(ps, real_exponents)
plot.legend(["mean", "real"])
plot.xticks(np.linspace(0, 1, 11))
plot.grid()

plot.subplot(2, 1, 2)
plot.hist([random_exponents[i][50] for i in range(len(random_exponents))], 20)
plot.plot(np.linspace(real_exponents[50], real_exponents[50]), np.linspace(0, 12))
plot.show()
