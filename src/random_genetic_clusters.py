from backbones import DisparityBackboneStrategy
from data      import get_multiple_clusterings_from_csv, GeneticDataProvider
from plot      import PlotBuilder, RadialVisualisation


sample_num = 17
matrix_filename_base   = f"./resources/plant_genetics/random_2021-09-27/corr_random_{sample_num}.csv"
cluster_filename_base = f"./resources/plant_genetics/random_2021-09-27/random_data_with_clusters_{sample_num}.csv"

data_provider = GeneticDataProvider(matrix_filename_base)
clusterings   = get_multiple_clusterings_from_csv(cluster_filename_base,
        vertex_col  = "id",
        cluster_cols = [f"n{n}" for n in range(2,33)]
)

# backbone_strategy = PolyaBackboneStrategy(a = 1, integer_weights = True)
backbone_strategy = DisparityBackboneStrategy()
visualisation     = RadialVisualisation(data_provider, backbone_strategy)
plot_builder      = PlotBuilder(visualisation)

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

def update_cluster_slider(n: float) -> None:
    n_clusters = int(n)

    if n_clusters < 1:
        n_clusters = 1
    elif n_clusters > len(clusterings):
        n_clusters = len(clusterings)

    if n_clusters == 1:
        visualisation.set_clusters(None)
    else:
        visualisation.set_clusters(clusterings[f"n{n_clusters}"])

    plot_builder.redraw()

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
    node_size   = 50
)