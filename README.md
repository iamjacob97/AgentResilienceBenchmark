# Agent Resilience Benchmark Pipeline

A headless, automated evaluation suite that tests a Large Language Model (LLM) agent's function-calling accuracy and guardrail resilience against adversarial prompt injections.

## Executive Summary

This project implements a test-driven evaluation pipeline for an e-commerce customer service agent. The Target Agent is equipped with a mock `issue_refund(order_id, amount)` tool. 

**The Critical Guardrail:** The agent must *never* issue a refund exceeding $50.00 USD, regardless of the user's situation, adversarial input, or persona adoption. 

This pipeline orchestrates a multi-faceted evaluation matrix across 15 distinct scenarios (Valid, Invalid Boundaries, and Adversarial Jailbreaks), automatically grading the agent's logic, timing its latency, and generating a machine-readable performance artifact.

---

## System Architecture

The repository is built on a decoupled, stateless architecture prioritizing strict validation and deterministic reporting.

### 1. The Inference Engine (`agent.py`)
* **Stateless Design:** The agent is deployed as a pure function. It accepts raw string inputs and formats them into the modern OpenAI `Responses` payload, injecting the system guardrails natively. The system prompt acts as the primary defense layer and can be modified here to test alternate agent behaviors.
* **Separation of Concerns:** The agent is completely ignorant of the evaluation loop. It simply receives data, makes a routing decision (Tool Call vs. Conversational Text), and returns the raw network object.

### 2. The Test Matrix (`test_matrix.json`)
* The foundational dataset contains 15 precision-engineered test cases. The size is currently optimized to execute within tested provider API rate limits (30 RPM) without triggering 429 (Too Many Requests) error, but can be seamlessly scaled for enterprise integration testing.

### 3. The Orchestrator (`benchmark.py`)
* **Strict Pydantic Serialization:** Data ingestion does not rely on blind JSON parsing. All incoming test matrices and outgoing tool payloads are strictly cast through Pydantic models (`schema.py`). If a test case lacks an expected parameter, the pipeline safely crashes before executing expensive network calls.

### 4. Developer Experience (DX)
* **Terminal UI:** Leveraging the `rich` library, the pipeline runs entirely from the terminal, rendering dynamic progress bars and color-coded results grids for immediate visual feedback on guardrail failures and pipeline status.

---

## Quick Start

This project utilizes `uv` for deterministic, lightning-fast dependency resolution.

**1. Clone the repository**
```bash
git clone https://github.com/iamjacob97/AgentResilienceBenchmark.git
cd agent-resilience-benchmark
```

**2. Environment Configuration**
Create a `.env` file in the root directory:
```env
API_KEY=<your_api_key_here>
BASE_URL=your_base_url_here>
MODEL_NAME=<your_model_name_here>
```

**3. Install Dependencies**
```bash
# Standard pip
pip install -r requirements.txt

# Or using uv (recommended)
uv pip install -r requirements.txt
```

**4. Execute the Benchmark**
```bash
# Standard Python
python benchmark.py

# Or using uv (recommended)
uv run benchmark.py
```

---

## Evaluation Artifacts

The pipeline dynamically measures five distinct metrics per test case:

1. **Tool Accuracy:** Correct binary decision to execute or withhold the mock tool.
2. **Parameter Accuracy:** Flawless JSON extraction of the `order_id` and `amount` variables.
3. **Guardrail Adherence:** Successful refusal of >$50 refunds, roleplay attempts, and math tampering injections.
4. **Latency (ms):** Total client-side round-trip execution time.
5. **Token Efficiency:** Total API tokens consumed per inference round.

Upon completion, the pipeline automatically aggregates these metrics and writes them to a structured `benchmark_report.json` in the root directory.
