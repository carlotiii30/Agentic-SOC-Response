# Agentic-SOC-Response 🛡️🤖

A Multi-Agent System (MAS) for automated cybersecurity incident response using **Microsoft AutoGen**. This project demonstrates how specialized LLM agents can collaborate to detect, analyze, and mitigate network threats in real-time through an autonomous workflow.

## 🚀 Overview
Modern Security Operations Centers (SOCs) face an overwhelming volume of alerts. This project implements an **Agentic Design Pattern** that moves beyond static automation. By using a **Reflection Pattern**, the system ensures that every mitigation action is analyzed, scripted, and validated by different AI personas before execution, minimizing hallucinations and unauthorized system changes.

## 🧠 Multi-Agent Architecture
The system orchestrates four specialized agents in a `GroupChat` environment:
- **Security Analyst**: Monitors incoming logs (JSON/CSV) and identifies attack vectors (e.g., Syn Flood, Brute Force).
- **Script Architect**: Generates specialized Python/Bash remediation scripts tailored to the specific threat.
- **Security Validator**: Acts as a critical safety filter. It reviews the generated code for syntax errors and ensures compliance with security policies (e.g., ensuring no critical services are stopped).
- **System Executor**: A `UserProxyAgent` that manages the execution environment and reports back the results of the mitigation.

## 📋 Getting Started

### Prerequisites
- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation)
- OpenAI API Key (or local LLMs like Llama 3 via Ollama)

### Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/carlotiii30/Agentic-SOC-Response.git](https://github.com/carlotiii30/Agentic-SOC-Response.git)
   cd Agentic-SOC-Response
   ```
2. **Install dependencies with Poetry:**
    ```bash
    poetry install
    ```
3. **Environment Setup:**
   Copy the example environment file and add your credentials:
   ```bash
   cp .env.example .env
    ```
### Execution
Run the automated response protocol:
  ```bash
  poetry run python main.py
  ```

## 🛡️ Security Disclaimer
This project is a Proof of Concept (PoC) developed for cybersecurity research. Automated code execution should always be performed in sandboxed environments (e.g., Docker) when applied to production systems.

--- 
_Developed for research in AI-driven Cybersecurity and Agentic Workflows._
