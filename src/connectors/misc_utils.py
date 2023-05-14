def parse_location(location:str):
    location_parsed = location.split(",")
    result = {'city': location_parsed[1], 'state': location_parsed[2], 'country': location_parsed[3]}

    return result