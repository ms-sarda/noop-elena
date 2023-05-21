""" will start the server -> receive client request -> 
send request details to orchestrator -> get result -> output to UI """
from model.map_model import MapModel
from orchestrator import Orchestrator


def map():
    m = Orchestrator()
    results = m.compute_path(
        "129 Brittany Manor Drive, Amherst, MA, USA",
        "667 N Pleasant St, Amherst, MA, USA",
        "max",
        "walk",
        150,
    )
    print("source: ", results["source"])
    print("destination: ", results["destination"])
    print("shortest_path_distance: ", results["shortest_path_distance"])
    print("elevation_path_distance: ", results["elevation_path_distance"])
    print("shortest_path_elevation: ", results["shortest_path_elevation"])
    print("elevation_path_elevation: ", results["elevation_path_elevation"])


if __name__ == "__main__":
    map()
