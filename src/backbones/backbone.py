from abc import ABC, abstractmethod

import networkx as nx

class BackboneStrategy(ABC):
    @abstractmethod
    def extract_backbone(self) -> nx.Graph:
        pass