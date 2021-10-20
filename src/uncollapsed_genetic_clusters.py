from backbones import DisparityBackboneStrategy
from data      import get_multiple_clusterings_from_csv, GeneticDataProvider
from plot      import PlotBuilder, RadialVisualisation

from matplotlib import pyplot as plt

ADJACENCY_MATRIX_FILE = "./resources/plant_genetics/ATvAC_contrast6_ATcorr_matrix.csv"
FAMILY_FILE           = "./resources/plant_genetics/AT_gene_family_2021-08-04.csv"

data_provider = GeneticDataProvider(sourcefile = ADJACENCY_MATRIX_FILE, namefile = FAMILY_FILE)

clusterings   = get_multiple_clusterings_from_csv("./resources/plant_genetics/ATvAC_contrast6_ATcorr_clusters.csv",
        vertex_col  = "gene_num",
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

# edges = [(v, u) for (v, u) in data_provider.graph.edges if data_provider.graph[v][u]["p"] < 0.15]
# visualisation.set_edges_to_display(edges)
# visualisation.set_clusters(clusterings[f"n32"])

# plot_builder.fig.set_size_inches(12, 12, forward = True)
# for side in ["top", "right", "bottom", "left"]:
#     plot_builder.ax.spines[side].set_visible(False)

# plt.gca().set_axis_off()
# plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
# plt.margins(0,0)

plot_builder.draw(
    node_size   = 200,
    xlim        = (-1.1, 1.1),
    ylim        = (-1.1, 1.1)
)
