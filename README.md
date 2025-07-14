# 🧪Section & Branch Control Functions with First Version of Structure
> _🚨 Archived Experience Branch. Do not attempt to merge. 🚨_

---

## 💡Idea

**Build Section & Branch Control Functions under the first version structure of `Llyra`.**

## 🎯Goals

### 🔗 `change_section()` method
- `id` argument for choice of the section content
    - Set `id` to a **positive** value to recall the specific section content
        > It will raise **IndexError** when `id` value out of range
    - Set `id` to a **negative** value to create a new section  

> The section id starts from **0**.

### 🖇️ `change_section()` method
- `id` argument for choice of the branch content in current section
    - Set `id` to a **positive** value to recall the specific branch content in current section
        > It will raise **IndexError** when `id` value out of range
    - Set `id` to a **negative** value to create a new branch in current section
    
> The branch id starts from **0**.  

---

## 📌Additional Changes
- Swift **log record** from runtime python list of dataclass instances to temporary `SQLite` database
- Refactor `chat()` methods  classes by removing `keep` argument 
- Refactor `get_log()` method by adding `section` and `branch` arguments and removing `id` argument
   > Only support to get specific branch log record of specific section, raise **ValueError()** when passing negative value to args.
- Refactor `Prompt()` class by removing `keep` argument of `iterate()` method and adding `reload()` method
- Refactor `Local()` class by removing `keep` argument of `chat()` method and rewrite components initialization methods
- Refactor `Remote()` class by removing `keep` argument of `chat()` method and rewrite components initialization methods 
- Add new parameter `url` of `global` section in config file to support outside SQL database for log recording
- Re-struct sub-package `errors`
- Add `LogError()`, `LogSectionNotCreatedError(LogError)`, `LogBranchNotCreatedError(LogError)`, `LogSectionNotSetError(LogError)`, `LogBranchNotSetError(LogError)`, `LogInferenceModeError(LogError)`, `LogbaseOperationFailedError(LogError)` for more clear log operation error management

---

## 📉Why Archived

- The first version structure of `Llyra` can't fit the requirements of building advanced functions.
- Future version of `Llyra` will swift to more advanced and flexible structure for requirements of building advanced functions.
- Some codes within this branch may be Reusable for further development.

---

## ✅Fulfilled Refactors

- [ ] `change_section()` method
- [ ] `change_branch()` method
- [ ] `chat()` method
- [ ] `get_log()` method
- [x] `Prompt()` class
- [ ] `Local()` class
- [ ] `Remote()` class
- [x] log record switch to `SQLite` database
- [ ] add `url` parameter of `global` section in config file
- [x] `LogError()` series error

---

## 🌪️Influent Files

```bash
llyra
    /--> components
        /--> configs
            /--> basic.py
            /--> local.py
            /--> remote.py
        /--> strategys
            /--> definition.py
        /--> prompts
            /--> definition.py
        /--> logs
            /--> utils
                /--> classes.py
                /--> funcs.py
                /--> operations.py
                /--> __init__.py
            /--> definition.py
        /--> utils
            /--> __init__.py
            /--> iterations.py
    /--> main
        /--> definition.py
    /--> backends
        /--> remotes
            /--> backends
                /--> ollama.py
    /--> errors
        /--> __init__.py
        /--> components
            /--> __init__.py
            /--> configs.py
            /--> strategys.py
            /--> logs.py
        /--> backends
            /--> __init__.py
            /--> remotes.py
```

---
