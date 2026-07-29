# Report format

Write both artifacts to `<out>` when the scan completes.

## findings.json

```json
{
  "scan": {
    "scope": "repository | paths | diff | working-tree",
    "target": "<repo root or refs>",
    "completedAt": "<ISO 8601>",
    "filesInScope": 123,
    "filesReviewed": 121
  },
  "findings": [
    {
      "id": "F001",
      "title": "SQL injection in order lookup",
      "severity": "critical | high | medium | low",
      "priority": "P0 | P1 | P2 | P3",
      "confidence": 0.8,
      "cwe": ["CWE-89"],
      "locations": [
        {"path": "src/db.py", "start_line": 42, "end_line": 44, "role": "sink"},
        {"path": "src/routes.py", "start_line": 10, "role": "source"}
      ],
      "description": "What the bug is and why the control fails.",
      "attack_path": "Source → control gap → sink → impact, with preconditions.",
      "remediation": "Concrete fix at the root control.",
      "validation": {"method": "code-trace | poc | test", "evidence": "..."}
    }
  ],
  "coverage": {
    "unreviewed": [{"path": "assets/logo.png", "reason": "binary"}],
    "suppressed": 4,
    "not_applicable": 2,
    "deferred": [{"id": "C009", "gap": "needs staging credentials"}]
  }
}
```

Keep paths repository-relative. Every ledger candidate must map to exactly
one bucket: finding, suppressed, not_applicable, or deferred.

## report.md

1. **Summary** — one paragraph; finding counts by severity; overall risk.
2. **Scope & coverage** — what was scanned, files reviewed vs total,
   unreviewed files with reasons.
3. **Findings** — one section each, ordered by severity: title, severity +
   confidence, locations as `path:line`, description, attack path,
   remediation. Include the code path (source → sink) that proves it.
4. **Deferred / proof gaps** — what could not be concluded and why.
5. **Methodology note** — phases run, threat model reference, and the
   statement that a clean scan does not prove absence of vulnerabilities.

When presenting to the user, lead with the severity counts and the worst
finding; link `file:line` locations.
