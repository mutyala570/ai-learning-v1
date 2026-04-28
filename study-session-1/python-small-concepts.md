# Python Small Concepts — Quick Reference

A short reference for the small Python concepts that keep showing up in AI / agent code but are easy to half-learn and forget. Each section explains *what it is*, *why it matters*, and shows a *minimal example* you can read in under a minute.

This is a cheatsheet, not a tutorial. Read top to bottom once, then come back to whichever section you need.

---

## 🎯 Tonight's Priority — Learn These First

Don't try to read all 20 sections in one sitting. Tonight, focus on **these 8** in this exact order. Each one is short — 2 to 5 minutes of reading. Once you have read a section, ping me and we will discuss it together until you have it locked in.

> Total time tonight: about **45 minutes of reading + discussion**. The rest of the file can wait.

### Round 1 — The four you explicitly said you don't know (do these first)

| # | Topic | Why tonight |
|---|---|---|
| 1 | [`*args` and `**kwargs`](#args-and-kwargs) | Show up in *every* LangChain / FastAPI function. Must know cold. |
| 2 | [`lambda`](#lambda-functions) | One-line functions for `sorted`, `filter`, `key=`. Tiny but constant. |
| 3 | [`typing.Literal`](#typingliteral) | This is how intent types are typed in your agent code. Will be used immediately. |
| 4 | [Docstrings](#docstrings) | Every function you write from now on should have one. Habit-forming. |

### Round 2 — Your weak spots from Exam 1 (drill these next)

| # | Topic | Why tonight |
|---|---|---|
| 5 | [Truthiness and falsy values](#truthiness-and-falsy-values) | You lost marks on `if x:` reasoning. Memorize the falsy list. |
| 6 | [`dict.get()` pattern](#dictget-pattern) | You said B3 was a "wrong program" — it was just dict iteration. Lock this in. |

### Round 3 — Universal building blocks (the rest of AI code uses these constantly)

| # | Topic | Why tonight |
|---|---|---|
| 7 | [Comprehensions](#comprehensions-list-dict-set) | One-line list/dict building. You will write 10+ a day. |
| 8 | [String methods](#string-methods) | `.strip()`, `.split()`, `.join()` — every script uses these. |

### How tonight works

There are **8 topics** to cover tonight (numbered 1 to 8 in the tables above). The 3 "Rounds" are just how I grouped them — Round 1 has topics 1–4, Round 2 has topics 5–6, Round 3 has topics 7–8.

1. Read **topic 1** — `*args` / `**kwargs`. Type the example into a Python file and run it.
2. Tell me **"done with 1"** — I will ask you a quick verbal question to confirm.
3. Move to **topic 2**, repeat.
4. After all 8 topics, we will run a quick **5-question oral quiz** (no writing, just chat) to confirm.

### What to skip tonight (cover later)

- Topics 9–13 (Optional/Union, enumerate/zip, unpacking, `is` vs `==`, f-string tricks) — useful but not blocking.
- Topics 14–20 (string methods are *included tonight* as topic 8, but slicing, `in`, `isinstance`, `sorted`, `json`, mutable default trap can wait) — pick these up over the week as you write code.
- Topics 21–27 (map/filter, any/all, built-ins, type conversion, list methods, dict methods, multiple returns) — bonus reference material, cover this weekend or next week.

## Topics Covered in This Document

1. [**`*args` and `**kwargs`**](#args-and-kwargs)
2. [**`lambda` Functions**](#lambda-functions)
3. [**`typing.Literal`**](#typingliteral)
4. [**Docstrings**](#docstrings)
5. [**Truthiness and Falsy Values**](#truthiness-and-falsy-values)
6. [**`dict.get()` Pattern**](#dictget-pattern)
7. [**Comprehensions (List, Dict, Set)**](#comprehensions-list-dict-set)
8. [**Ternary Expression**](#ternary-expression)
9. [**`typing.Optional` and `typing.Union`**](#typingoptional-and-typingunion)
10. [**`enumerate()` and `zip()`**](#enumerate-and-zip)
11. [**Unpacking**](#unpacking)
12. [**`is` vs `==`**](#is-vs)
13. [**f-string Formatting Tricks**](#f-string-formatting-tricks)
14. [**String Methods**](#string-methods)
15. [**Slicing**](#slicing)
16. [**`in` Operator**](#in-operator)
17. [**`isinstance()` and `type()`**](#isinstance-and-type)
18. [**`sorted()` vs `.sort()`**](#sorted-vs-sort)
19. [**`json.loads` and `json.dumps`**](#jsonloads-and-jsondumps)
20. [**Mutable Default Argument Trap**](#mutable-default-argument-trap)
21. [**`map()` and `filter()`**](#map-and-filter)
22. [**`any()` and `all()`**](#any-and-all)
23. [**Common Built-in Functions**](#common-built-in-functions)
24. [**Type Conversion Functions**](#type-conversion-functions)
25. [**List Methods**](#list-methods)
26. [**Dict Methods**](#dict-methods)
27. [**Multiple Return Values**](#multiple-return-values)

---

## `*args` and `**kwargs`

These let a function accept **any number** of extra arguments without listing them one by one. The names `args` and `kwargs` are a convention — the magic is in the `*` and `**`.

- `*args` collects extra **positional** arguments into a **tuple**.
- `**kwargs` collects extra **keyword** arguments into a **dict**.
- Order in a signature is fixed: `def f(positional, *args, keyword_only=None, **kwargs)`.

```python
def demo(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)

demo(1, 2, 3, name="Prem", role="dev")
# args:   (1, 2, 3)
# kwargs: {'name': 'Prem', 'role': 'dev'}
```

You can also use `*` and `**` at a **call site** to *unpack* a list or dict into a function call:

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
config = {"a": 10, "b": 20, "c": 30}

add(*nums)      # → 6   (same as add(1, 2, 3))
add(**config)   # → 60  (same as add(a=10, b=20, c=30))
```

You will see this pattern constantly in LangChain and FastAPI when configs are forwarded into another function.

---

## `lambda` Functions

A **lambda** is a tiny, anonymous, one-line function. It is useful when you need a function for a moment — usually as an argument to `sorted`, `filter`, `map`, or `key=`.

The syntax is `lambda <args>: <expression>` — note: only an expression, not a block of statements.

```python
square = lambda x: x * x
square(5)   # → 25
```

Where lambdas actually shine — passing a sort key:

```python
orders = [
    {"id": 1, "amount": 250},
    {"id": 2, "amount": 80},
    {"id": 3, "amount": 600},
]

sorted(orders, key=lambda o: o["amount"])
# [{'id': 2, 'amount': 80}, {'id': 1, 'amount': 250}, {'id': 3, 'amount': 600}]
```

If the lambda gets longer than one expression, switch to `def`. Lambdas are not better than `def` — they are just shorter when the function fits on one line.

---

## `typing.Literal`

`Literal` restricts a value to a **fixed set of constants** instead of any string or any int. The Python interpreter does not enforce this at runtime, but type checkers (mypy, Pyright, your IDE) will flag wrong values before the code ever runs.

```python
from typing import Literal

IntentName = Literal["order_status", "cancellation", "policy_qa", "small_talk"]

def route(intent: IntentName) -> str:
    return f"Routing to {intent}"

route("order_status")     # ok
route("random_text")      # type checker flags this
```

Use `Literal` when:
- A function argument should only be one of a small fixed set of strings (intent names, log levels, modes).
- The set is known at code time and rarely changes.

Use `enum.Enum` instead when:
- You want runtime-checked values, iteration over the set, or a single source of truth that lives as an object (`Status.ACTIVE`).

`Literal` is lighter (just a type hint); `Enum` is heavier (a real class). Both are valid — pick by whether you need runtime behavior.

---

## Docstrings

A **docstring** is a string that sits as the very first statement inside a function, class, or module. It is the official place to describe *what the thing does, what it expects, and what it returns*. Tools like IDE tooltips, `help()`, and documentation generators read it automatically.

```python
def count_words(text: str) -> dict[str, int]:
    """Return a dict of word -> count for `text`, case-insensitive.

    Args:
        text: any string. Empty strings return an empty dict.

    Returns:
        A dict mapping each lowercased word to how many times it appears.
    """
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

Conventions:
- Triple-quoted (`"""..."""`) so it can span multiple lines.
- First line: a one-sentence summary in imperative mood ("Return", not "Returns").
- Optional sections: **Args**, **Returns**, **Raises**, **Examples**.

A class docstring goes right under `class Foo:`. A module docstring goes at the very top of the file. You can read any docstring at runtime via `function.__doc__` or `help(function)`.

---

## Truthiness and Falsy Values

Python lets you write `if x:` directly — no need for `if x == True`. The `if` evaluates the **truthiness** of `x`. Knowing what counts as falsy is essential.

**Falsy values** (treated as `False`):
- `None`
- `0`, `0.0`
- `""` (empty string)
- `[]`, `{}`, `set()`, `()` (empty collections)
- `False`

Everything else is truthy.

```python
items = []
if items:
    print("has items")
else:
    print("empty")     # ← prints

name = ""
if name:
    print(f"hi {name}")
else:
    print("no name")   # ← prints
```

This is why `if response.get("data"):` is enough — you do not need `if response.get("data") is not None and len(response.get("data")) > 0`.

---

## `dict.get()` Pattern

`d[key]` raises `KeyError` if the key does not exist. `d.get(key, default)` returns the default instead. This is the safer pattern for any dict whose shape you do not 100% control — including LLM JSON output, API responses, and config files.

```python
config = {"timeout": 30}

config["timeout"]                  # 30
config["retries"]                  # KeyError!
config.get("retries")              # None  (no error)
config.get("retries", 3)           # 3     (default)
```

The classic counter idiom uses this pattern:

```python
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
```

For automatic defaults across many keys, `collections.defaultdict` is the next step up:

```python
from collections import defaultdict
counts = defaultdict(int)
for word in words:
    counts[word] += 1
```

---

## Comprehensions (List, Dict, Set)

A **comprehension** is a one-line way to build a list, dict, or set from another iterable, with an optional filter.

**List comprehension** — `[expression for item in iterable if condition]`:
```python
nums = [1, 2, 3, 4, 5]
even_squares = [n * n for n in nums if n % 2 == 0]
# [4, 16]
```

**Dict comprehension** — `{key: value for item in iterable if condition}`:
```python
inventory = {"apples": 5, "bananas": 0, "cherries": 12}
in_stock = {fruit: qty for fruit, qty in inventory.items() if qty > 0}
# {'apples': 5, 'cherries': 12}
```

**Set comprehension** — `{expression for item in iterable}`:
```python
words = ["apple", "banana", "apple", "cherry"]
unique = {w for w in words}
# {'apple', 'banana', 'cherry'}
```

Comprehensions are faster and more readable than building the same thing with a `for` loop and `.append()` — but only up to one or two clauses. Anything more complex should be a normal loop.

---

## Ternary Expression

A one-line `if/else` for a value, not a block. The shape is `<value_if_true> if <condition> else <value_if_false>`.

```python
age = 20
status = "adult" if age >= 18 else "minor"
# "adult"
```

Useful inside an f-string or comprehension:

```python
greeting = f"Hello {'Mr.' if is_male else 'Ms.'} {name}"
flags = [1 if x > 0 else 0 for x in numbers]
```

Use it for short, obvious checks. If it gets nested or hard to read, switch back to a regular `if/else`.

---

## `typing.Optional` and `typing.Union`

These describe values that can be **more than one type**.

- `Optional[X]` is shorthand for `Union[X, None]` — "either an `X` or `None`".
- `Union[X, Y]` means "either an `X` or a `Y`".

```python
from typing import Optional, Union

def find_user(user_id: int) -> Optional[dict]:
    """Return the user dict, or None if not found."""
    ...

def parse_input(value: Union[str, int]) -> str:
    return str(value)
```

In Python 3.10+, you can use the **pipe syntax** instead, which is now preferred:

```python
def find_user(user_id: int) -> dict | None: ...
def parse_input(value: str | int) -> str: ...
```

Both styles mean the same thing. Pipe syntax is shorter; `Optional`/`Union` are still common in older code and tutorials.

---

## `enumerate()` and `zip()`

Two built-ins that replace clumsy index-tracking loops.

**`enumerate(iterable)`** — gives you `(index, item)` pairs:
```python
for i, name in enumerate(["alice", "bob", "carol"]):
    print(i, name)
# 0 alice
# 1 bob
# 2 carol
```

**`zip(a, b)`** — pairs items from two (or more) iterables side-by-side:
```python
ids = [1, 2, 3]
names = ["alice", "bob", "carol"]

for user_id, name in zip(ids, names):
    print(user_id, name)
# 1 alice
# 2 bob
# 3 carol
```

`zip` stops at the shortest iterable. Combine the two when you need both an index and parallel data.

---

## Unpacking

Python lets you assign multiple variables at once by **unpacking** an iterable.

```python
a, b = (1, 2)              # a=1, b=2
x, y, z = [10, 20, 30]     # x=10, y=20, z=30

# Swap variables in one line:
a, b = b, a
```

You can also use `*` to capture "the rest":
```python
first, *rest = [1, 2, 3, 4]
# first=1, rest=[2, 3, 4]

*head, last = [1, 2, 3, 4]
# head=[1, 2, 3], last=4
```

This is exactly the same `*` you saw in `*args` — it means "collect into a list/tuple."

---

## `is` vs `==`

Two comparison operators, two different questions:

- `==` asks **are the values equal?**
- `is` asks **are these the *same object* in memory?**

```python
a = [1, 2, 3]
b = [1, 2, 3]

a == b   # True   (same values)
a is b   # False  (different list objects)

c = a
a is c   # True   (same object)
```

Rule of thumb:
- Use `==` for value comparisons (almost always what you want).
- Use `is` only when comparing to **`None`**, **`True`**, **`False`**, or singleton enum members.

```python
if x is None: ...        # ✅ correct
if x == None: ...        # works but not idiomatic
```

---

## f-string Formatting Tricks

f-strings can do more than simple substitution — they support format specifiers after a colon.

```python
pi = 3.14159265
print(f"{pi:.2f}")        # 3.14   (2 decimal places)
print(f"{pi:.4f}")        # 3.1416

n = 1234567
print(f"{n:,}")           # 1,234,567   (thousands separators)

name = "prem"
print(f"{name:>10}")      # "      prem"  (right-aligned in 10 chars)
print(f"{name:<10}")      # "prem      "  (left-aligned)
print(f"{name:^10}")      # "   prem   "  (centered)

print(f"{0.85:.0%}")      # 85%     (percentage)

obj = {"a": 1}
print(f"{obj!r}")         # {'a': 1}     (uses repr() instead of str())
```

A handy debug shortcut introduced in Python 3.8 — adding `=` after a variable inside an f-string prints both the name and value:

```python
x = 42
print(f"{x=}")        # x=42
print(f"{x*2=}")      # x*2=84
```

Useful for quick debug prints without typing the variable name twice.

---

## String Methods

A handful of string methods show up in almost every Python script. They all return a **new string** — the original is never modified, because strings in Python are immutable.

```python
s = "  Hello, World!  "

s.strip()                  # "Hello, World!"        (remove leading/trailing whitespace)
s.lower()                  # "  hello, world!  "
s.upper()                  # "  HELLO, WORLD!  "
s.replace("World", "Prem") # "  Hello, Prem!  "
s.startswith("  Hello")    # True
s.endswith("!")            # False                  (note the trailing spaces)
s.strip().endswith("!")    # True
```

`.split()` and `.join()` are the two you will use most for parsing and building text:

```python
"a,b,c,d".split(",")                # ['a', 'b', 'c', 'd']
"hello world  python".split()       # ['hello', 'world', 'python']  (no arg = any whitespace)

",".join(["a", "b", "c"])           # 'a,b,c'
" ".join(["hello", "world"])        # 'hello world'
```

A common pattern when handling user input: `.strip().lower()` to normalize before comparing.

```python
user_input = "  YES  "
if user_input.strip().lower() == "yes":
    confirm = True
```

---

## Slicing

Slicing extracts a sub-section of a sequence (string, list, tuple). The full form is `seq[start:stop:step]` — every part is optional.

- `start` — index to start at (inclusive). Default `0`.
- `stop` — index to stop **before** (exclusive). Default end of sequence.
- `step` — how far to jump. Default `1`. Negative reverses direction.

```python
nums = [10, 20, 30, 40, 50]

nums[1:4]      # [20, 30, 40]      (indices 1, 2, 3)
nums[:3]       # [10, 20, 30]      (start to index 3)
nums[2:]       # [30, 40, 50]      (index 2 to end)
nums[-2:]      # [40, 50]          (last two — negative counts from end)
nums[::-1]     # [50, 40, 30, 20, 10]   (reversed)
nums[::2]      # [10, 30, 50]      (every second item)
```

Strings work the same way — they are sequences of characters:

```python
s = "Hello, Prem"
s[:5]          # 'Hello'
s[-4:]         # 'Prem'
s[::-1]        # 'merP ,olleH'
```

Slicing **never raises an error** for out-of-bound indices — it just returns whatever fits. This makes it safe to write `s[:100]` even if `s` is shorter than 100 characters.

---

## `in` Operator

`in` checks whether something is **a member of** a sequence or collection. It returns `True` or `False`.

```python
"a" in ["a", "b", "c"]        # True
5 in (1, 2, 3)                # False
"hello" in "hello world"      # True   (substring check on strings)
"name" in {"name": "Prem"}    # True   (checks keys, not values)
```

The opposite is `not in`:

```python
if "admin" not in user.roles:
    raise PermissionError
```

**Speed matters**: `in` on a **set** or **dict** is roughly *constant time* (O(1)) because of hashing. `in` on a **list** is *linear time* (O(n)) — Python checks every element. For large collections used for membership checks, build a `set` once and reuse it.

```python
allowed = {"admin", "manager", "owner"}    # build once
if user.role in allowed: ...               # fast every time
```

---

## `isinstance()` and `type()`

Both ask "what type is this?" but they answer slightly different questions.

- `type(x)` returns the **exact** class of `x`.
- `isinstance(x, T)` returns `True` if `x` is of type `T` **or any subclass of `T`**.

```python
class Animal: pass
class Dog(Animal): pass

d = Dog()

type(d) == Dog           # True
type(d) == Animal        # False  (exact match only)

isinstance(d, Dog)       # True
isinstance(d, Animal)    # True   (Dog inherits from Animal)
```

**Use `isinstance` almost always** — it respects inheritance, which is what you want 99% of the time. `type()` is for rare cases where you genuinely need an exact match.

`isinstance` also accepts a tuple of types — handy for "any of these":

```python
def to_str(value):
    if isinstance(value, (int, float)):
        return f"{value:.2f}"
    if isinstance(value, str):
        return value.strip()
    return str(value)
```

You will see this pattern when validating LLM output that might come back as different types.

---

## `sorted()` vs `.sort()`

Two ways to sort a list — they look similar but behave differently:

- **`sorted(seq)`** — returns a **new sorted list**. Original is untouched.
- **`list.sort()`** — sorts the list **in place**. Returns `None`.

```python
nums = [3, 1, 4, 1, 5, 9, 2, 6]

# sorted() — original list stays the same
result = sorted(nums)
print(result)    # [1, 1, 2, 3, 4, 5, 6, 9]
print(nums)      # [3, 1, 4, 1, 5, 9, 2, 6]

# .sort() — original list is changed, returns None
nums.sort()
print(nums)      # [1, 1, 2, 3, 4, 5, 6, 9]
```

Both accept a `key=` callable (often a lambda) to sort by a derived value, and a `reverse=True` flag.

```python
orders = [{"id": 1, "amount": 250}, {"id": 2, "amount": 80}]

sorted(orders, key=lambda o: o["amount"], reverse=True)
# [{'id': 1, 'amount': 250}, {'id': 2, 'amount': 80}]
```

Common gotcha: `result = nums.sort()` makes `result` equal to `None`, not the sorted list. If you want both the sorted result and the original preserved, use `sorted()`.

`sorted()` also works on any iterable (not just lists) and always returns a list:

```python
sorted("hello")                  # ['e', 'h', 'l', 'l', 'o']
sorted({3, 1, 2})                # [1, 2, 3]
sorted({"b": 2, "a": 1}.items()) # [('a', 1), ('b', 2)]
```

---

## `json.loads` and `json.dumps`

The Python `json` module converts between Python objects and JSON strings — critical for handling LLM output, API requests, and config files.

The names are confusing: think of `s` as **string**.

- **`json.loads(string)`** — parse a JSON **string** into a Python object.
- **`json.dumps(obj)`** — serialize a Python **object** to a JSON string.

```python
import json

# JSON string → Python dict
text = '{"name": "Prem", "age": 27, "active": true}'
data = json.loads(text)
print(data)            # {'name': 'Prem', 'age': 27, 'active': True}
print(data["name"])    # Prem

# Python dict → JSON string
obj = {"name": "Prem", "items": [1, 2, 3]}
text = json.dumps(obj)
print(text)            # {"name": "Prem", "items": [1, 2, 3]}

# Pretty-printed
print(json.dumps(obj, indent=2))
# {
#   "name": "Prem",
#   "items": [
#     1,
#     2,
#     3
#   ]
# }
```

There is also `json.load(file)` and `json.dump(obj, file)` (no `s`) — those work directly with file objects instead of strings. The same `s` rule applies: `s` = string.

LLM output that claims to be JSON is often almost-but-not-quite valid JSON. Wrap parsing in a try/except so a bad response does not crash the whole flow:

```python
import json

try:
    parsed = json.loads(llm_output)
except json.JSONDecodeError as e:
    print(f"LLM returned invalid JSON: {e}")
    parsed = None
```

---

## Mutable Default Argument Trap

This is the most famous Python gotcha. **A default argument is evaluated once, when the function is defined — not every time the function is called.** Mutable defaults (like `[]` or `{}`) are then shared across every call.

```python
def add_item(item, basket=[]):    # ⚠️ trap
    basket.append(item)
    return basket

print(add_item("apple"))     # ['apple']
print(add_item("banana"))    # ['apple', 'banana']   ← surprise!
print(add_item("cherry"))    # ['apple', 'banana', 'cherry']
```

The same `[]` is reused across all three calls because the default was created once at `def` time.

**The fix** — use `None` as the default and create a fresh list inside the function:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket

print(add_item("apple"))     # ['apple']
print(add_item("banana"))    # ['banana']     ✅ fresh list each call
print(add_item("cherry"))    # ['cherry']
```

The same trap applies to `{}`, `set()`, and any other mutable default. **Rule: never put a mutable object as a default argument value.** Use `None` and build the real default inside the body.

Immutable defaults (`0`, `""`, `None`, tuples) are fine — they cannot be mutated, so the shared-state bug cannot happen.

---

## `map()` and `filter()`

These are **functional tools** — they apply a function to every item of an iterable. Both return an iterator (lazy), so you usually wrap them in `list()` to actually see the result.

**`map(func, iterable)`** — apply `func` to every item, return the results.
```python
nums = [1, 2, 3, 4]
squared = list(map(lambda x: x * x, nums))
# [1, 4, 9, 16]

# Same with a named function:
def double(x): return x * 2
list(map(double, nums))   # [2, 4, 6, 8]
```

**`filter(func, iterable)`** — keep only items where `func(item)` is truthy.
```python
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
# [2, 4, 6]
```

A **list comprehension** does the same thing and is usually more readable:

```python
# map version:
list(map(lambda x: x * x, nums))

# comprehension version (preferred):
[x * x for x in nums]

# filter version:
list(filter(lambda x: x % 2 == 0, nums))

# comprehension version (preferred):
[x for x in nums if x % 2 == 0]
```

**When to use which:**
- Use a comprehension as your default — it is more "Pythonic".
- Use `map`/`filter` when the function already exists and is named (`map(int, ["1", "2"])`).
- You will see `map`/`filter` in older codebases and in some LangChain pipelines, so recognize the syntax even if you do not write it yourself.

**`reduce()`** also exists in `functools` for cumulative reductions, but `sum()`, `min()`, `max()`, or a plain loop usually replaces it. Skip it unless you hit it.

---

## `any()` and `all()`

Two built-ins that ask boolean questions about an iterable. Both return `True` or `False`.

**`any(iterable)`** — `True` if **at least one** item is truthy.
**`all(iterable)`** — `True` if **every** item is truthy.

```python
any([False, False, True])      # True
any([False, False, False])     # False
any([])                        # False (vacuous — nothing truthy)

all([True, True, True])        # True
all([True, False, True])       # False
all([])                        # True  (vacuous — no counter-example)
```

The real power comes from combining them with a generator expression — a one-liner check across data:

```python
required = ["name", "email", "phone"]
data = {"name": "Prem", "email": "x@y.com", "phone": "555"}

if all(field in data for field in required):
    print("all required fields present")

users = [{"active": True}, {"active": False}, {"active": True}]
if any(u["active"] for u in users):
    print("at least one active user")
```

These two replace many ugly `for` loops with `flag = True` and early `break`.

---

## Common Built-in Functions

A small set of built-ins shows up in almost every Python file. Worth knowing without thinking.

```python
len([1, 2, 3])           # 3      — length of any sequence (str, list, dict, set, tuple)
sum([1, 2, 3])           # 6      — adds up a numeric iterable
min([3, 1, 4, 1, 5])     # 1      — smallest element
max([3, 1, 4, 1, 5])     # 5      — largest element
abs(-7)                  # 7      — absolute value
round(3.14159, 2)        # 3.14   — round to N decimal places
range(5)                 # 0..4   — generates 0, 1, 2, 3, 4 (lazy)
list(range(5))           # [0, 1, 2, 3, 4]
list(range(2, 8))        # [2, 3, 4, 5, 6, 7]
list(range(0, 10, 2))    # [0, 2, 4, 6, 8]   (with step)
```

`min` and `max` also accept a `key=` callable, just like `sorted`:

```python
orders = [{"id": 1, "amount": 250}, {"id": 2, "amount": 80}]
max(orders, key=lambda o: o["amount"])
# {'id': 1, 'amount': 250}
```

`sum`, `min`, and `max` work on any iterable — including generator expressions, which avoids building intermediate lists:

```python
total = sum(item["price"] for item in cart)   # no intermediate list
```

---

## Type Conversion Functions

Python has a built-in function for every basic type. Each one takes a value and returns a converted version (or raises `ValueError` if it cannot).

```python
int("42")            # 42        — string to int
int(3.9)             # 3         — float to int (truncates, does not round)
float("3.14")        # 3.14      — string to float
str(42)              # "42"      — anything to string
bool(0)              # False     — uses truthiness rules
bool("hello")        # True
list("abc")          # ['a', 'b', 'c']      — string to list of chars
list((1, 2, 3))      # [1, 2, 3]            — tuple to list
tuple([1, 2, 3])     # (1, 2, 3)            — list to tuple
set([1, 1, 2, 3])    # {1, 2, 3}            — list to set (drops duplicates)
dict([("a", 1), ("b", 2)])    # {"a": 1, "b": 2}   — list of pairs to dict
```

Common patterns in AI code:

```python
# Deduplicate while preserving the original list type
unique = list(set(items))

# LLM returned the count as a string — convert before doing math
count = int(response["count"])

# Force a value to be a string for safe printing/logging
log_value = str(value)
```

`int()` on a non-numeric string raises `ValueError`. Wrap in try/except when the source is untrusted:

```python
try:
    n = int(user_input)
except ValueError:
    n = 0
```

---

## List Methods

A list is mutable, and Python gives it a small set of methods to modify it in place. These all return `None` (except `.pop()` and `.index()`/`.count()` which return values).

```python
nums = [1, 2, 3]

nums.append(4)          # [1, 2, 3, 4]                 — add one item to the end
nums.extend([5, 6])     # [1, 2, 3, 4, 5, 6]           — add multiple items
nums.insert(0, 99)      # [99, 1, 2, 3, 4, 5, 6]       — insert at index
nums.pop()              # returns 6, nums becomes [99, 1, 2, 3, 4, 5]
nums.pop(0)             # returns 99, removes from front
nums.remove(3)          # removes first occurrence of value 3
nums.index(4)           # returns the index of value 4
nums.count(2)           # how many times 2 appears
nums.reverse()          # reverses in place
nums.sort()             # sorts in place (covered separately above)
nums.clear()            # empties the list
```

**Common gotchas:**

- `.append(x)` adds **one item**. `.extend([x, y])` adds **multiple items**. Mixing them up is a classic bug:
  ```python
  a = [1, 2, 3]
  a.append([4, 5])    # [1, 2, 3, [4, 5]]   ← nested!
  a.extend([4, 5])    # [1, 2, 3, 4, 5]     ← flat
  ```
- `.pop()` returns the removed item. `.remove(value)` does not — it returns `None`.
- `.remove(value)` only removes the **first** match and raises `ValueError` if the value is not in the list.

---

## Dict Methods

A dict is also mutable. The methods below cover 95% of dict work.

```python
d = {"a": 1, "b": 2, "c": 3}

d.keys()             # dict_keys(['a', 'b', 'c'])
d.values()           # dict_values([1, 2, 3])
d.items()            # dict_items([('a', 1), ('b', 2), ('c', 3)])

d.get("a")           # 1
d.get("z")           # None
d.get("z", 0)        # 0  (default)

d.setdefault("a", 99)   # 1   — key exists, returns current value, no change
d.setdefault("z", 99)   # 99  — key did not exist, inserts and returns

d.update({"a": 10, "x": 100})    # merges another dict in
# d → {"a": 10, "b": 2, "c": 3, "x": 100}

d.pop("a")           # 10, removes key "a"
d.pop("missing", None)   # None, no error because of the default

del d["b"]           # remove key "b"
d.clear()            # empties the dict
```

**`.setdefault` is the cleanest way to group items into a dict of lists** — it replaces the "if key not in d" check:

```python
groups = {}
for order in orders:
    groups.setdefault(order["status"], []).append(order)
# groups → {"pending": [...], "shipped": [...], ...}
```

`.keys()`, `.values()`, and `.items()` return **view objects** that update if the dict changes. To get a snapshot list, wrap in `list()`: `list(d.keys())`.

---

## Multiple Return Values

A function can return more than one value by returning a **tuple**. The caller can unpack it into separate variables in one line.

```python
def get_user():
    return "Prem", 27, "Hyderabad"

name, age, city = get_user()
# name="Prem", age=27, city="Hyderabad"
```

The parentheses are optional — `return "Prem", 27, "Hyderabad"` returns the tuple `("Prem", 27, "Hyderabad")`. Both styles are equivalent.

This is one of Python's nicest features. It removes the need for output-parameter tricks (which other languages need) or wrapping multiple values in a one-off class.

A common pattern is **return value + status flag**:

```python
def parse(text):
    try:
        return int(text), True       # success: value, ok=True
    except ValueError:
        return None, False           # failure: no value, ok=False

value, ok = parse("42")
if not ok:
    print("could not parse")
```

If you only care about some of the returned values, use `_` for the ones you want to ignore:

```python
name, _, city = get_user()    # ignore age
```

If a function returns **many** values, switch to a `dataclass` or a `TypedDict` instead — those scale better than tuples once you go past 3 or 4 fields.
