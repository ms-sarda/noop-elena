# noop-elena
EleNA - Elevation-based navigation system

To run dummy server
- create a new venv
- install all python dependencies from requirements.txt
- run the server with `python src/server.py`
- use command to fetch: 
  - ```curl --location --request POST '0.0.0.0:8000/get_directions' --header 'Content-Type: application/json' --data-raw '{"source":"138 Brittany Manor Drive, Amherst, MA", "destination": "Amherst Commons, Amherst, MA", "deviation":"100", "min_max":"min", "vehicle": "bike"}'```
