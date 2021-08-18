from backbones import PolyaBackboneStrategy
from data      import CommunicationsDataProvider
from plot      import PlotBuilder, RadialVisualisation

data_provider     = CommunicationsDataProvider()
backbone_strategy = PolyaBackboneStrategy(a = 1, integer_weights = False)
visualisation     = RadialVisualisation(data_provider, backbone_strategy)
plot_builder      = PlotBuilder(visualisation)

# def update_p_textbox(p_str: str) -> None:
#     p_val = 1

#     try:
#         p_val = float(p_str)
#     except ValueError:
#         pass

#     graph = visualisation.get_graph()

#     corrected_p_val = backbone_strategy.correct_p_value(graph, p_val)

#     edges = [(v, u) for (v, u) in graph.edges if graph[v][u]["p"] < corrected_p_val]
#     visualisation.set_edges_to_display(edges)

#     plot_builder.redraw()

# plot_builder.add_textbox(
#     label     = "p",
#     initial   = "1",
#     update_fn = update_p_textbox,
#     loc       = (0.2, 0.05, 0.2, 0.03)
# )

def update_day_slider(n: float) -> None:
    day = int(n)

    if day < 1:
        day = 1
    elif day > data_provider.get_num_graphs():
        day = data_provider.get_num_graphs()

    data_provider.set_current_graph(day - 1)
    visualisation.set_clusters(None)
    visualisation.set_edges_to_display(None)

    plot_builder.redraw()

plot_builder.add_slider(
    label     = "Day",
    min_val   = 1,
    max_val   = data_provider.get_num_graphs() + 1,
    init_val  = 1,
    update_fn = update_day_slider,
    loc       = (0.6, 0.05, 0.2, 0.03),
    valfmt    = "%i"
)

plot_builder.draw(
    node_size   = 50
)
