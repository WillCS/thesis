from typing import List, Tuple
from dataclasses import dataclass

import pandas   as pd
import networkx as nx

def get_starch_grain_dataset(filename: str = "./resources/starch_grains.xlsx") -> pd.DataFrame:
    return pd.read_excel(
        filename
    )

@dataclass
class StarchGrain:
    name:            str
    props:           List[float]
    # scale:           float
    # lamellae:        int
    # fissures:        int
    # flattened_hilum: int
    # faceting:        int
    # pits:            int
    # rough:           int
    # max_length:      float
    # max_angle:       float
    # area:            float
    # perimeter:       float
    # hilum_offset:    float
    # circle_metric:   float
    # c_0:             float
    # c_1:             float
    # c_2:             float
    # c_3:             float
    # c_4:             float
    # c_5:             float
    # c_6:             float
    # c_7:             float
    # c_8:             float
    # c_9:             float
    # c_10:            float
    # hilum_angle:     float
    # hilum_pos:       float
    # phi_1:           float
    # phi_2:           float
    # phi_3:           float
    # phi_4:           float
    # phi_5:           float
    # phi_6:           float
    # phi_7:           float
    # phi_8:           float
    # phi_9:           float
    # phi_10:          float

    def dot(self, other) -> float:
        return sum(a * b for (a, b) in zip(self.props, other.props))

def construct_starch_grain_network(dataset: pd.DataFrame) -> nx.Graph:
    grains: List[Tuple[str, List[float]]] = []

    for index, row in dataset.iterrows():
        name  = row.filename + "-" + str(row.ROI)
        props = [
            row.scale,
            row.Lamellae,
            row.Fissures,
            row["Flattend Hilum"],
            row.Faceting,
            row.Pits,
            row.Rough,
            row.maxlength,
            row.maxangle,
            row.Area,
            row.Perimeter,
            row.HilumOffset,
            row.CircleMetric,
            row.C0,
            row.C1,
            row.C2,
            row.C3,
            row.C4,
            row.C5,
            row.C6,
            row.C7,
            row.C8,
            row.C9,
            row.C10,
            row.HilumAngle,
            row.HilumPos,
            row.phi1,
            row.phi2,
            row.phi3,
            row.phi4,
            row.phi5,
            row.phi6,
            row.phi7,
            row.phi8,
            row.phi9,
            row.phi10
        ]

    grains.append((name, props))