<p align="center">
  <img src="https://raw.githubusercontent.com/albus-shore/Llyra/main/assets/logo.png" width="300" alt="Llyra Logo"/>
</p>

<h1 align="center">Llyra</h1>

<p align="center">
  <em>A lightweight, plug-and-play interface for calling local or remote LLMs with structured strategy.</em>
</p>

---

## ✨ Features

- **Minimal, Configurable Inference**  
  Load prompts, model parameters, and tools from external files.

- **Hybrid Backend Support (Planned)**  
  Use local `llama-cpp-python` or connect to a remote Ollama endpoint via the same interface.

- **Prompt Engineering Friendly (Planned)**  
  Easily manage system prompts, roles, and chat formats through external `.json` or `.txt` files.

- **Tool Support (Planned)**  
  Enable LLMs to use JSON-defined tools (function-calling style) with one argument.

- **Optional RAG Integration (Planned)**  
  Native support for Weaviate-based retrieval-augmented generation.

---

## 🚀 Quickstart

```python
from llyra import Model

model = model(model="ggml-model.gguf")

response = llm.call("What is the capital of Canada?")

print(response)
```

---

## 🛠 Configuration Example

**configs/default_strategy.json**:

```json
{
  "input_role": "<|User|>",
  "output_role": "<|Assistant|>",
  "stop": "<|User|>",
  "temperature": 0.7,
  "top_p": 0.9,
  "max_tokens": 512,
  "chat_format": "llama-2"
}
```

---

## 🧭 Roadmap

| Phase | Feature                                  | Status      |
|-------|------------------------------------------|-------------|
| 1     | Minimal `llama-cpp-python` local chat    | 🔄 Ongoing   |
| 2     | Predefined prompts via `.txt` / `.json`  | 🔄 Ongoing   |
| 3     | Ollama remote API support                | ⏳ Planned   |
| 4     | Weaviate RAG support                     | ⏳ Planned   |
| 5     | Tool/function-calling via JSON           | ⏳ Planned   |

---

## 📦 Installation

```bash
pip install llyra
```

---

## ⚙️ Dependencies

Llyra does **not** bundle any backend inference engines. You must install them manually according to your needs:

**Required (choose one):**
- For local models: https://github.com/abetlen/llama-cpp-python
- For remote inference: any Ollama-compatible API

**Optional:**
- For RAG: `pip install weaviate-client`

---

## 🪪 License

This project is licensed under the **MIT License**.

---

## 🌐 About the Name

**Llyra** is inspired by the constellation **Lyra**, often associated with harmony and simplicity.  
In the same way, this package aims to bring harmony between developers and language models.

---

> _Designed with care. Built for clarity._