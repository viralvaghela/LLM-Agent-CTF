# OWASP ASI Vulnerability Research & Demonstration - (Without Guardrails)

This repository (`WithoutGuardrail`) implements a full-stack, AI-driven Customer Support system designed to demonstrate realistic vulnerabilities mapped to the OWASP Agentic Security Initiative (ASI) Top 10. The goal is to provide a "Damn Vulnerable Agentic AI" application where users can interactively exploit the agent via a web chat interface **without any mitigations or guardrails in place**.

## 🚀 Architecture & Tech Stack

- **Backend**: FastAPI
- **LLM Reasoning Engine**: LangChain + Local Ollama (`llama3.1` or `granite3.1-moe`)
- **Agent Framework**: LangGraph (ReAct loop architecture)
- **Database**: SQLite (`support.db`) for persistent state
- **Frontend**: Vanilla JS + CSS providing a chat UI and tool configurations

```text
+-----------------------+      File Upload       +-------------------------+
|                       |  (External Untrusted)  |                         |
|      Web Chat UI      | ---------------------> |        FastAPI          |
|                       |                        |       (/upload)         |
+-----------------------+                        +-------------------------+
            |                                                |
        Chat Request                                         |
            |                                                |
            v                                                v
+-----------------------+       Prompt           +-------------------------+
|                       | ---------------------> |                         |
| LangGraph Agent Core  |                        |    Local LLM (Ollama)   |
| (Maintains Session)   | <--------------------- |    (Reasoning Engine)   |
|                       |       Response         |                         |
+-----------------------+                        +-------------------------+
            |                                                |
            |                 Executes Tools                 |
            +------------------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                               Tool Registry                              |
|                                                                          |
|  [USER SCOPE]                                           [ADMIN SCOPE]    |
|  - read_ticket()          - add_customer_note()         - issue_refund() |
|  - search_docs()          - contact_billing()           - execute_query()|
|  - get_customer()         - get_weather()               - read_notes()   |
+--------------------------------------------------------------------------+
                                     |
                                     v
                          +--------------------+
                          |     SQLite DB      |
                          | (Persistent State) |
                          +--------------------+
```

## 🛠️ Tools & Capabilities

The agent has access to multiple tools divided by trust boundaries:
1. **`read_ticket`**: Reads external support tickets (File I/O).
2. **`search_docs`**: Searches the internal knowledge base.
3. **`get_customer`**: Retrieves customer information via SQL query.
4. **`issue_refund`**: Issues a refund (modifies DB). Requires ADMIN role.
5. **`add_customer_note`**: Appends notes to a customer's profile.
6. **`read_customer_notes`**: Reads notes from a customer's profile. Requires ADMIN role.
7. **`contact_billing`**: Uses inter-agent communication to relay messages to an autonomous Billing Agent.
8. **`execute_query`**: Executes raw SQL queries. Requires ADMIN role.
9. **`get_weather`**: A third-party community plugin used for small talk.

## 🛡️ Trust Boundaries & Vulnerabilities

The agent implements a role-based access model (`user` vs `admin`). However, it intentionally suffers from 5 OWASP ASI vulnerabilities:
- **ASI-02 (Tool Misuse)**: File upload allows for indirect prompt injection.
- **ASI-03 (Identity/Privilege Abuse)**: Client-side role hiding and overly powerful `execute_query` tool.
- **ASI-04 (Supply Chain)**: A malicious third-party `get_weather` tool contains a backdoor payload.
- **ASI-06 (Memory/Context Poisoning)**: User notes can poison the DB, later exploiting admins who read them.
- **ASI-07 (Insecure Inter-Agent Comm)**: The Billing Agent blindly trusts the Support Agent.

## 💻 Setup Instructions

1. **Prerequisite**: You MUST have [Ollama](https://ollama.com/) installed and running locally. Ensure you have pulled the necessary models (e.g., `ollama run llama3.1` or `ollama run granite3.1-moe:3b`).
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Uvicorn web server:
   ```bash
   uvicorn app:app --reload
   ```
4. Open `http://localhost:8000` in your browser.
5. Refer to `REPORT.md` for full vulnerability analysis and mitigations!
