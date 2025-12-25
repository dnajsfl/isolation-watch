import streamlit as st
import pandas as pd
from datetime import datetime
import serial  # 추가: 아두이노 데이터를 읽기 위함
import time

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="고립사 예방 모니터링",
    layout="centered"
)

# =========================
# 시리얼 포트 설정 (본인의 포트 번호로 수정 필수!)
# =========================
@st.cache_resource
def get_serial_connection():
    # COM3 부분을 아두이노 IDE에서 확인한 포트 번호로 바꿔줘! (예: 'COM4', '/dev/ttyUSB0' 등)
    return serial.Serial('COM3', 115200, timeout=1)

try:
    ser = get_serial_connection()
except Exception as e:
    st.error(f"아두이노 연결 실패: {e}")
    ser = None

# =========================
# 세션 상태 초기화
# =========================
if "status" not in st.session_state:
    st.session_state.status = "active"

if "last_detected" not in st.session_state:
    st.session_state.last_detected = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if "today_count" not in st.session_state:
    st.session_state.today_count = 0

# =========================
# 제목 / 개요
# =========================
st.title("고립사 예방 생활 반응 모니터링")
st.info("실시간 아두이노 데이터가 연동 중입니다.")

# =========================
# 데이터 수신 및 로직 처리
# =========================
if ser:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        # 아두이노에서 보낸 "D:25,S:ACTIVE" 또는 "D:100,S:INACTIVE" 읽기
        if "S:" in line:
            status_part = line.split(",S:")[1]
            if status_part == "ACTIVE":
                if st.session_state.status == "inactive": # 위험에서 정상으로 바뀔 때만 카운트
                    st.session_state.today_count += 1
                st.session_state.status = "active"
                st.session_state.last_detected = datetime.now().strftime("%H:%M:%S")
            else:
                st.session_state.status = "inactive"

# =========================
# 상태 요약 박스
# =========================
st.subheader("현재 상태 요약")

if st.session_state.status == "active":
    st.success(f"🟢 정상 상태 (최근 감지: {st.session_state.last_detected})")
else:
    st.error("🔴 무활동 감지 (10초 이상 반응 없음)")

st.divider()

# =========================
# 핵심 지표
# =========================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("마지막 감지", st.session_state.last_detected)
with col2:
    st.metric("오늘 활동 횟수", st.session_state.today_count)
with col3:
    st.metric("시스템", "연결됨" if ser else "연결끊김")

# =========================
# 실시간 업데이트를 위한 자동 리프레시 (야매 팁)
# =========================
time.sleep(0.5)
st.rerun() # 화면을 계속 새로고침해서 아두이노 값을 반영해
