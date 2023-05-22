import json
from networkx import MultiDiGraph

from connectors.graph_utils import get_shortest_path

#Unit test for connectors.graph_utils.get_shortest_path
# Test case 1: Simple connected graph with 3 nodes
def test_get_shortest_path():

    
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

    shortest_path, shortest_path_length, shortest_elevation, path = get_shortest_path(city_map, ['A'], ['C'])
    print(shortest_path, shortest_path_length, shortest_elevation, path)
    assert path == ['A', 'B', 'C']
    assert shortest_path_length == 2
    assert shortest_elevation == 1
    assert shortest_path == [(0, 0), (1, 1), (2, 2)]


    
if __name__=="__main__":
    test_get_shortest_path()
