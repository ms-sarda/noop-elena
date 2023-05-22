import logging

logging.basicConfig(level=logging.INFO)


def parse_location(location: str):
    """
    Parses the input location to fetch

    Parameters
    ----------
    location : str
               Street address in the format: Street Address, City, State, Country

    Returns
    -------
    result : dict
             Dictionary with, city, state and country information

    """
    result = {}
    try:
        location_parsed = location.split(",")
        result = {
            "city": location_parsed[1],
            "state": location_parsed[2],
            "country": location_parsed[3],
        }
        return result
    except Exception as e:
        raise Exception("Error : Error parsing location. Ensure that the location is in a Street Address, City, "
                        "State, Country format")
