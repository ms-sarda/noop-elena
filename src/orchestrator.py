""" receive client request -> preferably start a thread -> 
validate client request params like locations -> get city map -> 
find shortest path -> find shortest path with constraints -> generate map ->
return details to server """

from connectors.osmnx_connector import get_city_map
from shortest_path_finder import find_shortest_path_dist, find_shortest_path_with_constraints


class Orchestrator:

    def find_path(self, request):
        self.validate_request()
        city = request["source"]["city"]
        state = request["source"]["state"]
        map = get_city_map(city, state)
        # get src and dest lat/long
        src, dest = None, None
        shortest_dist = find_shortest_path_dist(map, src, dest)
        limit = request["limit"]
        elevation_gain = request["elevation_gain"]
        required_path = find_shortest_path_with_constraints(map, src, dest, limit, elevation_gain, shortest_dist)
        return required_path

    def validate_request(self, request):
        # Cannot load graph of state or a country from osmnx as it crashes or takes a long time. 
        # Limiting size to city
        if request["source"]["city"] != request["destination"]["city"]:
            # throw error
            pass
