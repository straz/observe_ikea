import * as Plot from "npm:@observablehq/plot";
import {html} from "npm:htl";

export function zpad(n){
  return String(n).padStart(2, "0")
}

export function findDeviceName(device, devices){
  let deviceName;
  devices.forEach((spec)=> {
    if (spec[1] == device) {
      deviceName = spec[0];
    }
  })
  return deviceName;
}

export function toRawHtml(string){
  return html({raw: [string]})
}

export function toButton(string){
  return html({raw: [`<button class="btn btn-outline-secondary btn-sm  me-3">${string}</button>`]})
}

export function makeDeviceUrl(spec, d, relPath){
  // spec:  [name:string, id:string]
  // d:  {year, month, day}
  const name = spec[0];
  const id = spec[1];
  const ref=`${relPath}/${id}/${d.year}-${d.month}-${d.day}`;
  return `<A href="${ref}">${name}</A><br/>`;
}

export function showHumidity(env_data){
  const data = env_data.map(d => ({
    timestamp: new Date(d.timestamp),
    humidity: d.currentRH
  }));

  return Plot.plot(
    {x: {type: "time", label: "timestamp"},
     y: {axis: "left", label: "Relative humidity %", color: "green", domain: [15, 60]},
     marginBottom: 100,
     marks: [
       Plot.line(data, { x: "timestamp", y: "humidity",
   			 stroke: "green", label: "Humidity" }),
     ]
    }
  )
}


export function showTemp(env_data){
  function toF(C){return (C * 9/5) + 32; }

  const data = env_data.map(d => ({
    timestamp: new Date(d.timestamp),
    temperature: toF(d.currentTemperature)
  }));

  return  Plot.plot(
    {x: {type: "time"},
     y: {label: "Temperature °F", domain: [40,80]},
     marginBottom: 100,
     marks: [
       Plot.line(data, { x: "timestamp", y: "temperature", stroke: "red", }),
     ]
    }
  )
}

export function showVOC(env_data){
  const data = env_data.map(d => ({
    timestamp: new Date(d.timestamp),
    vocIndex: d.vocIndex
  }));

  return  Plot.plot(
    {x: {type: "time"},
     y: {label: "VOC index"},
     marginBottom: 100,
     marks: [
       Plot.line(data, { x: "timestamp", y: "vocIndex", stroke: "blue" })
     ]
    }
  )
}

export function showPM25(env_data){
  const data = env_data.map(d => ({
    timestamp: new Date(d.timestamp),
    PM25: d.currentPM25
  }));

  return  Plot.plot(
    {x: {type: "time"},
     y: {label: "PM 25"},
     marginBottom: 100,
     marks: [
       Plot.line(data, { x: "timestamp", y: "PM25", stroke: "purple" })
     ]
    }
  )
}



export function showLight(env_data){
  const data = env_data.map(d => ({
    timestamp: new Date(d.timestamp),
    light: d.illuminance
  }));

  return Plot.plot(
    {x: {type: "time"},
     y: {label: "Illuminance"},
     marginBottom: 100,
     marks: [
       Plot.line(data, { x: "timestamp", y: "light", stroke: "orange", }),
     ]
    }
  )
}


export function showPresence(env_data, date){

  const start = new Date(`${date.year}-${zpad(date.month)}-${zpad(date.day)}T00:00`)
  const end = new Date(`${date.year}-${zpad(date.month)}-${zpad(date.day)}T23:59`)
  
  const data = env_data
	.filter(d => d.isDetected)
	.map(d => ({
	  timestamp: new Date(d.timestamp),
	  motion: d.isDetected
	}));
  if (env_data.length == 0){
    console.error('nope')
    return ['No data', {raw: [`No presence data for ${date.year}-${date.month}-${date.day}`]}];
  }
  
  const battery = `Battery: ${env_data[0].batteryPercentage}%`

  return  [
    Plot.plot(
      {x: {type: "time", domain: [start, end]},
       y: {label: null, ticks: []},
       marginBottom: 100,
       marginLeft: 40,
       marks: [
         Plot.dot(data, { x: "timestamp", y: "motion", fill: "purple" }),
       ]
      }
    ),
    {raw: [ `<p>${battery}</p>` ]}
  ]
}
