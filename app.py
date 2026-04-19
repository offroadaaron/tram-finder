import os
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

API_BASE = "https://api.transitous.org/api"
HEADERS = {
    "User-Agent": "TramFinder/1.0 (offroadaaron@gmail.com)",
    "Accept": "application/json",
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/geocode")
def geocode():
    q = request.args.get("q", "")
    if not q:
        return jsonify({"error": "Missing query"}), 400
    r = requests.get(
        f"{API_BASE}/v1/geocode",
        params={"text": q, "numResults": 5},
        headers=HEADERS,
        timeout=10,
    )
    r.raise_for_status()
    return jsonify(r.json())


@app.route("/api/stops")
def stops():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Missing lat/lon"}), 400
    r = requests.get(
        f"{API_BASE}/v1/reverse-geocode",
        params={"place": f"{lat},{lon}", "type": "STOP", "numResults": 15},
        headers=HEADERS,
        timeout=10,
    )
    r.raise_for_status()
    return jsonify(r.json())


@app.route("/api/departures")
def departures():
    stop_id = request.args.get("stopId")
    if not stop_id:
        return jsonify({"error": "Missing stopId"}), 400
    r = requests.get(
        f"{API_BASE}/v5/stoptimes",
        params={"stopId": stop_id, "n": 20, "arriveBy": "false"},
        headers=HEADERS,
        timeout=10,
    )
    r.raise_for_status()
    return jsonify(r.json())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
