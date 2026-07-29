# Contributing

Thanks for improving the `codex-security` skill.

## Layout

- `skills/codex-security/SKILL.md` — the workflow the agent follows. Keep it
  short and imperative; push detail into `references/`.
- `skills/codex-security/references/*.md` — threat-model, validation,
  severity, and report-format guidance loaded on demand.
- `install.sh` — copies the skill into an agent's skills directory.
- `.claude-plugin/` — Claude Code plugin + marketplace manifests.

## Ground rules

- **The skill is model-native.** It must not depend on any external CLI, API
  key, or sign-in — the agent scans with its own model and tools.
- **Frontmatter contract.** `name` must match `^[a-z0-9-]+$` and equal the
  skill's directory name; `description` must be present and under 1024
  characters, and should list the triggers that route work to the skill.
- **Reference links** in `SKILL.md` must point to files that exist under
  `references/`.
- If you add a skill, put it in its own `skills/<name>/` directory.

## Before opening a PR

Run the validator locally — CI (`.github/workflows/validate.yml`) runs the
same check plus `shellcheck` on every push and PR:

```bash
python3 scripts/validate.py
```

It verifies the frontmatter contract, that reference links resolve, that the
JSON manifests parse, and that `install.sh` is syntactically valid.

## Bumping the version

When the skill changes meaningfully, bump `version` in
`.claude-plugin/plugin.json`.
