from __future__ import annotations

from .genetic_data_provider import GeneticDataProvider
from .random_genetic_data import create_random_complete_graph

class RandomGeneticDataProvider(GeneticDataProvider):
    def __init__(self) -> RandomGeneticDataProvider:
        self.graph = create_random_complete_graph(71)
        self.names = [v for v in range(71)]
