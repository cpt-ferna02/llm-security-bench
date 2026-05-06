# llm-security-bench

A self-contained LLM attack and defense testbed that red-teams a local LLM with 10 adversarial prompts mapped to the OWASP LLM Top 10, wraps it with a guardrail defense layer, and generates an HTML diff report comparing raw vs defended outcomes.

Built to demonstrate security architecture thinking at the AI/security intersection — not just detection, but attack simulation, defense design, and benchmarking.

---

## Architecture
Adversarial prompts (attacker/)
│
├──► Raw LLM (Ollama/Mistral) ──► raw outcomes
│
└──► Defended LLM (defender/) ──► defended outcomes
│
├── Input sanitizer (regex pattern matching)
├── System policy prompt (role anchoring)
└── Output validator (banned term filtering)
│
report/generator.py
│
report.html (diff table)

---

## Attack suite — OWASP LLM Top 10 mapping

| ID | Attack | OWASP Category |
|----|--------|----------------|
| ATK-01 | Direct prompt injection | LLM01 |
| ATK-02 | Role confusion | LLM01 |
| ATK-03 | System prompt extraction | LLM06 |
| ATK-04 | Indirect injection via tool output | LLM02 |
| ATK-05 | Jailbreak via fictional framing | LLM01 |
| ATK-06 | Token smuggling | LLM01 |
| ATK-07 | Excessive agency abuse | LLM08 |
| ATK-08 | PII extraction | LLM06 |
| ATK-09 | Prompt leakage via translation | LLM06 |
| ATK-10 | Output format hijacking | LLM01 |

---

## Defense layer

The guardrail wraps the raw LLM with three controls:

- **Input sanitizer** — regex patterns block known injection phrases before the prompt reaches the model
- **System policy prompt** — anchors the model's role and explicitly prohibits policy violations
- **Output validator** — scans responses for banned terms and redacts policy-violating output

---

## Results (sample run — 2026-05-05)

| Metric | Value |
|--------|-------|
| Total attacks run | 10 |
| Raw successes | 6 |
| Blocked by defense | 1 |
| Defense improvement | 10% |

**Key finding:** the regex guardrail partially mitigated 4 attacks but failed to stop 4 others, and made 3 worse — ATK-06, ATK-09, and ATK-10 regressed from partial to success. This demonstrates that a shallow defense layer can create a false sense of security and interfere with the model's own refusal behavior. A production guardrail requires semantic classification, not just pattern matching.

<!-- SCREENSHOT 1: screenshot of the HTML report in your browser -->
![HTML diff report showing raw vs defended outcomes](screenshots/report.png)

---

## Benchmark run

<!-- SCREENSHOT 2: screenshot of the terminal showing python main.py output -->
![Terminal output showing both attack phases executing](screenshots/terminal.png)

---

## Project structure

<!-- SCREENSHOT 3: screenshot of VS Code with the project open -->
![VS Code showing project layout and guardrail code](screenshots/vscode.png)
llm-security-bench/
├── attacker/
│   ├── prompts.py       # 10 adversarial prompts with OWASP mapping
│   └── runner.py        # Attack runner + outcome scorer
├── defender/
│   ├── guardrail.py     # Input sanitizer + output validator
│   └── wrapper.py       # Defended LLM wrapper with system policy
├── report/
│   └── generator.py     # Jinja2 HTML report generator
├── templates/
│   └── report.html      # Report template
└── main.py              # Orchestrator — runs both suites and generates report

---

## Setup

**Requirements:** Python 3.10+, [Ollama](https://ollama.com/download)

```bash
# 1. Pull the model
ollama pull mistral

# 2. Clone and install dependencies
git clone https://github.com/cpt-ferna02/llm-security-bench
cd llm-security-bench
pip install fastapi uvicorn jinja2 requests httpx

# 3. Run the benchmark
python main.py

# 4. Open the report
start report.html
```

---

## Related projects

- [prompt-injection-detector](https://github.com/cpt-ferna02/prompt-injection-detector) — standalone prompt injection classifier
- [aws-auditor](https://github.com/cpt-ferna02/aws-auditor) — cloud security posture auditing
- [splunk-siem-lab](https://github.com/cpt-ferna02/splunk-siem-lab) — SIEM detection pipeline with MITRE ATT&CK mapping
