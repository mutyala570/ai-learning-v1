# Exam 4 — Small Concepts (Concepts File Coverage)

**Topics:** `*args`/`**kwargs`, `lambda`, `typing.Literal`, docstrings, truthiness, `dict.get`, comprehensions, ternary, `Optional`/`Union`, `enumerate`/`zip`, unpacking, `is` vs `==`, f-strings, string methods, slicing, `in`, `isinstance`, `sorted`/`.sort()`, `json.loads`/`dumps`, mutable default trap, `any`/`all`, list/dict methods, multiple returns
**Source:** `study-session-1/python-small-concepts.md`
**Total marks:** 40 (+ self-rating section, ungraded)
**Suggested time:** 50–60 minutes
**Rules:** No running code, no looking at the concepts file or any other notes. Write answers as you would write them in a real Python file. If you genuinely do not know an answer, write **"skip"** — don't guess. The "skip" count is part of how I grade.

> **Why this exam:** verify that last week's P0 material is solid before W2, and surface which clusters you are already advanced in so we don't waste weekend time on topics you have already locked in.

---

## Section A — Concepts (10 marks · 2 each)

**A1.** What does `*args` collect into, and what does `**kwargs` collect into? Given the following call, write down the exact value of `args` and `kwargs` inside the function body:
```python
def f(*args, **kwargs):
    print(args) # (1, 2, 'hi')
    print(kwargs) # {'debug': True, 'retries': 3}

f(1, 2, "hi", debug=True, retries=3)
```

**A2.** What is a **docstring**, where exactly does it sit in a function, and name two tools or features that read it automatically. Then write a one-line summary docstring for this function (imperative mood, no Args/Returns block needed):
```python
def normalize(text: str) -> str:
    """Normalize text by stripping whitespace and converting to lowercase.
    args:
        text (str): The text to normalize.
    returns:
        str: The normalized text.

        tools:ide, linter
    """
    return text.strip().lower()
```

**A3.** List the **six falsy values** in Python (the categories, not every individual value). Then explain in one sentence why `if items:` is preferred over `if len(items) > 0:` for checking whether a list has elements.
Ans:None, False, 0, "", [], {}

**A4.** What is the difference between `dict[key]` and `dict.get(key, default)` when the key does not exist? Why is `.get()` the preferred pattern for parsing LLM output or untrusted JSON? Give one short example of the counter idiom that uses `.get()`.
Ans: `dict[key]` will raise a KeyError if the key does not exist, while `dict.get(key, default)` will return the default value if the key does not exist.   

**A5.** Explain the difference between `is` and `==` in one sentence each. Then state which operator should be used to check for `None`, and why.
Ans: `is` checks for identity , while `==` checks for equality (whether two objects have the same value). 

---

## Section B — Predict the Output (15 marks · 2.5 each)

**B1.**
```python
nums = [1, 2, 3, 4, 5, 6]
result = [n * n for n in nums if n % 2 == 1]
print(result) : [1, 9, 25]
print(len(result)) : 3
```

**B2.**
```python
orders = [
    {"id": 1, "amount": 250},
    {"id": 2, "amount": 80},
    {"id": 3, "amount": 600},
]
top = sorted(orders, key=lambda o: o["amount"], reverse=True)
print(top[0]["id"], top[-1]["id"])ans: 3 2
```

**B3.**
```python
def build(*parts, sep="-", **opts):
    base = sep.join(parts)
    if opts.get("upper"):
        base = base.upper()
    return base + opts.get("suffix", "")

print(build("a", "b", "c")) : a-b-c
print(build("a", "b", sep="_", upper=True, suffix="!")) : A_B!
print(build("x", "y", "z", **config)) : X:Y:Z
```

**B4.**
```python
raw = "  Hello, World!  "
parts = raw.strip().lower().replace(",", "").split()
print(parts): ['hello', 'world!']
print(" ".join(parts)): hello world!
```

**B5.**
```
ids = [101, 102, 103]
names = ["alice", "bob", "carol"]
for i, (uid, name) in enumerate(zip(ids, names)):
    print(f"{i}: {uid} -> {name}")

0: 101 -> alice
1: 102 -> bob
2: 103 -> carol
```

**B6.**
```python
required = ["name", "email", "phone"]
data = {"name": "Prem", "email": "x@y.com"}

print(all(field in data for field in required)): False
print(any(field not in data for field in required)): True
print(any(data.get(f) for f in required)): True
```

---

## Section C — Write Code (15 marks · 5 each)

**C1. Word counter that returns the top N words.**
Write a function `top_words(text: str, n: int = 3) -> list[tuple[str, int]]` that:
- Lowercases the text and splits on whitespace.
- Counts each word using the `dict.get(word, 0) + 1` pattern (no `defaultdict`, no `Counter` — exam tests the raw idiom).
- Returns a list of `(word, count)` tuples for the top `n` most-frequent words, sorted by count descending. Use `sorted` with a `key=` lambda.
- Includes a proper docstring.

Then call it once: `top_words("the cat sat on the mat the mat was warm", n=2)` and write what you expect it to return.

def top_words(text: str, n: int = 3) -> list[tuple[str, int]]:
    words = text.lower().split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]

print(top_words("the cat sat on the mat the mat was warm", n=2))
# Expected output: [('the', 3), ('mat', 2)]


---

**C2. Intent normalizer using `*args`, `**kwargs`, and `Literal`.**
Write a function `normalize_intent(*messages: str, default: Literal["small_talk", "out_of_scope"] = "small_talk", **flags) -> str` that:
- Joins all `messages` with a single space, then `.strip().lower()`.
- If the result contains `"order"` or `"status"`, returns `"order_status"`.
- If it contains `"cancel"` or `"refund"`, returns `"cancellation"`.
- Otherwise returns the `default` value.
- If `flags.get("debug")` is truthy, also prints `f"[debug] joined='{joined}' result='{result}'"` before returning.
- Has a proper docstring with a one-line summary plus an Args section.

