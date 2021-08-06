import csv
from typing import Dict, List

from common import Clustering

def get_clusters_from_csv(filename: str, vertex_col: str, cluster_col: str) -> Clustering:
    """
    Load a single clustering from a csv file, where each vertex-cluster association
    is contained in a distinct row.

    The column containing the vertex name is given by vertex_col and the column
    containing its associated cluster is given by cluster_col.
    
    Return a Clustering object.
    """
    clusters = {}
        
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            vertex  = row[vertex_col]
            cluster = row[cluster_col]

            if cluster not in clusters:
                clusters[cluster] = []
            
            clusters[cluster].append(vertex)

    return Clustering(clusters)

def get_multiple_clusterings_from_csv(filename: str, vertex_col: str, cluster_cols: List[str]) -> Dict[str, Clustering]:
    """
    Load a collection of clusterings from a csv file, where each vertex and its associated clusters
    are contained in a distinct row.

    The column containing the vertex name is given by vertex_col, and the columns containing
    the different clusterings are given in the cluster_cols list.

    Return a dict of Clustering objects.
    """
    clusterings = {}
    for cluster_col in cluster_cols:
        clusterings[cluster_col] = get_clusters_from_csv(filename, vertex_col, cluster_col)

    return clusterings
