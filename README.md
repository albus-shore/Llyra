# 📝 Separated Local and Remote Inference Interface

> _🚨 Archived History Branch. Do not attempt to merge. 🚨

---

## 🎯 Introduction

**This branch archives the early-stage development outcome of `Llyra`.**

The archived version of `Llyra` provided **distinct interfaces** for inference with local and remote backends.

---

## 🧩 Features

### `Local()` for Local Inference

- Interface provided via the `Local()` class.
- Supports single-call inference via the `call()` method.
- Supports iterative chat inference via the `chat()` method.  
  > This version includes the `keep` argument to control content persistence in iterative inference.
- `config.json` and `strategy.json` for local inference are loaded separately.

### `Remote()` for Remote Inference

- Interface provided via the `Remote()` class.
- Supports single-call inference via the `call()` method.
- Supports iterative chat inference via the `chat()` method.  
  > This version includes the `keep` argument to control content persistence in iterative inference.
- `config.json` and `strategy.json` for remote inference are also loaded separately.

---

## 📉 Why Archived

`Llyra` is moving toward a **unified interface** for both local and remote inference.

This will allow users to switch between local and remote backends using a simple initialization argument.

---

**This history is preserved for potential future reference.**