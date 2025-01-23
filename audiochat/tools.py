import os

from langchain_core.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper

os.environ["SERPER_API_KEY"] = "47feb2e7e7cb21054815ad84b4e8a2c7bd309458"

@tool
def search_tool(query: str) -> str:
    """This tool is only used when you need to know real-time information."""
    gserp = GoogleSerperAPIWrapper()
    result = gserp.run(query)
    print("搜索结果：", result)
    return result

@tool
def get_knowledge_base(query: str) -> str:
    """This tool is only used when you need to know real-time information."""
    return "搜索结果：" + query