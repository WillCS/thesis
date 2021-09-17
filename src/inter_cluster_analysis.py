from typing import List, Tuple

import numpy             as np
import networkx          as nx
import matplotlib.pyplot as plt

from backbones import DisparityBackboneStrategy
from data      import get_multiple_clusterings_from_csv, GeneticDataProvider

collapsed = True

collapsed_matrix   = "./resources/plant_genetics/ATvAC_collapsed_contrast6_ATcorr_matrix.csv"
collapsed_clusters = "./resources/plant_genetics/ATvAC_collapsed_contrast6_ATcorr_clusters.csv"

collapsed_data_provider = GeneticDataProvider(collapsed_matrix)
collapsed_clusterings   = get_multiple_clusterings_from_csv(collapsed_clusters,
        vertex_col  = "family",
        cluster_cols = [f"n{n}" for n in range(2,31)]
)

uncollapsed_matrix   = "./resources/plant_genetics/ATvAC_contrast6_ATcorr_matrix.csv"
uncollapsed_families = "./resources/plant_genetics/AT_gene_family_2021-08-04.csv"
uncollapsed_clusters = "./resources/plant_genetics/ATvAC_contrast6_ATcorr_clusters.csv"

uncollapsed_data_provider = GeneticDataProvider(uncollapsed_matrix, uncollapsed_families)
uncollapsed_clusterings   = get_multiple_clusterings_from_csv(uncollapsed_clusters,
        vertex_col  = "gene_num",
        cluster_cols = [f"n{n}" for n in range(2,33)]
)

ps = np.linspace(0, 1, 100)

def get_remaining_edges(graph: nx.Graph, p: float = 0.1, attribute: str = "p") -> List[Tuple]:
    remaining_edges = []

    for (u, v) in graph.edges:
        if graph[u][v][attribute] < p:
            remaining_edges.append((u, v))

    return remaining_edges

# backbone_strategy = PolyaBackboneStrategy(a = 1, integer_weights = True)
backbone_strategy = DisparityBackboneStrategy()

if collapsed:
    backbone    = backbone_strategy.extract_backbone(collapsed_data_provider.get_graph())
    clusterings = {n: c for (n, c) in collapsed_clusterings.items() if int(n[1:]) in [2, 4, 8, 16, 30]}
else:
    backbone    = backbone_strategy.extract_backbone(uncollapsed_data_provider.get_graph())
    clusterings = {n: c for (n, c) in uncollapsed_clusterings.items() if int(n[1:]) in [2, 4, 8, 16, 32]}

inter_counts = {c: [] for c in clusterings.keys()}
intra_counts = {c: [] for c in clusterings.keys()}

for (n, c) in clusterings.items():
    inter_count = []
    intra_count = []

    for p in ps:
        edges = get_remaining_edges(backbone, p)
        total = len(edges)

        if total == 0:
            inter_count.append(None)
            intra_count.append(None)
        else:
            inter = 0
            intra = 0

            for (v, u) in edges:
                if c.co_clustered(v, u):
                    intra += 1
                else:
                    inter += 1

            inter_count.append(inter / total)
            intra_count.append(intra / total)

    inter_counts[n] = inter_count
    intra_counts[n] = intra_count

legend = [n for n in clusterings.keys()]

for series in intra_counts.values():
    plt.plot(ps, series)

plt.title("Fraction of intra-cluster edges in " + ("collapsed" if collapsed else "uncollapsed") + " backbones")
plt.xlabel("p")
plt.ylabel("Fraction of intra-cluster edges")
plt.legend(legend)
plt.xticks(np.linspace(0, 1, 11))
plt.yticks(np.linspace(0, 1, 11))
plt.grid()
plt.show()

