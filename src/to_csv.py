from backbones import DisparityBackboneStrategy
from data      import MiscDataProvider, write_adjacency_matrix_to_csv

data_provider     = MiscDataProvider("./resources/sam_example.csv")
backbone_strategy = DisparityBackboneStrategy()

data_provider.apply_backbone_strategy(backbone_strategy)

write_adjacency_matrix_to_csv(data_provider.get_graph(), "adjacency_matrix.csv", attribute = "p")
