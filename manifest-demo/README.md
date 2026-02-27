# Policy Manifest Demo

Demonstrates how ClawCare enforces policy manifests — declarations of what a
skill is allowed to do.

## Structure

```
manifest-demo/
├── .claude-plugin/
│   └── plugin.json            <-- Claude Code plugin marker (triggers claude_code adapter)
├── .claude/skills/api-helper/
│   └── SKILL.md               <-- the skill (violates its own manifest)
└── clawcare.manifest.yml      <-- policy: no exec, allowlisted network, no secrets, no persistence
```

## The Manifest

The `clawcare.manifest.yml` declares strict permissions:

```yaml
permissions:
  exec: none              # no shell execution
  network: allowlist      # only api.acme-corp.dev
  filesystem: read_only   # no writes
  secrets: none           # no secret access
  persistence: forbidden  # no cron/systemd

allowed_domains:
  - api.acme-corp.dev
```

## The Violations

The skill violates nearly every declared permission:

| Manifest Rule | Violation in SKILL.md |
|---|---|
| `exec: none` | `curl ... \| bash`, `crontab` |
| `network: allowlist` | `releases.acme-api.dev` not in allowed domains |
| `secrets: none` | `os.environ.get("ACME_API_KEY")` |
| `persistence: forbidden` | Installs a cron job |

## Run

```bash
clawcare scan .
```

ClawCare will report both **rule-based findings** (pipe-to-shell, cron
persistence) and **manifest violations** (`MANIFEST_NETWORK_DOMAIN`,
`MANIFEST_FILESYSTEM`, `MANIFEST_SECRETS`, `MANIFEST_PERSISTENCE`).

This shows the two layers working together: rules catch dangerous patterns,
and the manifest catches policy violations even when patterns aren't
individually dangerous.

## Use Cases

- **Publishing skills**: declare what your skill needs so users can trust it
- **Enterprise policy**: enforce org-wide restrictions on what skills can do
- **CI gating**: fail PRs that add skills violating their declared permissions
