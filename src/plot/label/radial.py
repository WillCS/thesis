from __future__ import annotations
from typing import Dict, Any, Optional, List, Tuple
import math

import networkx as nx

from common import Clustering
from .label import LabelStrategy, Label

class RadialLabelStrategy(LabelStrategy):
    def __init__(self, factor) -> RadialLabelStrategy:
        self.factor = factor

    def generate_labels(self, 
        graph:          nx.Graph,
        node_positions: Dict[Any, Tuple[float, float]],
        edges:          Optional[List]       = None,
        clusters:       Optional[Clustering] = None
    ) -> Dict[Any, Label]:
        labels = {}

        for i, n in enumerate(graph.nodes):
            text  = f"{n}({clusters.get_cluster_of(n)})"
            x, y  = node_positions[n]
            pos   = (x * self.factor, y * self.factor)
            angle = math.atan2(y, x) * (180 / math.pi)
            labels[n] = Label(text, pos, angle)

        return labels
