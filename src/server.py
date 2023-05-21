from orchestrator import Orchestrator
from flask import Flask, request

app = Flask(__name__)


def get_parameters(json):
    return json["source"], json["destination"], json["min_max"], json["deviation"], json["vehicle"]


@app.route("/get_directions", methods=["POST"])
def get_directions():
    source, destination, min_max_route, percent_deviation, vehicle = get_parameters(request.json)
    orchestrator = Orchestrator()

    return orchestrator.compute_path(source, destination, min_max_route, vehicle, percent_deviation)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


# FOR DEVELOPMENT AND DEBUGGING ONLY
def get_path():
    m = Orchestrator()
    results = m.compute_path(
        "129 Brittany Manor Drive, Amherst, MA, USA",
        "667 N Pleasant St, Amherst, MA, USA",
        "max",
        "walk",
        200,
    )
    print("source: ", results["source"])
    print("destination: ", results["destination"])
    print("shortest_path_distance: ", results["shortest_path_distance"])
    print("elevation_path_distance: ", results["elevation_path_distance"])
    print("shortest_path_elevation: ", results["shortest_path_elevation"])
    print("elevation_path_elevation: ", results["elevation_path_elevation"])
