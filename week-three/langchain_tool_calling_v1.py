"""
LangChain Tool Calling — v1 (class demo reference).

Use this as the canonical version to follow along in class.
Compare against `langchain_tool_calling.py` later to spot mistakes.
"""

import math
import os
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()


@tool
def square_root(number: float) -> float:
    """Calculate the square root of a non-negative number."""
    if number < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    return math.sqrt(number)


tools = [square_root]
tool_map = {t.name: t for t in tools}

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
llm_with_tools = llm.bind_tools(tools)


def chat_with_tools(user_message: str) -> str:
    messages = [HumanMessage(content=user_message)]

    response = llm_with_tools.invoke(messages)
    messages.append(response)

    if response.tool_calls:
        for tc in response.tool_calls:
            result = tool_map[tc["name"]].invoke(tc["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
        final_response = llm_with_tools.invoke(messages).content
    else:
        final_response = response.content

    return final_response


if __name__ == "__main__":
    print(chat_with_tools("What is the square root of 144?"))
    print(chat_with_tools("What is the capital of France?"))
    print(chat_with_tools("Can you calculate the square root of 2025 for me?"))
