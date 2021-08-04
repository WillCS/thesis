from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

import networkx as nx

from common import Clustering

@dataclass
class Label():
    text:  str
    pos:   Tuple[float, float]
    angle: float

class LabelStrategy(ABC):
    @abstractmethod
    def generate_labels(self, 
        graph:          nx.Graph,
        node_positions: Dict[Any, Tuple[float, float]],
        edges:          Optional[List]       = None,
        clusters:       Optional[Clustering] = None
    ) -> Dict[Any, Label]:
        pass
