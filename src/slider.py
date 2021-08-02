import sys
import getopt
from typing import Optional

import networkx as nx
from matplotlib import pyplot
from matplotlib.widgets import Slider

from backbones import (
    disparity
)
from data import (
    get_us_airport_network,
    get_us_airport_locations
)

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

graph = get_us_airport_network(2006)
pos   = get_us_airport_locations()

graph = disparity(graph, 0.003)

weights    = nx.get_edge_attributes(graph, "weight")
max_weight = max(weights.values())
for (v, u) in graph.edges():
    graph[v][u]["normalised_weight"] = graph[v][u]["weight"] / max_weight

ps         = nx.get_edge_attributes(graph, "p")

fig, ax = pyplot.subplots()

slider_ax = pyplot.axes([0.25, 0.05, 0.5, 0.03])

p_slider = Slider(
    label   = "p",
    valmin  = 0,
    valmax  = 0.05,
    valinit = 0.05,
    orientation = "horizontal",
    ax      = slider_ax
)

pyplot.title("Disparity Backbone US Air travel 2006")

def update_plot(val):
    ax.clear()
    edges = [(v, u) for (v, u) in graph.edges() if graph[v][u]["p"] < val]
    widths = list([graph[v][u]["normalised_weight"] for (v, u) in edges])

    nx.draw_networkx(graph, pos,
        width       = widths,
        with_labels = False,
        node_size   = 1,
        ax          = ax,
        edgelist    = edges
    )

p_slider.on_changed(update_plot)

update_plot(0.05)

pyplot.show()
