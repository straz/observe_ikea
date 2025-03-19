---
layout: default
---

[Home](.)

<div class="mb-1 mt-3" id="today"></div>
<div class="mb-5" id="buttons"></div>
<div class="mb-5" id="otherDevices"></div>
<div id="chart"></div>

<script type="module">
  import {showDate, showOtherDevices, dateButtons, plotData} from "./js/graph.js";
  dateButtons("#buttons");
  showDate("#today");
  showOtherDevices('#otherDevices');
  plotData("#chart");
</script>
