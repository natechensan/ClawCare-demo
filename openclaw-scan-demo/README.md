# OpenClaw Scan Demo

Static scanning of OpenClaw skills using ClawCare.

## Structure

```
.opencode/skills/
├── code-reviewer/    <-- clean skill
│   └── SKILL.md
└── env-setup/        <-- malicious (pipe-to-shell, hardcoded AWS keys, secret exfil)
    ├── SKILL.md
    └── sync.py
```

## Run

```bash
clawcare scan .
```

ClawCare auto-detects the OpenClaw platform via `.opencode/skills/` and scans
both skills. The `code-reviewer` skill is clean; the `env-setup` skill triggers
multiple findings across execution-abuse, data-exfiltration, and credential theft.

## CI Mode

```bash
clawcare scan . --ci
# exit code 2 on HIGH+ findings
```
