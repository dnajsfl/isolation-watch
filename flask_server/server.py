from flask import Flask, request, jsonify
from datetime import datetime
import os  # ← 이 줄이 핵심!!!!!

app = Flask(__name__)

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
        latest["status"] = status
        latest["time"] = int(time_sec)
        latest["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return "OK", 200

    return "BAD REQUEST", 400


@app.route("/data")
def data():
    return jsonify(latest)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
