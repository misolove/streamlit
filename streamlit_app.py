# !pip install streamlit_chat

import streamlit as st
from streamlit_chat import message
import requests
import json

# 사용자 정의 CSS
st.markdown("""
<style>
body {
    color: #fff;
    background-color: #0E1117;
}
.stTextInput>label, .stButton>label {
    color: #4DD0E1;
}
.stTextInput>div>div>input {
    color: #000;
}
.stButton>button {
    color: #000;
}
</style>
""", unsafe_allow_html=True)

# Display the GIF with animation
gif_url = "/workspaces/streamlit-example/scaled_animation.gif"  # Replace with your GIF URL
st.image(gif_url, width=80)  # 필요에 따라 너비를 조정하세요
# st.markdown(f'<img src="{gif_url}" class="moving-gif">', unsafe_allow_html=True)

st.header("🤖 Q&A ChatBot ---^- 아웃라이어 ---^---")

# Custom CSS for animation
st.markdown("""
<style>
@keyframes move {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
.moving-gif {
    animation: move 10s linear infinite;
}
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

# 서버에 요청을 보내는 함수
def query(payload):
    response = requests.post('http://8d8c-35-196-203-176.ngrok.io/compute', json=payload)
    try:
        return response.json()
    except json.JSONDecodeError:
        st.error("잘못된 응답 형식.")
        return {"error": "잘못된 응답 형식"}

# 사용자 입력 폼
with st.form('form', clear_on_submit=True):
    user_input = st.text_input('질문을 입력해주세요:', '', key='input')
    submitted = st.form_submit_button('제출')

# 폼 제출 처리
if submitted and user_input:
    # 요청 데이터 준비
    payload = {
        "question": user_input,
        "past_user_inputs": st.session_state.past,
        "generated_responses": st.session_state.generated
    }

    # 서버에 요청
    output = query(payload)
    data = output.get("answer")
    print(data)
    # 응답 처리
    if 'error' not in data:
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output.get("answer"))

# 대화 내용 표시
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state['generated'][i], key=str(i))

