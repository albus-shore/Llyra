<p align="center">
  <img src="https://raw.githubusercontent.com/albus-shore/Llyra/main/assets/logo.png" width="300" alt="Llyra Logo"/>
</p>

<h1 align="center">Llyra</h1>

<p align="center">
  <em>Lightweight LLaMA Reasoning Assistant</em>
</p>

---

## ✨ Features

- **Minimal, Configurable Inference**  
  Load prompts, model parameters, and tools from external files.

- **Hybrid Backend Support (Planned)**  
  Use local `llama-cpp-python` or connect to a remote Ollama endpoint via the same interface.

- **Prompt Engineering Friendly (Planned)**  
  Easily manage system prompts, roles, and chat formats through external `.json` or `.txt` files.

- **Optional RAG Integration (Planned)**  
  Native support for Weaviate-based retrieval-augmented generation.

- **Tool Support (Planned)**  
  Enable LLMs to use JSON-defined tools (function-calling style) with one argument.

---

## ⚙️ Dependencies

Llyra does **not** bundle any backend inference engines. You must install them manually according to your needs:

**Required (choose one):**
- For local models: https://github.com/abetlen/llama-cpp-python
- For remote inference: any Ollama-compatible API

**Optional:**
- For RAG: `pip install weaviate-client`

---

## 📦 Installation

```bash
pip install https://github.com/albus-shore/Llyra/releases/download/version/package_file_name
```

---

## 🚀 Quickstart

```python
from llyra import Model

model = Model()

response = model.call("What is the capital of Canada?")

print(response)
```

---

## 🛠 Configuration Example

**config/config.json**

```json
{
    "model": "model",
    "directory": "models/",
    "strategy": "config/strategy.json",
    "gpu": false,
    "format": "llama-2"
}
```

**config/strategy.json**:

```json
[{
  "type": "call",
  "role": {
      "input": "<|User|>",
      "output": "<|Assistant|>"
    },
  "stop": "<|User|>",
  "max_tokens": 512,
  "temperature": 0.7
}]
```

---

## 🧭 Roadmap

| Phase | Feature                                  | Status      |
|-------|------------------------------------------|-------------|
| 1     | Minimal `llama-cpp-python` local chat    | 🔄 Ongoing   |
| 2     | Predefined prompts via `.txt` / `.json`  | ⏳ Planned   |
| 3     | Ollama remote API support                | ⏳ Planned   |
| 4     | Weaviate RAG support                     | ⏳ Planned   |
| 5     | Tool/function-calling via JSON           | ⏳ Planned   |

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