from model.map_model import MapModel
import connectors.misc_utils as misc_utils
import json


def test_get_shortest_path():
    with open("tests_examples/tests.json","r") as f:
        test_case = json.load(f)["get_shortest_path"][0]
    
    source_input = test_case["input"]["source"]
    destination_input = test_case["input"]["destination"]

    parsed_location = misc_utils.parse_location(source_input)
    city = parsed_location["city"]
    state = parsed_location["state"]
    country = parsed_location["country"]
    vehicle = test_case["input"]["vehicle"]


    map_model = MapModel(
            source_input , destination_input, city, state, country, vehicle
        )
    map_model.get_shortest_path()
    assert map_model.shortest_path_length == test_case["output"]["shortest_path_length"]
    assert map_model.shortest_path_elevation == test_case["output"]["shortest_path_elevation"]


def test_get_path():
    
if __name__=="__main__":
    test_get_shortest_path()
