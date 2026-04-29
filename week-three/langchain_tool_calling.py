"""
LangChain Tool Calling Practice

Companion code file to `langchain-tool-calling-practice.md`.
Practice exercises from Week 3 class on LangChain's tool-calling API.

You'll get a (Pdb) prompt at the top of chat_with_tools. Step through with n, inspect with p message, p response, p response.tool_calls. Type q to exit, c to run to the end.  
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

@tool
def capital_city(country: str) -> str:
    """Return the capital city of a given country."""
    capitals = {
        "France": "Paris",
        "Spain": "Madrid",
        "Italy": "Rome",
        "Germany": "Berlin",
        "United Kingdom": "London",
        "United States": "Washington, D.C.",
        # Add more countries and their capitals as needed
        #i gave this india but that is not there in the tool but llm decided to call the tool which country not there in the tool how to stop thst
        #where we do instrect the llm to call the tool or give anser like this 
        # give the same function but with eu ,asia and check how llm decides to call the tool

        # do chaceh for the same quastion and answer if the same question comes again then it should give the answer from cache instead of calling the tool agian
    }
    return capitals.get(country, "Capital city not found")


def chat_with_tools(user_message: str):
   breakpoint()
   message = [HumanMessage(content=user_message)]
   
   # 1. MODEL DECIDES — Groq reads the question + tool list and returns either
   #    a text answer (response.content) or a tool-call request (response.tool_calls).
   response = llm_with_tools.invoke(message)
   message.append(response)

   if tool_calls := response.tool_calls:
       for tc in tool_calls:
            # 2. TOOL EXECUTES — your Python actually runs the function here.
            #    tool_map[tc["name"]] looks up `squere_root`; .invoke(tc["args"]) calls it with {"a": 16}.
            result = tool_map[tc["name"]].invoke(tc["args"])
            message.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))

       # 3. MODEL SYNTHESISES — second call to Groq with the tool result attached.
       #    Model now writes the natural-language answer (e.g. "The square root of 16 is 4.0").
       final_response = llm_with_tools.invoke(message).content
   else:
        final_response = response.content
   return final_response

tools = [squere_root, capital_city]
tool_map = {t.name: t for t in tools}

#system prompt can give here need to lookint to it
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# response_1 = chat_with_tools("What is the square root of 16?")
# print(response_1)
response_2  = chat_with_tools("what is the captal of india?")
print(response_2)
# response_3 = chat_with_tools("can you calculate the squre root of 2025 for me?")
# print(response_3)

