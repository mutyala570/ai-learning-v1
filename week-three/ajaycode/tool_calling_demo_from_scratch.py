import json
import math
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq()

tools = [
    {
        "type": "function",
        "function": {
            "name": "square_root",
            "description": "Calculate the square root of a non-negative number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "number": {
                        "type": "number",
                        "description": "The non-negative number to take the square root of.",
                    }
                },
                "required": ["number"],
            },
        },
    }
]

def square_root(number: float) -> float:
    if number < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    return math.sqrt(number)

tool_map = {"square_root": square_root}

def chat_with_tools(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        temperature=0,
    )

    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls:
        for tc in message.tool_calls:
            fn_name = tc.function.name
            fn_args = json.loads(tc.function.arguments)
            result = tool_map[fn_name](**fn_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": str(result),
            })

        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0,
        )
        return final_response.choices[0].message.content
    else:
        return message.content


response_1 = chat_with_tools("What is the square root of 144?")
response_2 = chat_with_tools("What is the capital of France?")
response_3 = chat_with_tools("Can you calculate the square root of 2025 for me?")

print(response_1)
print(response_2)
print(response_3)
