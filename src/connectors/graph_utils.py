import heapq
import math

from networkx import MultiDiGraph


def get_shortest_path(city_map: MultiDiGraph, source_node, destination_node):
    """

    Parameters
    ----------
    city_map : MultiDiGraph

    source_node
    destination_node

    Returns
    -------

    """
    # TODO Djikstra's implementation

    #Check if source and destination nodes are the same
    if source_node == destination_node:
        return [], 0, 0, []
    
    unvisitied = []
    # distance elevation node
    heapq.heappush(unvisitied, (0, 0, source_node[0]))
    shortest_lengths = {source_node[0]: (0, None, 0)}

    while unvisitied:
        distance, elevation, curr_node = heapq.heappop(unvisitied)
        for edge in city_map.edges(curr_node, data="length"):
            _, next_node, distance_next_node = edge
            current_cost = distance + distance_next_node
            elevation_next_node = city_map.nodes[next_node]['elevation']
            elevation_curr_node = city_map.nodes[curr_node]['elevation']
            if (elevation_next_node - elevation_curr_node) > 0:
                net_elevation = elevation + (elevation_next_node - elevation_curr_node)
            else:
                net_elevation = elevation
            if next_node not in shortest_lengths.keys() or current_cost < shortest_lengths[next_node][0]:
                shortest_lengths[next_node] = (current_cost, curr_node, net_elevation)
                heapq.heappush(unvisitied, (current_cost, net_elevation, next_node))

    shortest_path_length = shortest_lengths[destination_node[0]][0]
    # print(shortest_lengths)
    shortest_path, path = build_path(city_map, shortest_lengths, source_node[0], destination_node[0])
    shortest_elevation = shortest_lengths[destination_node[0]][2]
    shortest_path = reduce_path(shortest_path)
    return shortest_path, shortest_path_length, shortest_elevation, path


def get_elevation_path(city_map: MultiDiGraph, source_node, destination_node, min_max: str, deviation: int, shortest_path_length: int):
    """

    Parameters
    ----------
    city_map
    source_node
    destination_node
    min_max
    deviation
    shortest_path_length

    Returns
    -------

    """
    unvisitied = []
    # elevation distance node
    heapq.heappush(unvisitied, (0, 0, source_node[0]))
    shortest_lengths = {source_node[0]: (0, None, 0)}

    while unvisitied:
        elevation, distance, curr_node = heapq.heappop(unvisitied)

        if distance > (deviation * shortest_path_length / 100):
            continue

        if curr_node == destination_node[0]:
            if shortest_lengths[curr_node][0] <= (deviation * shortest_path_length) / 100:
                break

        for edge in city_map.edges(curr_node, data="length"):
            _, next_node, distance_next_node = edge
            elevation_next_node = city_map.nodes[next_node]['elevation']
            elevation_curr_node = city_map.nodes[curr_node]['elevation']
            if (elevation_next_node - elevation_curr_node) > 0:
                if min_max == "max":
                    net_elevation = -1 * elevation + (elevation_next_node - elevation_curr_node)
                else:
                    net_elevation = elevation + (elevation_next_node - elevation_curr_node)
            else:
                if min_max == "max":
                    net_elevation = -1 * elevation
                else:
                    net_elevation = elevation
            current_cost = distance + distance_next_node
            if next_node not in shortest_lengths.keys() or current_cost < shortest_lengths[next_node][0]:
                shortest_lengths[next_node] = (current_cost, curr_node, net_elevation)
                if min_max == "max":
                    heapq.heappush(unvisitied, (-1 * net_elevation, current_cost, next_node))
                else:
                    heapq.heappush(unvisitied, (net_elevation, current_cost, next_node))

    shortest_path_length_result = shortest_lengths[destination_node[0]][0]
    shortest_elevation = shortest_lengths[destination_node[0]][2]
    shortest_path, shortest_path_debug = build_path(city_map, shortest_lengths, source_node[0], destination_node[0])
    shortest_path = reduce_path(shortest_path)
    # osmnx.plot_graph_route(city_map, shortest_path)
    print("Calculated elevation path")
    return shortest_path, shortest_path_length_result, shortest_elevation, shortest_path_debug


def build_path(city_map, node_tree, source_node: int, destination_node: int):
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
        final_path.append((city_map.nodes[i]['y'], city_map.nodes[i]['x']))
    return final_path, path


def reduce_path(path):
    """
    Reduces the path i.e. list of waypoints to 25 or lower waypoints

    Parameters
    ----------
    path : A list of latitudes and longitudes for the waypoints in the path

    Returns
    -------

    new_path : list
               A list with 25 or fewer latitudes and longitudes from the original path
    """
    # TODO change this implementation
    if len(path) <= 25:
        return path

    new_path = []

    step = math.ceil(len(path) / 23)
    for i in range(0, len(path) - 1, step):
        new_path.append(path[i])

    new_path.append(path[len(path) - 1])
    return new_path
