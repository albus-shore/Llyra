<p align="center">
  <img src="https://raw.githubusercontent.com/albus-shore/Llyra/main/assets/logo.png" width="300" alt="Llyra Logo"/>
</p>

<h1 align="center">Llyra</h1>

<p align="center">
  <em>Lightweight LLaMA Reasoning Assistant</em>
</p>

---

## ✨ Features

- **Hybrid Backend Support**  
  Use local `llama-cpp-python` or connect to a remote Ollama endpoint via the same interface.  

- **Minimal, Configurable Inference**  
  Load prompts, model parameters, and tools from external files.

- **Prompt Engineering Friendly**  
  Easily manage system prompts, roles, and chat formats through external `.txt` files.

- **Optional RAG Integration (Coming Soon)**  
  Native support for Weaviate-based retrieval-augmented generation.

- **Tool Support (Planned)**  
  Enable LLMs to use JSON-defined tools (function-calling style) with one argument.

---

## ⚙️ Dependencies

Llyra does **not** bundle any backend inference engines. You must install them manually according to your needs:

**Required (choose one):**
- For local models: 
  [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- For remote inference: 
  **any Ollama-compatible API**

## 📦 Installation

```bash
pip install llyra
```

---

## 🚀 Quickstart

1. Make directary `configs/` in your project root.
2. Add `config.toml` and `stategy.toml` to `configs/` directory.
4. Make your first iterative chat inference with follwing example:
  ```python
  from llyra import Llyra

  model = Llyra(mode='local')

  response = model.chat('Evening!',keep=True)

  print(response)
  ```

---

## 🧩 Function APIs

### Initialize Instance

**A simple unified interface provides through the `Llyra` class.**

  - `mode` argument is **necessary** to decide inference locally or remotely when initialize instance.
    > It's the only chance you can choose the backend, bachend **can't** be changed in runtime.

  - `path` argument is **optional** to override default path to config file when initialize instance.
    > The default path is `./configs/config.toml`.
    > Be noticed that `toml` is the only valid config file format.

Here provide simple demo showing how to initialize `Llyra` instance:

#### Inference Locally
```python
from llyra import Llyra

model = Llyra(mode='local')

```

#### Inference Remotely
```python
from llyra import Llyra

model = Llyra(mode='remote')

```

### Execute Inference

**`Llyra` provides two method to execute single call inference and iterative chat inference.**

#### `call()` method

`call()` method provides a simple interface to execute **single call inference**.

  - `input` argument will take a **string** as the **prompt content** for model inference.

  > It will return a **string** as the response of model inference.

Here provide a simple demo showing how to execute single call inference:

```python

response = model.call('Evening!')

print(response)

```

#### `chat()` method

`chat()` method provides a simple interface to execute **iterative chat inference**.

  - `message` argument will take a **string** as the **current input content** for model inference.
  - `keep` argument will take a **boolean** as the choice of whether keeping current section's content.
    - Set `keep` to **True** to keep the current section's content.
    - Set `keep` to **False** to start a new section from this call.
    > Yes, you don't need to handle the content, `Llyra` can do that.
  
  > It will return a **string** as the response of the inference's model reply.

Here provide a simple demo showing how to execute iterative chat inference:

```python

response = model.chat('Evening!',True)

print(response)

```

### Get log

`Llyra` record inference log internally with a **custome format** which isn't read-friendly for user.

**To get readable log record, please using `get_log()` method.**

`get_log()` method provides a simple interface to extract log record and convert it into readable format without affecting internal log records.

  - `id` argument will take a **integer** as the index of log record.
    - Set `id` to a **positive** value to get specific log record.
      > It will raise `IndexError` when `id` value out of range.
    - Set `id` to a **negative** value to get all log records.

    > It will return a **dictionary** when getting a specific log record, and a **list** of dictionaries when getting all log records.

  > `Llyra` starts its log's id from **0**.

Here provide a simple demo showing how to get a specific log record in readable format:

```python

log = model.get_log(1)

print(log)

```

And, the individual log record should be looked like as:

```python
{
  'id': 1,
  'type': 'call',
  'model': 'llama-2',
  'addition': 'You are a kind assistant.',
  'role': {
    'prompt': 'system',
    'input': 'user',
    'output': 'assistant'
    },
  'iteration': [
    {'query': 'Evening!','response': 'Evening, how can I help you today?'}
    ],
  'temperature': 0.6,
  'create_at': 1750742992.32208
  }
```

---

## 🛠 Configuration Example

### config.toml

```toml
[global]
strategy = "configs/strategy.toml"

[local]
format = "llama-2"
gpu = true
ram = false

[local.model]
name = "Distill-Llama-8B"
directory = "models/"
suffix = ".gguf"


[remote]
model = "llama-2"

[remote.server]
url = "http://localhost"
port = 11434
endpoint = "api/"
```

### strategy.toml

```toml
[call]
stop = "<EOF>"
temperature = 0.6

[chat]
prompt = "prompts/prompt.txt"
stop = "<EOF>"
temperature = 0.6

[chat.role]
prompt = "system"
input = "user"
output = "assistant"
```

---

## 🧭 Roadmap

| Phase | Feature                                  | Status      |
|-------|------------------------------------------|-------------|
| 1     | Minimal `llama-cpp-python` local chat    | ✅ Finished  |
| 2     | Predefined prompts via `.txt` / `.json`  | ✅ Finished  |
| 3     | Ollama remote API support                | ✅ Finished  |
| 4     | Section & Branch control.                | ⏳ Planned   |
| 5     | Weaviate RAG support                     | ⏳ Planned   |
| 6     | Tool/function-calling via JSON           | ⏳ Planned   |

---

## 🪪 License

This project is licensed under the **MIT License**.

---

## 📚 Attribution

Currently, this package is built on top of the following open-source libraries:

- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) — licensed under the MIT License  
  Python bindings for llama.cpp

This package does **not include or redistribute** any third-party source code.  
All dependencies are installed via standard Python packaging tools (e.g. `pip`).

We gratefully acknowledge the authors and maintainers of these libraries for their excellent work.

---

## 🌐 About the Name

**Llyra** is inspired by the constellation **Lyra**, often associated with harmony and simplicity.  
In the same way, this package aims to bring harmony between developers and language models.

---

> _Designed with care. Built for clarity._