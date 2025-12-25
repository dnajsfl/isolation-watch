from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 상태 기록과 로그 저장
latest = {
    "status": "WAITING",
    "time": 0,
    "updated": "-"
}

history = []  # 시간 순으로 활동 기록 저장 (무활동 시간 추적용)

@app.route("/update")
def update():
    status = request.args.get("status")
    time_sec = request.args.get("time")
    
    if status and time_sec:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        latest["status"] = status
        latest["time"] = int(time_sec)
        latest["updated"] = now_str
        
        # 기록 남기기
        history.append({
            "timestamp": now_str,
            "status": status,
            "time": int(time_sec)
        })
        # 기록 100개만 유지
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
