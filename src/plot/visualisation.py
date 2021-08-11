from abc import ABC, abstractmethod
from typing import Any, Optional, List, Tuple, Dict

import networkx as nx
from matplotlib import pyplot as plot

from common import Clustering

class Visualisation(ABC):
    @abstractmethod
    def get_graph(self) -> nx.Graph:
        pass
    
    @abstractmethod
    def set_clusters(self, clusters: Optional[Clustering]) -> None:
        pass
    
    @abstractmethod
    def set_edges_to_display(self, edges: Optional[List]) -> None:
        pass

    @abstractmethod
    def get_edges_to_display(self) -> List:
        pass

    @abstractmethod
    def draw(self, ax: plot.Axes) -> None:
        pass