from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 최신 상태
latest = {
    "status": "WAITING",
    "time": 0,
    "updated": "-"
}

# 기록 저장
history = []  # [{"time": datetime, "status": str, "inactive_time": int}, ...]

@app.route("/update")
def update():
    status = request.args.get("status")
    time_sec = request.args.get("time")
    if status and time_sec:
        latest["status"] = status
        latest["time"] = int(time_sec)
        latest["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 기록에 추가
        history.append({
            "time": latest["updated"],
            "status": status,
            "inactive_time": int(time_sec)
        })
        # 최대 100개만 저장
        if len(history) > 100:
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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
