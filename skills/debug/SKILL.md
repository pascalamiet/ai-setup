---
name: debug
description: |
  Systematic debugging workflow for any language or environment.
  Use when: something is broken and you need a structured approach to find and fix it.
  Covers error reading, isolation, hypothesis testing, and common bug patterns.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# Debug

You are a systematic debugger. Your job is to find the root cause of a bug through disciplined diagnosis — not trial and error. You follow a structured protocol: reproduce, isolate, hypothesize, verify, fix. You do not guess randomly or apply fixes without understanding the cause.

## When to Apply

Use this skill when:
- Something is broken and the cause is unclear
- An error message appears and needs interpretation
- A function returns unexpected output
- Tests are failing
- Behavior differs between environments
- A previously working system has stopped working

---

## The Debugging Protocol

### Step 1 — Reproduce
Before anything else, establish a reliable reproduction.

- [ ] Can you reproduce the bug consistently?
- [ ] What are the exact inputs, environment, and steps?
- [ ] Does it reproduce in a clean environment (fresh Python env, new R session, etc.)?
- [ ] Has anything changed recently? (last working commit, dependency update, data change)

**If you cannot reproduce it, you cannot debug it.** Focus on reproduction first.

Minimal reproducible example (MRE):
- Strip the failing code down to the smallest possible case that still fails
- Remove everything that is not necessary to trigger the bug
- Hard-code inputs; remove external dependencies

### Step 2 — Read the Error Message
Error messages tell you most of what you need. Read them carefully before doing anything else.

```
[Error type]: [Description]
  File "path/to/file.py", line 42, in function_name
    problematic_line_of_code
```

Extract:
1. **Error type** — what kind of failure is this? (TypeError, KeyError, SegFault, etc.)
2. **Location** — which file, line, function?
3. **Message** — what exactly does it say? Read it literally.
4. **Traceback** — read from bottom to top: the bottom is where the error occurred; the top is where it started

**Common mistake:** Reading only the last line. Always read the full traceback.

### Step 3 — Isolate
Narrow down where the bug lives using binary search.

- Comment out half the code — does the error still occur?
- Add print/log statements to trace values at each step
- Check: at what point does the variable have the wrong value?
- Test individual functions or components in isolation

**Bisection approach:**
- Bug occurs in steps 1–10
- Disable steps 6–10 — does bug still occur? → bug is in 1–5
- Disable steps 3–5 — does bug still occur? → bug is in 1–2
- Continue until isolated

### Step 4 — Hypothesize
Form a specific hypothesis about the cause before touching anything.

A good hypothesis:
- Is specific ("variable `x` is None at line 42 because the merge on line 28 drops all rows")
- Makes a testable prediction ("if I print `x` before line 42, it will be None")
- Implies a fix ("the merge condition should be `left_join` not `inner_join`")

A bad hypothesis:
- "Something is wrong with the function"
- "It might be a memory issue"
- "Maybe there's a bug in the library"

### Step 5 — Verify
Test your hypothesis *before* applying the fix.

- Add an assertion or print statement to confirm your predicted cause
- If the evidence doesn't match your hypothesis, revise the hypothesis
- Do not apply a fix based on an unverified hypothesis

### Step 6 — Fix and Confirm
Apply the minimal fix that addresses the root cause.

- Fix the cause, not the symptom (do not just catch the exception and move on)
- Verify the fix actually resolves the original error
- Run the full test suite to confirm no regressions
- Understand *why* the fix works before moving on

---

## Reading Error Messages by Language

### Python
```python
Traceback (most recent call last):
  File "script.py", line 15, in <module>
    result = process(data)
  File "script.py", line 8, in process
    return df['column']
KeyError: 'column'
```
→ Read bottom-up. The error is `KeyError: 'column'` in the `process` function. The column name probably doesn't exist in `df`. Check `df.columns`.

Common Python errors:
| Error | Likely cause |
|---|---|
| `KeyError` | Dict key or DataFrame column doesn't exist |
| `AttributeError` | Called method on wrong type (often `None`) |
| `TypeError` | Wrong type passed to function; check argument types |
| `ValueError` | Right type, wrong value (e.g., wrong shape for numpy) |
| `IndexError` | List/array access out of bounds |
| `ImportError` | Module not installed or path is wrong |
| `RecursionError` | Infinite recursion; check base case |

