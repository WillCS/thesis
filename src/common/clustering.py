from __future__ import annotations
from typing import Dict, List, Optional

class Clustering():
    """
    A class for wrapping clusterings of vertices so that
    they can easily be queried / interacted with in
    a variety of ways.
    """

    def __init__(self, clusters: Dict) -> Clustering:
        """
        A dictionary with cluster names as keys and lists of vertices as
        values is needed to initialise the clustering.
        """

        # Map from cluster names to clusters
        self.cluster_map  = clusters
        # List of clusters - i.e. a list of lists
        self.cluster_list = list(clusters.values())
        # Map from vertices to the cluster they are in
        self.reverse_map  = {}
        
        for k, c in self.cluster_map.items():
            for v in c:
                self.reverse_map[v] = k

    def get_cluster_of(self, v) -> Optional[int]:
        """
        Get the cluster a vertex belongs to,
        or None if the vertex is not present
        in the clustering.
        """
        if v in self.reverse_map.keys():
            return self.reverse_map[v]
        else:
            return None

    def co_clustered(self, v, u) -> bool:
        c_v = self.get_cluster_of(v)
        c_u = self.get_cluster_of(u)

        if c_v is not None:
            return c_v == c_u
        else:
            return False

    def get_cluster_named(self, c) -> Optional[int]:
        """
        Get the cluster with the given name,
        or None if there is no cluster with
        that name.
        """
        if c in self.cluster_map.keys():
            return self.cluster_map[c]
        else:
            return None

    def get_cluster_list(self) -> List:
        """
        Get a list of all clusters. That is,
        a list containing lists of vertices,
        each of which is a cluster.
        """
        return self.cluster_list

    def get_num_clusters(self) -> int:
        """
        Get the number of clusters in this clustering.
        """
        return len(self.cluster_list)
