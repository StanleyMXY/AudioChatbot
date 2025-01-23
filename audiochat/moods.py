from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from audiochat.prompts_cn import *

class Moods:
    def __init__(self):
        self.MOODS = {
            "default": {
                "role_set": "",
                "voice_set": "chat",
            },
            "friendly": {
                "role_set": ROLE_SET_FRIENDLY,
                "voice_set": "friendly",
            },
            "depressed": {
                "role_set": ROLE_SET_DEPRESSED,
                "voice_set": "customerservice",
            },
            "angry": {
                "role_set": ROLE_SET_ANGRY,
                "voice_set": "angry",
            },
            "excited": {
                "role_set": ROLE_SET_EXCITED,
                "voice_set": "excited",
            },
            "sad": {
                "role_set": ROLE_SET_SAD,
                "voice_set": "empathetic",
            },
            "cheerful": {
                "role_set": ROLE_SET_CHEERFUL,
                "voice_set": "cheerful",
            },
        }
        self.prompt = MOODS_PROMPT

    def get_role(self, llm: BaseChatModel, query):
        mood_chain = ChatPromptTemplate.from_template(self.prompt) | llm | StrOutputParser()
        mood = mood_chain.invoke({"query": query})
        role_set = self.MOODS[mood][("role_set")]
        voice_set = self.MOODS[mood][("voice_set")]
        return role_set, voice_set
