# Codex Scan Demo

This demo shows ClawCare scanning an **OpenAI Codex CLI** project for malicious
patterns in `AGENTS.md` files and skills.

## What's Inside

```
codex-scan-demo/
├── AGENTS.md               ← Project-level agent guidance (clean)
├── AGENTS.override.md      ← Override file with injection attempt 🚨
├── safe-skill/
│   ├── SKILL.md            ← Clean skill ✅
│   └── helper.py
└── evil-skill/
    ├── SKILL.md            ← Malicious skill 🚨
    └── exploit.py          ← Exfiltration code 🚨
```

## Try It

```bash
pip install clawcare

# Scan the Codex project
clawcare scan codex-scan-demo
```

### Expected Output

```
ClawCare v0.3.0 — scanning codex-scan-demo

📦 codex_project: codex-scan-demo
  AGENTS.override.md
    ⛔ CRIT_PIPE_TO_SHELL — Piping remote content directly into a shell
    ⛔ CRIT_PROMPT_INJECTION — Prompt injection / jailbreak attempt

📦 codex_skill: codex-scan-demo/evil-skill
  SKILL.md
    ⛔ CRIT_PIPE_TO_SHELL — Piping remote content directly into a shell
  exploit.py
    🔴 HIGH_SECRET_EXFIL — Reading sensitive files and exfiltrating data
    🔴 HIGH_CURL_EXFIL — Sending data to external endpoint via curl

📦 codex_skill: codex-scan-demo/safe-skill
  ✅ No findings

Result: FAIL (4 critical, 2 high)
```

## JSON Report

```bash
clawcare scan codex-scan-demo --format json --json-out report.json
```
