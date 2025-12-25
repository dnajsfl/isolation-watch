import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="고립사 예방 모니터링", layout="centered")
SERVER_URL = "https://isolation-watch.onrender.com/data"

# 기록을 담을 DataFrame 초기화
if 'history_df' not in st.session_state:
    st.session_state.history_df = pd.DataFrame(columns=["timestamp", "status", "time"])

placeholder = st.empty()
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


while True:
    try:
        res = requests.get(SERVER_URL, timeout=5)
        res.raise_for_status()
        latest = res.json()

        # 현재 시간 기록
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = {"timestamp": timestamp, "status": latest.get("status", "WAITING"), "time": latest.get("time", 0)}
        st.session_state.history_df = pd.concat([st.session_state.history_df, pd.DataFrame([new_row])], ignore_index=True)

        with placeholder.container():
            # 상태 표시
            if latest["status"] == "ACTIVE":
                st.success("🟢 정상 상태")
            elif latest["status"] == "INACTIVE":
                st.error("🚨 무활동 감지")
            else:
                st.warning("대기 중")

            st.metric("무활동 시간(초)", latest.get("time", 0))
            st.caption(f"마지막 갱신: {timestamp}")

            # 그래프 표시
            st.line_chart(st.session_state.history_df.set_index("timestamp")["time"])

        time.sleep(2)

    except requests.RequestException:
        st.warning("서버 연결 실패...")
        time.sleep(2)
