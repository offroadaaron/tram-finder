# Transit Finder

Real-time public transport departures powered by the [Transitous](https://transitous.org) / MOTIS API.

## Features

- Search by place name with autocomplete
- GPS to find nearby stops
- Filter by mode: Tram, Train, Subway, Bus, Ferry
- Tap any departure to see all stops on that service
- Save favourite stops (persisted in browser `localStorage`)
- Auto-refreshes every 30 seconds
- iPhone-optimised responsive UI with safe-area support
- HTTPS via mounted TLS certificate

---

## Deploying on a New Machine

### Requirements

- Docker (recommended) **or** Python 3.12+
- A TLS certificate for HTTPS (required for GPS/geolocation in browsers)

### 1 — Clone the repo

```bash
git clone https://github.com/offroadaaron/tram-finder.git
cd tram-finder
```

### 2 — Add your TLS certificate

Place your certificate files in a `certs/` directory (this folder is gitignored — never commit keys):

```
certs/
  cert.pem       # your domain certificate
  privkey.pem    # your private key
```

If you exported from Synology DSM, unzip the bundle into `certs/`.

### 3 — Build and run with Docker

```bash
docker build -t transit-finder .

docker run -d \
  --name transit-finder \
  --restart unless-stopped \
  -p 5443:5443 \
  -v "$(pwd)/certs:/certs:ro" \
  transit-finder
```

Open `https://<your-host>:5443`

### Updating to the latest version

```bash
git pull
docker build -t transit-finder .
docker rm -f transit-finder
docker run -d \
  --name transit-finder \
  --restart unless-stopped \
  -p 5443:5443 \
  -v "$(pwd)/certs:/certs:ro" \
  transit-finder
```

---

## Running without Docker (development)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py          # listens on http://0.0.0.0:5000
```

> GPS will not work over plain HTTP except on `localhost`.

---

## Project Layout

| Path | Purpose |
|---|---|
| `app.py` | Flask backend — proxies requests to Transitous API |
| `templates/index.html` | Full frontend UI and JS |
| `static/style.css` | Stylesheet |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container definition |
| `certs/` | TLS cert mount point — **gitignored, never commit** |

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Serves the UI |
| `GET /api/geocode?q=` | Address autocomplete / forward geocode |
| `GET /api/stops?lat=&lon=` | Nearby transit stops |
| `GET /api/departures?stopId=` | Live departures for a stop |
| `GET /api/trip?tripId=` | All stops on a specific trip/service |

All routes proxy to `https://api.transitous.org/api` with a proper `User-Agent` header as required by Transitous.

---

## Notes

- Favourites are stored in the browser (`localStorage`) — not on the server.
- The default filter enables Tram and Train; enable Bus/Subway/Ferry as needed.
- Tapping a favourite chip loads that exact stop directly, bypassing the nearby-stops search and showing all modes.
- Tapping a departure row fetches and displays the full stop list for that service.
