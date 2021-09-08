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
from data      import GeneticDataProvider, RandomGeneticDataProvider, MiscDataProvider

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

def get_random_backbone(strategy: BackboneStrategy) -> nx.Graph:
    provider = RandomGeneticDataProvider(n = graph_n)
    provider.apply_backbone_strategy(strategy)

    return provider.get_graph()

random_graph  = get_random_backbone(backbone_strategy)

def plot_weights(graph, name: str, p = 0.1):
    weights = [ graph[u][v]["weight"] for (u, v) in graph.edges if graph[u][v]["p"] < p]

    plot.hist(weights, 100)
    plot.title(name)
    plot.xlabel("Correlation")
    plot.ylabel("Occurrences")
    plot.show()

plot_weights(genetic_graph, "Histogram of Absolute Correlations from Real Data", 1.1)
plot_weights(random_graph, "Histogram of Absolute Correlations from Random Data", 1.1)
