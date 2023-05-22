import './InputBlock.css';


import { useEffect, useRef, useState } from 'react';
import { usePlacesWidget, } from 'react-google-autocomplete';

export interface InputObject {
  source: String;
  destination: String;
  minMax: String;
  deviation: number;
  mode: String;
}

export interface IInputBlockProps{
  onSubmit: (inputObject: InputObject) => void
};

export interface Address{
  StreetNumber: String;
  StreetName: String;
  City: String;
  State: String;
  Zip: String;
  Country: String;
}

function InputBlock(props: IInputBlockProps) {
  const sourceAutocompleteRef = useRef<google.maps.places.Autocomplete>();
  const sourceInputRef = useRef<HTMLInputElement>(null);
  const destAutocompleteRef = useRef<google.maps.places.Autocomplete>();
  const destInputRef = useRef<HTMLInputElement>(null);
  const options = {
    fields: ["address_components", "geometry", "icon", "name"], // reference for fields: https://developers.google.com/maps/documentation/places/web-service/place-data-fields#places-api-fields-support
   };

  const [source, setSource] = useState("Amherst");
  const [destination, setDestination] = useState("");
  const [minMax, setMinMax] = useState("");
  const [deviation, setDeviation] = useState(100);
  const [mode, setMode] = useState("bike"); 

  const formatAddress = (place: google.maps.places.PlaceResult) => {
    const address = {} as Address;
    var formattedAddress = "";
    place.address_components?.forEach(function(c) {
      switch(c.types[0]){
          case 'street_number':
              address.StreetNumber = c.short_name;
              break;
          case 'route':
              address.StreetName = c.short_name;
              break;
          case 'neighborhood': case 'locality':    // North Hollywood or Los Angeles?
              address.City = c.short_name;
              break;
          case 'administrative_area_level_1':     //  Note some countries don't have states
              address.State = c.short_name;
              break;
          case 'postal_code':
              address.Zip = c.short_name;
              break;
          case 'country':
              address.Country = c.short_name;
              break;
      }
      
  });

  if(address.StreetNumber != undefined){
    formattedAddress = address.StreetNumber + ", ";
  }
  if(address.StreetName != undefined){
    formattedAddress += address.StreetName + ", ";
  }
  if(address.City != undefined){
    formattedAddress += address.City + ", ";
  }
  if(address.State != undefined){
    formattedAddress += address.State + ", ";
  }
  if(address.Zip != undefined){
    formattedAddress += address.Zip + ", ";
  }
  if(address.Country != undefined){
    formattedAddress += address.Country;
  }

  return formattedAddress;
  }

  useEffect(() => {
    sourceAutocompleteRef.current = new google.maps.places.Autocomplete(
      sourceInputRef.current!,
      options
    );

    sourceAutocompleteRef.current.addListener("place_changed", async function() {
      const place = await sourceAutocompleteRef.current?.getPlace();
      console.log({place});
      setSource(formatAddress(place!));
    })
  }, [])

  useEffect(() => {
    destAutocompleteRef.current = new google.maps.places.Autocomplete(
      destInputRef.current!,
      options
    );

    destAutocompleteRef.current.addListener("place_changed", async function() {
      const place = await destAutocompleteRef.current?.getPlace();
      console.log({place});
      setDestination(formatAddress(place!));
    })
  }, [])

  const handleSourceChange = (e: any) => {
    setSource(e.target.value);
  }
  const handleDestinationChange = (e: any) => {
    setDestination(e.target.value);
  }

  const handleMinMaxChange = (e: any) => {
    console.log(e.target.value)
    setMinMax(e.target.value)
  }

  const handleDeviationChange = (e: any) => {
    const dev = e.target.value;
    setDeviation(dev);
  }

  const handleModeChange = (e: any) => {
    const mode = e.target.value;
    setMode(mode);
  }

  const { ref } = usePlacesWidget({
    apiKey: 'AIzaSyA1brenVRXYFkpBRQWscrZcqzSKHimZSkg',
    onPlaceSelected: (place) => console.log(place)
  })

  return (
    <div >
      <div className='input-box-container'>
        <div>
          <input type="text" id="source" name="source" placeholder='Source' className='input-box' onChange={handleSourceChange} ref={sourceInputRef!}></input>
          <div>
            <div className="input-header">
              Maximize/Minimize Elevation Gain
            </div>
            <div className='radio-group'>
              <div className='radio'><input type="radio" value="max" name="elevationGain" onClick={handleMinMaxChange}/> Maximize</div>
              <div className='radio'><input type="radio" value="min" name="elevationGain" onClick={handleMinMaxChange}/> Minimize</div>
            </div>
          </div>
          <div>
        <div className="input-header">
          Mode
        </div>
        <div className='radio-group'>
          <div className='radio'><input type="radio" value="bike" name="mode"  onClick={handleModeChange}/> Bike</div>
          <div className='radio'><input type="radio" value="drive" name="mode" onClick={handleModeChange}/> Drive</div>
          <div className='radio'><input type="radio" value="walk" name="mode" onClick={handleModeChange}/> Walk</div>
        </div>
      </div>

        </div>
        <div>
          <input type="text" id="destination" name="destination" placeholder='Destination' className='input-box' onChange={handleDestinationChange} ref={destInputRef}></input>
          <div>
          <div className="input-header">
            Limit to % of Shortest Path
          </div>
          <div>
            <input type="text" id="deviation" name="deviation" placeholder='Deviation' className='input-box' onChange={handleDeviationChange}/>
          </div>
        </div>
        </div>
      </div>
      
      <div className='submit-button-container'>
          <button className='submit-button' onClick = {() => props.onSubmit({
            source: source,
            destination: destination,
            minMax: minMax,
            deviation: deviation,
            mode: mode
          })}>
            Get Path
          </button>
        </div>
    </div>

  );
}

export default InputBlock;