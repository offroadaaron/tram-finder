# Tram Finder

Simple Flask web app for finding nearby public transport stops and live departures using the Transitous API.

The current UI is optimized for quick mobile use:
- Search by place name
- Use GPS to find nearby stops
- Filter by transport mode
- Save favourite stops in the browser
- Auto-refresh departures every 30 seconds

## Requirements

- Python 3.12 or newer
- Docker, if you want to run the container version
- TLS certificate files if you want to run the provided HTTPS container setup

## Project Layout

- `app.py`: Flask backend and Transitous API proxy routes
- `templates/index.html`: Main UI and frontend logic
- `static/style.css`: Styling
- `requirements.txt`: Python dependencies
- `certs/`: Local TLS certificate mount point for the container

## Local Python Setup

1. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python3 app.py
```

The Flask dev server listens on `http://0.0.0.0:5000` by default.

You can change the port with:

```bash
PORT=8080 python3 app.py
```

## Docker Build

Build the image:

```bash
docker build -t tram-finder .
```

## Docker Run

The current container image is configured to serve HTTPS on port `5443` and expects certificate files mounted into `/certs`.

Expected files:
- `certs/cert.pem`
- `certs/privkey.pem`

Run it with:

```bash
docker run -d \
  --name tram-finder \
  -p 5443:5443 \
  -v "$(pwd)/certs:/certs:ro" \
  tram-finder
```

Then open:

`https://<host>:5443/`

If you are using a self-signed certificate, the browser will warn until you trust that certificate.

## Certificates

The repo ignores `certs/` on purpose. Do not commit private keys or certificate material into Git.

If you need to create test certificates for local use, do that outside version control or keep them only in the ignored `certs/` directory.

## API Endpoints

Backend routes exposed by the app:
- `GET /`
- `GET /api/geocode?q=<query>`
- `GET /api/stops?lat=<lat>&lon=<lon>`
- `GET /api/departures?stopId=<stopId>`

The backend proxies requests to:
- `https://api.transitous.org/api`

## Notes On Behavior

- GPS uses the browser geolocation API, so it requires browser permission.
- Nearby stops are fetched independently from departures.
- By default the UI starts with `Tram` and `Train` filters enabled.
- If a location only has nearby bus stops, the app can appear empty until `Bus` is enabled.
- Favourites are stored in browser `localStorage`, not on the server.
- Departure data auto-refreshes every 30 seconds after a stop search completes.

## Error Handling

- Transit provider request failures are returned as JSON errors from the backend instead of raw Flask 500 pages.
- Frontend rendering escapes upstream and browser-stored values before inserting them into the DOM.

## Updating The Running Container

If you are already running the app in Docker, rebuild and restart it with:

```bash
docker build -t tram-finder .
docker rm -f tram-finder
docker run -d \
  --name tram-finder \
  -p 5443:5443 \
  -v "$(pwd)/certs:/certs:ro" \
  tram-finder
```

## Git Hygiene

- Keep the remote URL free of embedded access tokens
- Rotate any token that was previously exposed in local config or shell history
- Keep certificate files out of Git
