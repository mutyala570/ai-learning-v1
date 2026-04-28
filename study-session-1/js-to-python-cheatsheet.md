# JavaScript → Python Cheatsheet

A quick translation reference for developers coming from JavaScript. Same data structures and operations, different syntax. Bookmark this when you find yourself thinking "how do I do `[...arr]` in Python?"

## Topics Covered in This Document

1. [**Arrays / Lists**](#arrays--lists)
2. [**Objects / Dicts**](#objects--dicts)
3. [**Spread / Rest Operators**](#spread--rest-operators)
4. [**JSON**](#json)
5. [**Strings**](#strings)
6. [**Truthiness and Null**](#truthiness-and-null)
7. [**Async**](#async)
8. [**Common Gotchas When Translating**](#common-gotchas-when-translating)

---

## Arrays / Lists

| JavaScript | Python | Notes |
|---|---|---|
| `let a = [1, 2, 3]` | `a = [1, 2, 3]` | no `let`/`const` |
| `a.length` | `len(a)` | built-in function, not a property |
| `a.push(x)` | `a.append(x)` | add one item |
| `a.push(...items)` | `a.extend(items)` | add many items |
| `a.pop()` | `a.pop()` | same — removes and returns last |
| `a.shift()` | `a.pop(0)` | remove from front |
| `a.unshift(x)` | `a.insert(0, x)` | add to front |
| `a.indexOf(x)` | `a.index(x)` | Python raises `ValueError` if not found |
| `a.includes(x)` | `x in a` | membership operator |
| `a.slice(1, 3)` | `a[1:3]` | slicing is built-in syntax |
| `a.slice()` (copy) | `a[:]` or `a.copy()` or `list(a)` or `[*a]` | several idioms, all shallow |
| `a.concat(b)` | `a + b` or `[*a, *b]` | both work |
| `a.map(fn)` | `[fn(x) for x in a]` | comprehension is preferred |
| `a.filter(fn)` | `[x for x in a if fn(x)]` | comprehension is preferred |
| `a.reduce((acc, x) => ..., 0)` | `functools.reduce(fn, a, 0)` | rarely used; usually `sum`/loop |
| `a.find(fn)` | `next((x for x in a if fn(x)), None)` | first match or `None` |
| `a.some(fn)` | `any(fn(x) for x in a)` | |
| `a.every(fn)` | `all(fn(x) for x in a)` | |
| `a.sort()` (in place) | `a.sort()` | both mutate |
| `[...a].sort()` (new) | `sorted(a)` | returns new list |
| `a.reverse()` | `a.reverse()` or `a[::-1]` | second is a new list |
| `a.join(",")` | `",".join(a)` | reversed: separator first |
| `"a,b,c".split(",")` | `"a,b,c".split(",")` | same |
| `Array.from({length: 5}, (_, i) => i)` | `list(range(5))` | |

---

## Objects / Dicts

| JavaScript | Python | Notes |
|---|---|---|
| `let o = {a: 1, b: 2}` | `o = {"a": 1, "b": 2}` | keys must be quoted in Python |
| `o.a` | `o["a"]` | no dot notation for dicts |
| `o["a"]` | `o["a"]` | same |
| `o.a ?? "default"` | `o.get("a", "default")` | safe access |
| `"a" in o` | `"a" in o` | same |
| `delete o.a` | `del o["a"]` | |
| `Object.keys(o)` | `list(o.keys())` | `.keys()` returns a view |
| `Object.values(o)` | `list(o.values())` | |
| `Object.entries(o)` | `list(o.items())` | items returns `(key, value)` tuples |
| `Object.assign({}, o)` | `o.copy()` or `{**o}` | shallow copy |
| `{...a, ...b}` | `{**a, **b}` | merge two dicts |
| `for (let k in o)` | `for k in o:` | iterates keys |
| `for (let [k, v] of Object.entries(o))` | `for k, v in o.items():` | iterates pairs |
| `Object.freeze(o)` | no exact equivalent; use `types.MappingProxyType(o)` | rare |

---

## Spread / Rest Operators

The single most useful translation: `*` and `**` in Python work like `...` in JavaScript, but split between iterables (`*`) and dicts (`**`).

| JavaScript | Python | What it does |
|---|---|---|
| `[...a]` | `[*a]` | spread an iterable into a list |
| `{...o}` | `{**o}` | spread a dict into a new dict |
| `[...a, ...b]` | `[*a, *b]` | concat two iterables |
| `{...a, ...b}` | `{**a, **b}` | merge two dicts |
| `function f(...args) {}` | `def f(*args):` | rest of positional args (tuple) |
| `function f({a, b}) {}` | `def f(**kwargs):` | rest of keyword args (dict) |
| `f(...arr)` | `f(*arr)` | call-site spread |
| `f({...obj})` | `f(**obj)` | call-site spread for kwargs |

---

## JSON

| JavaScript | Python | Notes |
|---|---|---|
| `JSON.stringify(o)` | `json.dumps(o)` | needs `import json` |
| `JSON.stringify(o, null, 2)` | `json.dumps(o, indent=2)` | pretty-print |
| `JSON.parse(s)` | `json.loads(s)` | `s` for string |
| `fs.writeFileSync(path, JSON.stringify(o))` | `json.dump(o, open(path, "w"))` | no `s` = file mode |
| `JSON.parse(fs.readFileSync(path))` | `json.load(open(path))` | |

Memory aid: `loads` / `dumps` work on **strings** (`s` = string). `load` / `dump` work on **files**.

---

## Strings

| JavaScript | Python | Notes |
|---|---|---|
| `` `Hello ${name}` `` | `f"Hello {name}"` | f-string |
| `s.length` | `len(s)` | built-in, not a property |
| `s.toUpperCase()` | `s.upper()` | |
| `s.toLowerCase()` | `s.lower()` | |
| `s.trim()` | `s.strip()` | |
| `s.split(",")` | `s.split(",")` | same |
| `s.includes("x")` | `"x" in s` | |
| `s.startsWith("x")` | `s.startswith("x")` | snake_case |
| `s.endsWith("x")` | `s.endswith("x")` | |
| `s.replace("a", "b")` | `s.replace("a", "b")` | both replace **all** in Python (no global flag needed) |
| `s.repeat(3)` | `s * 3` | operator overload |
| `s.charAt(0)` | `s[0]` | strings are sliceable |
| `s.slice(1, 4)` | `s[1:4]` | |

---

## Truthiness and Null

| JavaScript | Python |
|---|---|
| `null`, `undefined` | `None` (one value, not two) |
| `0`, `""`, `null`, `undefined`, `false`, `NaN` are falsy | `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None`, `False` are falsy |
| `if (x)` | `if x:` |
| `x ?? default` | `x if x is not None else default` |
| `x \|\| default` | `x or default` (works on truthiness, like JS `\|\|`) |
| `x === null` | `x is None` |
| `x === y` (deep equal not built-in) | `x == y` |
| `x === y` (reference equal) | `x is y` |

---

## Async

| JavaScript | Python | Notes |
|---|---|---|
| `async function f() {}` | `async def f():` | |
| `await fetch(...)` | `await client.get(...)` | needs `httpx.AsyncClient` |
| `Promise.all([...])` | `await asyncio.gather(...)` | |
| `Promise.resolve(x)` | `asyncio.Future` / direct return from coroutine | rarely needed |
| `setTimeout(fn, 1000)` | `await asyncio.sleep(1)` | sleep is awaitable |
| top-level `await` (modules) | `asyncio.run(main())` | requires explicit entry point |

---

## Common Gotchas When Translating

### 1. Shallow vs deep copy — same problem in both languages
JS `[...a]` and Python `[*a]` (or `.copy()`) are **both shallow**. Nested objects are shared.

```js
const a = [[1, 2]]; const b = [...a]; b[0].push(99);    // a is also affected
```
```python
a = [[1, 2]]; b = [*a]; b[0].append(99)                  # a is also affected
```

For deep copy: JS `structuredClone(a)` / Python `copy.deepcopy(a)`.

### 2. `==` vs `is`
- JS `==` does coercion, `===` does strict equality. Most JS devs use `===`.
- Python `==` is value equality (like JS `===`). Python `is` checks identity (same object). Use `is` only with `None`, `True`, `False`.

### 3. Default parameter trap
JS:
```js
function add(item, basket = []) { basket.push(item); return basket; }
add("a");  // ["a"]
add("b");  // ["b"]   ← fresh each call (JS evaluates default per-call)
```

Python:
```python
def add(item, basket=[]):
    basket.append(item); return basket

add("a")    # ['a']
add("b")    # ['a', 'b']   ⚠️ same list reused!
```

Python evaluates default arguments **once at function definition time**, not per call. Use `basket=None` and create the list inside.

### 4. Snake_case vs camelCase
JS: `myVariable`, `myFunction()`. Python: `my_variable`, `my_function()`. Even built-in methods follow this — `startsWith` becomes `startswith`.

### 5. No semicolons, indentation matters
Python uses indentation to define blocks instead of `{}`. Inconsistent indentation is a syntax error. Pick 4 spaces and stick to it.

### 6. `length` is a function, not a property
- JS: `arr.length`, `str.length` — properties.
- Python: `len(arr)`, `len(str)` — built-in function.

### 7. No `null` AND `undefined` — only `None`
Python has just one "absence" value. No equivalent of `undefined`.

### 8. Method chaining returns vs in-place
JS `arr.sort()` returns the sorted array (so you can chain). Python `arr.sort()` returns `None` and sorts in place. Use `sorted(arr)` if you want a chainable / new-list version.
