from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 최신 상태
latest = {
    "status": "WAITING",
    "time": 0,
    "updated": "-"
}

# 모든 기록 저장 (서버 메모리)
history = []

@app.route("/update")
def update():
    status = request.args.get("status")
    time_sec = request.args.get("time")

    if status and time_sec:
        time_sec = int(time_sec)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 최신 상태 갱신
        latest["status"] = status
        latest["time"] = time_sec
        latest["updated"] = now

        # 기록에 추가
        history.append({
            "Time": now,
            "Status": status,
            "InactiveTime": time_sec
        })

        return "OK", 200

    return "BAD REQUEST", 400

@app.route("/data")
def data():
    return jsonify(latest)

@app.route("/history")
def get_history():
    return jsonify(history)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
