# Threat model guidance

Keep the threat model repository-scoped and reusable across unrelated diffs
in the same repo. Ignore the current scan target while writing it unless the
user explicitly asks for a target-scoped model.

While generating:

- Start at the repository root; use the minimum reading needed to understand
  the repo's real-world purpose before narrowing into critical components.
- Distinguish primary product/runtime code from developer-only, test-only,
  documentation, example, and one-off tooling paths.
- Identify the surfaces the repository actually exposes (HTTP routes, CLIs,
  parsers, IPC, plugins, message consumers, build/CI hooks).
- Identify trust boundaries and which actors sit on each side; explicitly
  separate attacker-controlled, operator-controlled, and
  developer-controlled inputs.
- Call out existing mitigations and controls when they materially affect
  severity or scope.
- Say which attacker stories are realistic, which are out of scope, and when
  real-world usage makes a vulnerability class less important. If a class
  requires attacker control that does not exist in this repo's usage, say so.
- Note context-specific concerns:
  - web apps: authn/authz, sessions, CSRF, XSS, SSRF, injection, tenant
    boundaries, rate limits, secret handling
  - crypto/privacy systems: key management, ACLs/RBAC, PII, auditability
  - libraries/frameworks: public interfaces, embedding assumptions,
    safe-by-default behavior, footguns
  - production paths vs CI/build/dev tooling
- Ground claims in specific files, components, or controls when possible.

## Output structure

Markdown with these sections:

1. **Overview** — what the repo is and its intended real-world usage
2. **Threat Model, Trust Boundaries, and Assumptions**
3. **Attack Surface, Mitigations, and Attacker Stories** (including
   out-of-scope stories)
4. **Severity Calibration** — when a vulnerability class would be critical /
   high / medium / low *in this repository*, with a couple of concrete
   examples at each level
