from typing import List, Tuple
from statistics import mean

import numpy             as np
import networkx          as nx
import matplotlib.pyplot as plt

from backbones import DisparityBackboneStrategy
from data      import get_multiple_clusterings_from_csv, GeneticDataProvider
from common    import print_progress_bar

def get_remaining_edges(graph: nx.Graph, p: float = 0.1, attribute: str = "p") -> List[Tuple]:
    remaining_edges = []

    for (u, v) in graph.edges:
        if graph[u][v][attribute] < p:
            remaining_edges.append((u, v))

    return remaining_edges

ps = np.linspace(0, 0.5, 100)
intra_counts = {(f"n{c}", i): [] for c in range(2, 33) for i, _ in enumerate(ps)}

for sample_num in range(1, 101):
    print_progress_bar("Sample", sample_num, 100)
    matrix_filename_base   = f"./resources/plant_genetics/random_2021-09-27/corr_random_{sample_num}.csv"
    cluster_filename_base = f"./resources/plant_genetics/random_2021-09-27/random_data_with_clusters_{sample_num}.csv"

    data_provider = GeneticDataProvider(matrix_filename_base)
    clusterings   = get_multiple_clusterings_from_csv(cluster_filename_base,
            vertex_col  = "id",
            cluster_cols = [f"n{n}" for n in range(2,33)]
    )

    backbone_strategy = DisparityBackboneStrategy()

    backbone    = backbone_strategy.extract_backbone(data_provider.get_graph())
    # clusterings = {n: c for (n, c) in clusterings.items() if int(n[1:]) in [2, 4, 8, 16, 32]}

    for (n, c) in clusterings.items():
        for (i, p) in enumerate(ps):
            edges = get_remaining_edges(backbone, p)
            total = len(edges)

            if total != 0:
                intra = 0

                for (v, u) in edges:
                    if c.co_clustered(v, u):
                        intra += 1

                intra_counts[(n, i)].append(intra / total)

series = {c: [] for c in range(2, 33)}

for c in range(2, 33):
    for i, _ in enumerate(ps):
        if len(intra_counts[(f"n{c}", i)]) == 0:
            series[c].append(None)
        else:
            series[c].append(mean(intra_counts[(f"n{c}", i)]))

legend = [n[1:] for n in clusterings.keys()]

fig = plt.figure(figsize = (8, 8))
ax  = plt.subplot(111)

for s in series.values():
    ax.plot(ps, s)

plt.title("Fraction of intra-cluster edges in backbones extracted from random genetic expression data vs $p$-value")
plt.xlabel("$$p$$")
plt.ylabel("Fraction of intra-cluster edges")
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
ax.legend(legend, title = "Clusters", loc = "center left", bbox_to_anchor = (1, 0.5))
plt.xticks(np.linspace(0, 0.5, 11))
plt.yticks(np.linspace(0, 1, 11))
plt.grid()
plt.show()

# plt.savefig("intra_cluster_edges.svg", bbox_inches = "tight")
