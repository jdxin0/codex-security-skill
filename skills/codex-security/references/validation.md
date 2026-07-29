# Validation guidance

Validation decides which candidates survive. Build a short rubric per
candidate (up to five concrete criteria grounded in the code), then complete
the proof tuple with exact `file:line` evidence:

**attacker-controlled source → missing/broken closest control → dangerous
sink → concrete security impact**

Prefer exact source/sink line evidence over prose. Read as much surrounding
code as needed; use nearby safe paths as negative controls, but a safe
sibling never suppresses a vulnerable sibling.

## Dispositions

- `reportable` — the full proof tuple holds with realistic preconditions.
- `suppressed` — name the **exact, complete** control that defeats this
  instance. Partial hardening, a safe sibling code path, a deprecation
  warning, an optional/empty-by-default filter, or "it's a documented
  feature" is not suppression evidence.
- `not_applicable` — the candidate misreads the code; state the proof.
- `deferred` — a proof gap remains (e.g. reproduction needs unavailable
  services, secrets, or infrastructure). A missing runtime environment is a
  proof gap, **not** counterevidence. Record what was attempted and what is
  missing.

## Rules that prevent bad suppressions

- Validate each instance independently; do not collapse multiple instances
  into one finding because they share a vulnerability family. One
  representative proof may support the family, but every sibling gets its
  own row (survived / suppressed-with-exact-control / deferred).
- When one route or helper exposes multiple same-family operations
  (`execute`/`executemany`, `pickle.load`/`loads`, create/delete/admin
  actions), decide each independently triggerable operation separately.
- Do not dismiss a real bug because the code is a demo, test, or "only runs
  locally" — that affects severity, not validity.
- A stricter deployment assumption, a missing downstream caller, or a
  stronger neighboring finding is a precondition or proof gap to state, not
  counterevidence.
- A proved bug of one class does not validate away a different-class bug in
  the same flow (command injection ≠ SSRF ≠ traversal ≠ authz).
- For authz suppressions, name the exact permission/authentication/tenant
  check on that endpoint.
- For parser/XML suppressions, name the exact complete control on the exact
  parser instance; secure-processing flags alone or a safe sibling parser do
  not suppress a different parse call.
- For archive/restore/path candidates, suppression requires proof that each
  untrusted path is normalized and contained **before** the write; writes
  inside the app root still count as arbitrary-file impact.
- Treat API/webhook-supplied values as attacker-controlled even when a
  frontend widget would normally constrain them.

## Class proof tuples (abbreviated)

- **authz/tenant/object**: attacker path + missing/wrong guard + protected
  object or state transition
- **injection/traversal/upload**: attacker bytes + sanitizer/canonicalization
  result + dangerous sink/context
- **XSS/SSTI**: attacker value + escaping/template context + execution sink
- **deserialization/code exec**: attacker-controlled serialized/code bytes +
  unsafe loader/evaluator + execution or object-construction effect
- **SSRF/callback**: attacker-controlled destination + destination-control
  bypass (optional filters and pre-redirect checks don't count) +
  network/read/side-effect impact
- **auth protocol/token**: attacker-controlled token or protocol state +
  validator semantics + validated-vs-consumed mismatch or missing binding +
  authentication impact
- **parser/format DoS**: untrusted structure + unchecked cast / recursion /
  allocation / numeric parse + crash or resource-exhaustion impact
- **secret/data exposure**: sensitive source + exposure boundary + missing
  protection (validate after the high-impact classes)
- **agent/MCP**: untrusted instruction or data source + privileged
  tool/action boundary + action, code-execution, or exfiltration effect

## Validation order and budget

Validate high-impact classes first: command/code execution, unsafe
deserialization, SSTI, SQL/query injection, SSRF, path traversal /
arbitrary file read-write, unsafe upload, authz/tenant bypass. Do not let
low-severity findings or one difficult reproduction setup consume the budget
before the high-impact queue is exhausted — fall back to code trace plus
existing tests/config evidence and continue.

## Evidence strength → confidence

Calibrate from the strongest evidence actually obtained, not the scariness
of the bug class. For compiled/runnable code, prefer (strongest first):
crash reproduction; sanitizer/valgrind output; debugger trace; focused test;
realistic-interface reproduction; code understanding.

- `1.0` reproduced PoC · `0.9+` sanitizer repro · `0.8+` debugger trace ·
  `0.3+` defensible code-understanding conclusion · `0.0` clear
  counterevidence

Keep commands short, non-interactive, and scoped. Never run destructive or
unbounded commands while validating. Save PoCs and logs under
`<out>/validation/<candidate-id>/`.
