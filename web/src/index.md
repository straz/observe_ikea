---
style: ''
sidebar: false
toc: false
pager: false
footer: ''
---


```js
//import {html} from "npm:htl";

import {css_link} from "./components/bootstrap.js";
display(css_link);

display(html`<div class="container"><h1>IKEA sensors</h1>`)

// get data
const sensors = FileAttachment("./data/sensors.json").json();
```

```js
import { makeDeviceUrl, toRawHtml} from "./components/show_data.js";



const now = new Date();
const year = now.getFullYear();
const month = now.getMonth()+1;
const day = now.getDate()

const homes = Object.entries(sensors);

display(html`<div class="container">`)

homes.map(([homeName, homeDevices]) => {
   const devices = Object.entries(homeDevices);
   devices.map((d)=> display(toRawHtml(makeDeviceUrl(d, {year, month, day}, './env'))))
})

display(html`</div>`)
```
