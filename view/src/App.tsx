import './App.css';
import './InputBlock';
import './MapPath'
import MapPath from './MapPath';
import InputBlock from './InputBlock';
import { InputObject } from './InputBlock';
import { useState } from 'react';


export interface IServerResponse {
  destination: number[];
  waypoints: number[][];
  distance: number;
  elevation: number;
  source: number[];
}

function App() {

  const [source, setSource] = useState<number[]>([0,0]);
  const [destination, setDestination] = useState<number[]>([0,0]);
  const [shortestWaypoints, setShortestWaypoints] = useState<number[][]>([[0,0]]);
  const [elevationWaypoints, setElevationWaypoints] = useState<number[][]>([[0,0]]);
  const [shortestDistance, setShortestDistance] = useState(0);
  const [elevationDistance, setElevationDistance] = useState(0);
  const [shortestElevation, setShortestElevation] = useState(0); 
  const [elevationElevation, setElevationElevation] = useState(0); 
  const [error, setError] = useState();

  const onSubmit = async (inputObject: InputObject) => {
    console.log(inputObject);
    const url = "http://localhost:8000";
    console.log(url);
    setError(undefined);
    const result = await fetch(url + '/get_directions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        source: inputObject.source,
        destination: inputObject.destination,
        min_max: inputObject.minMax,
        deviation: inputObject.deviation,
        transport: inputObject.mode
      })
    })
    const temp = await result.json();
    if(temp.error == undefined){
      setSource(temp.source);
      setDestination(temp.destination);
      setShortestWaypoints(temp.shortest_path_directions.slice(0, 24));
      setElevationWaypoints(temp.elevation_path_directions.slice(0, 24));
      setShortestDistance(Math.trunc(temp.shortest_path_distance));
      setShortestElevation(Math.trunc(temp.shortest_path_elevation));
      setElevationDistance(Math.trunc(temp.elevation_path_distance));
      setElevationElevation(Math.trunc(temp.elevation_path_elevation));
    }
    else{
      setError(temp.error)
    }
    
  }

  return (
    <div className="App">
      <link href='https://fonts.googleapis.com/css?family=Montserrat' rel='stylesheet'></link>
      <header className="App-header">
      </header>
      <div className='App-body'>
        <div className="App-bg">
          <div className="logo">
            <div className="logo-main">
              EleNa
            </div>
            <hr />
            <div>
              Elevation Navigation System
            </div>
          </div>
          <div className="inputs">
            <InputBlock onSubmit={onSubmit}/>
          </div>
          {error == undefined && <div>
          <div className='input-header'>
            Shortest Path
          </div>
          
          {shortestDistance >= 0 &&<div className='metrics'>
              Distance: {shortestDistance} m
              </div>}
              {shortestElevation >= 0 && <div  className='metrics'>
                  Elevation: {shortestElevation} m
              </div>}
            <div>
              <MapPath source={source} destination={destination} waypoints={shortestWaypoints} distance={shortestDistance} elevation={shortestElevation}/>
            </div>
            
              <div className='input-header'>
                Elevation Optimized Path
              </div>
              {elevationDistance >= 0 &&<div className='metrics'>
              Distance: {elevationDistance} m
              </div>}
              {elevationElevation >= 0 && <div  className='metrics'>
                  Elevation: {elevationElevation} m
              </div>}
            <div>
              <MapPath source={source} destination={destination} waypoints={elevationWaypoints} distance={elevationDistance} elevation={elevationElevation} />
            </div>
          </div> }
          {
            error != undefined && 
            <div className='error-box'>
                {error}
            </div>
          }
        </div>
      </div>
    </div>
  );
}

export default App;
