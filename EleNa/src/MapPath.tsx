import GoogleMap from 'react-google-maps/lib/components/GoogleMap';
import './MapPath.css';
import { useEffect, useState } from 'react';

import {
    DirectionsRenderer,
    withGoogleMap
} from "react-google-maps";
import { IServerResponse } from './App';

const MapComponent = withGoogleMap((props: {direction: google.maps.DirectionsResult | undefined}) => 
    <GoogleMap defaultZoom={8} defaultCenter={new google.maps.LatLng(41.8507300, -87.6512600)}>
    {props.direction && (
        <DirectionsRenderer directions={props.direction} />
    ) }
    </GoogleMap>
);
 
function MapPath(props: IServerResponse) {

    const [direction, setDirection] = useState<google.maps.DirectionsResult>();
    const [error, setError] = useState<google.maps.DirectionsResult>();

    useEffect(() => {
        const waypoints = props.waypoints.map(p => ({
            location: new google.maps.LatLng(p[0], p[1]),
            stopover: true
        }));

        if(waypoints.length >= 2) {
            const origin = waypoints.shift()?.location;
            const destination = waypoints.pop()?.location;
        
            const directionService = new google.maps.DirectionsService();
        
            directionService.route(
                {
                    origin: origin!,
                    destination: destination!,
                    travelMode: google.maps.TravelMode.BICYCLING,
                    waypoints: waypoints
                },
                (result: any, status: any) => {
                    if (status == google.maps.DirectionsStatus.OK) {
                        console.log(result);
                        result != null && setDirection(result);
                    } else {
                        console.log(result);
                        result != null && setError(result);
                    }
                }
            );
        }
    }, [props.waypoints]);
  
    if (error) {
        return (<h1>Error occured while loading directions.</h1>);
    }
    return (
        <div className='map-container'>
        <MapComponent 
        direction={direction}
        containerElement={<div style={{ height: `350px` }}/>}
        mapElement={<div style={{height: `100%`}}/>}
        />
        {props.distance > 0 &&<div className='metrics'>
            Distance: {props.distance}
        </div>}
        {props.elevation > 0 && <div  className='metrics'>
            Elevation: {props.elevation}
        </div>}
        </div>
    );
}

export default MapPath;