# LangChain Tool Calling — Code Explained

A line-by-line explanation of `langchain_tool_calling.py` so future me can re-read the file and remember what each part is doing. All line numbers refer to the current state of the `.py` file as of 2026-04-29.

## Topics Covered in This Document

1. [**What the File Does**](#1-what-the-file-does)
2. [**The Two Tools**](#2-the-two-tools)
3. [**The Tool-Calling Loop — Three Key Lines**](#3-the-tool-calling-loop--three-key-lines)
4. [**How the LLM Knows the Tools Exist**](#4-how-the-llm-knows-the-tools-exist)

---

# 1. What the File Does

The file defines two **tools** (a square-root function and a country-to-capital lookup), wraps them with the LangChain `@tool` decorator so the LLM can see their signatures, binds them to a Groq Llama model, and runs a `chat_with_tools` loop where the model decides whether to use a tool, your code executes the tool, and the model writes the final answer using the result.

Three things happen in sequence: **define tools** (lines 21–45), **wire them into the LLM** (lines 71–76), and **run the chat loop** (lines 48–69).

---

# 2. The Two Tools

## `squere_root` (lines 21–26)

A function that takes one integer `a`, raises `ValueError` if it is negative, otherwise returns `math.sqrt(a)`. The `@tool` decorator on line 21 turns this plain function into a LangChain `StructuredTool` — auto-generating a JSON Schema from the type hint (`a: int`) and pulling the description from the docstring.

## `capital_city` (lines 28–45)

A function that takes a country name and returns its capital from a small in-memory dict. Currently knows: France, Spain, Italy, Germany, United Kingdom, United States. For any other country the dict's `.get(country, "Capital city not found")` returns the fallback string. Same `@tool` decoration as `squere_root`.

> The TODO comments inside this function (lines 39–43) capture next-practice ideas — handling out-of-list countries, system prompt usage, adding regional versions, and caching repeated calls. Those are exploration tasks, not part of the current code's behaviour.

---

# 3. The Tool-Calling Loop — Three Key Lines

Inside `chat_with_tools` (lines 48–69), three lines do the actual work. Everything else is plumbing.

| # | Line | Code | What happens | Who does it |
|---|------|------|--------------|-------------|
| 1 | 54 | `response = llm_with_tools.invoke(message)` | Model reads question + tool list and returns either text content or a tool-call request | **Groq (LLM)** |
| 2 | 61 | `result = tool_map[tc["name"]].invoke(tc["args"])` | Your Python actually runs the chosen tool function | **Your code** |
| 3 | 66 | `final_response = llm_with_tools.invoke(message).content` | Model receives the tool result and writes the natural-language answer | **Groq (LLM)** |

## Step 1 — Model Decides (line 54)

Sends the user's message and the bound tool definitions to Groq. The model returns an `AIMessage` with two fields that matter: `content` (text answer) and `tool_calls` (list of tool requests). For *"square root of 16"*, `content` is empty and `tool_calls` has one entry. For *"capital of France"* — assuming the model recognises `capital_city` is the right tool — `tool_calls` has one entry pointing to that tool.

## Step 2 — Tool Executes (line 61)

The `if tool_calls := response.tool_calls:` walrus on line 57 captures the list and tests whether it's non-empty. If yes, the loop on line 58 iterates over each tool call. Inside the loop, line 61 looks up the tool by name in `tool_map` (line 72) and invokes it with the args dict (`{"a": 16}` for square root, `{"country": "France"}` for capital). Line 62 wraps the return value in a `ToolMessage` and appends it to the conversation, with `tool_call_id` matching the original request so the model knows which result corresponds to which call.

## Step 3 — Model Synthesises (line 66)

The conversation now contains three messages: the original `HumanMessage`, the `AIMessage` with the tool-call request, and the `ToolMessage` with the result. Line 66 sends this whole conversation back to Groq. The model uses the result to generate the final natural-language answer (e.g. *"The square root of 16 is 4.0"* or *"The capital of France is Paris."*). `.content` extracts just the text.

If `response.tool_calls` was empty in step 1 (the model decided no tool was needed — e.g. *"What is 2+2"*), the `else` branch on line 67 short-circuits straight to `response.content` without calling Groq a second time.

---

# 4. How the LLM Knows the Tools Exist

The model never sees your Python code — it only sees a JSON Schema description of each tool that LangChain generates from the `@tool` decoration. Three pieces of metadata get extracted and shipped to Groq with every API call.

## What gets extracted

1. **Function name** — `squere_root` or `capital_city` (taken from `def <name>(...)`).
2. **Description** — the docstring's first line. *"Calculate the square root of non negative numbers."* and *"Return the capital city of a given country."*
3. **Parameter schema** — auto-built from the type hints. `a: int` becomes `{"a": {"type": "integer"}}`, marked as required.

## What the model receives

For each tool, Groq sees a structured definition that looks like this (paraphrased):

```json
{
  "name": "squere_root",
  "description": "Calculate the square root of non negative numbers.",
  "parameters": {
    "type": "object",
    "properties": { "a": { "type": "integer" } },
    "required": ["a"]
  }
}
```

This is what the model uses to decide *"does any tool fit this question?"*. The `description` is the load-bearing field — if the docstring is vague (e.g. `"""does math"""`), the model often picks the wrong tool or none at all. The docstring is literally the model's user manual.

## How `bind_tools` wires this up

Line 76 (`llm_with_tools = llm.bind_tools(tools)`) creates a new model object that includes those JSON Schemas in every API call automatically. That is why the `prompt_tokens` count in `response_metadata` is so much higher than the user's question alone — most of those tokens are the tool schemas being injected invisibly into every prompt.

If you ever want to confirm what the model actually sees, print the schema directly:

```python
print(squere_root.args_schema.model_json_schema())
print(capital_city.args_schema.model_json_schema())
```

Run that once and you'll see the exact structure the model is reasoning over.
