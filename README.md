# codex-security skill

A portable [Agent Skill](https://agentskills.io) that teaches any coding
agent to run structured security scans **using its own model** — no ChatGPT
sign-in, no API key, no external CLI, no extra cost. The methodology
(threat model → discovery → validation → severity → report) is distilled
from OpenAI's [codex-security](https://github.com/openai/codex-security)
scanner prompts; your agent executes it directly with its normal tools.

The skill lives in [`skills/codex-security/`](skills/codex-security/):

- `SKILL.md` — the four-phase scan workflow
- `references/threat-model.md` — repository threat-model guidance
- `references/validation.md` — proof tuples, suppression rules, confidence
- `references/severity.md` — impact/likelihood policy and severity matrix
- `references/report-format.md` — `findings.json` + `report.md` contract

It covers: full-repo and scoped audits, PR/diff and working-tree reviews,
standalone threat modeling, single-finding validation ("is this real?"),
and validated fixes.

## Install

### Claude Code

As a plugin (this repo is also a plugin marketplace):

```text
/plugin marketplace add <path-or-github-slug-of-this-repo>
/plugin install codex-security@codex-security-skill
```

Or as a plain skill:

```bash
./install.sh claude            # personal:    ~/.claude/skills/codex-security
./install.sh claude-project    # this project: .claude/skills/codex-security
```

### OpenAI Codex CLI

```bash
./install.sh codex             # ~/.codex/skills/codex-security
```

### Any other agent

Agents supporting the Agent Skills standard load skills from a `skills/`
directory — copy the folder there:

```bash
./install.sh dir <that-agents-skills-directory>
```

For agents without skills support, reference the file from your
`AGENTS.md` / rules file:

```markdown
For security scans, follow the instructions in
skills/codex-security/SKILL.md.
```

## Try it

After installing (restart the agent to pick it up), ask things like:

- "Run a security scan on this repo"
- "Security-review my working tree before I commit"
- "Threat-model this codebase"
- "Is this SQL injection finding real? Validate it"

Scan artifacts (`threat_model.md`, `candidate_ledger.jsonl`,
`findings.json`, `report.md`) are written to `.codex-security/` in the
scanned repo by default.

## Repository layout

- `skills/codex-security/` — the portable skill (install this)
- `.claude-plugin/` — Claude Code plugin + marketplace manifests
- `install.sh` — copies the skill into common agent skill directories

The scanning methodology is distilled from OpenAI's
[codex-security](https://github.com/openai/codex-security) scanner prompts;
this repository does not vendor that code.

## Install targets

`install.sh` supports these agents:

| Command | Destination |
|---|---|
| `./install.sh claude` | `~/.claude/skills/` |
| `./install.sh claude-project` | `./.claude/skills/` |
| `./install.sh codex` | `~/.codex/skills/` |
| `./install.sh pi` | `~/.pi/agent/skills/` |
| `./install.sh dir <path>` | `<path>/codex-security` |

## License

MIT — see [LICENSE](LICENSE). The scanning methodology is derived from
OpenAI's [codex-security](https://github.com/openai/codex-security), which
is published by OpenAI under its own license.
