import asyncio

import requests

from audiochat.moods import Moods

msskey = ""

class Voice_generator:
    def __init__(self) :
        self.voice_set = "chat"
        pass

    def set_voice_set(self, voice_set: str) :
        self.voice_set = voice_set

    async def get_voice(self, text: str, uid: str) :
            print("voice style: ", self.voice_set)
            # use MS TTS to generate voice
            headers = {
                "Ocp-Apim-Subscription-Key": msskey,
                "Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": "audio-24khz-48kbitrate-mono-mp3",
                "User-Agent": "Dafu's Bot",
            }
            body = f"""
            <speak version='1.0' xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang='zh-CN'>
                <voice xml:lang='zh-CN' xml:gender='Female' name='zh-CN-XiaoshuangNeural'>
                    <mstts:express-as role='Girl' style='{self.voice_set}'>
                        {text}
                    </mstts:express-as>
                </voice>
            </speak>
            """
            # send request
            try:
                response = requests.post(
                    "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1",
                    headers=headers,
                    data=body.encode("utf-8")
                )
                print("status: ", response.status_code)
                if response.status_code == 200:
                    # save voice to file
                    with open(f"{uid}.mp3", "wb") as f:
                        f.write(response.content)
                else:
                    print("error: connection status error")
            except Exception as e:
                print("error: ", e)

    def background_voice_systhesis(self, text: str, uid: str) :
        # no return, just launch a voice systhesis task
        asyncio.run(self.get_voice(text, uid))
