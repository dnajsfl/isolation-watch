from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

latest = {
    "status": "WAITING",
    "time": 0,
    "updated": "-"
}


history = []

@app.route("/update")
def update():
    status = request.args.get("status")
    time_sec = request.args.get("time")

    if status and time_sec:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        latest["status"] = status
        latest["time"] = int(time_sec)
        latest["updated"] = now_str

        
        history.append({
            "timestamp": now_str,
            "status": status,
            "time": int(time_sec)
        })
        
        if len(history) > 200:
            history.pop(0)

        return "OK", 200

    return "BAD REQUEST", 400


@app.route("/data")
def data():
    return jsonify({
        "latest": latest,
        "history": history
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route("/reset")
def reset():
    latest["status"] = "WAITING"
    latest["time"] = 0
    latest["updated"] = "-"

    history.clear()

    return "RESET OK", 200

