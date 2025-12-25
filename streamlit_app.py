import streamlit as st
import requests
import time

st.set_page_config(page_title="고립사 예방 모니터링")

SERVER_URL = "https://isolation-watch.onrender.com/data"


st.title("고립사 예방 실시간 모니터링")

placeholder = st.empty()

while True:
    data = requests.get(SERVER_URL).json()

    with placeholder.container():
        if data["status"] == "ACTIVE":
            st.success("🟢 정상 상태")
        elif data["status"] == "INACTIVE":
            st.error("🚨 무활동 감지")
        else:
            st.warning("대기 중")

        st.metric("무활동 시간(초)", data["time"])
        st.caption(f"마지막 갱신: {data['updated']}")

    time.sleep(2)
