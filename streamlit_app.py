import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="고립사 예방 실시간 모니터링", layout="centered")

# --- 서버 URL ---
SERVER_URL = "https://isolation-watch.onrender.com/data"     # 최신 상태
HISTORY_URL = "https://isolation-watch.onrender.com/history"  # 기록

# --- 상단 설명글 ---
st.markdown("""
# 👨‍🦳 고립사 예방 실시간 모니터링
- 아두이노 센서로 움직임 감지
- 무활동 시 경고 표시
- 실시간 기록 및 선 그래프
- 화면은 2초마다 갱신
""")

# --- 화면 갱신용 placeholder ---
status_placeholder = st.empty()
chart_placeholder = st.empty()

# --- 자동 새로고침 (2초) ---
st_autorefresh = st.experimental_rerun

# --- 데이터 가져오기 ---
try:
    # 현재 상태
    res = requests.get(SERVER_URL, timeout=5)
    data = res.json()

    with status_placeholder.container():
        st.subheader("현재 상태")
        if data["status"] == "ACTIVE":
            st.success("🟢 정상 상태")
        elif data["status"] == "INACTIVE":
            st.error("🚨 무활동 감지")
        else:
            st.warning("⏳ 대기 중")

        st.metric("무활동 시간(초)", data["time"])
        st.caption(f"마지막 갱신: {data['updated']}")

    # 기록 불러오기
    hist_res = requests.get(HISTORY_URL, timeout=5)
    hist_json = hist_res.json()
    if hist_json:
        history_df = pd.DataFrame(hist_json, columns=["Time", "Status", "InactiveTime"])
        history_df["Time"] = pd.to_datetime(history_df["Time"])
        history_df["InactiveTime"] = history_df["InactiveTime"].astype(int)
        chart_placeholder.line_chart(history_df.set_index("Time")["InactiveTime"])

except Exception as e:
    st.error(f"데이터 로드 실패: {e}")

# --- 2초마다 새로고침 ---
time.sleep(2)
st.experimental_rerun()
