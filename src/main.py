from typing import Callable
import networkx as nx

from backbones import (
    BackboneStrategy,
    DisparityBackboneStrategy,
    PolyaBackboneStrategy
)

from data import (
    get_graph_from_csv_adjacency_matrix,
    get_multiple_clusterings_from_csv,
    get_clusters_from_csv,
    get_us_airport_network,
    get_us_airport_locations,
    DataProvider,
    GeneticDataProvider
)

from plot import PlotBuilder, Visualisation, RadialVisualisation

data_provider: DataProvider = GeneticDataProvider()

# clusterings = get_multiple_clusterings_from_csv("./resources/plant_genetics/ATvAC_contrast6_ATcorr_clusters.csv",
#         vertex_col  = "gene_num",
#         cluster_cols = [f"n{n}" for n in range(2,33)]
# )

clusterings = get_clusters_from_csv("./resources/plant_genetics/AT_gene_family_2021-08-04.csv",
    vertex_col  = "gene_num",
    cluster_col = "cl"
)

backbone_strategy: BackboneStrategy = PolyaBackboneStrategy(a = 1, integer_weights = False)
# backbone_strategy: BackboneStrategy = DisparityBackboneStrategy()
visualisation:     Visualisation    = RadialVisualisation(data_provider, backbone_strategy)
plot_builder:      PlotBuilder      = PlotBuilder(visualisation)

visualisation.set_clusters(clusterings)

def update_p_textbox(p_str: str) -> None:
    p_val = 1

    try:
        p_val = float(p_str)
    except ValueError:
        pass

    graph = visualisation.get_graph()

    corrected_p_val = backbone_strategy.correct_p_value(graph, p_val)

    edges = [(v, u) for (v, u) in graph.edges if graph[v][u]["p"] < corrected_p_val]
    visualisation.set_edges_to_display(edges)

    plot_builder.redraw()

plot_builder.add_textbox(
    label     = "p",
    initial   = "1",
    update_fn = update_p_textbox,
    loc       = (0.2, 0.05, 0.2, 0.03)
)

# def update_cluster_slider(n: float) -> None:
#     n_clusters = int(n)

#     if n_clusters < 1:
#         n_clusters = 1
#     elif n_clusters > len(clusterings):
#         n_clusters = len(clusterings)

#     if n_clusters == 1:
#         visualisation.set_clusters(None)
#     else:
#         visualisation.set_clusters(clusterings[f"n{n_clusters}"])

#     plot_builder.redraw()

# plot_builder.add_slider(
#     label     = "Clusters",
#     min_val   = 1,
#     max_val   = len(clusterings) + 1,
#     init_val  = 1,
#     update_fn = update_cluster_slider,
#     loc       = (0.6, 0.05, 0.2, 0.03),
#     valfmt    = "%i"
# )

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
