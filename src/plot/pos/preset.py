from __future__ import annotations
from typing import Dict, Any, List, Optional

import numpy as np
import networkx as nx

from .position import PositionStrategy

class PresetPositionStrategy(PositionStrategy):
    def __init__(self, positions: Dict[Any, np.ndarray]) -> PresetPositionStrategy:
        self.positions = positions

    def generate_positions(self, 
        graph:    nx.Graph,
        edges:    Optional[List] = None,
        clusters: Optional[List] = None
    ) -> Dict[Any, np.ndarray]:
        return self.positions
