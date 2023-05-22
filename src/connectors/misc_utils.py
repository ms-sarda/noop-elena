def parse_location(location: str):
    """
    Parses the input location string to fetch City State and Country information

    Parameters
    ----------

    location: The string to be parsed

    Returns
    -------

    result : dictionary
            containing city, state and country

    """
    location_parsed = location.split(",")
    result = {'city': location_parsed[1], 'state': location_parsed[2], 'country': location_parsed[3]}

    return result
