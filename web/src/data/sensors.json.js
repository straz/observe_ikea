const url = "http://backend:8000/sensors"

async function json(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`fetch failed: ${response.status}`);
  return await response.json();
}

const data = await json(url);

process.stdout.write(JSON.stringify(data));
