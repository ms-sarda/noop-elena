from networkx import MultiDiGraph

from model.path_finder import PathFinder

def setup_city_map():
    city_map = MultiDiGraph()
    city_map.add_edge('A', 'B', length=1)
    city_map.add_edge('B', 'C', length=1)

    city_map.nodes['A']['y'] = 0
    city_map.nodes['A']['x'] = 0
    city_map.nodes['A']['street_count'] = 1
    city_map.nodes['A']['elevation'] = 0
    
    city_map.nodes['B']['y'] = 1
    city_map.nodes['B']['x'] = 1
    city_map.nodes['B']['street_count'] = 1
    city_map.nodes['B']['elevation'] = 1

    city_map.nodes['C']['y'] = 2
    city_map.nodes['C']['x'] = 2
    city_map.nodes['C']['street_count'] = 1
    city_map.nodes['C']['elevation'] = 0

    return city_map

# Test case 1: Simple traversal
def test_get_shortest_path_simple():
    city_map = setup_city_map()

    source_node = ['A']
    destination_node = ['C']

    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = "79 Brighton Ave, Allston, MA, USA"
    vehicle = "walk"

    path_finder = PathFinder(source, destination, vehicle)
    shortest_path, shortest_path_length, shortest_elevation, path = path_finder.get_shortest_path_using_dijkstra(city_map, source_node, destination_node)

    assert path == ['A', 'B', 'C']
    assert shortest_path_length == 2
    assert shortest_elevation == 1
    assert shortest_path == [(0, 0), (1, 1), (2, 2)]

#Test case 2: Source and destination nodes same
def test_get_shortest_path_same_node():
    city_map = setup_city_map()
    source_node = ['A']
    destination_node = ['A']

    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = "79 Brighton Ave, Allston, MA, USA"
    vehicle = "walk"

    path_finder = PathFinder(source, destination, vehicle)
    shortest_path, shortest_path_length, shortest_elevation, path = path_finder.get_shortest_path_using_dijkstra(city_map, source_node, destination_node)

    assert shortest_path_length == 0
    assert shortest_elevation == 0


