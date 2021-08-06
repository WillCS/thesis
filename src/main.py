from typing import Callable
import networkx as nx

from backbones import (
    BackboneStrategy,
    DisparityBackboneStrategy
)

from data import (
    get_graph_from_csv_adjacency_matrix,
    get_multiple_clusterings_from_csv
)

from plot.label import LabelStrategy, RadialLabelStrategy
from plot.pos  import PositionStrategy, UndirectedRadialPositionStrategy
from plot import PlotBuilder

graph       = get_graph_from_csv_adjacency_matrix("./resources/plant_genetics/ATvAC_contrast6_ATcorr_matrix.csv", absolute = True)
clusterings = get_multiple_clusterings_from_csv("./resources/plant_genetics/ATvAC_contrast6_ATcorr_clusters.csv",
        vertex_col  = "gene_num",
        cluster_cols = [f"n{n}" for n in range(2,33)]
)

backbone_strategy: BackboneStrategy = DisparityBackboneStrategy(graph)
position_strategy: PositionStrategy = UndirectedRadialPositionStrategy(by_cluster = True, by_strength = True)
label_strategy:    LabelStrategy    = RadialLabelStrategy(1.2)

backbone = backbone_strategy.extract_backbone()

plot_builder: PlotBuilder = PlotBuilder(backbone, position_strategy)

plot_builder.set_node_label_strategy(label_strategy)

def update_p_textbox(p_str: str, graph: nx.Graph, draw_plot: Callable) -> None:
    p_val = 1

    try:
        p_val = float(p_str)
    except ValueError:
        pass

    edges = [(v, u) for (v, u) in graph.edges() if graph[v][u]["p"] < p_val]
    plot_builder.set_edges(edges)
    draw_plot(
        node_size   = 50
    )

plot_builder.add_textbox(
    label     = "p",
    initial   = "1",
    update_fn = update_p_textbox,
    loc       = (0.2, 0.05, 0.2, 0.03)
)

def update_cluster_slider(n: float, graph: nx.Graph, draw_plot: Callable) -> None:
    n_clusters = int(n)
    if n_clusters < 1:
        n_clusters = 1
    elif n_clusters > len(clusterings):
        n_clusters = len(clusterings)

    if n_clusters == 1:
        plot_builder.set_clusters(None)
    else:
        plot_builder.set_clusters(clusterings[f"n{n_clusters}"])

    draw_plot(
        node_size   = 50
    )

plot_builder.add_slider(
    label     = "Clusters",
    min_val   = 1,
    max_val   = len(clusterings) + 1,
    init_val  = 1,
    update_fn = update_cluster_slider,
    loc       = (0.6, 0.05, 0.2, 0.03),
    valfmt    = "%i"
)

# def export_adjacency_matrix(g: nx.Graph, edges, clusters) -> None:
#     graph = nx.Graph()
#     graph.add_nodes_from(g.nodes)
#     for (v, u) in edges:
#         graph.add_edge(v, u, weight = g[v][u]["weight"])
#     write_adjacency_matrix_to_csv(graph, "adjacency_matrix.csv")

# plot_builder.add_button(
#     label = "Export",
#     fn    = export_adjacency_matrix,
#     loc   = (0.45, 0.05, 0.1, 0.03)
# )

plot_builder.draw(
    node_size   = 50
)
