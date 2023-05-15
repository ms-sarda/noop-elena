""" will start the server -> receive client request -> 
send request details to orchestrator -> get result -> output to UI """
from model.map_model import MapModel
from orchestrator import Orchestrator


def map():
    m = Orchestrator()
    m.compute_path("129 Brittany Manor Drive, Amherst, MA, USA",
                   "667 N Pleasant St, Amherst, MA, USA", "max", "walk", 200)


if __name__ == "__main__":
    map()