import osmnx as ox


def add_elevation_to_graph(graph):
    try:
        G = ox.elevation.add_node_elevations_open_elevation(graph)
        G = ox.elevation.add_edge_grades(G)
        nc = ox.plot.get_node_colors_by_attr(G, "elevation", cmap="plasma")
        fig, ax = ox.plot_graph(
            G, node_color=nc, node_size=20, edge_linewidth=2, edge_color="#333"
        )
        return G
    except ImportError:
        print("You need a google_elevation_api_key to run this cell.")


def add_node_elevations_open_elevation(
    G,
    max_locations_per_batch=350,
    pause_duration=0,
    precision=3,
    url_template="https://api.open-elevation.com/api/v1/lookup?locations={}",
):  # pragma: no cover
    """
    Add `elevation` (meters) attribute to each node using a web service.

    By default, this uses the Google Maps Elevation API but you can optionally
    use an equivalent API with the same interface and response format, such as
    Open Topo Data. The Google Maps Elevation API requires an API key but
    other providers may not.

    For a free local alternative see the `add_node_elevations_raster`
    function. See also the `add_edge_grades` function.

    Parameters
    ----------
    G : networkx.MultiDiGraph
        input graph
    api_key : string
        a valid API key
    max_locations_per_batch : int
        max number of coordinate pairs to submit in each API call (if this is
        too high, the server will reject the request because its character
        limit exceeds the max allowed)
    pause_duration : float
        time to pause between API calls, which can be increased if you get
        rate limited
    precision : int
        decimal precision to round elevation values
    url_template : string
        a URL string template for the API endpoint, containing exactly two
        parameters: `locations` and `key`; for example, for Open Topo Data:
        "https://api.opentopodata.org/v1/aster30m?locations={}&key={}"

    Returns
    -------
    G : networkx.MultiDiGraph
        graph with node elevation attributes
    """
    # make a pandas series of all the nodes' coordinates as 'lat,lng'
    # round coordinates to 5 decimal places (approx 1 meter) to be able to fit
    # in more locations per API call
    node_points = pd.Series(
        {node: f'{data["y"]:.5f},{data["x"]:.5f}' for node, data in G.nodes(data=True)}
    )
    n_calls = int(np.ceil(len(node_points) / max_locations_per_batch))
    utils.log(f"Requesting node elevations from the API in {n_calls} calls")

    # break the series of coordinates into chunks of size max_locations_per_batch
    # API format is locations=lat,lng|lat,lng|lat,lng|lat,lng...
    results = []
    for i in range(0, len(node_points), max_locations_per_batch):
        chunk = node_points.iloc[i : i + max_locations_per_batch]
        locations = "|".join(chunk)
        url = url_template.format(locations, api_key)

        # check if this request is already in the cache (if global use_cache=True)
        cached_response_json = downloader._retrieve_from_cache(url)
        if cached_response_json is not None:
            response_json = cached_response_json
        else:
            # request the elevations from the API
            utils.log(f"Requesting node elevations: {url}")
            time.sleep(pause_duration)
            response = requests.get(url)
            if response.status_code == 200:
                response_json = response.json()
                downloader._save_to_cache(url, response_json, response.status_code)
            else:
                raise Exception(
                    f"Server responded with {response.status_code}: {response.reason} \n{response.json()}"
                )

        # append these elevation results to the list of all results
        results.extend(response_json["results"])

    # sanity check that all our vectors have the same number of elements
    if not (len(results) == len(G) == len(node_points)):
        raise Exception(
            f"Graph has {len(G)} nodes but we received {len(results)} results. \n{response_json}"
        )
    else:
        utils.log(f"Graph has {len(G)} nodes and we received {len(results)} results.")

    # add elevation as an attribute to the nodes
    df = pd.DataFrame(node_points, columns=["node_points"])
    df["elevation"] = [result["elevation"] for result in results]
    df["elevation"] = df["elevation"].round(precision)
    nx.set_node_attributes(G, name="elevation", values=df["elevation"].to_dict())
    utils.log("Added elevation data from API to all nodes.")

    return G
