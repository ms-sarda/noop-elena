from orchestrator import Orchestrator
import connectors.utils as utils

#Test Case 1: When source and destination are in different cities throw error
def test_orchestrator_validate_same_city():
    orchestrator = Orchestrator()

    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = "79 Brighton Ave, Allston, MA, USA"
    min_max = "max"
    deviation = 150
    transportation = "walk"

    results = orchestrator.compute_path(source, destination, min_max, transportation, deviation)
    assert results["error"] == "Source and Destination not in the same city. Cannot generate path"

#Test Case 2: When input source is null, the code should throw an error
def test_orchestrator_validate_source_input():
    orchestrator = Orchestrator()

    source = None
    destination = "79 Brighton Ave, Allston, MA, USA"
    min_max = "max"
    deviation = 150
    transportation = "walk"

    results = orchestrator.compute_path(source, destination, min_max, transportation, deviation)
    assert results["error"] == "Source cannot be Null.Please enter correct value."

#Test Case 3: When input destination is null, the code should throw an error
def test_orchestrator_validate_destination_input():
    orchestrator = Orchestrator()

    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = None
    min_max = "max"
    deviation = 150
    transportation = "walk"

    results = orchestrator.compute_path(source, destination, min_max, transportation, deviation)
    assert results["error"] == "Destination cannot be Null.Please enter correct value."

#Test Case 4: When min_max input is invalid, the code should throw an error
def test_orchestrator_validate_minmax_input():
    orchestrator = Orchestrator()

    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = "79 Brighton Ave, Allston, MA, USA"
    min_max = "invalid"
    deviation = 150
    transportation = "walk"

    results = orchestrator.compute_path(source, destination, min_max, transportation, deviation)
    assert results["error"] == "Elevation gain can only be maximized or minimized.Please enter correct value."


#Test Case 5: When transportation input is invalid, the code should throw an error
def test_orchestrator_validate_transportation_input():
    orchestrator = Orchestrator()

    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = "79 Brighton Ave, Allston, MA, USA"
    min_max = "min"
    deviation = 150
    transportation = "invalid"

    results = orchestrator.compute_path(source, destination, min_max, transportation, deviation)
    assert results["error"] == "Transport can be walk, bike or drive.Please enter correct value."

#Test Case 6: When deviation input is invalid, the code should throw an error
def test_orchestrator_validate_deviation_input():
    orchestrator = Orchestrator()

    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = "79 Brighton Ave, Allston, MA, USA"
    min_max = "min"
    deviation = 300
    transportation = "walk"

    results = orchestrator.compute_path(source, destination, min_max, transportation, deviation)
    assert results["error"] == "Deviation should lie between 100 and 200.Please enter correct value."

#Test Case 7: End to End test of the compute path
def test_orchestrator_compute_path():
    orchestrator = Orchestrator()

    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = "667 N Pleasant St, Amherst, MA, USA"
    min_max = "min"
    deviation = 150
    transportation = "walk"

    results = orchestrator.compute_path(source, destination, min_max, transportation, deviation)
    print(results)
    assert results["source"] == [42.349458, -72.528342]
    assert results["destination"] == [42.3937079566189, -72.5259946134036]
    assert results["shortest_path_distance"] == 5437.999
    assert results["elevation_path_distance"] == 6195.504000000001
    assert results["shortest_path_elevation"] == 62.82799999999997
    assert results["elevation_path_elevation"] == 52.99600000000001

