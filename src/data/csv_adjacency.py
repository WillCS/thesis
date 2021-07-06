import csv

import networkx as nx

def get_graph_from_csv_adjacency_matrix(filename: str, directed: bool = False):
    graph = None
    if directed:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()
        
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        row_index = 0

        for row in reader:
            col_index = 0
            for col in row:
                val = float(col)
                if val != 0:
                    graph.add_edge(row_index, col_index, weight = val)

                col_index += 1
            row_index += 1

    return graph