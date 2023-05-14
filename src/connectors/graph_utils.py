import heapq

# import osmnx
from networkx import MultiDiGraph


def get_shortest_path(city_map: MultiDiGraph, source_node, destination_node):
    # TODO Djikstra's implementation
    unvisitied = []
    heapq.heappush(unvisitied, (0, source_node[0]))
    shortest_lengths = {source_node[0]: (0, None)}

    while unvisitied:
        distance, curr_node = heapq.heappop(unvisitied)
        for edge in city_map.edges(curr_node, data="length"):
            _, next_node, distance_next_node = edge
            current_cost = distance + distance_next_node
            if next_node not in shortest_lengths.keys() or current_cost < shortest_lengths[next_node][0]:
                shortest_lengths[next_node] = (current_cost, curr_node)
                heapq.heappush(unvisitied, (current_cost, next_node))

    shortest_path_length = shortest_lengths[destination_node[0]][0]
    shortest_path = build_path(city_map, shortest_lengths, source_node[0], destination_node[0])

    return shortest_path, shortest_path_length


def get_elevation_path(city_map, source_lat_long, destination_lat_long, min_max, deviation, shortest_path_length):
    # TODO implementation to get final deliverable path
    return None, None


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
    # osmnx.plot.plot_graph_route(city_map, path)
    final_path = []
    for i in path:
        final_path.append((city_map.nodes[i]['y'], city_map.nodes[i]['x']))
    return final_path
