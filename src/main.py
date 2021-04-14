import networkx as nx
from matplotlib import pyplot

from backbones import disparity

graph = nx.Graph()
graph.add_nodes_from(["a", "b", "c", "d"])
graph.add_edge("a", "b", weight = 14)
graph.add_edge("a", "c", weight = 7)
graph.add_edge("a", "d", weight = 12)
graph.add_edge("b", "d", weight = 10)

# pyplot.figure()
# nx.draw_circular(graph)
# pyplot.show()

backbone = disparity(graph, 0.55)

positions = nx.spring_layout(graph)
g_weights = nx.get_edge_attributes(graph,    "weight")
b_weights = nx.get_edge_attributes(backbone, "weight")

pyplot.figure(figsize = (1, 2))
pyplot.subplot(1, 2, 1)
nx.draw_networkx(graph, positions)
nx.draw_networkx_edge_labels(graph, positions, edge_labels = g_weights)
pyplot.subplot(1, 2, 2)
nx.draw_networkx(backbone, positions)
nx.draw_networkx_edge_labels(backbone, positions, edge_labels = b_weights)
pyplot.show()
