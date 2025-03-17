import {sensorsUrl} from './common.js';

export async function listing(divId){
  const url = sensorsUrl()
  if (url == null){
    $(divId).html('Visit settings to configure url for data host.')
    return;
  }
  const response = await fetch(url);
  const homes = await response.json();
  for (let homeName in homes) {
    $(divId).append(make_home(homeName, homes[homeName]))
  }
}

// returns a div containing all the sensors in a home
//
//  <h3>home name</h3>
//   <li> <link to device> </li>
//   <li> ...
//  
// data is an object: {deviceId: {name: deviceName, type: deviceType}}
function make_home(homeName, data){
  const list = $('<div>', {class: 'mt-3'});
  list.append($('<h3>').html(homeName))
  for (let deviceId in data) {
    const entry = data[deviceId]
    list.append(make_menu_item(deviceId, entry['name'], entry['type'] ))
  }
  return list
} 

function make_menu_item(deviceId, name, type){
  const li = $('<li>')
  return li.append($('<a>', {'href': `graph?type=${type}&deviceId=${deviceId}`, html: name}))
}
