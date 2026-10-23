# Threat model and honest limitations

| Threat | Defense | Residual limitation |
|---|---|---|
| Malicious leader says `NO_KNOWN_CONFLICT` for disclosed paid relationship | Validator independently classifies frozen packet; must match verdict; regression checks forged leader | Independent models can still err or collude |
| Leader invents replacement, quorum, or ties | No leader-supplied nominees, weights or selection scores; deterministic SHA-256 ordering | Chair can strategically pick initial slate and seed |
| Recused original member casts a ballot | Consumer checks actual seated status and digest on every write | Consumer implementation/source must itself be verified |
| Alternate gets vote just because cleared | Consumer checks final roster rather than verdict | A badly written third-party consumer might ignore it |
| Nominee omits disclosure | Missing disclosure = `AMBIGUOUS`, not automatically eligible | A dishonest but signed false denial is not magically detected |
| Third party files false allegation | Attribution by caller, length limit, one concern per filer, frozen snapshot, `AMBIGUOUS` for unsupported claims | Four concern slots can be spammed; no source authentication; griefing and caps remain |
| Leader follows prompt injection in public evidence | Delimit untrusted text, explicit role instruction, bounded verdict, independent validator | Models remain susceptible to sophisticated attacks |
| Chair edits charter/evidence after seeing verdict | One-way phases; charter/matter immutable; disclosures write-once | Chair controls when evidence is closed; disclosure window has no enforced minimum |
| Review selectively excludes unfavorable nominees | Every original and alternate nominee must be assessed before finalization | Chair can leave case unfinalized by never closing evidence |
| New facts emerge after finalization | Finalized case cannot be mutated; consumer still pins panel digest | A new case/consumer migration is required, and old votes remain recorded |
| Membership status overridden by manual admin | No override method exists | Deploying owner can start a different case; downstream integrators must pin expected address |
| Evidence exposes private interests | Public-storage warning and per-record size cap | **All submitted text is public; don't submit secrets or PII** |
| Replay from wrong network | Fixed 61999 config and hard pre-deploy RPC identity guard | Operator must run the guard and verify receipt/finality after writes |

## Operational doctrine

1. Publish a clear recusal charter with specific classes of relationships and
   a bounded matter scope before any evidence arrives.
2. Make candidate and challenger identities auditable. Do not submit personal
   secrets, confidential contracts, or private medical records on chain.
3. Accept a classification as an evidence-bounded screening outcome, **not** a
   definitive legal judgment, identity proof, or guarantee of impartiality.
4. If allegations are contested, expect `AMBIGUOUS` and exclude that member.
5. If the case becomes `BLOCKED`, establish a new matter with a new vetted pool.
6. In production, integrate review deadlines, challenge standing, evidence
   authenticity and cryptographically unpredictable randomness in separate
   purpose-built contracts if your governance actually requires them.

## Explicit non-goals

- No private off-chain evidence vault and no claim of confidentiality.
- No autonomous verification that a link or document is genuine.
- No dynamic revocation of an already-finalized panel on post-close evidence.
- No guaranteed unbiased random selection (fixed hash ordering only).
- No payment, treasury movement, legal verdict or dispute settlement.
- No frontend, backend service or off-chain watcher.
