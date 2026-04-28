# Python Fast Track for Existing Developers (AI Engineer Edition)

A 2-week path from "I'm a developer new to Python" to "I can write AI / agent code." Designed for someone who already knows loops, conditions, classes, and error handling from another language. Skips conceptual basics, drills Python-specific idioms, and front-loads the AI-shaped parts (async, Pydantic, decorators).

> **Total time:** ~20 hours over 2 weeks. After this, you can jump straight into P1 (FastAPI) and P2 (LangChain) without finishing every numbered file in `learn-python/`.

## Topics Covered in This Document

1. [**The Core Principle**](#the-core-principle)
2. [**What to Skip or Skim**](#what-to-skip-or-skim)
3. [**Python-Specific Idioms You Must Learn**](#python-specific-idioms-you-must-learn)
4. [**AI Engineer Essentials Beyond Basics**](#ai-engineer-essentials-beyond-basics)
5. [**Week 1 — Python-Specific Essentials**](#week-1--python-specific-essentials)
6. [**Week 2 — AI-Shaped Python**](#week-2--ai-shaped-python)
7. [**After 2 Weeks — Where to Go Next**](#after-2-weeks--where-to-go-next)
8. [**Self-Check — Are You Ready to Move On**](#self-check--are-you-ready-to-move-on)

---

## The Core Principle

You already know what variables, loops, functions, and classes are. You do not need to relearn those concepts — you only need their Python syntax. The things that actually slow down experienced developers when moving to Python are the **idioms** (the "Pythonic" way to do things) and the **ecosystem** (libraries like Pydantic, FastAPI, LangChain that have their own conventions).

> **Skip what you already know conceptually. Drill what's Python-specific. Then drill what's AI-specific.**

That single sentence is the whole strategy. Everything below is just the breakdown of what to skip, what to drill, and in what order.

---

## What to Skip or Skim

You can read these in **one evening** — they are just syntax for ideas you already know from other languages. Skim, do not drill.

### From `learn-python/*.py` files
- `01_basics.py` — variables, primitive types, f-strings (you know these)
- `02_collections.py` — list, tuple, set, dict (you know these as arrays/maps)
- `03_control_flow.py` — `if/else`, `for`, `while` (universal); pay attention only to **list comprehensions**
- `05_exceptions.py` — `try/except` (same as `try/catch`)
- `06_file_io.py` — read/write files (universal); pay attention only to **`with` statement**
- `07_oop_basics.py`, `08_oop_inheritance.py` — classes (you know these); pay attention only to `__init__` vs `__new__` and dunder methods like `__str__`, `__repr__`, `__eq__`

### From `python-small-concepts.md`
- Topic 8 — String methods (same as any language)
- Topic 15 — Slicing (`s[1:5]`)
- Topic 16 — `in` operator
- Topic 8 — Ternary expression (`x if cond else y`)
- Topic 18 — `sorted()` vs `.sort()`
- Topic 23 — Common built-ins (`len`, `sum`, `min`, `max`, `range`)
- Topic 24 — Type conversion functions (`int()`, `str()`, etc.)

These are universal-developer-knowledge dressed in Python syntax.

---

## Python-Specific Idioms You Must Learn

These are the things even strong developers trip on when they first move to Python. Learn them properly — they are not skippable.

| Idiom | Where it lives | Why it matters |
|-------|----------------|----------------|
| `*args` and `**kwargs` | Topic 1 in `python-small-concepts.md` | Used in every framework function signature |
| List / dict / set comprehensions | Topic 7 | The Pythonic way to transform data |
| `typing.Literal` + type hints | Topic 3 | Critical for LLM tool schemas and intent typing |
| Truthiness rules | Topic 5 | Replaces `== null` / `=== undefined` checks from JS-land |
| `dict.get(key, default)` pattern | Topic 6 | Replaces null-check ceremonies elsewhere |
| Decorators (`@something`) | `12_decorators.py` | Foundation for `@tool`, `@app.post`, `@property` |
| `with` / context managers | `06_file_io.py` | Cleanest pattern for file I/O, DB connections |
| Mutable default argument trap | Topic 20 | Famous Python gotcha — bites everyone once |
| Multiple returns + unpacking | Topic 27 | `name, age = get_user()` — Python's nicest feature |
| Docstrings | Topic 4 | Tools and IDEs read these; it's a real habit |

---

## AI Engineer Essentials Beyond Basics

The cheatsheet topics above cover Python idioms. But to write AI code, you also need the **ecosystem-specific** skills below. These live in the numbered files in `learn-python/`, not in the cheatsheet.

| Topic | Where | Priority |
|-------|-------|----------|
| `async` / `await` | `10_async.py` | **Critical** — every LLM call is async |
| Pydantic `BaseModel` | `11_pydantic.py` | **Critical** — tool schemas and structured output |
| Decorators | `12_decorators.py` | **Critical** — `@tool` (LangChain), `@app.post` (FastAPI) |
| `json.loads` / `json.dumps` | Topic 19 in cheatsheet | **Critical** — LLM output is JSON |
| Generators (`yield`) | `12_decorators.py` extras | **Important** — streaming LLM responses |
| `pathlib.Path` | Weekend 2 extras (per `04-learning-status.md`) | **Important** — modern file paths |
| `dataclasses` | `09_dataclasses.py` | **Important** — Pydantic's lighter cousin |
| `logging` | Weekend 3 extras | **Nice to have** — used before `structlog` in P1 |

---

## Week 1 — Python-Specific Essentials

About **10 hours total**, spread across 5 days. Each day is one focused session, not a marathon.

### Day 1 — Syntax skim (~2 hrs)
- Skim `01_basics.py`, `02_collections.py`, `03_control_flow.py`, `04_functions.py`.
- Run each file once, type a few lines from each yourself.
- Goal: muscle memory for Python syntax — not memorization.

### Day 2 — Tonight's priority topics (~2 hrs)
- Topics 1–8 from `python-small-concepts.md`:
  - `*args` / `**kwargs`, `lambda`, `typing.Literal`, docstrings
  - truthiness, `dict.get()`, comprehensions, string methods.
- For each topic, type the example into a Python file and run it.

### Day 3 — Pythonic data tools (~2 hrs)
- Topic 17 — `isinstance()` and `type()`
- Topic 19 — `json.loads` / `json.dumps`
- Topic 25 — list methods (`.append`, `.extend` distinction)
- Topic 26 — dict methods (`.items()`, `.setdefault()`)
- Topic 27 — multiple return values
- These together unlock 80% of what you do with data in Python.

### Day 4 — Decorators (~2 hrs) — critical for AI
- Read `12_decorators.py` end to end.
- Write your own simple decorator: a `@timed` decorator that prints how long a function took to run.
- Understand the difference between a decorator and the `@` syntax for applying it.
- This is critical because LangChain's `@tool` and FastAPI's `@app.post` are decorators — you need to know what's actually happening when you write them.

### Day 5 — Context managers + `pathlib` (~2 hrs)
- Read `06_file_io.py` end to end, focus on the `with` block.
- Learn `pathlib.Path` for file paths — replaces `os.path.join` from older code.
- Write a small script: open a JSON file with `with`, parse it with `json.load`, do something, write it back with `json.dump`.

End of Week 1: you can read most non-async, non-AI Python code without surprises.

---

## Week 2 — AI-Shaped Python

About **10 hours total**. This week is where the work actually pays off — these three topics are the difference between "knows Python" and "can write AI engineering code."

### Day 1–2 — `async` / `await` (~4 hrs)
- Read `10_async.py` slowly. Do not rush.
- Understand: `async def`, `await`, `asyncio.run()`, `asyncio.gather()`.
- Concrete exercise: use `httpx.AsyncClient` to fetch three URLs concurrently. Compare the time to fetching them one by one.
- Why two days: every LLM call (`openai.chat.completions.create`, `anthropic.messages.create`) is async. Every framework (FastAPI, LangChain, LangGraph) is async. If async is not solid, nothing built on top will be either.

### Day 3–4 — Pydantic v2 (~4 hrs)
- Read `11_pydantic.py` end to end.
- Build:
  1. A `BaseModel` for a fictional `Order` (id, customer_id, items, total).
  2. A `BaseModel` with a custom validator (e.g. `total >= 0`).
  3. A `BaseSettings` class that reads env vars from a `.env` file.
- Why this matters: Pydantic is how you describe **tool schemas** for LLMs (`llm.bind_tools([...])`), how you parse structured output (`PydanticOutputParser`), and how you describe FastAPI request/response models. It is *the* most AI-specific Python skill.

### Day 5 — Generators (~2 hrs)
- Read the generator section of `12_decorators.py` extras.
- Write a generator that yields one integer per second for 5 seconds.
- Why: streaming LLM responses (`stream=True`) returns a generator. Async generators (`async for`) extend this for streaming over the network. You will hit this the moment you build a real-time chat UI.

End of Week 2: you can read AI engineering code (LangChain, FastAPI agents, async LLM calls) without losing the plot.

---

## After 2 Weeks — Where to Go Next

Once both weeks are done, jump straight into the project track:

1. **P1 — FastAPI + httpx + structlog** (per `04-learning-status.md`). Build a tiny `/echo` endpoint that calls Groq.
2. **P2 — LangChain / LangGraph.** LCEL pipelines, `bind_tools`, then `StateGraph`.
3. **P3 — RAG.** You already have most of the theory in `week-two/day-two-rag-architecture.md`; now wire it up in code.

The "skipped" topics from this fast track (slicing, ternary, `is` vs `==`, etc.) will fill in naturally as you write real code. You do **not** need to "complete" `learn-python/` end to end before moving on.

---

## Self-Check — Are You Ready to Move On

You're ready to leave the Python phase and move to FastAPI / LangChain when you can do all of these from memory, without looking anything up:

1. Write a function that takes `*args, **kwargs` and prints both.
2. Write a `BaseModel` with a custom validator.
3. Use `async`/`await` to call an HTTP endpoint with `httpx.AsyncClient`.
4. Write a decorator that wraps a function with `print` calls before and after.
5. Open a JSON file, parse it, modify it, and write it back using `with` and `json`.
6. Build a dict-of-lists with `.setdefault` from a flat list of items.
7. Explain the difference between `Literal` and `Enum`, and pick the right one for an intent type.

If 5 out of 7 are solid, move on. The remaining 2 will get drilled by usage.
