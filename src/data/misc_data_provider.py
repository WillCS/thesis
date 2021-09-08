from __future__ import annotations
from typing import Any, Tuple, Dict, List, Optional

import networkx as nx

from backbones import BackboneStrategy
from common import Clustering, strength

from .csv_adjacency import get_graph_from_csv_adjacency_matrix
from .data_provider import DataProvider, Label

class MiscDataProvider(DataProvider):
    def __init__(self, adjacency_matrix_file: str, **kwargs) -> MiscDataProvider:
        self.graph = get_graph_from_csv_adjacency_matrix(adjacency_matrix_file, **kwargs)

    def get_graph(self) -> nx.Graph:
        return self.graph

    def get_vertex_positions(self,
        visible_edges: Optional[List]       = None,
        clustering:    Optional[Clustering] = None,
    ) -> Dict[Any, Tuple(float, float)]:
        pass

    def get_vertex_labels(self,
        visible_edges: Optional[List]       = None,
        clustering:    Optional[Clustering] = None,
    ) -> Dict[Any, Label]:
        pass

    def apply_backbone_strategy(self, backbone: BackboneStrategy) -> None:
        backbone.extract_backbone(self.graph)
    