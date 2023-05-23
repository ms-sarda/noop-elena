import connectors.utils as utils
import connectors.osmnx_connector as ox_cnc

#Test Case 1: Get lat-long for the given address
def test_get_lat_long():
    address = "129 Brittany Manor Drive, Amherst, MA, USA"
    latitude, longitude = ox_cnc.get_lat_long(
            address
        )
    
    assert latitude == 42.349458
    assert longitude == -72.528342

#Test Case 2: Get graph nodes for the given address
def test_get_graph_nodes():
    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = "667 N Pleasant St, Amherst, MA, USA"
    transportation = "walk"

    city_details = utils.parse_location(source)

    city_map = ox_cnc.get_city_map(
            city_details["city"],
            city_details["state"],
            city_details["country"],
            transportation,
        )
    
    source_lat_long = ox_cnc.get_lat_long(source)
    destination_lat_long = ox_cnc.get_lat_long(destination)

    source_node = ox_cnc.get_graph_nodes(
            city_map, source_lat_long[0], source_lat_long[1]
        )
    destination_node = ox_cnc.get_graph_nodes(
            city_map, destination_lat_long[0], destination_lat_long[1]
        )
    print(source_node, destination_node)
    assert source_node == (66634686, 16.471150769569732)
    assert destination_node == (2264382590, 0.7237707786983189)

#Test Case 3: Get city map for the given address
def test_get_city_map():
    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = "667 N Pleasant St, Amherst, MA, USA"
    transportation = "walk"

    city_details = utils.parse_location(source)

    city_map = ox_cnc.get_city_map(
            city_details["city"],
            city_details["state"],
            city_details["country"],
            transportation,
        )
    
    assert city_map.number_of_nodes() == 7400
    assert city_map.number_of_edges() == 20622

#Test Case 4: Generate city map for the given address if not present in cache
def test_generate_city_map():
    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = "149 Brittany Manor Drive, Amherst, MA, USA"
    transportation = "walk"

    city_details = utils.parse_location(source)

    city_map = ox_cnc.generate_city_map(
            city_details["city"],
            city_details["state"],
            city_details["country"],
            transportation,
        )
    
    assert city_map.number_of_nodes() == 7400
    assert city_map.number_of_edges() == 20622

#Test Case 5: Generate city map for the given address if present in cache
def test_generate_city_map_from_cache():
    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = "667 N Pleasant St, Amherst, MA, USA"
    transportation = "walk"

    city_details = utils.parse_location(source)

    city_map = ox_cnc.get_map_from_cache(
            city_details["city"],
            city_details["state"],
            city_details["country"],
            transportation,
        )
    
    assert city_map.number_of_nodes() == 7400
    assert city_map.number_of_edges() == 20622
