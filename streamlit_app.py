import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="고립사 예방 실시간 모니터링")

SERVER_URL = "https://isolation-watch.onrender.com/data"
HISTORY_URL = "https://isolation-watch.onrender.com/history"

# --- 설명글 ---
st.markdown("""
# 👨‍🦳 고립사 예방 실시간 모니터링

이 시스템은 아두이노 센서로 움직임을 감지하고, 
무활동 시 웹사이트에서 경고 상태를 표시합니다.

작동 원리:
- 아두이노가 실시간으로 서버에 상태(`ACTIVE`/`INACTIVE`)와 무활동 시간을 전송
- 서버는 최신 상태를 저장하고 기록으로 남김
- Streamlit이 서버를 2초마다 호출하여 화면 갱신
""")

placeholder = st.empty()
chart_placeholder = st.empty()

# --- 기록용 DataFrame ---
history_df = pd.DataFrame(columns=["Time", "Status", "InactiveTime"])

while True:
    try:
        res = requests.get(SERVER_URL, timeout=5)
        data = res.json()

        # --- 최신 상태 표시 ---
        with placeholder.container():
            st.subheader("현재 상태")
            if data["status"] == "ACTIVE":
                st.success("🟢 정상 상태")
            elif data["status"] == "INACTIVE":
                st.error("🚨 무활동 감지")
            else:
                st.warning("대기 중")
            st.metric("무활동 시간(초)", data["time"])
            st.caption(f"마지막 갱신: {data['updated']}")

        # --- 기록 가져오기 ---
        hist_res = requests.get(HISTORY_URL, timeout=5)
        hist_json = hist_res.json()
        if hist_json:
            history_df = pd.DataFrame(hist_json, columns=["Time", "Status", "InactiveTime"])
            history_df["Time"] = pd.to_datetime(history_df["Time"])
            history_df["InactiveTime"] = history_df["InactiveTime"].astype(int)
            chart_placeholder.line_chart(history_df.set_index("Time")["InactiveTime"])

        time.sleep(2)
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        time.sleep(5)
