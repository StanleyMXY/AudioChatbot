import os

import dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor, tool
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationTokenBufferMemory, ConversationSummaryBufferMemory

from audiochat.prompts_cn import SYSTEM_PROMPT_FOR_FAIR_TALES
from audiochat.moods import Moods
from audiochat.tools import search_tool
from audiochat.voice_generator import Voice_generator

dotenv.load_dotenv()

os.environ['DASHSCOPE_API_KEY'] = 'sk-f2ffee508ad14054bbd0550634b8573b'

class AudioBot:
    def __init__(self):
        self.model = ChatTongyi(
            model_name="qwen-plus-latest",
            temperature=0.2,
            streaming=True,
        )
        self.role_set = ""
        self.voice_set = ""
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT_FOR_FAIR_TALES.format(role_set=self.role_set)),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        memory = ConversationSummaryBufferMemory(
            llm=self.model,
            memory_key="chat_history",
            output_key="output",
            return_messages=True,
            max_token_limit=1000,

        )
        tools = [search_tool]
        agent = create_tool_calling_agent(
            llm=self.model,
            tools=tools,
            prompt=self.prompt,
        )
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
        )

    def run(self, query):
        self.role_set, self.voice_set = Moods().get_role(self.model, query)
        print(f"当前情绪设定：{self.role_set}")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT_FOR_FAIR_TALES.format(role_set=self.role_set)),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        print(self.prompt.messages[0])
        response = self.agent_executor.invoke({"input": query})
        return response

