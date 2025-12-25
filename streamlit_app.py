import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime


SERVER_URL = "https://isolation-watch.onrender.com/data"

st.set_page_config(page_title="고립사 예방 모니터링", layout="centered")

st.title("👨‍🦳 고립사 예방 실시간 모니터링")
st.markdown("""
---
### 작동 원리
- ESP8266 초음파 센서가 움직임을 감지합니다.
- 일정 시간 무활동 시 '위험(INACTIVE)' 상태로 서버에 기록됩니다.
- 선그래프를 통해 과거 무활동 기록을 확인할 수 있습니다.

- 초록: 정상 활동
- 빨강: 무활동
---
""")

placeholder = st.empty()
graph_placeholder = st.empty()
status_placeholder = st.empty()

history = []

while True:
    try:
        # 서버에서 최신 데이터 가져오기
        res = requests.get(SERVER_URL, timeout=5)
        if res.status_code == 200 and res.headers.get("Content-Type") == "application/json":
            latest = res.json()
            # timestamp가 없으면 현재 시간 추가
            if "timestamp" not in latest:
                latest["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history.append(latest)
        else:
            latest = {"status": "WAITING", "time": 0, "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    except Exception as e:
        latest = {"status": "WAITING", "time": 0, "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        st.error(f"서버 연결 실패: {e}")

    # 최신 상태 출력
    with status_placeholder.container():
        if latest["status"] == "ACTIVE":
            st.success("🟢 정상 상태")
        elif latest["status"] == "INACTIVE":
            st.error("🚨 무활동 감지")
        else:
            st.warning("⏳ 대기 중")
        st.metric("무활동 시간(초)", latest["time"])
        st.caption(f"마지막 갱신: {latest['timestamp']} | 현재 무활동 시간: {latest['time']}초")

    # 기록 데이터프레임 생성 및 그래프 그리기
    if history:
        df = pd.DataFrame(history)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp")
            df["time"] = df["time"].astype(int)
            with graph_placeholder.container():
                st.line_chart(df.set_index("timestamp")["time"])
    else:
        with graph_placeholder.container():
            st.info("기록 없음")

    # 1초마다 갱신
    time.sleep(1)
