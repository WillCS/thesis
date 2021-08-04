from __future__ import annotations
from typing import List, Optional

class Clustering():
    def __init__(self, clusters) -> Clustering:
        self.clusters = clusters
        self.reverse_map = {}
        
        for i, c in enumerate(self.clusters):
            for v in c:
                self.reverse_map[v] = i

    def get_cluster(self, v) -> Optional[int]:
        if v in self.reverse_map.keys():
            return self.reverse_map[v]
        else:
            return None

    def get_vertices(self, c) -> Optional[List]:
        if c < len(self.clusters) and c >= 0:
            return self.clusters[c]
        else:
            return None

    def get_clusters(self) -> List:
        return self.clusters

    def num_clusters(self) -> int:
        return len(self.clusters)
