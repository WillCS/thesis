import networkx as nx

def threshold(G, t: float):
    edges = [(u, v, d["weight"]) for (u, v, d) in G.edges(data = True) if d["weight"] >= t]

    backbone = nx.Graph()
    backbone.add_nodes_from(G)
    backbone.add_weighted_edges_from(edges)

    return backbone