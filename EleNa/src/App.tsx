import './App.css';
import './InputBlock';
import './MapPath'
import MapPath from './MapPath';
import InputBlock from './InputBlock';
import Abc from './MapPath';
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
  const [waypoints, setWaypoints] = useState<number[][]>([[0,0]]);
  const [distance, setDistance] = useState(0);
  const [elevation, setElevation] = useState(0); 

  const onSubmit = async (inputObject: InputObject) => {
    console.log(inputObject);
    const url = process.env.BACKEND_SERVER_URL;
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
        vehicle: inputObject.mode
      })
    })
    const temp = await result.json();
    //let temp: IServerResponse = JSON.parse(res);
    setSource(temp.source);
    setDestination(temp.destination);
    setWaypoints(temp.directions.slice(0, 24));
    setDistance(temp.distance);
    setElevation(temp.elevation);
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
          <div>
            <MapPath source={source} destination={destination} waypoints={waypoints} distance={distance} elevation={elevation} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
