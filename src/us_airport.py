from backbones import DisparityBackboneStrategy
from data      import USAirportDataProvider
from plot      import PlotBuilder, MapVisualisation

data_provider = USAirportDataProvider()

# backbone_strategy = PolyaBackboneStrategy(a = 1, integer_weights = True)
backbone_strategy = DisparityBackboneStrategy()
visualisation     = MapVisualisation(data_provider, backbone_strategy)
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

plot_builder.draw(
    xlim      = (-180,  0),
    ylim      = (   0, 90),
    node_size = 1
)
