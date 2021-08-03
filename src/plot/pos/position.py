from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

import numpy as np
import networkx as nx

class PositionStrategy(ABC):
    @abstractmethod
    def generate_positions(self, 
        graph:    nx.Graph,
        edges:    Optional[List] = None,
        clusters: Optional[List] = None
    ) -> Dict[Any, np.ndarray]:
        pass
