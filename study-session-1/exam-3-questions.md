# Exam 3 — Weekend 1 Python (Practice Paper — Harder)

**Topics:** basics, collections, control flow, functions, `enum.Enum`, `typing.Literal`
**Total marks:** 30
**Suggested time:** 30–40 minutes
**Rules:** No running code, no looking at files. Write answers as you'd write them in a Python file.

> **Difficulty:** harder than Exams 1 and 2. Tests deeper understanding — mutation, default-argument gotchas, dict comprehensions, and combining enums + Literal in real agent-shaped code.

---

## Section A — Concepts (10 marks · 2 each)

**A1.** Why is **mutating** a list inside a function visible outside the function, but **reassigning** it is not? Trace what happens here and explain:
```python
def modify(items):
    items.append(99)
    items = [1, 2, 3]
    items.append(100)

data = [10, 20]
modify(data)
print(data)
```

**A2.** What is the **mutable default argument** trap? What does this print on the second call, and how do you fix it?
```python
def add_item(item, basket=[]):
    basket.append(item)
    return basket

print(add_item("apple"))
print(add_item("banana"))
```

**A3.** What is the difference between `range(5)`, `list(range(5))`, and a list comprehension `[i for i in range(5)]`? Are they all the same type? When would you pick which?

**A4.** Compare `enum.Enum` and `typing.Literal` for representing a fixed set of values. When would you pick one over the other? Give one situation each where the choice matters.

**A5.** What does `dict.get(key, default)` do that `dict[key]` doesn't? Why is it the preferred pattern for counters and lookups in code that handles untrusted input (like LLM output)?

---

## Section B — Predict the Output (10 marks · 2.5 each)

**B1.**
```python
data = [{"id": 1, "active": True},
        {"id": 2, "active": False},
        {"id": 3, "active": True},
        {"id": 4, "active": True}]

active_ids = [row["id"] for row in data if row["active"]]
print(active_ids)
print(len(active_ids))
```

**B2.**
```python
config = {"timeout": 30, "retries": 3, "debug": False}

for key, value in config.items():
    if value:
        print(f"{key} -> {value}")
```

**B3.**
```python
def build(*parts, sep="-", **opts):
    base = sep.join(parts)
    if opts.get("upper"):
        base = base.upper()
    suffix = opts.get("suffix", "")
    return base + suffix

print(build("order", "123", "status"))
print(build("order", "123", "status", sep="_", upper=True))
print(build("ID", "42", suffix="!", upper=True))
```

**B4.**
```python
from enum import Enum
from typing import Literal

class Role(Enum):
    ADMIN = "admin"
    USER = "user"

def check(role: Role, action: Literal["read", "write"]) -> bool:
    if role == Role.ADMIN:
        return True
    return action == "read"

print(check(Role.ADMIN, "write"))
print(check(Role.USER, "read"))
print(check(Role.USER, "write"))
print(check(Role.USER.value, "read"))   # subtle — what happens?
```

---

## Section C — Write Code (10 marks · 5 each)

**C1.** Write a function `group_by_status(orders)` that takes a list of order dicts and returns a dict grouping orders by their `status` field.

Example:
```python
orders = [
    {"id": 1, "status": "pending"},
    {"id": 2, "status": "shipped"},
    {"id": 3, "status": "pending"},
    {"id": 4, "status": "delivered"},
]

group_by_status(orders)
# →
# {
#   "pending":   [{"id": 1, ...}, {"id": 3, ...}],
#   "shipped":   [{"id": 2, ...}],
#   "delivered": [{"id": 4, ...}],
# }
```

Hint: use `dict.setdefault(key, [])` or `defaultdict` to avoid the "first time, key doesn't exist" check.

---

**C2.** You are building a small intent classifier wrapper. Write the following:

1. An `enum.Enum` called `Intent` with four members: `ORDER_STATUS`, `CANCELLATION`, `POLICY_QA`, `SMALL_TALK`. Each value is the lowercase string form (e.g. `"order_status"`).
2. A function `classify(text: str) -> Intent` that returns:
   - `Intent.ORDER_STATUS` if the text contains the word `"order"` or `"status"`
   - `Intent.CANCELLATION` if it contains `"cancel"` or `"refund"`
   - `Intent.POLICY_QA` if it contains `"policy"` or `"return"`
   - `Intent.SMALL_TALK` otherwise
   - Comparison must be **case-insensitive**.
3. A function `summarize(text: str) -> str` that calls `classify` and returns: `"Text classified as <intent_value>"`. Use `.value` on the enum to get the string form.
4. Call `summarize` with three different example inputs and print each result.

---

When you finish, paste your answers into the chat and I'll grade with detailed feedback per question.
