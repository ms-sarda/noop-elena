import osmnx

import connectors.utils as utils
import connectors.graph_utils as graph_utils
import connectors.osmnx_connector as ox_cnc


# TODO this is not a model - it is in between model and controller. Rename?
# Call it graph and put graph utils here?


class MapModel:
    def __init__(
        self,
        source: str,
        destination: str,
        vehicle: str,
    ):
        self.vehicle = vehicle
        city_details = utils.parse_location(source)
        self.city_map = ox_cnc.get_city_map(
            city_details["city"],
            city_details["state"],
            city_details["country"],
            vehicle,
        )
        self.source_lat_long = ox_cnc.get_lat_long(source)
        self.destination_lat_long = ox_cnc.get_lat_long(destination)

    def get_shortest_path(self):
        source_node = ox_cnc.get_graph_nodes(
            self.city_map, self.source_lat_long[0], self.source_lat_long[1]
        )
        destination_node = ox_cnc.get_graph_nodes(
            self.city_map, self.destination_lat_long[0], self.destination_lat_long[1]
        )
        (
            self.shortest_path,
            self.shortest_path_length,
            self.shortest_path_elevation,
            shortest_path_debug,
        ) = graph_utils.get_shortest_path(self.city_map, source_node, destination_node)
        return (
            self.source_lat_long,
            self.destination_lat_long,
            self.shortest_path,
            self.shortest_path_length,
            self.shortest_path_elevation,
            shortest_path_debug,  # TODO what does this debug do?
        )

    def get_path(self, min_max: str = "max", deviation: float = 0.0):
        source_node = ox_cnc.get_graph_nodes(
            self.city_map, self.source_lat_long[0], self.source_lat_long[1]
        )
        destination_node = ox_cnc.get_graph_nodes(
            self.city_map, self.destination_lat_long[0], self.destination_lat_long[1]
        )
        return graph_utils.get_elevation_path(
            self.city_map,
            source_node,
            destination_node,
            min_max,
            deviation,
            self.shortest_path_length,
            self.shortest_path,
        )

    def store_results(self):
        # TODO
        return
