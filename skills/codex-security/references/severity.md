# Severity policy

Apply only after validation establishes reachability and counterevidence.
Rate `impact` and `likelihood`, then read the matrix mechanically — do not
re-argue severity afterward.

## Hard suppressions first

Set final decision `ignore` when: impact is self-only; preconditions are
unachievable or highly unrealistic; or the path requires privileged /
operator-only / developer-only / physical access — unless the
privilege-escalation delta itself is the finding. Real-but-not-security bugs
are `ignore` too. Do not suppress solely because a surface is internal when
the evidence still shows a meaningful authorization, trust-boundary, or
security-control regression — reduce likelihood instead.

## Likelihood from network position

`remote` → usually high (when the attacker position is realistic and in
scope) · `local_network` → usually medium · `localhost` → usually low ·
`none` → does not raise likelihood. Missing deployment evidence lowers
confidence or stays `unknown`; it does not automatically defeat a finding.

## Impact calibration

**Critical-supporting** (needs proof of reachability from in-scope surface):
credible RCE/arbitrary code execution; XSS with proven session/account
compromise; account takeover or strong auth bypass; missing-authz/tenant
break with broad impact; severe sensitive-data leak (secrets, keys, PII at
scale); sandbox/interpreter escape; SSTI reaching RCE or secrets; arbitrary
file write in executable/startup/config paths; compromise-equivalent logic
flaws at scale.

**High-supporting**: proven SSRF with attacker-controlled destination and
reachable internal targets; exploitable memory corruption; arbitrary file
read of source/less-sensitive data; CSRF on important state-changing
actions; valid reachable hardcoded/default credentials; signature/token
forgery; supply-chain/update-channel compromise; narrower authz
bypass/IDOR; proven XXE; dangerous upload with stored active content;
deserialization/SSTI with dangerous primitives reachable but short of
proven RCE.

**Usually NOT high/critical without a proven chain**: generic
correctness/reliability bugs; low-impact info leaks (banners, versions,
stack traces, user enumeration); open redirect, clickjacking, rate limits;
missing headers/cookie flags/CSP/TLS observations; self-XSS; CSRF on
low-impact actions; "could matter if chained" arguments; transient or
self-targeting DoS; bugs requiring pre-existing admin/root/shell access;
theoretical memory corruption not triggerable from in-scope input.

High/critical acceptance checklist (all should hold, absent explicit threat
model support): in-scope component · realistic attacker · in-scope attack
surface · credible exploitation path, not speculation · major security
impact · would survive triage by a serious auditing firm.

## Matrix (impact × likelihood → severity)

| impact \ likelihood | high | medium | low | unknown | ignore |
|---|---|---|---|---|---|
| **high** | critical* / high | medium | low | medium | ignore |
| **medium** | medium | low | low | low | ignore |
| **low** | low | low | low | low | ignore |
| **unknown** | medium | low | low | low | ignore |
| **ignore** | ignore | ignore | ignore | ignore | ignore |

\* `critical` only when the critical criteria above are satisfied;
otherwise `high`.

Real findings with low impact are downgraded, never dropped. Priority
mapping: critical→P0, high→P1, medium→P2, low→P3; no priority for `ignore`.
