# What I Learned — Study Session 1

**Date:** 2026-04-27
**Track:** Python catch-up (Weekend 1 missed) + AI course revision (RAG architecture)
**Total time:** ~one evening
**Result:** From "developer new to Python" → comfortable with Python idioms and dict-shaped data structures.

A timeline of what was covered, what stuck, and what to drill next. Read this first the next time you sit down — it will tell you exactly where you left off.

## Topics Covered in This Document

1. [**The Big Picture**](#the-big-picture)
2. [**Python Concepts I Now Know**](#python-concepts-i-now-know)
3. [**Things I Got Wrong (and Now Understand)**](#things-i-got-wrong-and-now-understand)
4. [**Files I Created in This Session**](#files-i-created-in-this-session)
5. [**Exam Performance**](#exam-performance)
6. [**Open Items / What's Next**](#open-items--whats-next)

---

## The Big Picture

I missed Saturday and Sunday's Python self-study because of work, so this session was a catch-up sprint. The deal was: I would learn through reading + small examples, then take exams to confirm understanding.

The session ended up covering more than just Saturday and Sunday's planned material — once Python idioms were solid, we went deeper into dicts (because those drive every AI / LLM / API workflow) and added a JS-to-Python translation reference.

In parallel, I revised the AI course's Day 2 RAG architecture content into structured notes (15 slides, plus a summary file) so the course notes stay in sync.

---

## Python Concepts I Now Know

The reference material lives in `python-small-concepts.md`. The concepts I have actually internalized (not just read once) are below.

### Solid

- **Tuples vs lists vs sets** — what each is, when to pick which, and the immutability link.
- **Dict access patterns** — `d[key]`, `d.get(key)`, `d.get(key, default)`, and *when each is appropriate*.
- **`.get(key, default)` rule** — the default fires only when the key is *missing*, not when its value is falsy.
- **Dict iteration** — `for k, v in d.items():` and *why* the unpacking works (because `.items()` returns tuples).
- **Comprehensions** — the four-position template (`KEEP → for → in → if`) for list and dict comprehensions, including filter-only and dict-keyed forms.
- **`*args` / `**kwargs`** — at function definition AND at call site, plus the spread parallel to JavaScript's `[...arr]` and `{...obj}`.
- **`typing.Literal`** — restricting values to a fixed set of strings, vs `Enum` for runtime objects.
- **Hashability** — *why* tuples can be dict keys and lists cannot, including the edge case of `(1, [2, 3])` being unhashable because the inner list is mutable.
- **Setdefault group-by pattern** — `d.setdefault(key, []).append(item)` for bucketing items by a key.
- **Counter pattern** — both manual (`d[key] = d.get(key, 0) + 1`) and library (`Counter` from `collections`).
- **Shallow vs deep copy** — `[*a]` / `a.copy()` are shallow, same as JS `[...a]`; `copy.deepcopy(a)` for nested structures.
- **JSON ↔ dict** — `json.loads(string)` and `json.dumps(obj)`; `s` always means "string."

### Just covered, needs another pass

- **Lambdas** — read about them, used them in `sorted(..., key=lambda x: ...)`. Need to write a few more before they're automatic.
- **Docstrings** — know the format. Need to start writing them on every function.
- **Truthiness rules** — read the falsy list; need to *recall* it without looking when writing `if x:`.
- **`isinstance()` vs `type()`** — read about it, not yet used in code.
- **`map()` / `filter()`** — recognize them; comprehensions are still my default.

### Skipped on purpose (covered later in the schedule)

- Async / await → Weekend 3
- Pydantic → Weekend 3
- Decorators → Weekend 3
- Generators / `yield` → Weekend 3
- Classes / inheritance → Weekend 2
- Context managers (`with`) → Weekend 2
- `pathlib.Path` → Weekend 2 extras

---

## Things I Got Wrong (and Now Understand)

Listing the actual mistakes from the exams and quizzes — these are the ones to drill, because each one represents a misconception that almost made it into real code.

1. **Default fallback misread**
   - Wrote `user.get("name", "Unknown")` returns `"Unknown"`.
   - Reality: returns `"Prem"` because the key exists.
   - **Rule:** the default fires only when the key is missing, not when the value is falsy or "looks empty."

2. **Dict keys without quotes**
   - Wrote `{**a, **b, role: "admin"}`.
   - Reality: Python requires `"role": "admin"` because dict keys are string literals, not bare names.
   - **Rule:** Python dicts use quoted strings. JS-style bare keys are wrong.

3. **`user.age` instead of `user["age"]`**
   - Used JS-style dot notation on a dict.
   - Reality: dicts in Python don't support `.attribute` access. Only classes do.
   - **Rule:** if it's a dict, use brackets. If it's a class instance, use dot.

4. **Tuple containing a list = unhashable**
   - Marked `(1, [2, 3])` as hashable.
   - Reality: the outer tuple is immutable, but the inner list is not, so the whole thing is unhashable.
   - **Rule:** a container is hashable only if *everything inside it* is hashable, all the way down.

5. **`.sort()` returns `None`**
   - Wrote `result = nums.sort()`.
   - Reality: `.sort()` mutates in place and returns `None`. Use `sorted(nums)` for a new list.
   - **Rule:** in Python, methods that mutate usually return `None`. Use the function form (`sorted`) when you want a return value.

6. **"This program is wrong" when iterating a dict**
   - Marked B3 (a normal `for k, v in d.items():` loop) as a wrong program.
   - Reality: it was correct dict iteration; output was `5`.
   - **Rule:** when an answer is "this is wrong," walk through one iteration before declaring it. Don't bail out without tracing.

7. **Counter pattern needs an initial value**
   - Original code `counts[word] += 1` raised `KeyError` because the key didn't exist.
   - **Rule:** for counting, use one of:
     - `counts[word] = counts.get(word, 0) + 1`
     - `counts = defaultdict(int)` then `counts[word] += 1`
     - `Counter(words)` (one-liner)

---

## Files I Created in This Session

Everything in this folder. Quick descriptions:

| File | Purpose |
|---|---|
| `python-small-concepts.md` | The big reference — 27 small Python concepts, organized by priority. Tonight's priority list (topics 1–8) at the top. |
| `fast-track-for-developers.md` | A 2-week plan for an experienced dev → AI engineer. Skip what I already know, drill Python idioms, then async + Pydantic + decorators. |
| `js-to-python-cheatsheet.md` | Direct JS → Python translations for arrays, objects, spread/rest, JSON, strings, async, plus 8 common gotchas. |
| `exam-1-with-answers.md` | First exam paper, with my answers and the model answer key. Score: 24.5/30 (B+). |
| `exam-2-questions.md` | Practice paper #2 — same difficulty as Exam 1, drills truthiness/dict iteration/exact output prediction. Not yet attempted. |
| `exam-3-questions.md` | Practice paper #3 — harder. Mutation, default-arg trap, dict comprehensions, enums + Literal combined. Not yet attempted. |

Outside this folder, also touched in this session:

- `week-two/day-two-rag-architecture.md` — added Slides 12–15 (naive vs late chunking, query pre-processing, embedding model selection, vector DB selection).
- `week-two/day-two-rag-summary.md` — high-level summary of the six RAG design questions with pointers back to the slides.

---

## Exam Performance

| Quiz / Exam | Score | Notes |
|---|---|---|
| Exam 1 (Weekend 1 catch-up) | 24.5 / 30 (B+, ~82%) | Code-writing was perfect (10/10). Lost marks on output prediction and dict iteration. |
| Tuple/Dict 5-question check | 3 / 5 | Hashability concept was half-formed; missed the tuple-with-list edge case. |
| Q5 retry on dict keys | 6 / 7 | Same edge case missed again — *now* fully understood. |
| List quick check (4 questions) | 3.5 / 4 | Q4 had a `user.age` instead of `user["age"]` slip. |
| Dict quick check (5 questions) | 4.15 / 5 (≈83%) | `.get()` default rule misapplied; otherwise solid. |

**Pattern:** code-writing is ahead of mental simulation. I write correct code more reliably than I predict what code will print. Worth practicing trace-through-by-hand drills before the next exam.

---

## Open Items / What's Next

### Immediate (next session)
- Take **Exam 2** (`exam-2-questions.md`) — drills the weak spots from Exam 1.
- Take **Exam 3** (`exam-3-questions.md`) — harder, includes mutation and default-arg trap.

### This week (per `learn-python/fast-track-for-developers.md`)
- Day 4: **Decorators** (`12_decorators.py`) — critical for AI: `@tool`, `@app.post`.
- Day 5: **`with` / context managers + `pathlib.Path`**.

### Next week
- Days 1–2: **`async` / `await`** — every LLM call is async.
- Days 3–4: **Pydantic v2** — most AI-specific Python skill.
- Day 5: **Generators** (`yield`) for streaming.

### When ready to move on from Python
The self-check at the bottom of `fast-track-for-developers.md` lists 7 questions. Move to P1 (FastAPI) when 5 of 7 are solid.

### AI course track (parallel)
- Today's weekday slot was the AI course (no slides shared yet).
- Next time slides come in, build them into `week-two/day-three-<topic>.md` using the same style as Day 2.
