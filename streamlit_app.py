import streamlit as st
import pandas as pd
import time

# 1. 본인의 구글 시트 ID (확인 완료)
sheet_id = "1yPzX_ZG734XT_5G80TqNAxYjNdfpPQ4cKqDLPh7GkWk"
# 2. 구글 시트 CSV 주소 (캐시 방지를 위해 뒤에 파라미터 추가 가능)
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

st.set_page_config(page_title="고립사 예방 시스템", layout="centered")

st.title("👨‍🦳 실시간 어르신 안전 모니터링")

placeholder = st.empty()

while True:
    try:
        # 구글 시트에서 최신 데이터 읽기
        # 주소 뒤에 시간을 붙여서 매번 새로고침되게 함
        df = pd.read_csv(f"{csv_url}&t={time.time()}")
        
        # A2, B2 셀에서 상태와 시간 가져오기
        status = str(df.iloc[0, 0]).strip()
        last_update = str(df.iloc[0, 1]).strip()
        
        with placeholder.container():
            if "Danger" in status:
                st.error("🚨 위험: 현재 움직임이 감지되지 않습니다!")
                st.metric(label="현재 상태", value="DANGER", delta="-위험 발생", delta_color="inverse")
            else:
                st.success("🟢 정상: 어르신이 활동 중입니다.")
                st.metric(label="현재 상태", value="NORMAL", delta="정상 활동")
            
            st.info(f"마지막 신호 확인 시간: {last_update}")
                
    except Exception as e:
        st.warning("데이터 동기화 중... (구글 시트 게시를 확인해주세요)")
        
    time.sleep(3) # 3초마다 업데이트
    st.rerun()
