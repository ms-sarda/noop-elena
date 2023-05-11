""" will start the server -> receive client request -> 
send request details to orchestrator -> get result -> output to UI """
from osmnx import graph, distance
import osmnx
from flask import Flask, request
app = Flask(__name__)


def get_parameters(json):
    return json["source"], json["destination"], json["min_max"], json["deviation"], json["vehicle"]


@app.route("/get_directions", methods=["POST"])
def get_directions():
    source, destination, min_max_route, percent_deviation, vehicle = get_parameters(request.json)
    g = osmnx.graph_from_place("Amherst, MA, USA", vehicle)
    source_gdf = osmnx.geocoder.geocode(source)
    source_node = osmnx.distance.nearest_nodes(g, source_gdf[1], source_gdf[0])

    dest_gdf = osmnx.geocoder.geocode(destination)
    dest_node = osmnx.distance.nearest_nodes(g, dest_gdf[1], dest_gdf[0])

    path = osmnx.shortest_path(g, source_node, dest_node)
    # fig = osmnx.plot.plot_graph_route(g, path)
    coords = []
    for i in path:
        coords.append((g.nodes[i]['y'], g.nodes[i]['x']))

    res = {
        "directions": coords,
        "source": [source_gdf[0], source_gdf[1]],
        "destination": [dest_gdf[0], dest_gdf[1]],
        "distance": 99,
        "elevation": 99
    }

    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
