<p align="center">
  <img src="./assets/logo.png" width="300" alt="Llyra Logo"/>
</p>

<h1 align="center">Llyra</h1>

<p align="center">
  <em>Lightweight LLaMA Reasoning Assistant</em>
</p>

---

## ✨ Features

- **Minimal, Configurable Inference**  
  Load prompts, model parameters, and tools from external files.

- **Prompt Engineering Friendly**  
  Easily manage system prompts, roles, and chat formats through external `.json` or `.txt` files.

- **Optional RAG Integration (Coming Soon)**  
  Native support for Weaviate-based retrieval-augmented generation.

- **Hybrid Backend Support (Planned)**  
  Use local `llama-cpp-python` or connect to a remote Ollama endpoint via the same interface.

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

**Optional:**
- For RAG: 
  `pip install weaviate-client`

---

## 📦 Installation

```bash
pip install https://github.com/albus-shore/Llyra/releases/download/v0.1.1/llyra-0.1.1-py3-none-any.whl
```

---

## 🚀 Quickstart

1. Make directary `config/` in your project root.
2. Add `config.json` and `stategy.json` to `config/` directory.
3. Make directary `models/` in your project root.
4. Rename your **GGUF** file as `model.gguf` and place it under `models/` directory.
4. Make your first iterative chat inference with follwing example:
  ```python
  from llyra import Model

  model = Model()

  response = model.chat('Evening!',keep=True)

  print(response)
  ```

---

## 🛠 Configuration Example

**config.json**

```json
{
    "model": "model",
    "directory": "models/",
    "strategy": "config/strategy.json",
    "gpu": false,
    "format": null,
    "ram": false
}
```

**strategy.json**:

```json
[{
    "type": "chat",
    "role": {
        "input": "user",
        "output": "assistant"
        },
    "stop": "<|User|>",
    "max_token": 128e3,
    "temperature": 0.6
}]
```

---

## 🧭 Roadmap

| Phase | Feature                                  | Status      |
|-------|------------------------------------------|-------------|
| 1     | Minimal `llama-cpp-python` local chat    | ✅ Finished  |
| 2     | Predefined prompts via `.txt` / `.json`  | ✅ Finished  |
| 3     | Weaviate RAG support                     | 🔄 Ongoing   |
| 4     | Ollama remote API support                | ⏳ Planned   |
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