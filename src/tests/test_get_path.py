from networkx import MultiDiGraph

from connectors.graph_utils import get_shortest_path, get_elevation_path

def setup_city_map():
    city_map = MultiDiGraph()
    city_map.add_edge('A', 'B', length=1)
    city_map.add_edge('B', 'C', length=1)
    city_map.add_edge('C', 'D', length=1)
    city_map.add_edge('A', 'E', length=1)
    city_map.add_edge('E', 'D', length=1)


    city_map.nodes['A']['y'] = 0
    city_map.nodes['A']['x'] = 0
    city_map.nodes['A']['street_count'] = 1
    city_map.nodes['A']['elevation'] = 0
    
    city_map.nodes['B']['y'] = 1
    city_map.nodes['B']['x'] = 1
    city_map.nodes['B']['street_count'] = 1
    city_map.nodes['B']['elevation'] = 0

    city_map.nodes['C']['y'] = 2
    city_map.nodes['C']['x'] = 2
    city_map.nodes['C']['street_count'] = 1
    city_map.nodes['C']['elevation'] = 0

    city_map.nodes['D']['y'] = 3
    city_map.nodes['D']['x'] = 3
    city_map.nodes['D']['street_count'] = 1
    city_map.nodes['D']['elevation'] = 0

    city_map.nodes['E']['y'] = 4
    city_map.nodes['E']['x'] = 4
    city_map.nodes['E']['street_count'] = 1
    city_map.nodes['E']['elevation'] = 0

    return city_map

# Test case 1: Minimize elevation with deviation of 50%
def test_get_path_simple():

    city_map = setup_city_map()
    source_node = ['A']
    destination_node = ['D']

    #Add elevation to E
    city_map.nodes['E']['elevation'] = 1

    #Calculate shortest path
    shortest_path, shortest_path_length, shortest_elevation, path = get_shortest_path(city_map, source_node, destination_node)

    min_max = "min"
    deviation = 150

    deviated_path, deviated_path_length_result, deviated_elevation, deviated_path_debug = get_elevation_path(city_map, source_node, destination_node, min_max, deviation, shortest_path_length, path)

    #The deviated path should be A -> B -> C -> D to minimize elevation
    assert deviated_path_debug == ['A', 'B', 'C', 'D']
    assert deviated_path_length_result == 3
    assert deviated_elevation == 0
    assert deviated_path == [(0, 0), (1, 1), (2, 2), (3, 3)]

# Test case 2: Minimize elevation with deviation of 50% but both paths have equal elevation
def test_get_path_same_elevation():

    city_map = setup_city_map()

    #Add elevation to both B and E
    city_map.nodes['B']['elevation'] = 1
    city_map.nodes['E']['elevation'] = 1

    source_node = ['A']
    destination_node = ['D']

    shortest_path, shortest_path_length, shortest_elevation, path = get_shortest_path(city_map, source_node, destination_node)

    min_max = "min"
    deviation = 150

    deviated_path, deviated_path_length_result, deviated_elevation, deviated_path_debug = get_elevation_path(city_map, source_node, destination_node, min_max, deviation, shortest_path_length, path)
    print(deviated_path, deviated_path_length_result, deviated_elevation, deviated_path_debug)

    #The deviated path should be A -> E -> D to minize distance as the elevation is the same
    assert deviated_path_debug == ['A', 'E', 'D']
    assert deviated_path_length_result == 2
    assert deviated_elevation == 1
    assert deviated_path == [(0, 0), (4,4), (3, 3)]