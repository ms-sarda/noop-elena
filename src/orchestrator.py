import connectors.misc_utils as misc_utils
from model.map_model import MapModel


class Orchestrator:
    def __init__(self):
        self.city = None
        self.state = None
        self.country = None
        self.map_model = None

    def compute_path(self, source, destination, min_max, vehicle, deviation):
        print("Starting to compute path with constraints")
        parsed_location = misc_utils.parse_location(source)
        self.city = parsed_location["city"]
        self.state = parsed_location["state"]
        self.country = parsed_location["country"]

        # TODO : validate source, destination, city, state, country, vehicle, deviation, min_max

        self.map_model = MapModel(
            source, destination, self.city, self.state, self.country, vehicle
        )
        self.map_model.get_shortest_path()
        self.map_model.get_path(min_max, deviation)

        return self.map_model.get_results()
