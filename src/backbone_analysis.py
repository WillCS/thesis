import numpy    as np
from matplotlib import pyplot as plot

from backbones import HighSalienceSkeletonBackboneStrategy, DisparityBackboneStrategy
from data      import USAirportDataProvider, GeneticDataProvider, RandomGeneticDataProvider, MiscDataProvider
from analysis  import (
    plot_graph_property,
    plot_p_values,
    size,
    order,
    total_strength,
    average_strength,
    average_degree,
    average_edge_weight,
    degree_sequence,
    degree_sequence_exponents,
    plot_means_and_stdevs,
    scatter_seq,
    plot_line
)

data_provider     = GeneticDataProvider()
backbone_strategy = DisparityBackboneStrategy()
backbone          = backbone_strategy.extract_backbone(data_provider.get_graph())

collapsed   = False
n_backbones = 10

if collapsed:
    data_provider = MiscDataProvider("resources/plant_genetics/ATvAC_collapsed_contrast6_ATcorr_matrix.csv",
        vertex_name_row = False,
        directed        = False,
        absolute        = True
    )
    graph_n = 44
else:
    data_provider = GeneticDataProvider()
    graph_n = 71

random_backbones = [backbone_strategy.extract_backbone(RandomGeneticDataProvider(n = graph_n).get_graph()) for _ in range(n_backbones)]
ps = [p for p in np.linspace(0, 1, 100)]

exponents = [degree_sequence_exponents(random_backbone, ps) for random_backbone in random_backbones]

plot_means_and_stdevs(ps, exponents)
plot_line(ps, degree_sequence_exponents(backbone, ps))
# deeg = degree_sequence(backbone, 0.003)
# print(deeg)
# scatter_seq([i + 1 for i in range(len(deeg))], deeg)
plot.show()

# plot_p_values(backbone, "Salience", "salience")
# plot_graph_property(size,                ps, [backbone], "Backbone Size",                attribute = "salience")
# plot_graph_property(order,               ps, [backbone], "Backbone Order",               attribute = "salience")
# plot_graph_property(total_strength,      ps, [backbone], "Backbone Total Strength",      attribute = "salience")
# plot_graph_property(average_strength,    ps, [backbone], "Backbone Average Strength",    attribute = "salience")
# plot_graph_property(average_degree,      ps, [backbone], "Backbone Average Degree",      attribute = "salience") 
# plot_graph_property(average_edge_weight, ps, [backbone], "Backbone Average Edge Weight", attribute = "salience")
