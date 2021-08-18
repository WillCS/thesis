import csv

import networkx as nx

def get_graph_from_csv_edge_list(filename: str, directed: bool = False, absolute = False):
    graph = None
    if directed:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()
        
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if len(row) == 3:
                start = row[0].strip()
                end   = row[1].strip()
                value = int(float(row[2].strip()))

                if absolute:
                    value = abs(value)

                graph.add_edge(start, end, weight = value)
            else:
                break

    return graph