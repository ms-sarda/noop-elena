# import networkx as nx
import os.path

import osmnx as ox
import logging


# %matplotlib inline
# ox.__version__

# TODO check if needs to be class, depends how handling multithreading

class OsmnxConnector:

    def get_graph_nodes(self, graph, lat: float, long: float):
        node, distance = os.distance.nearest_nodes(graph, long, lat, return_dist=True)
        return node, distance

    def get_lat_long(self, address: str):
        if address is None:
            raise Exception("Address cannot be None")
        return ox.geocoder.geocode(address)

    def get_city_map(self, city, state, country, vehicle):
        # check in cache, generate if not
        city_graph = self.get_map_from_cache(city, state, country, vehicle)
        if city_graph is None:
            city_graph = self.generate_city_map(city, state, country, vehicle)
            # cache it
        return city_graph

    def get_map_from_cache(self, city, state, country, vehicle):
        filepath = "./" + city + "_" + state + "_" + country + "_" + vehicle + ".graphml"
        if not os.path.isfile(filepath):
            return None
        g = ox.io.load_graphml(filepath=filepath)
        return g

    def cache_map(self, G, city, state, country, vehicle):
        filepath = "./" + city + "_" + state + "_" + country + "_" + vehicle + ".graphml"
        ox.io.save_graphml(G, filepath=filepath)

    def generate_city_map(self, city: str, state: str, country: str = "USA", vehicle: str = "walk"):
        # call osmnx lib and generate graph
        place = {"city": city, "state": state, "country": country}
        logging.debug("Generating city map for " + str(place))
        G = ox.graph_from_place(place, network_type=vehicle, truncate_by_edge=True)
        self.cache_map(G, city, state, country, vehicle)
        return G
