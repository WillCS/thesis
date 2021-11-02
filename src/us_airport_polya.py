from backbones import PolyaBackboneStrategy
from data      import USAirportDataProvider
from plot      import PlotBuilder, MapVisualisation

from matplotlib import pyplot as plt

data_provider = USAirportDataProvider()

backbone_strategy = PolyaBackboneStrategy(a = 1, integer_weights = False)
visualisation     = MapVisualisation(data_provider, backbone_strategy)
plot_builder      = PlotBuilder(visualisation)

edges = [(v, u) for (v, u) in data_provider.graph.edges if data_provider.graph[v][u]["p"] < 0.003]
visualisation.set_edges_to_display(edges)

plot_builder.fig.set_size_inches(12, 8, forward = True)
for side in ["top", "right", "bottom", "left"]:
    plot_builder.ax.spines[side].set_visible(False)

plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
plt.margins(0,0)
plot_builder.draw(
    xlim       = (-180, -64),
    ylim       = (  17,  72),
    node_size  = 1,
)
