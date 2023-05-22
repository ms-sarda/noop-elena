""" receive client request -> preferably start a thread -> 
validate client request params like locations -> get city map -> 
find shortest path -> find shortest path with constraints -> generate map ->
return details to server """

import connectors.utils as utils
from model.map_model import MapModel


class Orchestrator:
    """
    This class orchestrates the process of computing the new path fulfilling
    the user constraints. It first validates the source and destination and
    then calls the Map Model to generate the required paths.
    """

    def __init__(self):
        self.map_model = None

    def compute_path(self, source, destination, min_max, vehicle, deviation):
        """
        Takes the user input and calculates the shortest as well as the
        elevated path with constraints.
        """
        print("Starting to compute path with constraints")
        src_city_details = utils.parse_location(source)
        dest_city_details = utils.parse_location(destination)
        error = self.validate_src_dest(src_city_details, dest_city_details)
        if error is not None:
            return {"error": error}  # TODO interpret in UI
        # TODO : validate vehicle, deviation, min_max - these are dropdowns right? How can they be wrong?
        return self.get_path(source, destination, min_max, vehicle, deviation)

    def validate_src_dest(self, src, dest):
        """
        Validates if the source and destination lie in the same city.
        """
        if src != dest:
            error = "Source and Destination not in the same city. Cannot generate path"
            print(error)
            return error
        else:
            return None

    def get_path(self, src, dest, min_max, vehicle, deviation):
        """
        Calls the Map Model to generate the shortest and elevated path
        between source and destination.
        """
        self.map_model = MapModel(src, dest, vehicle)
        self.map_model.get_shortest_path()
        self.map_model.get_path(min_max, deviation)
        return self.map_model.get_results()

    # def get_results(self):
    #     res = {
    #         "shortest_path_directions": self.shortest_path,
    #         "elevation_path_directions": self.elevation_path,
    #         "source": [self.source_lat_long[0], self.source_lat_long[1]],
    #         "destination": [self.destination_lat_long[0], self.destination_lat_long[1]],
    #         "shortest_path_distance": self.shortest_path_length,
    #         "elevation_path_distance": self.elevation_path_length,
    #         "shortest_path_elevation": self.shortest_path_elevation,
    #         "elevation_path_elevation": self.elevation_path_elevation,
    #     }
    #     # osmnx.plot_graph_routes(
    #     #     self.city_map,
    #     #     [self.shortest_path_debug, self.elevation_path_debug],
    #     #     route_colors=["r", "b"],
    #     # )
    #     return res
