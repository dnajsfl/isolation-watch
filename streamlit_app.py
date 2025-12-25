import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="고립사 예방 모니터링",
    layout="centered"
)

# =========================
# 세션 상태
# =========================
if "status" not in st.session_state:
    st.session_state.status = "active"
    st.session_state.logs = []

# =========================
# URL에서 아두이노 신호 받기
# =========================
query_params = st.query_params
if "status" in query_params:
    incoming = query_params["status"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if incoming in ["active", "inactive"]:
        st.session_state.status = incoming
        st.session_state.logs.append({
            "시간": now,
            "상태": "정상" if incoming == "active" else "무활동 감지"
        })

# =========================
# 화면 표시
# =========================
st.title("고립사 예방 생활 반응 모니터링")

if st.session_state.status == "active":
    st.success("정상: 생활 반응이 감지되었습니다.")
else:
    st.error("⚠ 일정 시간 동안 생활 반응이 없습니다.")

st.divider()

st.subheader("상태 요약")
st.metric("현재 상태", "정상" if st.session_state.status=="active" else "무활동")

st.divider()

st.subheader("감지 기록")
if st.session_state.logs:
    df = pd.DataFrame(st.session_state.logs)
    st.dataframe(df, use_container_width=True)
else:
    st.caption("기록 없음")

st.caption("아두이노 초음파 센서 기반 시연용 프로토타입")
