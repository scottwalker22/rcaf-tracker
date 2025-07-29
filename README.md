# RCAF Aircraft Tracker

A lightweight aircraft tracking dashboard for use with PiAware or dump1090-fa. This tool identifies RCAF C-130 Hercules and C-17 Globemaster III aircraft (using known ICAO hex codes) and displays them in real-time on an auto-refreshing map — all hosted directly on your Pi.

If no military aircraft are present, it falls back to showing a random visible aircraft so the display remains functional for testing or demos.

---

## ⚙️ Requirements

To use this script, you’ll need:

- A Raspberry Pi (or similar Linux system)
- A working ADS-B setup (e.g. **PiAware**, **dump1090-fa**, or **SkyAware**)
- Access to the JSON feed at:  
  `/run/dump1090-fa/aircraft.json`
- A web server that serves files from:  
  `/usr/share/skyaware/html/` *(used by default with SkyAware)*

---

## 📦 Example Setup

Tested on:

- Raspberry Pi 3B+
- Raspberry Pi OS Bullseye (64-bit)
- PiAware 8.x + SkyAware
- Accessible at:  
  `http://192.168.20.25:8080/rcaf.html`

---

## 📂 Output

This script generates two files:

| File        | Purpose                                   |
|-------------|-------------------------------------------|
| `rcaf.html` | The real-time webpage (auto-refreshing)   |
| `rcaf.json` | The current aircraft data for the browser |

---

## 🗺 Features

- Real-time Leaflet map showing aircraft position
- Auto-updates every 30 seconds without reloading the page
- Identifies RCAF aircraft by ICAO hex code
- Falls back to a random aircraft if none are present
- Clean HTML + JavaScript, no external dependencies except Leaflet CDN

---

## 🚀 Usage

1. Clone the repo:

```bash
git clone https://github.com/scottwalker22/rcaf-tracker.git
cd rcaf-tracker

