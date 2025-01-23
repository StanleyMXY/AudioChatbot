import json
import os
import asyncio
import requests
import streamlit as st
import speech_recognition as sr
from vosk import Model

st.title("毛大福讲故事 :blue[棒棒哒!] :sunglasses:")

with st.sidebar:
    audio_input = st.audio_input(
        label="请讲话",
        label_visibility="visible",
        help="按麦克风按钮开始录制声音",
    )

text_input = st.chat_input("请输入问题")

async def check_audio(audio_path: str):
    while True:
        if os.path.exists(audio_path):
            st.audio(audio_path, format="audio/mpeg", autoplay=True)
            st.session_state.messages.append(
                {"role": "audio", "content": audio_path}
            )
            break
        else:
            await asyncio.sleep(1)


def do_process(query: str):
    if query != "":
        try:
            response = requests.post("http://0.0.0.0:8000/chat?query="+query, timeout=120)
            if response.status_code == 200:
                response_json = response.json()
                st.session_state.messages.append(
                    {"role": "ai", "content": response_json["msg"]["output"]}
                )
                st.chat_message("ai").markdown(response_json["msg"]["output"])
                audio_resp = requests.post(f"http://0.0.0.0:8000/download/{response_json["id"]}.mp3", timeout=300)
                if audio_resp.status_code == 200:
                    with open(f'audio/{response_json["id"]}.mp3', 'wb') as f:
                        f.write(audio_resp.content)
                else:
                    st.error("download服务器连接失败，请稍后再试")
                asyncio.run(check_audio(f'audio/{response_json["id"]}.mp3'))
                requests.post(f"http://0.0.0.0:8000/remove/{response_json["id"]}.mp3")
            else:
                st.error("chat服务器连接失败，请稍后再试")
        except requests.exceptions.ConnectionError as e:
            print(e)
            st.error("exception服务器连接失败，请稍后再试")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown(
    """
    <style>
        .st-emotion-cache-1c7y2kd {
            flex-direction: row-reverse;
            text-align: right;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    elif message["role"] == "ai":
        st.chat_message("ai").markdown(message["content"])
    elif message["role"] == "audio":
        st.audio(message["content"], format="audio/mpeg")


if audio_input:
    try:
        r = sr.Recognizer()
        r.vosk_model = Model(model_path='models/vosk-model-small-cn-0.22', model_name='vosk-model-small-cn-0.22')
        with sr.AudioFile(audio_input) as source:
            audio = r.record(source)
        text = r.recognize_vosk(audio, language="zh-CN")
        query = json.loads(text)["text"].replace(" ", "")
        st.session_state.messages.append({"role": "user", "content": query})
        st.chat_message("user").markdown(query)
        # st.audio(audio_input, format="audio/mpeg")
    except Exception as e:
        print(e)
        st.error("语音识别失败，请重试")
    do_process(query)

elif text_input:
    st.session_state.messages.append({"role": "user", "content": text_input})
    st.chat_message("user").markdown(text_input)
    do_process(text_input)



