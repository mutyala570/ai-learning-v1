# Week 3 — Weekly Plan

This document scopes everything I need to cover between **Tue 2026-04-28** and **Sun 2026-05-03**. The week splits across two tracks: the external AI course revision on weekdays and Python self-study on the weekend. Both are part of P0 — neither track is optional.

## Topics Covered in This Document

1. [**The Week at a Glance**](#the-week-at-a-glance)
2. [**Weekday Track — AI Course Revision (Tue–Fri)**](#weekday-track--ai-course-revision-tuefri)
3. [**Weekend Track — Python P0 Weekend 2 (Sat–Sun)**](#weekend-track--python-p0-weekend-2-satsun)
4. [**Carryover from Weekend 1**](#carryover-from-weekend-1)
5. [**Exit Checks for the Week**](#exit-checks-for-the-week)

---

# The Week at a Glance

Weekdays go to the external AI course. Each weekday I sit through the live session and then revise that day's topic into a fresh note inside `week-three/`. The note must be self-contained so future me can re-read it without the slides. The doc-creation rules in `doc-creation-guidelines.md` (filename format `day-<N>-<topic>.md`, slide-indexed table of contents, full sentences, no bullet dumps) apply to every one of these notes.

Weekends go to Python self-study. This weekend is **P0 Weekend 2**, the second of three weekends in P0. The plan is fixed in `goal/04-learning-status.md`: two main files per day plus a small extras track that is needed for real AI code. Skipping the extras is not allowed even though they look small — `pathlib`, `json`, `@property` and `abc.ABC` show up everywhere in production AI code, so cutting them now means revisiting them under pressure later.

| Day | Date | Track | Output location |
|-----|------|-------|-----------------|
| Tue | 2026-04-28 | AI course revision | `week-three/day-one-<topic>.md` |
| Wed | 2026-04-29 | AI course revision | `week-three/day-two-<topic>.md` |
| Thu | 2026-04-30 | AI course revision | `week-three/day-three-<topic>.md` |
| Fri | 2026-05-01 | AI course revision | `week-three/day-four-<topic>.md` |
| Sat | 2026-05-02 | Python P0 W2 day 1 | `learn-python/05_exceptions.py`, `06_file_io.py` |
| Sun | 2026-05-03 | Python P0 W2 day 2 | `learn-python/07_oop_basics.py`, `08_oop_inheritance.py` |

> If a weekday course session is cancelled, that slot does **not** convert into a Python session — the weekend boundary is fixed by the schedule in `goal/04-learning-status.md`.

---

# Weekday Track — AI Course Revision (Tue–Fri)

The deliverable each weekday is one revision note in `week-three/`. The note is not a transcript — it is the topic explained in my own words, with the "why" and the intuition that the slides do not always state. The course is currently feeding the conceptual layer that the roadmap's later phases (P2 LangChain, P3 RAG, P4 agents) will cement, so these notes are how I avoid drifting away from the code track even while the code track waits for the weekend.

## What each daily note must contain

Every revision note follows the same shape so future me can scan a row of them quickly. Title at the top in the form `# Week 3 — Day <M>: <Topic Title> (Video <V>)`. A "Slides Covered in This Document" section that is a clickable index of every slide grouped by sub-topic. A horizontal rule. Then the body, where each slide gets its own `# Slide <N> — <Title>` heading and is written as full sentences in paragraphs, not bullet dumps. The exact rules are in `doc-creation-guidelines.md` — re-read it on Tuesday morning before writing the first note of the week.

## Topic placeholders (fill in as the course unfolds)

I do not know in advance what the course will cover this week, so the table below is a placeholder I update each evening after the session. Filename and topic stay TBD until the session names them.

| Day | Course topic (filled in after the session) | Note file |
|-----|---------------------------------------------|-----------|
| Tue 04-28 | _TBD — fill in after session_ | `week-three/day-one-<topic>.md` |
| Wed 04-29 | _TBD_ | `week-three/day-two-<topic>.md` |
| Thu 04-30 | _TBD_ | `week-three/day-three-<topic>.md` |
| Fri 05-01 | _TBD_ | `week-three/day-four-<topic>.md` |

## What "done" looks like for the weekday track

By Friday evening `week-three/` should contain four day-prefixed notes that I can hand to a stranger and have them understand the topic without watching the source videos. If I cannot do that, the note is incomplete and I revise it before the weekend starts — Saturday belongs to Python, not to catching up on revision debt.

---

# Weekend Track — Python P0 Weekend 2 (Sat–Sun)

This weekend is the **I/O and OOP** weekend. Weekend 1 covered the language basics (variables, collections, control flow, functions). Weekend 2 builds on that with the things a real Python program actually has to handle: files that may not exist, errors that need to be caught and reraised cleanly, and the class system that every Python library — including Pydantic, FastAPI, and LangChain — is built on top of. Weekend 3 then turns this into AI-shaped Python (dataclasses, async, Pydantic, decorators).

## Saturday 2026-05-02 — Exceptions and File I/O

The main files are `learn-python/05_exceptions.py` and `learn-python/06_file_io.py`. Saturday is about teaching myself what Python does when something goes wrong, and how Python reads and writes the outside world. By the end of Saturday I should be able to write a function that opens a file, fails gracefully if the file is missing, and either propagates or wraps the error so a caller can react to it without inspecting strings.

The extras track for Saturday is small but load-bearing for everything that follows. **`pathlib.Path`** is the modern replacement for `os.path` string-juggling and is what every modern Python codebase uses for filesystem paths. The **`json`** module's `load`, `loads`, `dump`, and `dumps` functions are how Python talks to LLM APIs, vector databases, and config files, so the round-trip from dict to string and back must feel automatic. Finally, writing my own context manager with `__enter__` and `__exit__` is the small exercise that makes the `with` statement stop being magical — once I have written one by hand, every subsequent `with open(...) as f` and `with httpx.AsyncClient() as client` reads as ordinary code rather than as a special form.

## Sunday 2026-05-03 — OOP Basics and Inheritance

The main files are `learn-python/07_oop_basics.py` and `learn-python/08_oop_inheritance.py`. Sunday introduces classes, `__init__`, `self`, instance versus class versus static methods, then layers inheritance, `super()`, and method resolution order on top. The roadmap singles out the **dunder methods** — `__str__`, `__repr__`, `__eq__`, `__len__` — as the part to actually internalise, because Pydantic and dataclasses will lean on them later and reading their source becomes much easier once `__repr__` is no longer mysterious.

The extras track is two ideas. **`@property`** is how Python exposes computed attributes that look like fields, used heavily in Pydantic and in any class that has a "derived value" (think `Order.total` computed from `Order.lines`). **`abc.ABC`** plus `@abstractmethod` is how Python expresses "this is an interface" — every LangChain `BaseChatModel`, every LangGraph node base, every retriever interface uses it, so understanding what `ABC` actually enforces (instantiation guard, nothing else) prevents a lot of confusion later.

## What "done" looks like for the weekend track

By Sunday evening I should be able to, without looking at the docs, define a class with typed attributes, override `__repr__`, raise and catch a custom exception, read a JSON file from a `pathlib.Path`, and explain why `with open(...) as f:` is preferable to `f = open(...)`. If any of those is shaky, that's the topic to revisit on the next weekday evening, not next weekend.

---

# Carryover from Weekend 1

Weekend 1's main files (`01_basics.py` through `04_functions.py`) were completed and ticked in `goal/04-learning-status.md`. The Sunday **extras** for Weekend 1 — `enum.Enum` and `typing.Literal` — are the part I need to confirm I actually finished. These two are not optional curiosities: `Literal["order_status", "cancellation", "policy_qa", "small_talk"]` is the exact pattern the agent project will use for its intent type, and `enum.Enum` is the form the same idea takes when I want a real Python value rather than a string union.

If either of these is still shaky, I should spend fifteen minutes on a weekday evening this week writing a tiny script under `python-practice/2026-04-28/` (or whichever evening I pick) that defines an `Intent` literal, a `Status` enum, and one function that takes each as a parameter and returns something. That closes the W1 loop before W2 stacks more material on top.

---

# Exit Checks for the Week

By Sunday evening the following must all be true. If any of them is not, the week is not actually done regardless of what was attempted.

1. `week-three/` contains four substantive day-prefixed revision notes, each conformant to `doc-creation-guidelines.md`.
2. `learn-python/05_exceptions.py`, `06_file_io.py`, `07_oop_basics.py`, `08_oop_inheritance.py` have all been worked through, not just opened.
3. The Saturday extras (`pathlib`, `json`, hand-written context manager) and the Sunday extras (`@property`, `abc.ABC`) are each represented by at least a small working snippet I wrote myself.
4. Weekend 1's `enum.Enum` and `typing.Literal` carryover is genuinely closed, not just planned.
5. `goal/04-learning-status.md` and `goal/README.md` are updated on Sunday evening: W2 marked done, the Day 3–4 OOP boxes ticked under "P0 — Python core", `Last updated` bumped, and the next-action line in the dashboard pointed at Weekend 3 (Sat 2026-05-09).

> If checks 1–4 pass, **P0 is two-thirds complete** and Weekend 3 is the final stretch before P1 (FastAPI + httpx + structlog) unblocks the M1 agent skeleton.
