import streamlit as st
import os
from datetime import datetime

STATUS_FILE = "status.txt"

# 🔴 ESP 전용 엔드포인트
query = st.query_params
if "update" in query:
    status = query.get("status", "UNKNOWN")
    time = query.get("time", "0")

    with open(STATUS_FILE, "w") as f:
        f.write(f"{status},{time},{datetime.now()}")

    st.stop()  # 여기서 UI 렌더링 안 하고 종료 (중요!)

# 🟢 일반 사용자 UI
st.set_page_config(page_title="실시간 모니터링")
st.title("실시간 안전 상태")

if os.path.exists(STATUS_FILE):
    with open(STATUS_FILE) as f:
        status, time, last = f.read().split(",")
else:
    status, time, last = "UNKNOWN", "-", "-"

if status == "ACTIVE":
    st.success("🟢 정상 상태")
elif status == "INACTIVE":
    st.error("🚨 위험 상태")
else:
    st.warning("대기 중")

st.info(f"무활동 시간: {time}초")
st.caption(f"마지막 수신: {last}")

st.autorefresh(interval=2000)
