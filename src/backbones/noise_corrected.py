import math

import networkx as nx
from networkx.algorithms.smallworld import sigma

from common import outgoing_strength, incoming_strength, strength

def noise_corrected(G, delta: float):
    total_weight = 0

    backbone = G.copy()

    for u, v, a in G.edges(data = True):
        total_weight = total_weight + a["weight"]
        
    for u, v, a in G.edges(data = True):
        weight = a["weight"]

        u_strength = 0
        v_strength = 0

        if nx.is_directed(G):
            u_strength = outgoing_strength(G, u)
            v_strength = incoming_strength(G, v)
        else:
            u_strength = strength(G, u)
            v_strength = strength(G, v)

        expected_weight  = u_strength * (weight / total_weight)
        kappa            = 1 / expected_weight
        weight_deviation = (kappa * weight - 1) / (kappa * weight + 1)
        
        sum_strengths  = u_strength + v_strength
        prod_strengths = u_strength * v_strength

        mu = (1 / total_weight) * (prod_strengths / total_weight)
        sigma_squared = (1 / math.pow(total_weight, 2)) * (prod_strengths * (total_weight - u_strength) * (total_weight - v_strength) / math.pow(total_weight, 2) * (total_weight - 1))

        alpha = (math.pow(mu, 2) / sigma_squared) * (1 - mu) - mu
        beta  = mu * (math.pow(1 - mu, 2) / sigma_squared) - mu

        expected_P = alpha / (alpha + beta)

        if expected_P < 0:
            expected_P = 0

        weight_variance    = total_weight * expected_P * (1 - expected_P)
        d_kappa            = (1 / prod_strengths) - total_weight * (sum_strengths / math.pow(prod_strengths, 2))
        deviation_variance = weight_variance * math.pow((2 * (kappa + weight * d_kappa)) / math.pow(kappa * weight + 1, 2), 2)

        if deviation_variance < 0:
            deviation_variance = 0

        if weight_deviation < delta * math.sqrt(deviation_variance):
            backbone.remove_edge(u, v)
            print(f"Removed edge {(u, v)} with weight {a['weight']}")

    return backbone
            