import streamlit as st
from datetime import datetime

st.set_page_config(page_title="고립사 예방 모니터링", layout="centered")

# =========================
# 상태 저장소 (서버 메모리)
# =========================
if "status" not in st.session_state:
    st.session_state.status = "ACTIVE"

if "inactive_time" not in st.session_state:
    st.session_state.inactive_time = 0

if "last_update" not in st.session_state:
    st.session_state.last_update = "대기 중"

# =========================
# HTTP 수신 엔드포인트
# =========================
query = st.query_params

if "status" in query:
    st.session_state.status = query["status"]
    st.session_state.inactive_time = int(query.get("time", 0))
    st.session_state.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# =========================
# UI
# =========================
st.title("고립사 예방 생활 반응 모니터링")

if st.session_state.status == "ACTIVE":
    st.success("🟢 정상 상태\n\n최근 생활 반응이 감지되었습니다.")
else:
    st.error("🔴 무활동 감지\n\n일정 시간 이상 움직임이 없습니다.")

st.metric("무활동 지속 시간(초)", st.session_state.inactive_time)
st.caption(f"마지막 수신 시간: {st.session_state.last_update}")

st.divider()

st.caption(
    "※ 본 상태는 ESP8266이 WiFi를 통해 실시간 전송한 데이터에 의해 갱신된다."
)
