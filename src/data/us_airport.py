from typing import List, Dict, Tuple, Set
from itertools import chain
from os import path

import pandas   as pd
import networkx as nx



def get_us_airport_dataset(year: int) -> pd.DataFrame:
    return pd.read_csv(f"./resources/us_airport_{year}.csv")

def get_us_airport_index(filename: str = "./resources/us_airports.csv") -> pd.DataFrame:
    return pd.read_csv(filename)

def get_us_airport_locations(filename: str = "./resources/us_airport_locations.csv") -> Dict[str, Tuple[float, float]]:
    if path.isfile(filename):
        df = pd.read_csv(filename)

        locations: Dict[str, Tuple[float, float]] = {}

        for i, row in df.iterrows():
            locations[row["iata_code"]] = (row["long"], row["lat"])

        return locations
    else:
        index_df = get_us_airport_index()

        locations: Dict[str, Tuple[float, float]] = {}

        for i, row in index_df.iterrows():
            locations[row["iata_code"]] = (row["longitude_deg"], row["latitude_deg"])

        df_construction = {
            "iata_code": list(locations.keys()),
            "lat":       list(x[1] for x in locations.values()),
            "long":      list(x[0] for x in locations.values())
        }

        new_df = pd.DataFrame(df_construction, columns = ["iata_code", "lat", "long"])

        new_df.to_csv(filename, index = False, header = True)

        return locations

def construct_us_airport_network(dataset: pd.DataFrame, index: pd.DataFrame) -> nx.Graph:
    links:     Dict[Tuple[str, str], int]     = {}
    airports = get_us_airport_locations().keys()
    num_rows = len(dataset)
    print("Generating Airport Network")

    for i, row in dataset.iterrows():
        origin      = row["ORIGIN"]
        destination = row["DEST"]
        passengers  = row["PASSENGERS"]

        if i % 10000 == 0 and i > 0:
            print(f"{i} / {num_rows}")

        if passengers == 0:
            continue

        if not origin in airports or not destination in airports:
            continue

        if (origin, destination) in links.keys():
            links[origin, destination] = links[origin, destination] + passengers
        elif (destination, origin) in links.keys():
            links[destination, origin] = links[destination, origin] + passengers
        else:
            links[origin, destination] = passengers
            
    airports = set(chain(*links.keys()))

    network = nx.Graph()
    network.add_nodes_from(airports)
    
    for ((origin, destination), weight) in links.items():
        network.add_edge(origin, destination, weight = weight)

    return network

def load_us_airport_network(year: int) -> Tuple[nx.Graph, Dict[Tuple[str, str], int]]:
    network_df = pd.read_csv(f"./resources/us_airport_network_{year}.csv")
    
    network = nx.Graph()
    
    for i, row in network_df.iterrows():
        origin      = row["origin"]
        destination = row["destination"]
        weight      = row["weight"]

        network.add_edge(origin, destination, weight = weight)

    return network

def get_us_airport_network(year: int) -> nx.Graph:
    dataset = get_us_airport_dataset(year)
    index   = get_us_airport_index()

    exists = path.isfile(f"./resources/us_airport_network_{year}.csv")

    if exists:
        return load_us_airport_network(year)
    else:
        network = construct_us_airport_network(dataset, index)

        df_construction = {
            "origin":      list(u for u, v, w in network.edges(data = True)),
            "destination": list(v for u, v, w in network.edges(data = True)),
            "weight":      list(w["weight"] for u, v, w in network.edges(data = True))
        }

        new_df = pd.DataFrame(df_construction, columns = ["origin", "destination", "weight"])

        new_df.to_csv(f"./resources/us_airport_network_{year}.csv", index = False, header = True)
        
        return network

def get_undefined_airports(year: int) -> List[str]:
    locations = get_us_airport_locations()
    network   = get_us_airport_network(year)

    print("The following airports have no defined location:")
    for airport in network:
        if not airport in locations.keys():
            print(airport)