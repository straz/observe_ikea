import {parseArgs} from "node:util";

const {values: {device, year, month, day}} = parseArgs(
  {
    options: {device: {type: "string"},
	      year: {type: "string"},
	      month: {type: "string"},
	      day: {type: "string"}}
  });

const url = `http://backend:8000/data/${device}/day/${year}/${month}/${day}`

async function json(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`fetch failed: ${response.status}`);
  return await response.json();
}

const day_data = await json(url);

process.stdout.write(JSON.stringify(day_data));
