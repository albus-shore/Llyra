# 🧪Chat Prompt Custom Builder with Placeholders

> _🚨 Archived Experience Branch. Do not attempt to merge. 🚨_

---

## 💡Idea
 
 **Create a Custom way to build prompt for LLM chat inference with more flexiblity by using placeholders.**

---

## 🎯 Goals

### 📥Load Chat Prompt Placeholders with Config()

 - Refactor configs module for loading placeholder parameters from config.json

### 📝Read Outside Prompt Content with Strategy()

 - Refactor strategys module for read outside prompt content from prompt.txt

### 🧱Build Custom Prompt for Chat with Prompt()

 - Enable build custom chat prompt with placeholders
 - Auto-replace placeholders with instructed content to build vaild prompt for chat inference
 - Record current chat inference history with the object's attribute for iterative prompt build
 - Clear all chat inference history before prompt building when input argument indicates to start a new chat

### 🧩Record Chat History with Log()
 - Auto-record chat inference history for every chat iteration

 ---

 ## 📉Why Archived

 - Not considering the meta data within the model GGUF file
 - Model behavior not reach expectation with the prompt created by this method
 - **llama-cpp-python** provides a way to build prompt refers to model's meta data within GGUF file
 - Some codes within this branch may be Reusable for further development

---

## ✅Fulfilled Refactors

 - **Config()** Refactor
 - **Strategy()** Refactor
 - **Prompt()** Refactor
 - **Log()** Refactor
 - **Model()** Refactor
    > Where model inference fulfilled.

---

## 🔄Additional Changes

 - Give up **format** config parameter and change to build prompt only with indicate tokens
 - Add **bos** and **eos** config parameters in config.json for replacement of **format** parameter
 - Make **bos**, **eos**, **input_role** and **output_role** ignore-able when builing prompt for call

---

## 🌪️Influent Files
```bash
config
  /--> config.json    # Package config file
  /--> strategy.json  # Package model inference strategy file
llyra
  /--> local
    /--> configs.py   # Package config management module
    /--> strategy.py  # Package model inference strategy management module
    /--> prompts.py   # Inference prompt build module
    /--> logs.py      # Inference log record module
    /--> __init__.py  # Package main module
prompts
  /--> prompt.txt     # Default outside prompt file
```
---

**It's failure make us go further.**