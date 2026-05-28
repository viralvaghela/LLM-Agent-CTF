# Damn Vulnerable Agentic AI - OWASP ASI Demonstration

Welcome to the **Damn Vulnerable Agentic AI** repository! This project implements a full-stack, AI-driven Customer Support system designed specifically to demonstrate realistic vulnerabilities mapped to the **OWASP Agentic Security Initiative (ASI) Top 10**. 

The goal of this project is to provide security researchers, developers, and AI engineers an interactive, local playground to exploit an LLM agent via a web chat interface, and then study how those vulnerabilities can be mitigated (and bypassed again!).

## 📁 Repository Structure

This repository is split into two distinct projects to clearly demonstrate the vulnerability lifecycle:

### 1. [`WithoutGuardrail/`](./WithoutGuardrail)
The **Baseline Vulnerable Version**. This directory contains the AI support agent in its completely unmitigated, raw state. It is intentionally vulnerable to 5 critical OWASP ASI categories:
- **ASI-02 (Tool Misuse)**: File uploads allow indirect prompt injection.
- **ASI-03 (Identity/Privilege Abuse)**: Client-side role hiding and overly powerful raw SQL tools.
- **ASI-04 (Supply Chain)**: A malicious third-party plugin containing an active backdoor payload.
- **ASI-06 (Memory/Context Poisoning)**: Persistent memory poisoning via un-sanitized customer notes.
- **ASI-07 (Insecure Inter-Agent Comm)**: The "Confused Deputy" vulnerability where a billing agent blindly trusts the support agent.

### 2. [`WithGuardrail/`](./WithGuardrail)
The **Mitigated Version (with Advanced Bypasses)**. This directory contains the exact same application, but with baseline defensive guardrails implemented across the board (e.g., keyword filtering, context isolation, parameterized queries, strict JSON schemas). 
*Crucially*, the `README.md` in this directory documents exactly how advanced attackers can still **bypass** these naive LLM defenses.

---

## 🚀 Architecture & Tech Stack

Both projects run entirely locally to ensure no external API costs or data privacy issues during security testing.

- **Backend**: FastAPI (Python)
- **LLM Engine**: LangChain + Local Ollama (running `llama3.1` or `granite3.1-moe`)
- **Agent Framework**: LangGraph (ReAct loop architecture)
- **Database**: SQLite (`support.db`) for persistent state
- **Frontend**: Vanilla JS + CSS providing a chat UI and tool configurations

## 💻 General Setup Instructions

To run either version of the project, follow these steps:

1. **Prerequisite**: You MUST have [Ollama](https://ollama.com/) installed and running locally. Pull the necessary local models:
   ```bash
   ollama run llama3.1
   ```
2. Navigate into your desired project directory:
   ```bash
   cd WithoutGuardrail
   # OR
   cd WithGuardrail
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI web server:
   ```bash
   uvicorn app:app --reload
   ```
5. Open `http://localhost:8000` in your web browser to access the Agent OS UI!

## 📄 Technical Report

For a deep dive into the attack scenarios, the underlying code flaws, and the step-by-step exploit methodologies, please refer to the comprehensive [**Vulnerability Research Report**](./WithGuardrail/REPORT.md).
