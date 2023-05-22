from orchestrator import Orchestrator
import connectors.utils as utils

#Test Case 1: When source and destination are in different cities throw error
def test_orchestrator_validate_same_city():
    orchestrator = Orchestrator()

    source = "129 Brittany Manor Drive, Amherst, MA, USA"
    destination = "79 Brighton Ave, Allston, MA, USA"
    min_max = "max"
    deviation = 150
    vehicle = "walk"

    src_city = utils.parse_location(source)
    dest_city = utils.parse_location(destination)

    results = orchestrator.compute_path(source, destination, min_max, vehicle, deviation)
    print(results)
    assert results["error"] == "Source and Destination not in the same city. Cannot generate path"
