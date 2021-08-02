import sys
import getopt
from typing import Optional

import numpy as np
import networkx as nx
from matplotlib import pyplot
from matplotlib.widgets import Slider
from matplotlib.colors import Colormap

from backbones import (
    disparity
)
from data import (
    get_us_airport_network,
    get_us_airport_locations
)
from data.csv_adjacency import get_graph_from_csv_adjacency_matrix
from data.csv_clustering import get_clusterings_from_csv

# pyplot.figure()
# nx.draw_circular(graph)
# pyplot.show()

# Options:
# p - threshold / significance value
# b - backbone type
# d - data type
# s - data source
# t - title
# v - visualisation type
# o - output filename
# z - slider

n_clusters = 2

graph       = get_graph_from_csv_adjacency_matrix("./resources/plant_genetics/ATvAC_contrast6_ATcorr_matrix.csv")
pos         = nx.circular_layout(graph)
clusterings = get_clusterings_from_csv("./resources/plant_genetics/ATvAC_contrast6_ATcorr_clusters.csv")

graph = disparity(graph, 0.0000005)

weights    = nx.get_edge_attributes(graph, "weight")
max_weight = max(weights.values())
for (v, u) in graph.edges():
    graph[v][u]["normalised_weight"] = graph[v][u]["weight"] / max_weight

ps         = nx.get_edge_attributes(graph, "p")

fig, ax = pyplot.subplots()

slider_ax = pyplot.axes([0.25, 0.05, 0.5, 0.03])

colormap = pyplot.get_cmap("gist_rainbow")

colours = [colormap(i) for i in np.linspace(0, 0.9, n_clusters)]

node_colours = []
for node in range(graph.order()):
    for c in range(len(clusterings[n_clusters])):
        if node in clusterings[n_clusters][c]:
            node_colours.append(colours[c])
            break

p_slider = Slider(
    label   = "p",
    valmin  = 0,
    valmax  = 0.0000005,
    valinit = 0.0000005,
    orientation = "horizontal",
    ax      = slider_ax
)

# pyplot.title("")

def update_plot(val):
    ax.clear()
    edges = [(v, u) for (v, u) in graph.edges() if graph[v][u]["p"] < val]
    m = max([graph[v][u]["weight"] for (v, u) in edges])
    widths = list([graph[v][u]["weight"] / m for (v, u) in edges])

    nx.draw_networkx(graph, pos,
        width       = widths,
        with_labels = False,
        node_size   = 50,
        ax          = ax,
        edgelist    = edges,
        node_color  = node_colours
    )

p_slider.on_changed(update_plot)

update_plot(0.0000005)

pyplot.show()
