# Python `pdb` — Quick Debugging Reference

How to step through any Python script line by line on Mac, no IDE needed.

## How to start

Add **one line** at the spot you want to pause:

```python
def some_function(...):
    breakpoint()                      # ← drops into pdb here
    ...
```

Run the script normally:

```bash
python3 path/to/script.py
```

Execution stops at `breakpoint()` and you get a `(Pdb)` prompt.

## Commands at the `(Pdb)` prompt

| Command | What it does |
|---------|--------------|
| `n` | run the **next** line (step over) |
| `s` | step **into** a function call |
| `c` | **continue** until the next `breakpoint()` or end of script |
| `q` | **quit** the debugger and stop the script |
| `l` | **list** the surrounding code with `->` showing the current line |
| `p variable` | **print** any variable's value |
| `pp variable` | **pretty-print** (good for long objects) |

## The arrow gotcha

```
(Pdb) -> response = some_call(...)
            ^
            NOT yet executed.
```

The `->` arrow points to the line **about to run**, not the one that just ran. So:

- `p response` here raises `NameError` — the line hasn't run yet, the variable doesn't exist.
- Press `n` first to **execute** the line. Then `p response` works.

> **Mental model:** `p` shows what *exists* now, not what's about to happen.

## Typical session

```
(Pdb) l               # list current code with arrow
(Pdb) p message       # inspect a variable that already exists
(Pdb) n               # run the current line
(Pdb) p response      # now inspect what was just assigned
(Pdb) c               # run to end (or next breakpoint)
```

## Don't forget to remove `breakpoint()` when done

Otherwise the script pauses every time you run it. Just delete the line.