### R
```r
Error in df[["column"]] : subscript out of bounds
```
Common R errors:
| Error | Likely cause |
|---|---|
| `object not found` | Typo in variable name; not in scope |
| `subscript out of bounds` | Column or index doesn't exist |
| `non-numeric argument to binary operator` | Type mismatch; inspect `class()` |
| `NAs introduced by coercion` | `as.numeric()` on non-numeric strings |
| `could not find function` | Package not loaded; function name typo |
| `unused argument` | Passed an argument the function doesn't accept |

### Stata
Common Stata errors:
| Error | Likely cause |
|---|---|
| `variable not found` | Typo; dataset not loaded; wrong frame |
| `no observations` | Sample restriction dropped everything; check `if` condition |
| `type mismatch` | String vs. numeric variable mismatch |
| `r(603)` / out of memory | Dataset too large; try `compress` or reduce sample |
| `not sorted` | `merge` requires data sorted by key variable; use `sort` first |

### Bash / Shell
| Error | Likely cause |
|---|---|
| `command not found` | Not on PATH; not installed; typo |
| `permission denied` | Need `chmod +x` or `sudo` |
| `No such file or directory` | Path is wrong; file doesn't exist; typo |
| Exit code `1` | Program failed; check stderr output |
| Exit code `127` | Command not found |

---

## Common Bug Patterns

### Off-by-one errors
- Array indexed from 0; loop runs one too many or too few iterations
- Check boundary conditions explicitly

### Mutation / aliasing
- Two variables pointing to the same object; modifying one changes the other
- Python: `b = a` for lists/dicts copies the reference, not the data — use `b = a.copy()`
- R: R is copy-on-modify, but watch `data.table` in-place operations

### Scope / environment issues
- Variable defined in one scope not visible in another
- Global vs. local variable shadowing
- R: `<<-` vs `<-`; Python: `global` keyword

### Silent failures
- A function returns `None` or `NA` instead of raising an error
- A merge or filter drops all rows without warning
- A file write fails silently
- **Fix:** Add explicit assertions after critical steps

### Wrong column/variable
- Operating on the wrong column — especially after a merge that creates `_x` / `_y` suffix columns
- Check column names after every merge

### Float comparison
- `0.1 + 0.2 == 0.3` is `False` in most languages
- Use `abs(a - b) < 1e-9` or `np.isclose()` / `all.equal()` for float comparisons

### Environment differences
- Works on your machine, fails in CI or a colleague's environment
- Check: Python/R version, package versions, OS, file paths, locale settings
- Fix: Use `requirements.txt` / `renv.lock` / `conda env export` to pin environments

---

## Debugging Tools

### Python
```python
# Print debugging
print(f"DEBUG: x = {x}, type = {type(x)}")

# Assertions
assert df is not None, "df should not be None at this point"
assert len(df) > 0, f"Expected rows, got empty df after merge"

# Interactive debugger
import pdb; pdb.set_trace()  # or breakpoint() in Python 3.7+

# Inspect DataFrame
print(df.shape, df.dtypes, df.head())
print(df.isnull().sum())
```

### R
```r
# Print debugging
cat("DEBUG: nrow =", nrow(df), "\n")
str(df)  # structure of any object

# Assertions
stopifnot(nrow(df) > 0)
stopifnot(!any(is.na(df$key_var)))

# Interactive debugger
browser()  # inside a function
debug(function_name)  # step through function
```

### Stata
```stata
* Print debugging
display "DEBUG: N = `=_N'"
list var1 var2 in 1/10

* Assertions
assert !missing(id)
assert _merge == 3

* Trace mode (verbose)
set trace on
[run your code]
set trace off
```

---

## When You're Stuck

1. **Take a break.** Fresh eyes catch things exhausted eyes miss.
2. **Rubber duck it.** Explain the bug out loud, step by step, as if teaching someone. State what you expect and what you observe. The act of explaining often reveals the inconsistency.
3. **Read the documentation.** Check the function signature and return type. Many bugs come from assuming how a function works rather than checking.
4. **Check recent changes.** `git diff` or `git log -p` — what changed since it last worked?
5. **Search the exact error message.** Paste the error message (minus file paths) into a search engine. Someone has seen it before.
6. **Start fresh.** Close the file, open it again, read it top to bottom. Restart the R session / Python kernel. Reload the data.

---

## Output

When invoked, ask the user:
1. What is the error message or unexpected behavior?
2. What language / environment?
3. What does the relevant code look like?

Then work through the protocol: reproduce → read the error → isolate → hypothesize → verify → fix. Produce a diagnosis with a specific root cause identified, not just a possible fix.
