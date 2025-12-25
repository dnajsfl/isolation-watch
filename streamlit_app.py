import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="고립사 예방 모니터링", layout="centered")

# 1. 아두이노가 보낸 데이터 가져오기
# URL 파라미터(?status=...&time=...)를 읽음
query = st.query_params

# 2. 데이터가 들어왔을 때만 세션에 저장 (휘발 방지)
if "status" in query:
    st.session_state["status"] = query["status"]
    st.session_state["time"] = query.get("time", "0")
    st.session_state["last_update"] = datetime.now().strftime("%H:%M:%S")

# 3. 화면에 표시할 기본값 설정
current_status = st.session_state.get("status", "Waiting...")
inactive_sec = st.session_state.get("time", "0")
last_sync = st.session_state.get("last_update", "No Signal")

# 4. UI 디자인 (에러 없이 깔끔하게!)
st.title("👨‍🦳 실시간 고립사 예방 시스템")

if "INACTIVE" in current_status.upper():
    st.error(f"🚨 위험: 무활동 감지! ({inactive_sec}초째 멈춤)")
    st.markdown("<style>stApp {background-color: #ff4b4b; color: white;}</style>", unsafe_allow_html=True)
elif "ACTIVE" in current_status.upper():
    st.success(f"🟢 정상: 활동 중 (최근 움직임: {inactive_sec}s 전)")
    st.markdown("<style>stApp {background-color: #ffffff;}</style>", unsafe_allow_html=True)
else:
    st.info("⏳ 아두이노의 신호를 기다리는 중입니다...")

st.divider()
st.write(f"⏱ 마지막 통신 시간: {last_sync}")

# 5. 자동 새로고침 (2초마다 화면을 다시 그려서 아두이노 신호 반영)
time.sleep(2)
st.rerun()
