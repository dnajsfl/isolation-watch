import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="고립사 예방 모니터링", layout="centered")
SERVER_URL = "https://isolation-watch.onrender.com/data"

KST = timezone(timedelta(hours=9))

st.title("👀 고립사 예방 실시간 모니터링")
st.markdown("""
---
### 작동 원리
- 초음파 센서가 움직임을 감지합니다.
- 일정 시간 무활동 시 '위험(INACTIVE)' 상태로 서버에 기록됩니다.
- 선그래프를 통해 과거 무활동 기록을 확인할 수 있습니다.

- 초록: 정상 활동 / 빨강: 무활동
---
""")

placeholder_status = st.empty()
placeholder_metric = st.empty()
placeholder_graph = st.empty()
placeholder_caption = st.empty()

history_df = pd.DataFrame(columns=["timestamp", "status", "time"])

while True:
    try:
        res = requests.get(SERVER_URL, timeout=5)
        if res.status_code == 200:
            data = res.json()
            latest = data.get("latest", {})
            history = data.get("history", [])

            latest_status = latest.get("status", "WAITING")
            latest_time = latest.get("time", 0)

            # 서버시간 KST로
            server_updated = latest.get("updated")
            if server_updated and server_updated != "-":
                try:
                    dt_obj = datetime.strptime(server_updated, "%Y-%m-%d %H:%M:%S")
                    latest_updated = (dt_obj + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
                except:
                    latest_updated = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
            else:
                latest_updated = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

            # 기록업뎃
            if history:
                history_df = pd.DataFrame(history)
                history_df["time"] = history_df["time"].astype(int)
                try:
                    history_df["timestamp"] = pd.to_datetime(history_df["timestamp"]) + timedelta(hours=9)
                except:
                    pass
        else:
            latest_status, latest_time, latest_updated = "WAITING", 0, datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        latest_status, latest_time, latest_updated = "WAITING", 0, datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
        st.error(f"서버 연결 실패: {e}")

    # 상태
    with placeholder_status.container():
        if latest_status == "ACTIVE":
            st.success("🟢 정상 상태")
        elif latest_status == "INACTIVE":
            st.error("🚨 무활동 감지")
        else:
            st.warning("⏳ 대기 중")

    # 무활동 시간
    with placeholder_metric.container():
        st.metric("무활동 시간(초)", latest_time)

    # 그래프
    with placeholder_graph.container():
        if not history_df.empty:
            st.line_chart(history_df.set_index("timestamp")["time"])

    # 마지막 갱신
    with placeholder_caption.container():
        st.caption(f"마지막 갱신: {latest_updated} | 현재 무활동 시간: {latest_time}초")

    time.sleep(1)
