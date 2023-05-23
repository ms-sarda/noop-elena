import heapq
import logging
import math

from networkx import MultiDiGraph

import connectors.osmnx_connector as ox_cnc
import connectors.utils as utils


class PathFinder:
    """Class to generate the shortest and elevated paht based on user constraints"""

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
        ) = self.get_shortest_path_using_dijkstra(
            self.city_map, source_node, destination_node
        )
        return (
            self.source_lat_long,
            self.destination_lat_long,
            self.shortest_path,
            self.shortest_path_length,
            self.shortest_path_elevation,
            shortest_path_debug,
        )

    def get_elevation_path(self, min_max: str = "max", deviation: float = 0.0):
        source_node = ox_cnc.get_graph_nodes(
            self.city_map, self.source_lat_long[0], self.source_lat_long[1]
        )
        destination_node = ox_cnc.get_graph_nodes(
            self.city_map, self.destination_lat_long[0], self.destination_lat_long[1]
        )
        return self.get_elevation_path_using_modified_dijkstra(
            self.city_map,
            source_node,
            destination_node,
            min_max,
            deviation,
            self.shortest_path_length,
        )

    def get_shortest_path_using_dijkstra(
        self, city_map: MultiDiGraph, source_node, destination_node
    ):
        """
        Gets the shortest path between src and dest nodes using Dijkstra.

        Parameters
        ----------
        city_map : MultiDiGraph
        source_node
        destination_node

        Returns
        -------
        shortest_path: shortest path of all nodes with lat-long info
        shortest_path_length: distance of the shortest path
        shortest_elevation: elevation of the shortest path
        path: shortest path of all nodes with node-id info
        """
        # Check if source and destination nodes are the same
        if source_node == destination_node:
            return [], 0, 0, []

        unvisited = []
        # distance elevation node
        heapq.heappush(unvisited, (0, 0, source_node[0]))
        shortest_lengths = {source_node[0]: (0, None, 0)}

        while unvisited:
            distance, elevation, curr_node = heapq.heappop(unvisited)
            for edge in city_map.edges(curr_node, data="length"):
                _, next_node, distance_next_node = edge
                current_cost = distance + distance_next_node
                elevation_next_node = city_map.nodes[next_node]["elevation"]
                elevation_curr_node = city_map.nodes[curr_node]["elevation"]
                if (elevation_next_node - elevation_curr_node) > 0:
                    net_elevation = elevation + (
                        elevation_next_node - elevation_curr_node
                    )
                else:
                    net_elevation = elevation
                if (
                    next_node not in shortest_lengths.keys()
                    or current_cost < shortest_lengths[next_node][0]
                ):
                    shortest_lengths[next_node] = (
                        current_cost,
                        curr_node,
                        net_elevation,
                    )
                    heapq.heappush(unvisited, (current_cost, net_elevation, next_node))

        shortest_path_length = shortest_lengths[destination_node[0]][0]
        # print(shortest_lengths)
        shortest_path, path = self.build_path(
            city_map, shortest_lengths, source_node[0], destination_node[0]
        )
        shortest_elevation = shortest_lengths[destination_node[0]][2]
        shortest_path = self.reduce_path(shortest_path)
        return shortest_path, shortest_path_length, shortest_elevation, path

    def get_elevation_path_using_modified_dijkstra(
        self,
        city_map: MultiDiGraph,
        source_node,
        destination_node,
        min_max: str,
        deviation: int,
        shortest_path_length: int,
    ):
        """
        Gets the shortest path between src and dest nodes using modified Dijkstra
        satisying user constraints of elevation gain and deviation.

        Parameters
        ----------
        city_map : MultiDiGraph
        source_node
        destination_node
        min_max: Elevation gain to be minimized or maximized
        deviation: The allowed deviation of the path length from the shortest path
        shortest_path_length: shortest path length computed using Dijkstra

        Returns
        -------
        shortest_path: shortest path of all nodes with lat-long info
        shortest_path_length: distance of the shortest path
        shortest_elevation: elevation of the shortest path
        shortest_path_debug: shortest path of all nodes with node-id info
        """
        unvisited = []
        # elevation distance node
        heapq.heappush(unvisited, (0, 0, source_node[0]))
        shortest_lengths = {source_node[0]: (0, None, 0)}

        while unvisited:
            elevation, distance, curr_node = heapq.heappop(unvisited)

            if distance > (deviation * shortest_path_length / 100):
                continue

            if curr_node == destination_node[0]:
                if (
                    shortest_lengths[curr_node][0]
                    <= (deviation * shortest_path_length) / 100
                ):
                    break

            for edge in city_map.edges(curr_node, data="length"):
                _, next_node, distance_next_node = edge
                elevation_next_node = city_map.nodes[next_node]["elevation"]
                elevation_curr_node = city_map.nodes[curr_node]["elevation"]
                if (elevation_next_node - elevation_curr_node) > 0:
                    if min_max == "max":
                        net_elevation = -1 * elevation + (
                            elevation_next_node - elevation_curr_node
                        )
                    else:
                        net_elevation = elevation + (
                            elevation_next_node - elevation_curr_node
                        )
                else:
                    if min_max == "max":
                        net_elevation = -1 * elevation
                    else:
                        net_elevation = elevation
                current_cost = distance + distance_next_node
                if (
                    next_node not in shortest_lengths.keys()
                    or current_cost < shortest_lengths[next_node][0]
                ):
                    shortest_lengths[next_node] = (
                        current_cost,
                        curr_node,
                        net_elevation,
                    )
                    if min_max == "max":
                        heapq.heappush(
                            unvisited, (-1 * net_elevation, current_cost, next_node)
                        )
                    else:
                        heapq.heappush(
                            unvisited, (net_elevation, current_cost, next_node)
                        )

        shortest_path_length_result = shortest_lengths[destination_node[0]][0]
        shortest_elevation = shortest_lengths[destination_node[0]][2]
        shortest_path, shortest_path_debug = self.build_path(
            city_map, shortest_lengths, source_node[0], destination_node[0]
        )
        shortest_path = self.reduce_path(shortest_path)
        # osmnx.plot_graph_route(city_map, shortest_path)
        logging.info("Calculated elevation path")
        return (
            shortest_path,
            shortest_path_length_result,
            shortest_elevation,
            shortest_path_debug,
        )

    def build_path(self, city_map, node_tree, source_node: int, destination_node: int):
        """
        Traverses the inverted tree to build a list that includes the path from the destination to the source node.
        Then reverses the list and parses the latitude and longitude for each node in the path

        Parameters
        ----------
        city_map : OSMNX graph for the city
        node_tree : Inverted tree with a node pointing to its parent node and the distance between them
        source_node : Source node from which the path starts
        destination_node : Destination node where the path ends

        Returns
        -------
        final_path : list
                    List of Latitudes and Longitudes acting as waypoints
        path : list
            List of OpenStreetMap Node IDs acting as waypoints
        """
        path = [destination_node]
        curr_node = destination_node
        while True:
            parent_node = node_tree[curr_node][1]
            curr_node = parent_node
            path.append(curr_node)
            if parent_node == source_node:
                break

        path.reverse()

        final_path = []
        for i in path:
            final_path.append((city_map.nodes[i]["y"], city_map.nodes[i]["x"]))
        return final_path, path

    def reduce_path(self, path):
        """
        Reduces the path i.e. list of waypoints to 25 or lower waypoints as
        Google only allows using of 25 points to plot the map.

        Parameters
        ----------
        path : A list of latitudes and longitudes for the waypoints in the path

        Returns
        -------
        new_path : list
                A list with 25 or fewer latitudes and longitudes from the original path
        """
        num_nodes = len(path)
        if num_nodes <= 25:
            return path
        new_path = []
        # 23 because 1st and last node need to be added as src and dest
        step = math.ceil(num_nodes / 23)
        for i in range(0, len(path) - 1, step):
            new_path.append(path[i])
        # append the dest node
        new_path.append(path[num_nodes - 1])
        return new_path
