import streamlit as st
import openai
from dotenv import load_dotenv
import os
import time

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 페이지 설정
st.set_page_config(
    page_title="운세 채팅 서비스",
    page_icon="🔮",
    layout="wide"
)

# 타이틀과 설명
st.title("🔮 운세 채팅 서비스")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 초기 메시지 추가
    st.session_state.messages.append({
        "role": "assistant",
        "content": "안녕하세요! 어떤 방식으로 운세를 봐드릴까요?"
    })

# 운세 상담 시스템 프롬프트
SYSTEM_PROMPT = """당신은 전문적인 운세 상담사입니다. 
사용자의 생년월일과 시간을 바탕으로 사주팔자, 운세, 그리고 미래에 대한 조언을 제공해주세요.
답변은 친절하고 긍정적이며, 구체적인 조언을 포함해야 합니다.
단, 절대적으로 믿을 수 없는 예측은 피하고, 현실적인 조언을 제공해주세요."""

# 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 운세 유형 선택 버튼들
if len(st.session_state.messages) == 1:  # 초기 메시지만 있을 때만 선택지 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✨ 별자리 운세"):
            st.session_state.messages.append({"role": "user", "content": "별자리 운세를 보고 싶어요."})
            st.experimental_rerun()
    with col2:
        if st.button("🎋 사주팔자"):
            st.session_state.messages.append({"role": "user", "content": "사주팔자를 보고 싶어요."})
            st.experimental_rerun()
    with col3:
        if st.button("🎯 타로카드"):
            st.session_state.messages.append({"role": "user", "content": "타로카드로 운세를 보고 싶어요."})
            st.experimental_rerun()

# 사용자 입력
user_input = st.text_input("궁금하신 점을 입력해주세요:", key="user_input")

# 사용자 입력이 있을 경우 처리
if user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 로딩 메시지 표시
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("...")
        
        # AI 응답 생성
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content
            
            # 로딩 애니메이션
            for i in range(3):
                message_placeholder.markdown("..." * (i + 1))
                time.sleep(0.5)
            
            # 최종 응답 표시
            message_placeholder.markdown(ai_response)
            
            # AI 응답 추가
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.error(f"죄송합니다. 오류가 발생했습니다: {str(e)}")

# 사이드바에 추가 정보
with st.sidebar:
    st.header("📝 사용 방법")
    st.markdown("""
    1. 원하는 운세 유형을 선택해주세요
    2. 생년월일과 시간을 입력해주세요
    3. 궁금하신 점을 자유롭게 물어보세요
    4. AI가 상세한 운세를 알려드립니다
    """)
    
    st.header("⚠️ 주의사항")
    st.markdown("""
    - 이 서비스는 재미로만 참고해주세요
    - 중요한 인생 결정은 전문가와 상담하시기 바랍니다
    - 개인정보는 안전하게 보호됩니다
    """) 