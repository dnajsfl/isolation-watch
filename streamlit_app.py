import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="고립사 예방 모니터링", layout="centered")

# 1. 아두이노가 URL을 통해 보낸 데이터 가져오기 (예: ?status=ACTIVE&time=5)
query = st.query_params

# 2. 데이터가 들어왔을 때 세션에 저장 (새로고침해도 유지되도록)
if "status" in query:
    st.session_state["status"] = str(query["status"]).upper()
    st.session_state["time"] = query.get("time", "0")
    st.session_state["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 3. 화면에 표시할 값 설정 (기본값 세팅)
current_status = st.session_state.get("status", "WAITING")
inactive_sec = st.session_state.get("time", "0")
last_sync = st.session_state.get("last_update", "No Signal Yet")

# 4. UI 구성
st.title("👨‍🦳 실시간 어르신 안전 모니터링")

if "INACTIVE" in current_status:
    # 위험 상태 디자인
    st.error(f"🚨 위험 상황 발생! {inactive_sec}초간 무활동")
    st.metric(label="현재 상태", value="DANGER", delta=f"{inactive_sec}s", delta_color="inverse")
    st.markdown("<style>stApp {background-color: #ff4b4b;}</style>", unsafe_allow_html=True)
elif "ACTIVE" in current_status:
    # 정상 상태 디자인
    st.success(f"🟢 정상 활동 중 (최근 움직임: {inactive_sec}s 전)")
    st.metric(label="현재 상태", value="NORMAL", delta="Active")
    st.markdown("<style>stApp {background-color: #ffffff;}</style>", unsafe_allow_html=True)
else:
    st.info("⏳ 센서 신호를 기다리고 있습니다...")

st.divider()
st.caption(f"최종 데이터 수신 시간: {last_sync}")

# 5. 2초마다 자동 새로고침 (실시간 연동의 핵심)
time.sleep(2)
st.rerun()
