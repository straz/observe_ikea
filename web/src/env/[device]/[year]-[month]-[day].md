---
sidebar: false
toc: false
pager: false
head: <a class="ms-4" href="/">Home</a>
footer: ''
---

```js
import {css_link} from "../../components/bootstrap.js";
import {zpad, makeDeviceUrl, toRawHtml, toButton, findDeviceName, showTemp,
        showHumidity, showVOC, showPresence, showLight} from "../../components/show_data.js";

display(css_link);
const devices = [
  ["kitchen", "9ae7ed57-1b6c-4e43-8cd5-3e7578f81e4f_1"],
  ["basement", "6a278780-19e5-4ac5-abbb-8c304fed2c55_1"],
  ["motion", "d1452ac7-7d65-403d-a13d-7120545b1cfe_1"],
  ["light", "d1452ac7-7d65-403d-a13d-7120545b1cfe_3"]
]

const deviceId = observable.params.device;
const deviceName = findDeviceName(deviceId, devices);

display(html({raw: [`<h1>${deviceName}</h1>`]}))


const year = observable.params.year;
const month = observable.params.month;
const day = observable.params.day;
const dateStr = `${year}-${month}-${day}`

const date = new Date(dateStr);
const nextDay = new Date(dateStr);
const prevDay = new Date(dateStr);
nextDay.setDate(nextDay.getDate() + 1);
prevDay.setDate(prevDay.getDate() - 1);

display(html({raw: [ `<h3>${year}-${month}-${day}</h3>` ]}))



const prevDaySpec = {
   year: prevDay.getFullYear(),
   month: prevDay.getMonth()+1,
   day: prevDay.getDate()
}
const nextDaySpec = {
   year: nextDay.getFullYear(),
   month: nextDay.getMonth()+1,
   day: nextDay.getDate()
}
			   
display(toButton(makeDeviceUrl(['previous day', deviceId], prevDaySpec, '..')))
display(toButton(makeDeviceUrl(['next day', deviceId], nextDaySpec, '..')))
```


```js

// Show menu of other devices
devices.map((d) => display(toRawHtml(makeDeviceUrl(d, {year, month, day}, ".."))))


// Get data from backend server

const env_sensor = FileAttachment(
  `../../data/${observable.params.device}/sensor-${observable.params.year}-${observable.params.month}-${observable.params.day}.json`
).json();
```

```js
// Show the graphs

if (["kitchen", "basement"].indexOf(deviceName) > -1){
	display(showTemp(env_sensor));
	display(showHumidity(env_sensor));
	display(showVOC(env_sensor));
} else if (deviceName == "motion"){
	const widget =showPresence(env_sensor, {year, month, day});
	display(widget[0]);
	display(html(widget[1]));
} else if (deviceName == "light"){
	display(showLight(env_sensor));
}

```
