import logging
import os.path

import osmnx as ox

import connectors.elevation_connector as open_cnc


def get_graph_nodes(graph, lat: float, long: float):
    """
    Returns a MultiDiGraph node nearest to input latitude and longitude. Also returns distance between node and
    latitude and longitude

    Parameters
    ----------
    graph : The MultiDiGraph of the city
    lat : Latitude of the location
    long : Longitude of the location

    Returns
    -------

    node : int
           Node id
    distance : float
               distance between latitude and longitude and nearest node

    """
    try:
        node, distance = ox.distance.nearest_nodes(graph, long, lat, return_dist=True)
        return node, distance
    except Exception as e:
        raise Exception("Error getting nearest graph node", e)


def get_lat_long(address: str):
    """
    Get lat-long for the given address

    Parameters
    ----------
    address : str
              Address for which we need lat and long

    Returns
    -------
    tuple
    Latitude and Longitude

    """
    if address is None:
        raise Exception("Address cannot be None")
    try:
        return ox.geocoder.geocode(address)
    except Exception as e:
        raise Exception("Error parsing location into latitude and longitude. Ensure that the location is in a Street "
                        "Address, City, State, Country format", e)


def get_map_from_cache(city, state, country, vehicle):
    """
    Loads a city map if it is already cached

    Parameters
    ----------
    city : City name
    state : State name
    country : Country name
    vehicle : Vehicle name

    Returns
    -------
    g : MultiDiGraph
        Returns map of the city

    """
    try:
        filepath = generate_map_filepath(city, state, country, vehicle)
        if not os.path.isfile(filepath):
            return None
        g = ox.io.load_graphml(filepath=filepath)
        return g
    except Exception as e:
        raise Exception("Error fetching map from cache", e)


def cache_map(G, city: str, state: str, country: str = "USA", vehicle: str = "walk"):
    """
    Cache a newly generated map for efficient perf. The file is saved in graphml format

    Parameters
    ----------
    G : MultiDiGraph
    city : City name
    state : State name
    country : Country name
    vehicle : Vehicle name

    """
    try:
        filepath = generate_map_filepath(city, state, country, vehicle)
        logging.debug("Caching map @ " + str(filepath))
        ox.io.save_graphml(G, filepath=filepath)
    except Exception as e:
        raise Exception("Error caching Map", e)


def generate_city_map(
    city: str, state: str, country: str = "USA", vehicle: str = "walk"
):
    """
    Generates the city map using the OSMnx library

    Parameters
    ----------
    city : City name
    state : State name
    country : Country name
    vehicle : Vehicle name

    Returns
    -------
    G : MultiDiGraph
        Returns map of the city

    """
    # call osmnx lib and generate graph
    try:
        place = {"city": city, "state": state, "country": country}
        logging.debug("Generating city map for " + str(place))
        g = ox.graph_from_place(place, network_type=vehicle, truncate_by_edge=True)
        return g
    except Exception as e:
        raise Exception("Error generating Map", e)


def get_city_map(city: str, state: str, country: str = "USA", vehicle: str = "walk"):
    """
    Returns city map with elevations added from Open-Elevation/Google Maps.
    Loads the map from cache if available. If the map is generated, the new
    map is cached.

    Parameters
    ----------
    city : City name
    state : State name
    country : Country name
    vehicle : Vehicle name

    Returns
    -------
    city_graph : MultiDiGraph
                 Returns map of the city
    """
    city_graph = get_map_from_cache(city, state, country, vehicle)

    if city_graph is None:
        logging.info("Did not find Graph in cache. Generating graph")
        city_graph = generate_city_map(city, state, country, vehicle)
        city_graph = open_cnc.add_elevation_to_graph(city_graph)
        cache_map(city_graph, city, state, country, vehicle)
    else:
        logging.info("Found Graph in cache. Generating graph")
    return city_graph


def generate_map_filepath(
    city: str, state: str, country: str = "USA", vehicle: str = "walk"
):
    """
    Generates the file path at which the generated graph is to be stored

    Parameters
    ----------
    city : City name
    state : State name
    country : Country name
    vehicle : Vehicle name

    Returns
    -------
    str
    filename that will be used to cache and fetch from cache

    """
    return f"./graphs_cache/{city}_{state}_{country}_{vehicle}.graphml"
