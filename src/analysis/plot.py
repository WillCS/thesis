from typing import Callable, List, Optional
from statistics import mean, stdev

from matplotlib import pyplot as plot
import networkx as nx
import numpy    as np

from common import print_progress_bar

from .measures import p_values

def plot_graph_property(
    prop:      Callable[[nx.Graph, float], float],
    ps:        List[float],
    backbones: List[nx.Graph],
    name:      str,
    attribute: str = "p",
    legend:    Optional[List[str]] = None
) -> None:
    plot.clf()

    for backbone in backbones:
        plot.plot(ps, [prop(backbone, p, attribute) for p in ps])

    plot.title(f"{name} vs {attribute}")
    if legend:
        plot.legend(legend)

    plot.ylabel(name)
    plot.xlabel(attribute)

    plot.xticks(np.linspace(0, 1, 11))
    plot.grid()

    plot.show()

def plot_p_values(
    backbone:  nx.Graph,
    title:     str,
    attribute: str = "p"
) -> None:
    plot.clf()

    sample = p_values(backbone, attribute)
    plot.hist(sample, bins = 100)

    plot.title(title)

    plot.ylabel("occurrences")
    plot.xlabel(attribute)
    plot.show()

def plot_weights(
    graph:     nx.Graph,
    p:         float = 0.1,
    attribute: str   = "p"
) -> None:
    weights = [ graph[u][v]["weight"] for (u, v) in graph.edges if graph[u][v][attribute] < p]

    plot.hist(weights, 100)
    plot.show()

def plot_means_and_stdevs(xs: np.ndarray, ys: List[List[float]]) -> None:
    averages = []
    std_devs = []

    start_index = 0

    for (i, _) in enumerate(xs):
        samples = [y[i] for y in ys if y[i] is not None]

        if len(samples) > 0:
            average = mean(samples)
        else:
            average = None
            start_index = i + 1
        
        if len(samples) > 1:
            std_dev = stdev(samples, xbar = average)
        else:
            std_dev = 0

        averages.append(average)
        std_devs.append(std_dev)

    averages_np = np.array(averages[start_index:])
    std_devs_np = 3 * np.array(std_devs[start_index:])

    plot_line(xs[start_index:], averages_np, std_devs_np)

def plot_line(xs: np.ndarray, ys: np.ndarray, deltas: Optional[np.ndarray] = None) -> None:
    plot.plot(xs, ys)

    if deltas is not None:
        plot.fill_between(xs, ys + deltas, ys - deltas, alpha = 0.2)

def scatter_seq(xs: np.ndarray, ys: np.ndarray) -> None:
    plot.scatter(xs, ys)
