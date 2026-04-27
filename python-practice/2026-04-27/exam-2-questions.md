# Exam 2 — Weekend 1 Python (Practice Paper)

**Topics:** basics, collections, control flow, functions, `enum.Enum`, `typing.Literal`
**Total marks:** 30
**Suggested time:** 30 minutes
**Rules:** No running code, no looking at files. Write answers as you'd write them in a Python file.

> **Focus areas this paper drills harder:** truthiness, dict iteration, and exact output prediction — the three weak spots from Exam 1.

---

## Section A — Concepts (10 marks · 2 each)

**A1.** What is the difference between `==` and `is` in Python? Give one example where they give different results.

**A2.** List **all the falsy values** in Python. Why does this matter when you write `if user_input:` instead of `if user_input != "":`?

**A3.** Explain `*` and `**` when used at a **call site** (not in a function definition). What does this print?
```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
config = {"a": 10, "b": 20, "c": 30}

print(add(*nums))
print(add(**config))
```

**A4.** What is a **lambda** function? Give one example where using a lambda is cleaner than defining a regular `def`. (Hint: think `sorted()` or `filter()`.)

**A5.** Why is a `set` faster than a `list` when checking membership with `in`? When would you still pick a list anyway?

---

## Section B — Predict the Output (10 marks · 2.5 each)

**B1.**
```python
items = ["apple", "", "banana", None, "cherry", 0]
keep = [x for x in items if x]
print(keep)
```

**B2.**
```python
inventory = {"apples": 5, "bananas": 0, "cherries": 12}
in_stock = {fruit: qty for fruit, qty in inventory.items() if qty > 0}
print(in_stock)
```

**B3.**
```python
def make_greeting(name, *titles, **details):
    titles_str = " ".join(titles)
    details_str = ", ".join(f"{k}={v}" for k, v in details.items())
    return f"Hello {titles_str} {name}! ({details_str})"

print(make_greeting("Prem", "Mr.", "Dr.", age=27, city="Hyderabad"))
```

**B4.**
```python
from enum import Enum

class Status(Enum):
    ACTIVE = 1
    INACTIVE = 2

s = Status.ACTIVE
print(s.name)
print(s.value)
print(Status.ACTIVE is Status.ACTIVE)
print(Status(1) == Status.ACTIVE)
```

---

## Section C — Write Code (10 marks · 5 each)

**C1.** Write a function `top_n_words(text, n)` that returns the **top `n` most frequent words** in `text` (case-insensitive), as a list of `(word, count)` tuples sorted by count descending.

Example:
```python
top_n_words("the cat sat on the mat the cat", 2)
# → [("the", 3), ("cat", 2)]
```

Hints: reuse the `count_words` pattern from Exam 1, then sort the dict's items.

---

**C2.** You are building a customer router. Write the following:

1. A `typing.Literal` alias called `IntentName` for the four intent strings: `"order_status"`, `"cancellation"`, `"policy_qa"`, `"small_talk"`.
2. A function `route(intent: IntentName, customer_id: str) -> dict` that returns a dict with three keys: `intent`, `customer_id`, and `handler` — where `handler` is one of `"orders_service"`, `"cancellations_service"`, `"rag_service"`, or `"chat_service"` depending on the intent.
3. Call the function once with a sample input and print the result.

---

When you finish, paste your answers into the chat and I'll grade with detailed feedback per question.
