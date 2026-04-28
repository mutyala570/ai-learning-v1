# Learning Status

**Purpose:** tracks Python + AI learning progress only. Agent build status lives in `03-status.md`.

**Read this file first when the user asks about learning or says "I'm studying X now".** Update at the end of every learning session.

---

## Current phase
- **Phase:** P0 — Python core — **in progress (W1 done, `05_exceptions.py` done early; W2 continues Sat 2026-05-02 with `06_file_io.py`)**
- **Last updated:** 2026-04-28

---

## Learning schedule (read this before planning work)

| Day type | Activity | Output location |
|----------|----------|-----------------|
| **Weekdays (Mon–Fri)** | Attending external AI course. User revises/consolidates each topic into notes. | `week-one/`, `week-two/`, `week-three/`, … |
| **Weekends (Sat + Sun)** | Python self-study — working through `learn-python/01..12_*.py` in order. | `learn-python/` + small practice scripts in `python-practice/YYYY-MM-DD/` |

**Implications for planning:**
- P0 is paced across **~3 weekends (6 days)**, not 7 consecutive days. Do NOT treat the roadmap's "Week 1" as a calendar week.
- Conceptual AI topics (RAG, agents, function calling) arrive via the course, not this roadmap. The `week-N/` notes are where that lives — already ahead of where pure-code progress is.
- When user says "status", check both tracks: course-revision track (`week-N/`) and Python-code track (`learn-python/`).

### P0 weekend plan (first 3 weekends)

Each weekend day has a **main files** track (the scaffolded `learn-python/*.py`) and an **extras** track (short 15–30 min add-ons needed for real AI code). Both are part of P0 — don't skip extras.

| Weekend | Date | Main files | Extras (same day) |
|---------|------|------------|-------------------|
| 1 ✅ | Sat 2026-04-25 | `01_basics.py`, `02_collections.py` | Jupyter notebook — 15 min, run one cell, understand the REPL |
| 1 ✅ | Sun 2026-04-26 | `03_control_flow.py`, `04_functions.py` | `enum.Enum` + `typing.Literal` — used for intent types everywhere |
| 2 (partial) | Sat 2026-05-02 | ~~`05_exceptions.py`~~ done early on 2026-04-28 · `06_file_io.py` still pending | `pathlib.Path` (modern file paths) · `json` module (load/dump) · writing your own `__enter__`/`__exit__` context manager |
| 2 | Sun 2026-05-03 | `07_oop_basics.py`, `08_oop_inheritance.py` | `@property` getters/setters · `abc.ABC` abstract classes |
| 3 | Sat 2026-05-09 | `09_dataclasses.py`, `10_async.py` | Type hints deep: `Optional`, `Union`, `Callable`, `TypedDict` · `httpx.AsyncClient` quick intro |
| 3 | Sun 2026-05-10 | `11_pydantic.py`, `12_decorators.py` | Generators (`yield`) — LangChain streaming depends on it · `logging` module basics (before `structlog` in P1) |

**Focus per weekend:**
- W1 → language basics: vars, collections, control flow, functions, enums.
- W2 → I/O + OOP: files, exceptions, classes, inheritance, context managers.
- W3 → AI-shaped Python: dataclasses, async, **Pydantic (critical for LLMs)**, decorators, generators, logging.

**End of Weekend 3 → P0 exit criteria check.** If passed, Weekend 4 begins P1 (FastAPI + httpx async + structlog).

---

## P0 — Python core (prerequisite for everything else)
Source: `AI_ENGINEER_ROADMAP.md` Phase 1, Week 1.

### Day 1–2: Python Basics
- [x] Variables, data types (int, float, str, bool, None)  *(W1 Sat — `01_basics.py`)*
- [x] Lists, tuples, sets, dictionaries  *(W1 Sat — `02_collections.py`)*
- [x] Control flow: `if/elif/else`, `for`, `while`, comprehensions  *(W1 Sun — `03_control_flow.py`)*
- [x] Functions: args, `*args`, `**kwargs`, default values, lambda  *(W1 Sun — `04_functions.py`)*
- [x] f-strings  *(W1 Sat — `01_basics.py`)*
- [x] Exception handling: `try/except/finally`, custom exceptions  *(2026-04-28 — `05_exceptions.py`, done early)*
- [ ] File I/O, `with` context manager  *(W2 Sat)*
- [ ] Modules, imports, `pip`, `venv`

