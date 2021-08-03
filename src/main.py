from typing import Callable
import networkx as nx

from backbones import (
    BackboneStrategy,
    DisparityBackboneStrategy
)

from plot import PlotBuilder

from data import (
    get_graph_from_csv_adjacency_matrix,
    get_clusterings_from_csv
)
from plot.pos import PositionStrategy, UndirectedRadialPositionStrategy

graph       = get_graph_from_csv_adjacency_matrix("./resources/plant_genetics/ATvAC_contrast6_ATcorr_matrix.csv")
clusterings = get_clusterings_from_csv("./resources/plant_genetics/ATvAC_contrast6_ATcorr_clusters.csv")

backbone_strategy: BackboneStrategy = DisparityBackboneStrategy(graph)
position_strategy: PositionStrategy = UndirectedRadialPositionStrategy(by_cluster = True, by_strength = True)

backbone = backbone_strategy.extract_backbone()

plot_builder: PlotBuilder = PlotBuilder(backbone, position_strategy)

def update_p_textbox(p_str: str, graph: nx.Graph, draw_plot: Callable) -> None:
    p_val = 1

    try:
        p_val = float(p_str)
    except ValueError:
        pass

    edges = [(v, u) for (v, u) in graph.edges() if graph[v][u]["p"] < p_val]
    plot_builder.set_edges(edges)
    draw_plot(
        with_labels = False,
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
        plot_builder.set_clusters([graph.nodes])
    else:
        plot_builder.set_clusters(clusterings[n_clusters])

    draw_plot(
        with_labels = False,
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

plot_builder.draw(
    with_labels = False,
    node_size   = 50
)
