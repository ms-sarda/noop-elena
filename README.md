# noop-elena
EleNA - Elevation-based navigation system

## Documentation
Detailed Document containing SRS, Design, Evaluation and Contribution Details: https://docs.google.com/document/d/19qApLdoTNcHBYhysiba59BlV8nbRGzRxK5PwEZXYjbA/edit?usp=sharing
Presentation: https://docs.google.com/presentation/d/1Yb0KgTRrt_tiVHJ69h4NDjUMYyCGweB3jO9whibhh-0/edit?usp=sharing
Usability Survey: https://docs.google.com/spreadsheets/d/1aWlcEIV8ukUC0-ae5YYNeL9y3ft9hFyl8gWcMwCkzRs/edit?usp=sharing
Test Plan: https://docs.google.com/spreadsheets/d/1-uIVOKXPB065MITYvwrBJPdYXD-93CmeMsA9FNBIZv0/edit?usp=sharing

## Problem Statement

Navigation systems optimize for the shortest or fastest route. However, they do not consider elevation gain. Let’s say you are hiking or biking from one location to another. You may want to literally go the extra mile if that saves you a couple thousand feet in elevation gain. Likewise, you may want to maximize elevation gain if you are looking for an intense yet time-constrained workout.
The high-level goal of this project is to develop a software system that determines, given a start and an end location, a route that maximizes or minimizes elevation gain, while limiting the total distance between the two locations to x% of the shortest path.

## Deploying the Service

### Deploying the Server
- Ensure you have python3 installed on your machine.
- Create a new virutal environment and install all dependencies using the following command:
``` pip install requirements.txt```
- In a new command line terminal run the following the command, from the project root:
 ```sh run_server.sh```
- This will block the terminal for port 8000


### Deploying the front end
- Ensure you have node and npm installed on your machine
- In a new command line terminal, navigate to the `view` directory
- Run the following command to install all the node modules:
```npm install```
- Run the following command to start a local frontend server on localhost:3000 -
```npm start```
- Hit `Ctrl+C` to stop this server.

## Using the Application
Once deployed, you should see a form
- In the source and destination section, fill in your desired source and destination.
- As of now, our software only supports addresses that are in a certain format - `Street address, city, state, country`.
- Select "Maximise/Minimise Elevation Gain" radio button
- Select "Mode" of travel
- Finally enter the "Limit to % of Shortest Path". This value is greater than 100 and less than 200
- Hit the "Get Path" button

## Limitations
- As of now, our software only supports addresses that are in a certain format - `Street address, city, state, country`.
- The source and destination need to be in the same city.

## Testing the service

### Run Unit Tests
- We have used Pytest to implement unit testing functions
- From your virtualenv run the following command (make sure to run it from project root) :
`pytest`

### Testing the backend
- Deploy the backend using the commands above
- Using postman or command line, hit the following curl request

command line
` curl --location --request POST '0.0.0.0:8000/get_directions' \
--header 'Content-Type: application/json' \
--data-raw '{"source":"129 Brittany Manor Dr, Amherst, MA, US","destination":"136 Gray St, Amherst, MA, US","min_max":"max","deviation":"125","transport":"bike"}
`


- You should get a response similar to
json
```
{
    "destination": [
        42.38055235,
        -72.51107221798244
    ],
    "elevation_path_directions": [
        [
            42.349435,
            -72.52854
        ],
        [
            42.349854,
            -72.527639
        ],
        [
            42.351557,
            -72.52788
        ],
        [
            42.351411,
            -72.53352
        ],
        [
            42.353229,
            -72.534707
        ],
        [
            42.3575195,
            -72.5326012
        ],
        [
            42.3636782,
            -72.5300508
        ],
        [
            42.366986,
            -72.523823
        ],
        [
            42.370744,
            -72.521171
        ],
        [
            42.3721902,
            -72.5194434
        ],
        [
            42.373214,
            -72.518882
        ],
        [
            42.375481,
            -72.5189908
        ],
        [
            42.3757673,
            -72.5183056
        ],
        [
            42.376334,
            -72.5168376
        ],
        [
            42.377174,
            -72.5142895
        ],
        [
            42.378423,
            -72.513208
        ],
        [
            42.3792388,
            -72.5117238
        ],
        [
            42.379776,
            -72.511614
        ],
        [
            42.3804475,
            -72.5115566
        ]
    ],
    "elevation_path_distance": 5445.0120000000015,
    "elevation_path_elevation": 87.17900000000002,
    "shortest_path_directions": [
        [
            42.349435,
            -72.52854
        ],
        [
            42.349854,
            -72.527639
        ],
        [
            42.351601,
            -72.525857
        ],
        [
            42.354221,
            -72.522022
        ],
        [
            42.3574592,
            -72.5209175
        ],
        [
            42.3581509,
            -72.5208795
        ],
        [
            42.360697,
            -72.520781
        ],
        [
            42.3632958,
            -72.5207438
        ],
        [
            42.3671126,
            -72.5201978
        ],
        [
            42.367305,
            -72.520172
        ],
        [
            42.3704154,
            -72.5198274
        ],
        [
            42.373212,
            -72.519809
        ],
        [
            42.3745986,
            -72.5198341
        ],
        [
            42.3754598,
            -72.5198356
        ],
        [
            42.3757481,
            -72.5185973
        ],
        [
            42.3758214,
            -72.5168714
        ],
        [
            42.3771762,
            -72.5148979
        ],
        [
            42.377692,
            -72.513816
        ],
        [
            42.3792432,
            -72.5129541
        ],
        [
            42.3797087,
            -72.5128175
        ],
        [
            42.3804475,
            -72.5115566
        ]
    ],
    "shortest_path_distance": 4425.169000000001,
    "shortest_path_elevation": 73.094,
    "source": [
        42.349458,
        -72.528342
    ]
}
```

## Shutting Down

### Shutting down the Server
- Run the command `lsof -i TCP:8000`
- For each listed process, kill the process using the command `kill -9 <pid>`
