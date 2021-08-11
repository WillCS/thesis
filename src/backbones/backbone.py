from abc import ABC, abstractmethod

import networkx as nx

class BackboneStrategy(ABC):
    @abstractmethod
    def extract_backbone(self, graph: nx.Graph) -> nx.Graph:
        pass

    @abstractmethod
    def correct_p_value(self, graph: nx.Graph, p: float) -> float:
        pass
