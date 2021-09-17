from backbones import DisparityBackboneStrategy
from data      import get_clusters_from_csv, GeneticDataProvider
from plot      import PlotBuilder, RadialVisualisation

ADJACENCY_MATRIX_FILE = "./resources/plant_genetics/ATvAC_contrast6_ATcorr_matrix.csv"
FAMILY_FILE           = "./resources/plant_genetics/AT_gene_family_2021-08-04.csv"

data_provider = GeneticDataProvider(sourcefile = ADJACENCY_MATRIX_FILE, namefile = FAMILY_FILE)

clusterings   = get_clusters_from_csv("./resources/plant_genetics/AT_gene_family_2021-08-04.csv",
    vertex_col  = "gene_num",
    cluster_col = "cl"
)

# backbone_strategy = PolyaBackboneStrategy(a = 1, integer_weights = True)
backbone_strategy = DisparityBackboneStrategy()
visualisation     = RadialVisualisation(data_provider, backbone_strategy)
plot_builder      = PlotBuilder(visualisation)

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

plot_builder.draw(
    node_size   = 50
)
