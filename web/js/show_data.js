import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

// date is {year: year, month: month, day: day}
export function showChart(params, env_data){
  switch(params.type){
  case 'environmentSensor':
    return $('<div>').append(
      showTemp(env_data),
      showVOC(env_data),
      showPM25(env_data)
    );
  case 'lightSensor':
    return showLight(env_data);
  case 'motionSensor':
    return showPresence(env_data, params);    
  }
}

function showTemp(env_data){
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

function showVOC(env_data){
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

function showPM25(env_data){
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



function showLight(env_data){
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


function showPresence(env_data, p){

  const start = new Date(`${p.year}-${zpad(p.month)}-${zpad(p.day)}T00:00`)
  const end = new Date(`${p.year}-${zpad(p.month)}-${zpad(p.day)}T23:59`)
  
  const data = env_data
	.filter(d => d.isDetected)
	.map(d => ({
	  timestamp: new Date(d.timestamp),
	  motion: d.isDetected
	}));
  if (env_data.length == 0){
    console.error('nope')
    return ['No data', {raw: [`No presence data for ${p.year}-${p.month}-${p.day}`]}];
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

function zpad(n){
  return String(n).padStart(2, "0")
}
