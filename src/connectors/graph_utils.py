import heapq
import math

import osmnx
from networkx import MultiDiGraph


def get_shortest_path(city_map: MultiDiGraph, source_node, destination_node):
    # TODO Djikstra's implementation
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
            net_elevation = elevation + (elevation_next_node - elevation_curr_node)
            if next_node not in shortest_lengths.keys() or current_cost < shortest_lengths[next_node][0]:
                shortest_lengths[next_node] = (current_cost, curr_node, net_elevation)
                heapq.heappush(unvisitied, (current_cost, net_elevation, next_node))

    shortest_path_length = shortest_lengths[destination_node[0]][0]
    shortest_path, path = build_path(city_map, shortest_lengths, source_node[0], destination_node[0])
    shortest_elevation = shortest_lengths[destination_node[0]][2]
    shortest_path = reduce_path(shortest_path)

    return shortest_path, shortest_path_length, shortest_elevation, path


def get_elevation_path(city_map, source_node, destination_node, min_max, deviation, shortest_path_length, path):
    # TODO implementation to get final deliverable path
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
            net_elevation = elevation + (elevation_next_node - elevation_curr_node)
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

    return shortest_path, shortest_path_length_result, shortest_elevation, shortest_path_debug


def build_path(city_map, node_tree, source_node: int, destination_node: int):
    path = [destination_node]
    curr_node = destination_node
    while True:
        parent_node = node_tree[curr_node][1]
        curr_node = parent_node
        path.append(curr_node)
        if parent_node == source_node:
            break

    path.reverse()

    # osmnx.plot_graph_route(city_map, path)

    # osmnx.plot.plot_graph_route(city_map, path)
    final_path = []
    for i in path:
        final_path.append((city_map.nodes[i]['y'], city_map.nodes[i]['x']))
    return final_path, path


def reduce_path(path):
    # TODO change this implementation
    if len(path) <= 25:
        return path

    new_path = []

    step = math.ceil(len(path) / 23)
    for i in range(0, len(path) - 1, step):
        new_path.append(path[i])

    new_path.append(path[len(path) - 1])
    return new_path
