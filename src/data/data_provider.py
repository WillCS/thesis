from abc import ABC, abstractmethod
from dataclasses import dataclass

from typing import Any, Tuple, Dict, List, Optional

import networkx as nx

from common import Clustering

@dataclass
class Label():
    text:  str
    pos:   Tuple[float, float]
    angle: float
    
class DataProvider(ABC):
    @abstractmethod
    def get_graph(self) -> nx.Graph:
        pass

    @abstractmethod
    def get_vertex_positions(self,
        visible_edges: Optional[List]       = None,
        clustering:    Optional[Clustering] = None,
    ) -> Dict[Any, Tuple[float, float]]:
        pass

    @abstractmethod
    def get_vertex_labels(self,
        visible_edges: Optional[List]       = None,
        clustering:    Optional[Clustering] = None,
    ) -> Dict[Any, Label]:
        pass
