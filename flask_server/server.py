import os
import csv
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

LATEST_FILE = "latest.json"
HISTORY_FILE = "history.csv"

latest = {
    "status": "WAITING",
    "time": 0,
    "updated": "-"
}

@app.route("/update")
def update():
    status = request.args.get("status")
    time_sec = request.args.get("time")

    if status and time_sec:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        latest["status"] = status
        latest["time"] = int(time_sec)
        latest["updated"] = now

        # 기록 저장
        with open(HISTORY_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([now, status, time_sec])

        return "OK", 200

    return "BAD REQUEST", 400

@app.route("/data")
def data():
    return jsonify(latest)

@app.route("/history")
def history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            reader = csv.reader(f)
            return jsonify(list(reader))
    else:
        return jsonify([])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