Then call it three times with different inputs (one normal, one with `default="out_of_scope"`, one with `debug=True`) and write the expected printed output and return value of each call.

def normalize_intent(*messages: str, default: Literal["small_talk", "out_of_scope"] = "small_talk", **flags) -> str:
    joined = " ".join(messages).strip().lower()
    if "order" in joined or "status" in joined:
        result = "order_status"
    elif "cancel" in joined or "refund" in joined:
        result = "cancellation"
    else:
        result = default
    if flags.get("debug"):
        print(f"[debug] joined='{joined}' result='{result}'")
    return result

print(normalize_intent("I want to check my order status", debug=True))
# Expected output: [debug] joined='i want to check my order status' result='order_status'
# Return value: 'order_status'

print(normalize_intent("I want to cancel my order", default="out_of_scope"))
# Expected output: None
# Return value: 'cancellation'

print(normalize_intent("What's the weather like?", debug=True))
# Expected output: [debug] joined='what's the weather like?' result='small_talk'
# Return value: 'small_talk'

---

**C3. JSON parsing with safe defaults.**
Given the following raw string returned by an LLM (which is *almost* valid JSON), write a function `parse_orders(raw: str) -> list[dict]` that:
- Tries `json.loads(raw)`.
- On `json.JSONDecodeError`, returns an empty list `[]` (not None, not raise).
- On success, returns only the orders where `status` is `"active"`, using a list comprehension. Use `dict.get("status")` so a missing field does not crash.
- Has a docstring.

```python
raw = '[{"id": 1, "status": "active"}, {"id": 2, "status": "cancelled"}, {"id": 3}]'
```

What does `parse_orders(raw)` return for the input above? What does it return if `raw = "not json at all"`?
def parse_orders(raw: str) -> list[dict]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    return [order for order in data if order.get("status") == "active"]

print(parse_orders(raw))
# Expected output: [{'id': 1, 'status': 'active'}]
print(parse_orders("not json at all"))
# Expected output: []

---

## Section D — Self-Rating (ungraded, but please fill in)

For each cluster below, mark yourself **1 (shaky)**, **2 (ok)**, or **3 (solid)**. Be honest — this is how I will calibrate which topics to push you on next, and which to mark as "advanced — skip drilling".

| # | Cluster | Self-rating (1 / 2 / 3) |
|---|---------|--------------------------|
| 1 | `*args`, `**kwargs`, call-site unpacking (`*list`, `**dict`) | _ |2
| 2 | `lambda` + use with `sorted`, `min`, `max`, `key=` | _ |2
| 3 | `typing.Literal` and when to pick it over `enum.Enum` | _ |2
| 4 | Docstrings (placement, conventions, reading via `help()`) | _ |1
| 5 | Truthiness — six falsy categories, when `if x:` is enough | _ |3
| 6 | `dict.get(key, default)` and the counter idiom | _ |3
| 7 | List / dict / set comprehensions with filter clauses | _ |3
| 8 | String methods — `.strip()`, `.lower()`, `.split()`, `.join()`, `.replace()` | _ |3
| 9 | Ternary expression `a if cond else b` | _ |3
| 10 | `Optional[X]` / `Union[X, Y]` and the `X \| Y` pipe syntax | _ |0
| 11 | `enumerate()` and `zip()` (and combining them) | _ |3
| 12 | Unpacking — `a, b = ...`, `first, *rest`, `*head, last` | _ |3
| 13 | `is` vs `==` (and when each is correct) | _ |3
| 14 | f-string format specifiers (`:.2f`, `:,`, alignment, `{x=}`) | _ |3
| 15 | Slicing `seq[start:stop:step]` (incl. negative step, out-of-bounds safety) | _ |2
| 16 | `in` operator (set-vs-list speed implications) | _ |3
| 17 | `isinstance(x, T)` vs `type(x) == T` | _ |3
| 18 | `sorted(seq)` vs `seq.sort()` (return value, in-place behaviour) | _ |3
| 19 | `json.loads` / `json.dumps` (incl. handling invalid LLM JSON) | _ |3
| 20 | Mutable default argument trap and the `=None` fix | _ |2
| 21 | `any()` / `all()` with generator expressions | _ |3
| 22 | Common built-ins: `len`, `sum`, `min`, `max`, `range`, `round`, `abs` | _ |3
| 23 | Type conversion: `int()`, `str()`, `float()`, `bool()`, `list()`, `set()` | _ |3
| 24 | List methods: `append` vs `extend`, `pop`, `remove`, `index`, `count` | _ |3
| 25 | Dict methods: `keys`, `values`, `items`, `setdefault`, `update`, `pop` | _ |3
| 26 | Multiple return values (tuple unpacking, `_` for ignored values) | _ |2

---

## How I will grade

When you submit, I'll do four things:

1. Score Section A, B, C against the marking scheme (40 total).
2. Group your wrong/skipped answers into **clusters** (e.g. "comprehensions weak", "json fine, slicing fine, mutable defaults missed").
3. Compare your **self-ratings (Section D)** with your **actual performance** — gaps in either direction are interesting (you rated yourself low on something you actually got right → push to "advanced", or vice versa).
4. Produce a short list of **"topics you are advanced in — safe to skip future drilling"** and **"topics to revisit before W2 starts"** so the rest of the week is targeted instead of broad.

When you finish, paste your answers into the chat and I'll grade with per-question feedback plus the cluster summary.
