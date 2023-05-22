import logging

import connectors.utils as utils
from model.path_finder import PathFinder


class Orchestrator:
    """
    This class orchestrates the process of computing the new path fulfilling
    the user constraints. It first validates the source and destination and
    then calls the Map Model to generate the required paths.
    """

    def __init__(self):
        self.path_finder = None

    def compute_path(self, source, destination, min_max, transport, deviation):
        """
        Takes the user input and calculates the shortest as well as the
        elevated path with constraints.

        Parameters
        ----------
        source : The source address from which the user want to plot the path. The address must be the street address of the place, in the format Street Address, City, State, Country.
        destination : The destination address to which the user want to plot the path. The address must be in the same format as the source. The destination must also be in the same City as the source.
        deviation : The allowed deviation of the path length from the shortest path. This value is in per cents i.e. a value of 120 means that 120% of the length of the shortest path is allowed for the new path's length
        min_max : "min" or "max" depending on whether we want to minimise or maximise the elevation
        transport : Mode of transport. Values accepted are "bike", "drive" or "walk"

        Returns
        -------
        json : Details of shortest and elevated path - directions, distance,
        elevation, source and destination lat-long
        """
        logging.info("Starting to compute path with constraints")
        try:
            self.validate_input(source, destination, min_max, transport, deviation)
            src_city_details = utils.parse_location(source)
            dest_city_details = utils.parse_location(destination)
            self.validate_src_dest(src_city_details, dest_city_details)
            return self.get_path(source, destination, min_max, transport, deviation)
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, source, destination, min_max, transport, deviation):
        """Validates input values for all the request params.
        Raises an exception if input is incorrect

        Parameters
        ----------
        source : The source address
        destination : The destination address
        deviation : The allowed deviation of the path length from the shortest path
        min_max : "min" or "max"
        transport : Mode of transport - "bike", "drive" or "walk"
        """
        error = "Please enter correct value."
        if source is None or source == "":
            raise ValueError("Source cannot be Null." + error)
        if destination is None or destination == "":
            raise ValueError("Destination cannot be Null." + error)
        if min_max not in ["min", "max"]:
            raise ValueError(
                "Elevation gain can only be maximized or minimized." + error
            )
        if transport not in ["walk", "bike", "drive"]:
            raise ValueError("Transport can be walk, bike or drive." + error)
        if deviation not in range(100, 200):
            raise ValueError("Deviation should lie between 100 and 200." + error)

    def validate_src_dest(self, src, dest):
        """
        Validates if the source and destination lie in the same city.
        Raises an exception if input is incorrect

        Parameters
        ----------
        source : The source address
        destination : The destination address
        """
        if src != dest:
            error = "Source and Destination not in the same city. Cannot generate path"
            print(error)
            raise ValueError(error)
        else:
            return None

    def get_path(self, src, dest, min_max, transport, deviation):
        """
        Calls the Map Model to generate the shortest and elevated path
        between source and destination.

        Parameters
        ----------
        source : The source address
        destination : The destination address
        deviation : The allowed deviation of the path length from the shortest path
        min_max : "min" or "max"
        transport : Mode of transport - "bike", "drive" or "walk"

        Returns
        -------
        json : Details of shortest and elevated path - directions, distance,
        elevation, source and destination lat-long
        """
        self.path_finder = PathFinder(src, dest, transport)
        (
            self.source_lat_long,
            self.destination_lat_long,
            self.shortest_path,
            self.shortest_path_length,
            self.shortest_path_elevation,
            _,
        ) = self.path_finder.get_shortest_path()
        (
            self.elevation_path,
            self.elevation_path_length,
            self.elevation_path_elevation,
            _,
        ) = self.path_finder.get_elevation_path(min_max, deviation)

        return self.get_results()

    def get_results(self):
        """Creates a json consisting of all values required by the UI to plot the graphs
        Returns
        -------
        json : Details of shortest and elevated path - directions, distance,
        elevation, source and destination lat-long
        """
        res = {
            "shortest_path_directions": self.shortest_path,
            "elevation_path_directions": self.elevation_path,
            "source": [
                self.source_lat_long[0],
                self.source_lat_long[1],
            ],
            # TODO is this being used?
            "destination": [
                self.destination_lat_long[0],
                self.destination_lat_long[1],
            ],
            "shortest_path_distance": self.shortest_path_length,
            "elevation_path_distance": self.elevation_path_length,
            "shortest_path_elevation": self.shortest_path_elevation,
            "elevation_path_elevation": self.elevation_path_elevation,
        }
        # Used for debugging and printing graphs while testing
        # osmnx.plot_graph_routes(
        #     self.city_map,
        #     [self.shortest_path_debug, self.elevation_path_debug],
        #     route_colors=["r", "b"],
        # )
        return res
