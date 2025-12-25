import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime, timedelta, timezone # <-- timedelta, timezone 추가

st.set_page_config(page_title="고립사 예방 모니터링", layout="centered")
SERVER_URL = "https://isolation-watch.onrender.com/data"

# 한국 시간대 정의
KST = timezone(timedelta(hours=9))

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
            
            # [수정 포인트 1] 서버에서 받은 시간을 한국 시간으로 변환
            server_updated = latest.get("updated")
            if server_updated:
                # 서버 시간을 파이썬 시각 객체로 변환 (서버가 보내주는 형식이 %Y-%m-%d %H:%M:%S 라고 가정)
                try:
                    dt_obj = datetime.strptime(server_updated, "%Y-%m-%d %H:%M:%S")
                    # 서버 시간이 UTC이므로 9시간을 더해줌
                    latest_updated = (dt_obj + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
                except:
                    latest_updated = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
            else:
                latest_updated = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

            # [수정 포인트 2] 기록 DataFrame의 타임스탬프도 보정
            if history:
                history_df = pd.DataFrame(history)
                history_df["time"] = history_df["time"].astype(int)
                
                # 그래프 시간축도 한국 시간으로 보이게 (기존값에 9시간 더하기)
                try:
                    history_df["timestamp"] = pd.to_datetime(history_df["timestamp"]) + pd.Timedelta(hours=9)
                except:
                    pass
        else:
            latest_status, latest_time, latest_updated = "WAITING", 0, datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
            
    except Exception as e:
        latest_status, latest_time, latest_updated = "WAITING", 0, datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
        st.error(f"서버 연결 실패: {e}")

    # 상태 표시
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
