import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime


SERVER_URL = "https://isolation-watch.onrender.com/data"

st.set_page_config(page_title="고립사 예방 모니터링", layout="centered")

st.title("👨‍🦳 고립사 예방 실시간 모니터링")
st.markdown("""
이 페이지는 ESP8266 센서가 감지한 움직임을 기반으로 
실시간으로 무활동 상태를 모니터링합니다.
- 초록: 정상 활동
- 빨강: 무활동
""")
placeholder = st.empty()
graph_placeholder = st.empty()

placeholder_status = st.empty()
placeholder_graph = st.empty()
placeholder_last = st.empty()

while True:
    try:
        res = requests.get(SERVER_URL, timeout=5)
        res.raise_for_status()
        data = res.json()
        
        latest = data["latest"]
        history = data["history"]

        # 상태 출력
        with placeholder.container():
            if latest["status"] == "ACTIVE":
                st.success("🟢 정상 상태")
            elif latest["status"] == "INACTIVE":
                st.error("🚨 무활동 감지")
            else:
                st.warning("대기 중")
            
            st.metric("현재 무활동 시간(초)", latest["time"])
            st.caption(f"마지막 갱신: {latest['updated']}")

        # 기록 데이터프레임으로 변환
        # 기록 데이터프레임으로 변환
if history:
    df = pd.DataFrame(history)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        df["time"] = df["time"].astype(int)

        # 선그래프
        with graph_placeholder.container():
            st.line_chart(df.set_index("timestamp")["time"])
else:
    with graph_placeholder.container():
        st.info("기록 없음")

    
    time.sleep(1)  # 1초마다 갱신
