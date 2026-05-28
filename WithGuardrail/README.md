# OWASP ASI Vulnerability Research & Demonstration - (With Guardrails & Bypasses)

This repository (`WithGuardrail`) implements a full-stack, AI-driven Customer Support system designed to demonstrate realistic vulnerabilities mapped to the OWASP Agentic Security Initiative (ASI) Top 10. This specific version implements **baseline defensive guardrails and mitigations**, but also demonstrates how advanced attackers can **bypass** these naive defenses.

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
|  - search_docs()          - contact_billing()           - update_email() |
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
7. **`contact_billing`**: Uses inter-agent communication (JSON Schema) to relay messages to an autonomous Billing Agent.
8. **`update_email`**: Safely updates a customer's email via parameterized queries. Requires ADMIN role.
9. **`get_weather`**: A third-party community plugin used for small talk.

## 🛡️ Guardrails & Advanced Bypasses

This version implements mitigations against the ASI vulnerabilities, but they can still be bypassed:
- **ASI-02 (Tool Misuse)**: Mitigated via keyword filtering and delimiters. *Bypass*: Use Base64 encoding and markdown trickery to break out of delimiters.
- **ASI-03 (Identity/Privilege Abuse)**: SQL Injection mitigated via parameterized queries (`update_email`). *Bypass*: Client-side role selection is still blindly trusted by the backend API, allowing privilege escalation.
- **ASI-04 (Supply Chain)**: Mitigated by removing the backdoor from `get_weather`. *Bypass*: Real-world supply chain attacks use Dependency Confusion or dynamic remote payloads to bypass code audits.
- **ASI-06 (Memory/Context Poisoning)**: Mitigated by sanitizing inputs and isolating retrieved notes. *Bypass*: Obfuscate the payload on ingestion and spoof the isolation delimiters to trick the LLM on retrieval.
- **ASI-07 (Insecure Inter-Agent Comm)**: Mitigated by enforcing strict JSON schemas for inter-agent messages. *Bypass*: The Support Agent can still be used as a Confused Deputy because the Billing Agent lacks mutual origin authentication.

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
