import os
import asyncio
import requests
import streamlit as st

st.title("毛大福讲故事")

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

if query := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").markdown(query)
    try:
        response = requests.post("http://127.0.0.1:8000/chat?query="+query, timeout=120)
        if response.status_code == 200:
            response_json = response.json()
            st.session_state.messages.append(
                {"role": "ai", "content": response_json["msg"]["output"]}
            )
            st.chat_message("ai").markdown(response_json["msg"]["output"])
            audio_resp = requests.post(f"http://127.0.0.1:8000/download/{response_json["id"]}.mp3", timeout=300)
            if audio_resp.status_code == 200:
                with open(f'audio/{response_json["id"]}.mp3', 'wb') as f:
                    f.write(audio_resp.content)
            else:
                st.error("服务器连接失败，请稍后再试")
            asyncio.run(check_audio(f'audio/{response_json["id"]}.mp3'))
            requests.post(f"http://127.0.0.1:8000/remove/{response_json["id"]}.mp3")
        else:
            st.error("服务器连接失败，请稍后再试")
    except requests.exceptions.ConnectionError as e:
        print(e)
        st.error("服务器连接失败，请稍后再试")

