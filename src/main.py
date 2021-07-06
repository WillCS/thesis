import sys
import getopt
from typing import Optional

import networkx as nx
from matplotlib import pyplot

from backbones import (
    disparity,
    threshold,
    high_salience_skeleton,
    noise_corrected
)
from common.common import map_graph

from data import (
    get_us_airport_network,
    get_us_airport_locations,
    get_undefined_airports,
    get_graph_from_csv_adjacency_matrix,
    write_adjacency_matrix_to_csv
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

options, args = getopt.getopt(sys.argv[1:], "b:d:s:p:t:v:o:")
options_dict = dict(options)

def get_graph(data_type: str, source: Optional[str] = None):
    if data_type == "us_airport":
        get_undefined_airports(2006)

        graph     = get_us_airport_network(2006)
        positions = get_us_airport_locations()

        return (graph, positions)
    elif data_type == "adj" and source is not None:
        graph     = get_graph_from_csv_adjacency_matrix(source)
        positions = nx.circular_layout(graph)

        return (graph, positions)

if "-b" not in options_dict.keys() or "-d" not in options_dict.keys():
    print("Try again")
else:
    data_source = None
    if "-s" in options_dict:
        data_source = options_dict["-s"]

    p_val = None
    if "-p" in options_dict:
        p_val = float(options_dict["-p"])

    vis_type = "normal"
    if "-v" in options_dict:
        vis_type = options_dict["-v"]

    backbone_type = options_dict["-b"]
    data_type     = options_dict["-d"]

    graph, positions = get_graph(data_type, data_source)

    g_weights   = nx.get_edge_attributes(graph, "weight")
    weight_list = list(g_weights.values())
    max_weight  = max(weight_list)

    display_weight = True
    backbone = None
    title = []
    if "-t" in options_dict:
        title.append(options_dict["-t"])

    if backbone_type == "threshold":
        if p_val is None:
            avg = sum(weight_list) / len(weight_list)
            p_val = 5 * avg

        backbone = threshold(graph, p_val)

        title.append("Threshold Backbone")
        title.append(f"t = {p_val}")
    if backbone_type == "display":
        backbone = graph
    elif backbone_type == "disparity":
        if p_val is None:
            p_val = 0.003

        backbone = disparity(graph, p_val)

        title.append("Disparity Backbone")
        title.append(f"p = {p_val}")
    elif backbone_type == "hss":
        if p_val is None:
            p_val = 0.5
        
        backbone = high_salience_skeleton(graph, p_val)
        display_weight = False

        title.append("High Salience Skeleton")
        title.append(f"t = {p_val}")
    elif backbone_type == "nc":
        if p_val is None:
            p_val = 1.28

        backbone = noise_corrected(graph, p_val)
        display_weight = True

        title.append("Noise Corrected Backbone")
        title.append(f"delta = {p_val}")

    pyplot.title(" - ".join(title))

    if display_weight:
        backbone_weights     = nx.get_edge_attributes(backbone, "weight")
        backbone_weight_list = list(backbone_weights.values())
        max_backbone_weight  = max(backbone_weight_list)

        normalised_backbone_weight_list = [x / max_backbone_weight for x in backbone_weights.values()]

        if vis_type == "invert":
            normalised_backbone_weight_list = [1 - x for x in normalised_backbone_weight_list]

        if vis_type == "spectrum":
            colours = [(x, 0, 1 - x) for x in normalised_backbone_weight_list]
            nx.draw_networkx(backbone, positions, edge_color = colours, with_labels = False, node_size = 1)
        else:
            nx.draw_networkx(backbone, positions, width = normalised_backbone_weight_list, with_labels = False, node_size = 1)
    else:
        nx.draw_networkx(backbone, positions, with_labels = False, node_size = 1)
    pyplot.show()

    if "-o" in options_dict:
        filename = options_dict["-o"]
        write_adjacency_matrix_to_csv(backbone, filename)


# get_undefined_airports(2006)

# graph = get_us_airport_network(2006)
# positions = get_us_airport_locations()
# # exit()

# g_weights = nx.get_edge_attributes(graph,    "weight")

# weight_list = list(g_weights.values())
# avg = sum(weight_list) / len(weight_list)
# max_weight = max(weight_list)

# backbone           = disparity(graph, 0.003)
# threshold_backbone = threshold(graph, 5 * avg)
# hss                = high_salience_skeleton(graph)

# b_weights = nx.get_edge_attributes(backbone,           "weight")
# t_weights = nx.get_edge_attributes(threshold_backbone, "weight")

# weight_list           = [x / max_weight for x in weight_list]
# backbone_weight_list  = [x / max_weight for x in b_weights.values()]
# threshold_weight_list = [x / max_weight for x in t_weights.values()]

# pyplot.figure(figsize = (1, 2))
# pyplot.subplot(1, 2, 1)
# nx.draw_networkx(backbone, positions, width = backbone_weight_list, with_labels = False, node_size = 1)
# # nx.draw_networkx(threshold_backbone, positions, width = threshold_weight_list, with_labels = False, node_size = 1)
# # nx.draw_networkx_edge_labels(graph, positions, edge_labels = g_weights)
# pyplot.subplot(1, 2, 2)
# nx.draw_networkx(hss, positions, with_labels = False, node_size = 1)
# # nx.draw_networkx_edge_labels(backbone, positions, edge_labels = b_weights)
# pyplot.show()
