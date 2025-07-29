#!/usr/bin/env python3

import json
import random
from datetime import datetime

AIRCRAFT_JSON = "/run/dump1090-fa/aircraft.json"
HTML_OUT = "/usr/share/skyaware/html/rcaf.html"
JSON_OUT = "/usr/share/skyaware/html/rcaf.json"

known_c130_hexes = {
    "43C5A7", "43C5A8", "43C5A9", "43C5AA", "43C5AC", "43C5AD",
    "43C5AE", "43C5AF", "43C5B0", "43C5B1", "43C5B2", "43C5B3",
    "43C5B4", "43C5B5", "43C5B6", "43C5B7", "43C5B8", "43C5B9",
    "43C5BA", "43C5BB", "43C5BC", "43C5BD", "43C5BE", "43C5BF",
    "43C5C0", "43C5C1", "43C5C2"
}

known_c17_hexes = {
    "C2B3F5", "C2B401", "C2B402", "C2B403", "C2B404", "C2B405",
    "C2B406", "C2B407", "C2B408", "C2B409", "C2B40A", "C2B40B",
    "C2B40C", "C2B40D"
}

def get_aircraft_type(hexid):
    if hexid in known_c130_hexes:
        return "C-130 Hercules"
    elif hexid in known_c17_hexes:
        return "C-17 Globemaster III"
    return "Unknown Aircraft"

def write_json(ac):
    hexid = ac.get("hex", "").upper()
    lat = ac.get("lat")
    lon = ac.get("lon")
    data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "hex": hexid,
        "type": get_aircraft_type(hexid),
        "lat": lat,
        "lon": lon,
        "maps_link": f"https://www.google.com/maps/place/{lat},{lon}" if lat and lon else "N/A"
    }
    with open(JSON_OUT, "w") as f:
        json.dump(data, f)

def write_html():
    html = """<!DOCTYPE html>
<html>
<head>
  <title>Live RCAF Tracker</title>
  <meta charset="UTF-8" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; }
    #map { height: 500px; width: 100%; margin-top: 20px; }
  </style>
</head>
<body>
  <h1>Live RCAF Aircraft</h1>
  <p><strong>Last updated:</strong> <span id="timestamp">Loading...</span></p>
  <p><strong>Aircraft Type:</strong> <span id="type">Loading...</span></p>
  <p><strong>Hex Code:</strong> <span id="hex">Loading...</span></p>
  <p><strong>Location:</strong> <a id="maps_link" href="#" target="_blank">Loading...</a></p>
  <div id="map"></div>

  <script>
    let map = L.map('map').setView([45, -77], 11); // Zoomed in closer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    let marker = null;

    async function fetchData() {
      try {
        const res = await fetch('rcaf.json?' + new Date().getTime()); // prevent caching
        const data = await res.json();

        document.getElementById('timestamp').textContent = data.timestamp;
        document.getElementById('type').textContent = data.type;
        document.getElementById('hex').textContent = data.hex;
        document.getElementById('maps_link').textContent = `${data.lat}, ${data.lon}`;
        document.getElementById('maps_link').href = data.maps_link;

        if (marker) map.removeLayer(marker);
        marker = L.marker([data.lat, data.lon]).addTo(map)
            .bindPopup(`<b>${data.hex}</b><br>${data.lat}, ${data.lon}`).openPopup();
        map.setView([data.lat, data.lon], 11);
      } catch (err) {
        console.error("Failed to load aircraft data:", err);
      }
    }

    fetchData();
    setInterval(fetchData, 30000);
  </script>
</body>
</html>"""
    with open(HTML_OUT, "w") as f:
        f.write(html)

def main():
    try:
        with open(AIRCRAFT_JSON, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read aircraft data: {e}")
        return

    visible = [a for a in data.get("aircraft", []) if a.get("lat") and a.get("lon")]
    if not visible:
        print("⚠️ No aircraft with coordinates.")
        return

    selected = random.choice(visible)
    write_json(selected)
    write_html()

if __name__ == "__main__":
    main()

