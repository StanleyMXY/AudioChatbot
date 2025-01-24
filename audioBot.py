import json
import os
import asyncio
import uuid

import requests
import streamlit as st
import speech_recognition as sr
from vosk import Model

from audiochat.agents import AudioBot
from audiochat.voice_generator import Voice_generator

audio_bot = AudioBot()
voice_gen = Voice_generator()

st.set_page_config(
    page_title="毛大福讲故事",
    page_icon=":book:",
    layout="wide",
)

st.title("毛大福讲故事 :blue[棒棒哒!] :sunglasses:")

with st.sidebar:
    audio_input = st.audio_input(
        label="请讲话",
        label_visibility="visible",
        help="按麦克风按钮开始录制声音",
    )

text_input = st.chat_input("请输入问题")

# async def check_audio(audio_path: str):
#     while True:
#         if os.path.exists(audio_path):
#             st.audio(audio_path, format="audio/mpeg", autoplay=True)
#             st.session_state.messages.append(
#                 {"role": "audio", "content": audio_path}
#             )
#             break
#         else:
#             await asyncio.sleep(1)

def do_process(query: str):
    if query != "":
        try:
            response = audio_bot.run(query)
            st.session_state.messages.append(
                 {"role": "ai", "content": response["output"]}
            )
            st.chat_message("ai").markdown(response["output"])
            try:
                unique_id = uuid.uuid4()
                voice_gen.set_voice_set(audio_bot.voice_set)
                voice_gen.background_voice_systhesis(response["output"], unique_id)
                audio_path = f'{unique_id}.mp3'
                if os.path.exists(audio_path):
                    st.audio(audio_path, format="audio/mpeg", autoplay=True)
                    st.session_state.messages.append(
                        {"role": "audio", "content": audio_path}
                    )
                else:
                    st.error("语音合成失败，请重试")
            except Exception as e:
                print(e)
                st.error("语音合成失败：", e)
            # asyncio.run(check_audio(f'audio/{response_json["id"]}.mp3'))
        except requests.exceptions.ConnectionError as e:
            print(e)
            st.error("生成回复失败：", e)

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



