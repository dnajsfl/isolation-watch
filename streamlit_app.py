import streamlit as st

import pandas as pd

from datetime import datetime



# =========================

# 기본 설정

# =========================

st.set_page_config(

    page_title="고립사 예방 모니터링",

    layout="centered"

)



# =========================

# 세션 상태 초기화 (시연용)

# =========================

if "status" not in st.session_state:

    st.session_state.status = "active"  # active / inactive



if "last_detected" not in st.session_state:

    st.session_state.last_detected = datetime.now().strftime("%Y-%m-%d %H:%M:%S")



if "today_count" not in st.session_state:

    st.session_state.today_count = 2



# =========================

# 제목 / 개요

# =========================

st.title("고립사 예방 생활 반응 모니터링")



st.info(

    "본 웹앱은 독거 가구의 생활 반응 여부를 간접적으로 확인하여 "

    "고립 위험을 조기에 인지하는 것을 목표로 한 시연용 프로토타입이다.\n\n"

    "직접적인 생체 정보나 영상 감시는 사용하지 않으며, "

    "일정 시간 동안 반응이 없을 경우 주의 신호로 표시한다."

)



st.divider()



# =========================

# 상태 요약 박스 (핵심)

# =========================

st.subheader("현재 상태 요약")



if st.session_state.status == "active":

    st.success(

        "🟢 정상 상태\n\n"

        "- 최근 30초 이내 생활 반응 감지\n"

        "- 현재 위험 신호 없음"

    )

else:

    st.error(

        "🔴 무활동 감지\n\n"

        "- 30초 이상 반응 없음\n"

        "- 버저 작동 및 빨간 LED 점등\n"

        "- 서버 및 웹앱에 경고 기록 저장"

    )



st.caption(

    "※ 시연 기준: 30초 이상 초음파 센서 반응이 없을 경우 무활동 상태로 판단"

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

    st.metric("오늘 감지 횟수", st.session_state.today_count)



with col3:

    st.metric(

        "현재 상태",

        "정상" if st.session_state.status == "active" else "반응 없음"

    )



st.divider()



# =========================

# 생활 반응 기록 (시각화)

# =========================

st.subheader("오늘의 생활 반응 기록")



data = pd.DataFrame({

    "시간": ["09:00", "12:00", "15:00", "18:00"],

    "감지 여부": [1, 1, 0, 0]

})



st.line_chart(data.set_index("시간"))



st.divider()



# =========================

# 시연용 상태 변경 버튼

# =========================

st.subheader("시연용 상태 변경")



col_a, col_b = st.columns(2)



with col_a:

    if st.button("생활 반응 감지 (정상)"):

        st.session_state.status = "active"

        st.session_state.last_detected = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.session_state.today_count += 1



with col_b:

    if st.button("무활동 상황 발생"):

        st.session_state.status = "inactive"



st.caption(

    "※ 실제 환경에서는 초음파 센서(HC-SR04)의 입력에 따라 "

    "상태가 자동으로 갱신된다."

)



st.divider()



# =========================

# 프로젝트 구조 설명

# =========================

st.subheader("시스템 구성")



st.markdown(

    """

    **① 센서 모듈 (NodeMCU + HC-SR04)**  

    - 일정 시간 동안 움직임 감지 여부 판단  

    - 무활동 시 버저 및 LED로 1차 경고  



    **② 서버 / 웹앱**  

    - 상태 데이터 기록  

    - 보호자·관리자가 원격으로 확인 가능  



    **③ 웹 대시보드**  

    - 현재 상태 시각화  

    - 생활 반응 기록 그래프 제공

    """

)



st.divider()



# =========================
