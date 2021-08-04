from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

import numpy as np
import networkx as nx

from common import Clustering

class PositionStrategy(ABC):
    @abstractmethod
    def generate_positions(self, 
        graph:    nx.Graph,
        edges:    Optional[List]       = None,
        clusters: Optional[Clustering] = None
    ) -> Dict[Any, np.ndarray]:
        pass
