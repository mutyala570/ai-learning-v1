"""
LangChain Tool Calling Practice

Companion code file to `langchain-tool-calling-practice.md`.
Practice exercises from Week 3 class on LangChain's tool-calling API.
"""

import json
import math
import os
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

@tool
def squere_root(a: int) -> float:
    """Calculate the square root of non negative numbers."""
    if a < 0:
        raise ValueError("Input must be a non negative number")
    return math.sqrt(a)

def chat_with_tools(user_message: str):
   message = [HumanMessage(content=user_message)]
   
   response = llm_with_tools.invoke(message)
   message.append(response)

   if tool_calls := response.tool_calls:
       for tc in tool_calls:
            result = tool_map[tc["name"]].invoke(tc["args"])
            message.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))

       final_response = llm_with_tools.invoke(message).content
   else:
        final_response = response.content
   return final_response

tools = [squere_root]
tool_map = {t.name: t for t in tools}

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
llm_with_tools = llm.bind_tools(tools)

response_1 = chat_with_tools("What is the square root of 16?")
print(response_1)
response_2 = chat_with_tools("what is the captal of France?")
print(response_2)
response_3 = chat_with_tools("can you calculate the squre root of 2025 for me?")
print(response_3)

