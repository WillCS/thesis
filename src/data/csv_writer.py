import csv
import os

import networkx as nx

def write_adjacency_matrix_to_csv(G, filename: str, attribute: str = "weight"):
    if os.path.isfile(filename):
        raise FileExistsError()
    else:
        with open(filename, "w") as csvfile:
            writer = csv.writer(csvfile)

            for v in G:
                row = []
                for u in G:
                    if u in G[v]:
                        row.append(G[v][u][attribute])
                    else:
                        row.append(0)

                writer.writerow(row)
