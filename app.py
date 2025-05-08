import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# 페이지 설정 (반드시 첫 번째 st 명령어여야 함)
st.set_page_config(
    page_title="운세 챗봇",
    page_icon="🔮",
    layout="centered"
)

# OpenAI API 키 로드 (오류 처리 추가)
try:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.warning("환경 변수에 OPENAI_API_KEY가 설정되지 않았습니다.")
        api_key = "sk-demo-key"  # 데모용 키 (실제로 작동하지 않음)
except Exception as e:
    st.warning(f"환경 변수 로드 중 오류가 발생했습니다: {e}")
    api_key = "sk-demo-key"  # 데모용 키 (실제로 작동하지 않음)

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요 어떤 방식으로 운세를 봐드릴까요?"}
    ]

if "show_options" not in st.session_state:
    st.session_state.show_options = True

if "waiting_for_input" not in st.session_state:
    st.session_state.waiting_for_input = False

if "fortune_type" not in st.session_state:
    st.session_state.fortune_type = None

# 운세 유형에 따른 시스템 메시지 정의
system_messages = {
    "별자리 운세": "당신은 별자리 운세를 전문적으로 봐주는 점성술사입니다. 사용자의 별자리에 대한 정보를 분석하여 운세, 성격, 대인관계, 직업 등에 대한 통찰력 있는 답변을 제공해주세요. 사용자가 별자리를 언급하지 않았다면, 먼저 별자리가 무엇인지 물어보세요."
}

# 기본 시스템 메시지
default_system_message = "당신은 별자리 운세를 전문적으로 봐주는 점성술사입니다. 사용자의 질문에 대해 운세와 관련된 통찰력 있는 답변을 제공해주세요."

# 챗봇 응답 함수
def get_fortune_response(messages):
    try:
        # 선택된 운세 유형에 따른 시스템 메시지 설정
        fortune_type = st.session_state.fortune_type
        system_msg = system_messages.get(fortune_type, default_system_message)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                *messages
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"죄송합니다, 오류가 발생했습니다: {str(e)}"

# 옵션 선택 함수
def handle_option_click(option):
    st.session_state.messages.append({"role": "user", "content": option})
    st.session_state.show_options = False
    st.session_state.waiting_for_input = True
    st.session_state.fortune_type = option
    
    # 사용자 선택 후 바로 응답 생성
    response = get_fortune_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})

# CSS 스타일 적용
st.markdown("""
<style>
    .fortune-option {
        margin: 5px;
    }
    /* 옵션 버튼 스타일 수정 */
    .stButton>button {
        width: auto !important;
        padding: 5px 10px !important;
        border-radius: 20px;
        background-color: #f0f0f0;
        color: #333;
        font-weight: bold;
        font-size: 0.8rem !important;
        transition: background-color 0.3s;
        position: relative;
        margin-left: 5px;
        margin-bottom: 2px;
    }
    .stButton>button:hover {
        background-color: #e0e0e0;
    }
    /* 버튼 컨테이너 위치 조정 */
    .option-container {
        position: relative;
        margin-bottom: -10px;
        text-align: left;
    }
    /* 알림 스타일 */
    .notice {
        margin-top: -5px;
        margin-bottom: 20px;
        color: #666;
        font-size: 0.9rem;
        font-style: italic;
    }
    /* 구분선 스타일 */
    .divider {
        margin: 20px 0;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# 애플리케이션 제목 표시
st.title("🔮 운세 챗봇")

# 서비스 안내 문구 (제목 바로 아래)
st.markdown('<p class="notice">🔮 이 서비스는 참고용으로만 사용하시기 바랍니다.</p>', unsafe_allow_html=True)

# 구분선
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 옵션 버튼 표시
if st.session_state.show_options:
    st.markdown('<div class="option-container">', unsafe_allow_html=True)
    if st.button("별자리 운세", key="zodiac", help="별자리 운세 보기"):
        handle_option_click("별자리 운세")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 사용자 입력 처리
if st.session_state.waiting_for_input or not st.session_state.show_options:
    user_input = st.chat_input("무엇이 궁금하신가요?")
    if user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.write(user_input)
        
        # 챗봇 응답 생성
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = get_fortune_response(st.session_state.messages)
            message_placeholder.write(full_response)
        
        # 챗봇 메시지 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.waiting_for_input = True
        st.rerun()