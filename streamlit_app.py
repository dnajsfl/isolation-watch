import streamlit as st
import requests
import time
from datetime import datetime
import pandas as pd

SERVER_URL = "https://isolation-watch.onrender.com/data"

st.set_page_config(page_title="고립사 예방 모니터링", layout="centered")

st.title("👨‍🦳 고립사 예방 실시간 모니터링")
st.markdown("""
이 페이지는 ESP8266 센서가 감지한 움직임을 기반으로 
실시간으로 무활동 상태를 모니터링합니다.
- 초록: 정상 활동
- 빨강: 무활동
""")

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
        
        df = pd.DataFrame(history)
        if not df.empty:
            df["time"] = pd.to_datetime(df["time"])
            df["inactive_time"] = pd.to_numeric(df["inactive_time"])

        # 상태 표시
        with placeholder_status.container():
            if latest["status"] == "ACTIVE":
                st.success("🟢 정상 상태")
            elif latest["status"] == "INACTIVE":
                st.error("🚨 무활동 감지!")
            else:
                st.warning("대기 중")

        # 선그래프
        with placeholder_graph.container():
            if not df.empty:
                st.line_chart(df.set_index("time")["inactive_time"])

        # 마지막 갱신 → 현재 시각으로 갱신
        with placeholder_last.container():
            st.caption(f"마지막 갱신: {latest['updated']} | 현재 무활동 시간: {latest['time']}초")

    except requests.exceptions.RequestException:
        st.warning("⚠️ 서버 연결 실패, 재시도 중...")

    time.sleep(1)
