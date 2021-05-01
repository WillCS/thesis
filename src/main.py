import networkx as nx
from matplotlib import pyplot

from backbones import disparity
from data import (
    get_us_airport_network,
    get_us_airport_locations,
    get_undefined_airports
)

graph = nx.Graph()
graph.add_nodes_from(["a", "b", "c", "d"])
graph.add_edge("a", "b", weight = 14)
graph.add_edge("a", "c", weight = 7)
graph.add_edge("a", "d", weight = 12)
graph.add_edge("b", "d", weight = 10)

# pyplot.figure()
# nx.draw_circular(graph)
# pyplot.show()

get_undefined_airports(2006)

graph = get_us_airport_network(2006)
positions = get_us_airport_locations()
# exit()

backbone = disparity(graph, 0.0005)

# positions = nx.spring_layout(graph)
g_weights = nx.get_edge_attributes(graph,    "weight")
b_weights = nx.get_edge_attributes(backbone, "weight")

weight_list = list(g_weights.values())
max_weight = max(weight_list)
weight_list = [x / max_weight for x in weight_list]

backbone_weight_list = [x / max_weight for x in b_weights.values()]

pyplot.figure(figsize = (1, 2))
pyplot.subplot(1, 2, 1)
nx.draw_networkx(graph, positions, width = weight_list, with_labels = False, node_size = 1)
# nx.draw_networkx_edge_labels(graph, positions, edge_labels = g_weights)
pyplot.subplot(1, 2, 2)
nx.draw_networkx(backbone, positions, width = backbone_weight_list, with_labels = False, node_size = 1)
# nx.draw_networkx_edge_labels(backbone, positions, edge_labels = b_weights)
pyplot.show()
