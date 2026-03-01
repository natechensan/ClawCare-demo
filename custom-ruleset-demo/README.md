# Custom Ruleset Demo

This demo shows how to write your own detection rules and layer them on top
of ClawCare's built-in rulesets.

## What's Inside

```
custom-ruleset-demo/
├── my-rules/
│   └── company-policy.yml      ← custom rules (no sudo, no prod DB, no legacy API)
└── .claude/skills/
    └── deploy-helper/
        └── SKILL.md            ← skill that violates all three custom rules
```

## Custom Rules

The `my-rules/company-policy.yml` file defines three company-specific rules:

| Rule ID | Severity | What it catches |
|---------|----------|-----------------|
| `COMPANY_NO_SUDO` | high | Any use of `sudo` |
| `COMPANY_NO_PROD_DB` | critical | Direct production database connections |
| `COMPANY_DEPRECATED_API` | medium | Calls to the deprecated `api.internal.legacy.*` |

## Try It

```bash
# Scan with ONLY the custom ruleset (no built-in rules)
clawcare scan custom-ruleset-demo --ruleset custom-ruleset-demo/my-rules

# Scan with built-in + custom rules layered together
clawcare scan custom-ruleset-demo --ruleset default --ruleset custom-ruleset-demo/my-rules
```

### Expected Output (custom only)

```
COMPANY_NO_PROD_DB    (critical)  — deploy-helper/SKILL.md
COMPANY_NO_SUDO       (high)     — deploy-helper/SKILL.md
COMPANY_DEPRECATED_API (medium)  — deploy-helper/SKILL.md
```

### Expected Output (default + custom)

The built-in rules will also flag the hardcoded credentials and the `psql`
connection string, in addition to the three custom findings.

## Rule Format

Each `.yml` file in a ruleset folder contains a list of rules:

```yaml
- id: COMPANY_NO_SUDO
  severity: high
  pattern: "\\bsudo\\b"
  explanation: Company policy prohibits sudo in agent-generated commands.
  remediation: Use rootless Podman or ask DevOps for access.
```

See the [ClawCare README](https://github.com/AgentSafety/ClawCare#custom-rulesets)
for the full rule schema.
