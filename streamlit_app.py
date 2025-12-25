import streamlit as st
import pandas as pd
import serial
from datetime import datetime

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="고립사 예방 모니터링",
    layout="centered"
)

# =========================
# 시리얼 연결
# =========================
SERIAL_PORT = "COM3"   # ⚠ 네 환경에 맞게 수정
BAUD_RATE = 115200

if "ser" not in st.session_state:
    st.session_state.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# =========================
# 상태 저장용 세션
# =========================
if "status" not in st.session_state:
    st.session_state.status = "WAITING"

if "inactive_time" not in st.session_state:
    st.session_state.inactive_time = 0

if "last_detected" not in st.session_state:
    st.session_state.last_detected = "-"

# =========================
# 시리얼 데이터 읽기
# =========================
ser = st.session_state.ser

if ser.in_waiting:
    line = ser.readline().decode().strip()

    # 예: S:INACTIVE|12
    if "|" in line:
        state, t = line.split("|")
        st.session_state.status = state
        st.session_state.inactive_time = int(t)

        if state == "S:ACTIVE":
            st.session_state.last_detected = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# =========================
# 제목 / 개요
# =========================
st.title("고립사 예방 생활 반응 모니터링")

st.info(
    "본 웹앱은 독거 가구의 생활 반응 여부를 간접적으로 확인하여 "
    "고립 위험을 조기에 인지하는 것을 목표로 한 실시간 프로토타입이다.\n\n"
    "초음파 센서 기반 움직임 감지를 활용하며, "
    "일정 시간 무반응 시 위험 상태로 전환된다."
)

st.divider()

# =========================
# 현재 상태 요약
# =========================
st.subheader("현재 상태 요약")

if st.session_state.status == "S:ACTIVE":
    st.success(
        "🟢 정상 상태\n\n"
        "- 최근 생활 반응 감지됨\n"
        "- 현재 위험 신호 없음"
    )
elif st.session_state.status == "S:INACTIVE":
    st.error(
        "🔴 무활동 감지\n\n"
        "- 일정 시간 이상 반응 없음\n"
        "- 버저 및 빨간 LED 작동\n"
        "- 웹 대시보드 경고 표시"
    )
else:
    st.warning("⏳ 센서 데이터 대기 중")

st.caption(
    "※ 판단 기준: 설정된 시간 이상 초음파 센서 반응 없음"
)

st.divider()

# =========================
# 핵심 지표
# =========================
st.subheader("핵심 지표")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("마지막 감지 시간", st.session_state.last_detected)

with col2:
    st.metric("무활동 지속 시간(초)", st.session_state.inactive_time)

with col3:
    st.metric(
        "현재 상태",
        "정상" if st.session_state.status == "S:ACTIVE" else "반응 없음"
    )

st.divider()

# =========================
# 시스템 구성 설명
# =========================
st.subheader("시스템 구성")

st.markdown(
    """
    **① 센서 모듈 (NodeMCU + HC-SR04)**  
    - 움직임 변화 감지  
    - 무활동 시 LED·버저 경고  

    **② 로컬 서버 (Streamlit)**  
    - 시리얼 통신으로 상태 수신  
    - 실시간 상태 분석  

    **③ 웹 대시보드**  
    - 정상 / 무활동 상태 시각화  
    - 보호자·관리자 확인 가능
    """
)

st.caption(
    "본 시스템은 고립사 예방을 위한 기술적 가능성을 탐구하는 교육용 프로토타입이다."
)
