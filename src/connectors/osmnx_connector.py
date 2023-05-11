# import networkx as nx
import osmnx as ox

# %matplotlib inline
# ox.__version__

# TODO check if needs to be class, depends how handling multithreading

def get_city_map(city, state):
    # check in cache, generate if not
    city_graph = get_map_from_cache(city, state)
    if city_graph is None:
        city_graph = generate_city_map(city, state)
        # cache it
    return city_graph


def get_map_from_cache(city, state):
    return None


def generate_city_map(city, state):
    # call osmnx lib and generate graph
    place = {"city": city, "state": state, "country": "USA"}
    # TODO change to walk
    #print("getting graph")
    G = ox.graph_from_place(place, network_type="bike", truncate_by_edge=True)
    #fig, ax = ox.plot_graph(G, figsize=(10, 10), node_size=0, edge_color="y", edge_linewidth=0.2)
    #print("got graph")
    #print(fig, ax)


generate_city_map("Amherst", "Massachusetts")