### Day 3–4: OOP in Python
- [ ] Classes, `__init__`, `self`
- [ ] Instance vs class vs static methods
- [ ] Inheritance, `super()`, MRO
- [ ] Dunder methods: `__str__`, `__repr__`, `__eq__`, `__len__`
- [ ] `@property`, getters/setters
- [ ] Abstract classes (`abc`)
- [ ] Dataclasses (`@dataclass`)
- [ ] Type hints (`typing`): `List`, `Dict`, `Optional`, `Union`, `Callable`

### Day 5–6: Async Python
- [ ] Sync vs async (transfers from Node.js)
- [ ] `async def`, `await`, coroutines
- [ ] `asyncio.run()`, `asyncio.gather()`, `asyncio.create_task()`
- [ ] `aiohttp` / `httpx` for async HTTP
- [ ] Async iterators, `async for`, `async with`

### Day 7: Python for AI ecosystem
- [ ] `pydantic` (critical for LLMs)
- [ ] `python-dotenv`
- [ ] `requests` / `httpx`
- [ ] Decorators & generators (used heavily in LangChain)

**P0 exit criteria:** can read and write a class with type hints, use `async/await`, and define a Pydantic model without looking at docs. Then P1 starts.

---

## P1 — Python for AI ecosystem (unblocks M1)
- [ ] Pydantic v2: `BaseModel`, `Field`, validators, `BaseSettings`
- [ ] FastAPI: routing, request/response models, dependencies, streaming
- [ ] `httpx.AsyncClient` patterns
- [ ] `structlog` structured logging
- [ ] Type hints: `Literal`, `TypedDict`, `Annotated`

---

## P2 — LangChain / LangGraph (unblocks M2–M5)
- [ ] LangChain LCEL recap (`|`, `RunnablePassthrough.assign`, `RunnableLambda`, `StrOutputParser`) — already seen in exercises
- [ ] `ChatPromptTemplate.from_messages` with system + few-shot
- [ ] `PydanticOutputParser` / `JsonOutputParser`
- [ ] `llm.bind_tools([...])` + tool-calling loop
- [ ] `@tool` decorator / `StructuredTool`
- [ ] LangGraph `StateGraph` — nodes, edges, conditional edges, checkpointers
- [ ] `trim_messages`, conversation summarization

---

## P3 — RAG (unblocks M3)
- [ ] What embeddings are + cosine similarity intuition
- [ ] OpenAI `text-embedding-3-small` vs local `bge-small` trade-off
- [ ] Chunking strategies: fixed-size, semantic, header-based, overlap
- [ ] Vector DBs: Chroma (dev), Qdrant/Pinecone (prod)
- [ ] Hybrid search (BM25 + dense)
- [ ] Reranking with cross-encoder
- [ ] Citations / chunk metadata

---

## P4 — Agent patterns (unblocks M5)
- [ ] ReAct (Thought → Action → Observation → repeat)
- [ ] Plan-and-Execute
- [ ] When to let LLM decide vs hard-code flow
- [ ] Stop conditions (max iterations, confidence thresholds)

---

## P5 — Security / Guardrails (unblocks M7)
- [ ] Prompt-injection defences (input quoting, dual-LLM)
- [ ] PII detection & scrubbing (Presidio or regex)
- [ ] Rate limiting (`slowapi` + Redis)
- [ ] Per-session cost caps
- [ ] JWT pass-through pattern for customer auth

---

## P6 — Evaluation (unblocks M8)
- [ ] Golden-set design
- [ ] LLM-as-judge prompts
- [ ] RAGAS metrics (faithfulness, context precision, answer relevance)
- [ ] Regression testing tied to prompt versions

---

## P7 — Observability (unblocks M8)
- [ ] LangSmith trace structure (spans, runs, datasets)
- [ ] Token / cost accounting per layer
- [ ] Latency percentiles per node

---

## P8 — Deploy (unblocks M9)
- [ ] Multi-stage Python Dockerfile
- [ ] Uvicorn + Gunicorn for prod
- [ ] Streaming responses (SSE / WebSocket)

---

## Exposure so far (ran examples, not studied yet)
- Ran prompt-chaining scripts: Groq, OpenAI, Ollama → `week-one/day-two/*.py`
- Ran multi-turn chat example → `week-one/day-two/prompt-multiturn.py`
- Seen `ChatPromptTemplate`, `RunnablePassthrough`, `RunnableLambda`, `StrOutputParser` in action

---

## How to update this file
- When the user says "started X" / "finished X" / "currently learning X", move the relevant boxes.
- When a phase is complete, note the date next to the phase header.
- If a topic is skipped (e.g. decided not to use LangSmith), strike it through and note why.
- Keep phase order — don't skip P0 to P2 without flagging it.
