from __future__ import annotations
from typing import Any, Tuple, Dict, List, Optional
from math import cos, sin, pi, atan2
from csv import DictReader

import networkx as nx
import pandas   as pd

from backbones import BackboneStrategy
from common import Clustering, strength

from .csv_adjacency import get_graph_from_csv_adjacency_matrix
from .data_provider import DataProvider, Label

DATASET_FILE  = "./resources/us_airport_network_2006.csv"
POSITION_FILE = "./resources/us_airport_locations.csv"

def load_graph() -> nx.Graph:
    network_df = pd.read_csv(DATASET_FILE)
    
    network = nx.Graph()
    
    for _, row in network_df.iterrows():
        origin      = row["origin"]
        destination = row["destination"]
        weight      = row["weight"]

        network.add_edge(origin, destination, weight = weight)

    return network

def load_locations() -> Dict[str, Tuple[float, float]]:
    df = pd.read_csv(POSITION_FILE)

    locations: Dict[str, Tuple[float, float]] = {}

    for i, row in df.iterrows():
        locations[row["iata_code"]] = (row["long"], row["lat"])

    return locations

class USAirportDataProvider(DataProvider):
    def __init__(self) -> USAirportDataProvider:
        self.graph     = load_graph()
        self.positions = load_locations()

    def get_graph(self) -> nx.Graph:
        return self.graph

    def get_vertex_positions(self,
        visible_edges: Optional[List]       = None,
        clustering:    Optional[Clustering] = None,
    ) -> Dict[Any, Tuple(float, float)]:
        return self.positions

    def get_vertex_labels(self,
        visible_edges: Optional[List]       = None,
        clustering:    Optional[Clustering] = None,
    ) -> Dict[Any, Label]:
        labels = {}

        return labels

    def apply_backbone_strategy(self, backbone: BackboneStrategy) -> None:
        backbone.extract_backbone(self.graph)
    