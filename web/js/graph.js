import jquery from 'https://cdn.jsdelivr.net/npm/jquery@3.7.1/+esm'
import { showChart } from './show_data.js';
import { sensorsUrl, dataUrl } from './common.js';

export function params(){
  // returns object with all the query params: {deviceId, type, year, month, day}
  const p =  new URLSearchParams(window.location.search);
  const today = new Date() // default to today
  return {
    year: parseInt(p.get('year') || today.getFullYear()),
    month: parseInt(p.get('month') || today.getMonth()+1),
    day: parseInt(p.get('day') || today.getDate()),
    deviceId: p.get('deviceId'),
    type: p.get('type')
  }
}

export function showDate(divId){
  const p = params()
  const d = new Date()
  const isToday = JSON.stringify([d.getFullYear(), d.getMonth()+1, d.getDate()])
	== JSON.stringify([p.year, p.month, p.day])
  const todayStr = isToday ? '<span style="color:green">today</span>' : '';
  $(divId).html(`${p.year}-${p.month}-${p.day} ${todayStr}`);  
}

function type2emoji(type){
  switch (type) {
  case 'environmentSensor': return '&#x1F321;'; // thermometer
  case 'motionSensor': return '&#x1F44B'; // waving hand
  case 'lightSensor': return '&#x2600;&#xfe0f;'; // sun
  default: return '&#x1F4A1;';  // lightbulb
  }
}

function make_url(p){
  return  `graph?type=${p.type}&deviceId=${p.deviceId}&year=${p.year}&month=${p.month}&day=${p.day}`
}


export async function showOtherDevices(divId){
  const p = params();
  const selectedDevice = p.deviceId
  
  function onChange(){
    // option value = "<deviceId>,<type>"
    const [deviceId, type] = $(this).val().split(",");
    const params = {...p, deviceId, type}
    window.location = make_url(params)
  }

  const response = await fetch(sensorsUrl());
  const homes = await response.json();
  const select = $('<select>').on("change", onChange);
  for (let homeName in homes) {
    const data = homes[homeName];
    for (let deviceId in data) {
      const entry = data[deviceId];
      const checked = deviceId == selectedDevice;
      const emoji = type2emoji(entry.type);
      const value = `${deviceId},${entry.type}`;
      const option = $('<option>', {selected: checked, value: value, html: `${emoji} ${entry.name}`});
      $(select).append(option)
    }
  }
  $(divId).append(select)
}


export function dateButtons(divId){
  // renders 'prev day' and 'next day' buttons
  const p = params()
  const date = new Date(p.year, p.month-1, p.day)
  const next = new Date(date.getTime());
  const prev = new Date(date.getTime());
  next.setDate(date.getDate()+1)
  prev.setDate(date.getDate()-1)
  const back = urlButton('prev day', pageUrl(p.deviceId, p.type, prev), 'me-2')
  const fwd = urlButton('next day', pageUrl(p.deviceId, p.type, next))  
  $(divId).append(back, fwd)
}

// clickable button that goes to url
function urlButton(name, url, extraClass ){
  const goTo = ()=>{window.location = url};
  return $('<button>', {
    class: "btn btn-sm btn-outline-secondary mt-2 " + extraClass,
    html: name}).on('click', goTo)
}

function pageUrl(deviceId, type, date){
  const year =date.getFullYear();
  const month =date.getMonth()+1;
  const day =date.getDate();
  return `graph?type=${type}&deviceId=${deviceId}&year=${year}&month=${month}&day=${day}`
}
    
export async function plotData(divId) {
  const p = params()
  const url = dataUrl(p)
  if (url == null){
    $(divId).html('Visit <a href="/login">settings</a> to configure url for data host.')
    return;
  }
  // calls showChart from show_data.js
  try {
    const response = await fetch(url);
    const data = await response.json();
    const chart = showChart(p, data);
    $(divId).append(chart);

  } catch (error) {
    console.error("Error loading or plotting data:", error);
    document.getElementById(divId).innerHTML = "Error loading data.";
  }
}
