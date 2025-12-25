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

- 초록: 정상 활동 / 빨강: 무활동
---
""")

placeholder_status = st.empty()
placeholder_metric = st.empty()
placeholder_graph = st.empty()
placeholder_caption = st.empty()

# 기록 저장용 데이터프레임
history = pd.DataFrame(columns=["timestamp", "status", "time"])

while True:
    # 서버에서 데이터 가져오기
    try:
        res = requests.get(SERVER_URL, timeout=5)
        if res.status_code == 200:
            latest = res.json()
            latest_status = latest.get("status", "WAITING")
            latest_time = latest.get("time", 0)
            latest_updated = latest.get("updated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            latest_status = "WAITING"
            latest_time = 0
            latest_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        latest_status = "WAITING"
        latest_time = 0
        latest_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.error(f"서버 연결 실패: {e}")

    # 상태 표시
    with placeholder_status.container():
        if latest_status == "ACTIVE":
            st.success("🟢 정상 상태")
        elif latest_status == "INACTIVE":
            st.error("🚨 무활동 감지")
        else:
            st.warning("⏳ 대기 중")

    # 무활동 시간 표시
    with placeholder_metric.container():
        st.metric("무활동 시간(초)", latest_time)

    # 기록 데이터 추가
    timestamp_now = datetime.now().strftime("%H:%M:%S")
    history = pd.concat([history, pd.DataFrame([{
        "timestamp": timestamp_now,
        "status": latest_status,
        "time": latest_time
    }])], ignore_index=True)

    # 선그래프 그리기
    with placeholder_graph.container():
        if not history.empty:
            st.line_chart(history.set_index("timestamp")["time"])

    # 마지막 갱신 표시
    with placeholder_caption.container():
        st.caption(f"마지막 갱신: {latest_updated} | 현재 무활동 시간: {latest_time}초")

    time.sleep(1)
