import logging

from flask import Flask, request
from flask_cors import CORS

from orchestrator import Orchestrator

app = Flask(__name__)
CORS(app)


def get_parameters(json):
    """
    Parses the input JSON for parameters

    Parameters
    ----------
    json : Input json to get_directions

    Returns
    -------
    source : The source address from which the user want to plot the path. The address must be the street address of the place, in the format Street Address, City, State, Country.
    destination : The destination address to which the user want to plot the path. The address must be in the same format as the source. The destination must also be in the same City as the source.
    deviation : The allowed deviation of the path length from the shortest path. This value is in per cents i.e. a value of 120 means that 120% of the length of the shortest path is allowed for the new path's length
    min_max : "min" or "max" depending on whether we want to minimise or maximise the elevation
    transport : Mode of transport. Values accepted are "bike", "drive" or "walk"

    """
    return (
        json["source"],
        json["destination"],
        json["min_max"],
        int(json["deviation"]),
        json["transport"],
    )


@app.route("/get_directions", methods=["POST"])
def get_directions():
    """
    The POST REST API endpoint for the service. The service returns a path that is within a user defined deviation from
    the shortest path, while minimising or maximising the elevation gain along the path. Takes in a JSON as input with
    the following parameters:

    - **source:** The source address from which the user want to plot the path. The address must be the street
    address of the place, in the format Street Address, City, State, Country.

    - **destination:** The destination address to which the user want to plot the path. The address must be in the
    same format as the source. The destination must also be in the same City as the source.

    - **deviation:** The allowed deviation of the path length from the shortest path. This value is in per cents i.e.
    a value of 120 means that 120% of the length of the shortest path is allowed for the new path's length

    - **min_max:** 'min' or 'max' depending on whether we want to minimise or maximise the elevation

    - **transport:** Mode of transport. Values accepted are 'bike', 'drive' or 'walk'

    An example JSON is:

    .. code-block:: json

        {
            "source":"138 Brittany Manor Drive, Amherst, MA, USA",
            "destination": "667 N Pleasant St, Amherst, MA, USA",
            "deviation": 150,
            "min_max": "min",
            "transport": "walk"
        }

    Returns
    -------

    Returns a JSON containing the following information:


    - **shortest_path_directions:** List of Latitudes and Longitudes acting as waypoints for the shortest path

    - **elevation_path_directions:** List of Latitudes and Longitudes acting as waypoints for the new elevated path

    - **source:** Latitude and Longitude of the source in list

    - **destination:** Latitude and Longitude of the destination in list

    - **shortest_path_distance:** Shortest distance between the source and the destination

    - **elevation_path_distance:** Distance between the source and the destination when taking the new elevated path

    - **shortest_path_elevation:** Elevation gain between the source and the destination when taking the shortest path

    - **elevation_path_elevation:** Elevation gain between the source and the destination when taking the new elevated path
    """

    logging.info("0.0.0.0:8000 : POST /get_directions", request.json)
    source, destination, min_max_route, percent_deviation, transport = get_parameters(
        request.json
    )
    orchestrator = Orchestrator()

    return orchestrator.compute_path(
        source, destination, min_max_route, transport, percent_deviation
    )


if __name__ == "__main__":
    logging.info(" Starting server on 0.0.0.0:8080")
    app.run(host="0.0.0.0", port=8000, debug=True)


# FOR DEVELOPMENT AND DEBUGGING ONLY
def get_elevation_path():
    """
    A method for debugging the end to end functionality of the service without deploying the server
    """
    orchestrator = Orchestrator()
    results = orchestrator.compute_path(
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
