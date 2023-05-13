import connectors.osmnx_connector as ox_cnc
import connectors.graph_utils as g_u


class MapModel:

    def __init__(self, source: str, destination: str, city: str, state: str, country: str, vehicle: str):
        self.city = city
        self.state = state
        self.country = country
        self.vehicle = vehicle
        self.city_map, in_cache = ox_cnc.get_city_map(city, state, country, vehicle)
        if not in_cache:
            ox_cnc.cache_map(self.city_map, city, state, country, vehicle)
        self.shortest_path = []
        self.shortest_path_length = float('inf')
        self.elevation_path = []
        self.elevation_path_length = float('inf')
        self.elevation = 0
        self.source_lat_long = ox_cnc.get_lat_long(source)
        self.destination_lat_long = ox_cnc.get_lat_long(destination)

    def get_shortest_path(self):
        # TODO : implement get shortest path method
        source_node = ox_cnc.get_graph_nodes(self.city_map, self.source_lat_long[0], self.source_lat_long[1])
        destination_node = ox_cnc.get_graph_nodes(self.city_map, self.destination_lat_long[0], self.destination_lat_long[1])
        self.shortest_path, self.shortest_path_length = g_u.get_shortest_path(self.city_map, source_node,
                                                                              destination_node)

    def get_path(self, min_max: str = "max", deviation: float = 0.0):
        # TODO : implement get path method
        self.elevation_path, self.elevation_path_length = g_u.get_elevation_path(self.city_map, self.source_lat_long,
                                                                                 self.destination_lat_long, min_max,
                                                                                 deviation, self.shortest_path_length)

    def get_results(self):
        res = {
            "shortest_path_directions": self.shortest_path,
            "elevation_path_directions": self.elevation_path,
            "source": [self.source_lat_long[0], self.source_lat_long[1]],
            "destination": [self.destination_lat_long[0], self.destination_lat_long[1]],
            "shortest_path_distance": self.shortest_path_length,
            "elevation_path_distance": self.elevation_path_length,
            "elevation": self.elevation
        }

        return res

