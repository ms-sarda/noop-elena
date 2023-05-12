import connectors.osmnx_connector as ox_cnc


class MapModel:

    def __init__(self, source: str, destination: str, city: str, state: str, country: str, vehicle: str):
        self.city = city
        self.state = state
        self.country = country
        self.vehicle = vehicle
        self.city_map, in_cache = ox_cnc.get_city_map(city, state, country, vehicle)
        if not in_cache:
            ox_cnc.cache_map(self.city_map, city, state, country, vehicle)

    def get_shortest_path(self):
        # TODO : implement get shortest path method
        return

    def get_path(self, min_max: str = "max", deviation: float = 0.0):
        # TODO : implement get path method
        return
