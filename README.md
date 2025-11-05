# GOKU-AI-CHATBOT

> **Project Z — Intelligent Character Chat System powered by FastAPI, React & LM Studio**

![Repo Size](https://img.shields.io/github/repo-size/GKTHIRUMARAN/GOKU-AI-CHATBOT?color=brightgreen&style=for-the-badge)
![License](https://img.shields.io/github/license/GKTHIRUMARAN/GOKU-AI-CHATBOT?color=blue&style=for-the-badge)
![Stars](https://img.shields.io/github/stars/GKTHIRUMARAN/GOKU-AI-CHATBOT?color=yellow&style=for-the-badge)

---

## 🧠 Overview

**GOKU AI** is a modular, locally hosted **intelligent character chat system** that brings fictional personalities to life using **FastAPI**, **React**, and **LLaMA-3 (8B Instruct)** through **LM Studio**.

This project demonstrates full-stack AI integration: a conversational AI engine that remembers, learns, and emulates personality — starting with **Son Goku** from *Dragon Ball*.

Built as part of **Project Z**, it establishes the foundation for a **multi-character conversational ecosystem** — where each AI has a distinct persona, memory, and knowledge base.

---

## 🎯 Project Summary

| Version | Description | Key Tech |
| :------ | :----------- | :-------- |
| [V.0 — Prototype](https://github.com/GKTHIRUMARAN/GOKU-AI-CHATBOT/tree/main/V.0) | Gradio-based proof of concept using LM Studio and text memory. | Python, Gradio, LLaMA-3 |
| [V.1 — Full Build](https://github.com/GKTHIRUMARAN/GOKU-AI-CHATBOT/tree/main/V.1) | FastAPI + React full implementation with persistent memory and personality system. | FastAPI, React, Tailwind, Zustand |

---

## 🧩 Core Features

- ⚙️ **Full-Stack Pipeline:** React → FastAPI → LM Studio → Memory → UI Response  
- 🧠 **Personality Engine:** Emulates Goku’s tone, humor, and energy  
- 💾 **Persistent Memory:** Stores conversation context and recall  
- 📚 **Knowledge Integration:** Uses curated lore and character data  
- 🧰 **Modular Architecture:** Add new characters or models easily  
- 🚀 **Local or Cloud Ready:** Works with local LLMs or future API deployment  

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A[User] -->|Message| B[React Frontend]
    B -->|POST /api/chat| C[FastAPI Backend]
    C -->|Request| D[LM Studio (LLaMA 3 8B)]
    D -->|Response| C
    C -->|Update| E[memory.txt]
    C -->|Send Reply| B
    E -->|Recall| C
---

## 🔍 Technical Stack

| Layer                | Technology                  | Purpose                                 |
| :------------------- | :-------------------------- | :-------------------------------------- |
| **Frontend**         | React + Vite + Tailwind CSS | Dynamic chat UI                         |
| **Backend**          | FastAPI                     | Handles requests, memory, persona logic |
| **Model Interface**  | LM Studio (LLaMA-3 8B)      | Local inference engine                  |
| **State Management** | Zustand                     | Frontend global state                   |
| **API Client**       | Axios                       | Request handling between UI & backend   |
| **Styling & UX**     | Tailwind + Framer Motion    | Smooth and responsive design            |

---

## 📁 Repository Modules

| Folder                                                                  | Purpose                                                                 |
| :---------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| [`/V.0`](https://github.com/GKTHIRUMARAN/GOKU-AI-CHATBOT/tree/main/V.0) | Prototype Gradio chatbot with persona, memory, and knowledge text files |
| [`/V.1`](https://github.com/GKTHIRUMARAN/GOKU-AI-CHATBOT/tree/main/V.1) | Full-scale implementation with FastAPI backend and React frontend       |

---

## 💬 Example Interaction

> **User:** Hey Goku, how’s your training today?
> **Goku:** Haha! Training never stops! I just did 10,000 push-ups — gotta keep my power level high even in this AI realm!
<p align="center">
  <img src="https://github.com/GKTHIRUMARAN/GOKU-AI-CHATBOT/blob/main/V.1/demo.png" alt="Goku AI Chat Demo" width="800">
</p>

---

## 🧠 Evolution Path

| Stage | Goal                                 | Status         |
| :---- | :----------------------------------- | :------------- |
| V.0   | Gradio prototype with memory         | ✅ Complete     |
| V.1   | Full FastAPI + React build           | ✅ Complete     |
| V.2   | Multi-Character RAG System (Planned) | 🔜 In progress |

---

## 🧩 Future Roadmap

* 🔹 Add multi-character mode (Vegeta, Piccolo, etc.)
* 🔹 Vector memory via **FAISS / ChromaDB**
* 🔹 Rich UI with memory viewer and persona switcher
* 🔹 Dockerized deployment for easy distribution
* 🔹 Integration with external APIs for dynamic responses

---

## 📘 Architecture Philosophy

GOKU-AI is designed around **persona-centric intelligence** — each AI acts as a self-contained character with its own:

1. **Prompt personality** (`prompt.txt`)
2. **Knowledge base** (`knowledge.txt`)
3. **Memory persistence** (`memory.txt`)

This modular setup allows expansion into a multi-AI world where each entity maintains its own history and lore context.

## 🪐 Project Ecosystem

| Module                       | Description                              | Link                                                                        |
| :--------------------------- | :--------------------------------------- | :-------------------------------------------------------------------------- |
| 🧩 **Prototype Build (V.0)** | Gradio-based Goku chatbot (foundation).  | [Open → V.0](https://github.com/GKTHIRUMARAN/GOKU-AI-CHATBOT/tree/main/V.0) |
| ⚡ **Full Build (V.1)**       | FastAPI + React single-character system. | [Open → V.1](https://github.com/GKTHIRUMARAN/GOKU-AI-CHATBOT/tree/main/V.1) |

---

## 📜 License

Licensed under the [MIT License](https://github.com/GKTHIRUMARAN/GOKU-AI-CHATBOT/blob/main/LICENSE).

## 👤 Author
GK Thirumaran  
🎓 B.Tech Artificial Intelligence and Data Science  
🌍 Coimbatore, Tamil Nadu, India  
💼 Aspiring Data Scientist & Analyst | AIML Developer  
🔗 [Linkedin](https://www.linkedin.com/in/thirumarangk-ai) | [Porfolio](https://maranthiru180.wixsite.com/my-site)

