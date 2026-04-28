# Exam 1 — Weekend 1 Python (Sat + Sun catch-up)

**Date taken:** 2026-04-27
**Topics:** basics, collections, control flow, functions, `enum.Enum`, `typing.Literal`
**Total marks:** 30
**Score:** 24.5 / 30 (≈ 82%, B+ / Solid)

---

## Section A — Concepts (10 marks · 2 each)

### A1. Difference between list, tuple, and set + one use case each.

**Model answer:**
- **list** — ordered, mutable, allows duplicates. Use case: queue of orders to process in arrival order.
- **tuple** — ordered, immutable, allows duplicates. Use case: a fixed pair like `(latitude, longitude)`.
- **set** — unordered, mutable, no duplicates. Use case: tracking unique customer IDs already greeted.

```python
orders = ["o1", "o2", "o3"]              # list
location = (17.385, 78.486)              # tuple
seen_ids = {"c1", "c2"}                  # set
```

---

### A2. What does this print and why?
```python
x = None
if x:
    print("yes")
else:
    print("no")
```

**Model answer:** Prints `no`.

`None` is **falsy** in Python. The `if x:` check evaluates the *truthiness* of `x` directly — it does not need `x == True`. Falsy values in Python: `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `False`. Everything else is truthy.

---

### A3. Difference between `*args` and `**kwargs` + a one-line function using both.

**Model answer:**
- `*args` collects extra **positional** arguments into a **tuple**.
- `**kwargs` collects extra **keyword** arguments into a **dict**.

```python
def demo(*args, **kwargs):
    print(args, kwargs)

demo(1, 2, a=10, b=20)
# (1, 2) {'a': 10, 'b': 20}
```

`*args` must come before `**kwargs` in the signature.

---

### A4. What is an f-string? Rewrite the example using one.

**Model answer:** An f-string is a string literal prefixed with `f` that evaluates `{expression}` placeholders inline. It is faster and cleaner than `+` concatenation or `.format()`.

```python
name = "Prem"
age = 27
print(f"Hello {name}, you are {age} years old")
```

---

### A5. What does `typing.Literal` do? Why use it instead of `str`?

**Model answer:** `Literal` restricts a value to a **fixed set of constants** (instead of any string). Type checkers like mypy or Pyright will flag a call that passes anything outside the allowed values, so bugs are caught before runtime.

```python
from typing import Literal

Intent = Literal["order_status", "cancellation", "policy_qa"]

def route(intent: Intent) -> str:
    return f"Routing to {intent}"

route("order_status")     # ok
route("random_text")      # type checker error
```

This is exactly how intent types are declared in agent code.

---

## Section B — Predict the Output (10 marks · 2.5 each)

### B1.
```python
nums = [1, 2, 3, 4, 5]
squares = [n * n for n in nums if n % 2 == 0]
print(squares)
```

**Output:** `[4, 16]`

The list comprehension keeps only even numbers (`2`, `4`) and squares them.

---

### B2.
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Prem"))
print(greet("Prem", greeting="Hi"))
```

**Output:**
```
Hello, Prem!
Hi, Prem!
```

When predicting output, copy the format string **exactly** — every comma and `!` is part of the result.

---

### B3.
```python
data = {"a": 1, "b": 2, "c": 3}
total = 0
for key, value in data.items():
    if value > 1:
        total += value
print(total)
```

**Output:** `5`

`data.items()` yields `("a", 1)`, `("b", 2)`, `("c", 3)`. Skip 1, add 2 (total=2), add 3 (total=5). Dict iteration with `.items()` is the standard pattern for walking JSON-like data — used constantly in AI code.

---

### B4.
```python
from enum import Enum

class Intent(Enum):
    ORDER = "order_status"
    CANCEL = "cancellation"

x = Intent.ORDER
print(x.value)
print(x == Intent.ORDER)
print(x == "order_status")
```

**Output:**
```
order_status
True
False
```

The trick: `Intent.ORDER == "order_status"` is **False**. An enum member is not equal to its raw value. To compare against the string, use `x.value == "order_status"`.

---

## Section C — Write Code (10 marks · 5 each)

### C1. Write `count_words(text)` that returns a dict of word → count, case-insensitive.

**Model answer:**
```python
def count_words(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


print(count_words("hello world Hello"))
# {'hello': 2, 'world': 1}
```

Key idiom: `dict.get(key, 0) + 1` is the cleanest counter pattern.

---

### C2. Build an `OrderStatus` enum, a `describe_order` function, and call it.

**Model answer:**
```python
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


def describe_order(order_id: int, status: OrderStatus) -> str:
    return f"Order {order_id} is currently {status.value}"


print(describe_order(123, OrderStatus.SHIPPED))
# Order 123 is currently shipped
```

This is the exact shape used for intent-tagged routing in the agent build later.

---

## Feedback Summary

| Section | Score |
|---------|-------|
| A — Concepts | 8.5 / 10 |
| B — Predict Output | 6 / 10 |
| C — Write Code | 10 / 10 |
| **Total** | **24.5 / 30 (B+)** |

**Strengths:** code-writing is solid — `dict.get`, `Enum`, type hints, f-strings all comfortable.

**Weak spots to drill before the next exam:**
1. **Truthiness rules** — memorize the falsy values: `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `False`.
2. **Output prediction precision** — copy punctuation exactly when predicting f-string output.
3. **Dict iteration** — `for k, v in d.items():` walkthroughs. Don't say "wrong program" without tracing one loop.
4. **Read the question** — A3 asked for one function using both `*args` and `**kwargs`; two separate functions lost half a mark.
