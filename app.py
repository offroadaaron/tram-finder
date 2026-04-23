import os

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

API_BASE = "https://api.transitous.org/api"
HEADERS = {
    "User-Agent": "TransitFinder/1.0 (offroadaaron@gmail.com)",
    "Accept": "application/json",
}
REQUEST_TIMEOUT = 10


def proxy_get(path, params):
    try:
        response = requests.get(
            f"{API_BASE}{path}",
            params=params,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else 502
        return (
            jsonify(
                {
                    "error": "Transit provider request failed",
                    "status": status_code,
                }
            ),
            status_code,
        )
    except requests.RequestException:
        return jsonify({"error": "Transit provider unavailable"}), 502


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/geocode")
def geocode():
    q = request.args.get("q", "")
    if not q:
        return jsonify({"error": "Missing query"}), 400
    return proxy_get("/v1/geocode", {"text": q, "numResults": 5})


@app.route("/api/stops")
def stops():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Missing lat/lon"}), 400
    return proxy_get(
        "/v1/reverse-geocode",
        {"place": f"{lat},{lon}", "type": "STOP", "numResults": 15},
    )


@app.route("/api/trip")
def trip():
    trip_id = request.args.get("tripId")
    if not trip_id:
        return jsonify({"error": "Missing tripId"}), 400
    return proxy_get("/v1/trip", {"tripId": trip_id})


@app.route("/api/departures")
def departures():
    stop_id = request.args.get("stopId")
    if not stop_id:
        return jsonify({"error": "Missing stopId"}), 400
    return proxy_get("/v5/stoptimes", {"stopId": stop_id, "n": 20, "arriveBy": "false"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
