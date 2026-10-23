# Recusal — Consensus-Verified Conflict-of-Interest Exclusion and Deterministic Committee Replacement

Recusal is a reusable GenLayer Intelligent Contract primitive for screening a
frozen committee slate against a case-specific conflict charter. Ordinary
smart contracts can enforce membership and authorization, but cannot reliably
interpret whether described financial, employment, professional, or personal
relationships cross a contextual materiality threshold.

GenLayer validators independently establish one bounded semantic result for
each nominee: `MATERIAL_CONFLICT`, `NON_MATERIAL_RELATIONSHIP`,
`NO_KNOWN_CONFLICT`, or `AMBIGUOUS`. Deterministic contract code—not the model—
enforces authorization, immutable phase boundaries, evidence caps, missing-
disclosure failure, exclusion, alternate ranking, exact panel size, canonical
panel commitment, and finalization. Ambiguous and unresolved nominees never
become eligible.

Cleared primaries retain nomination order. Vacancies are filled from the
previously frozen, cleared alternate pool using a reproducible SHA-256 ranking
over canonical length-prefixed seed, matter, and address fields. This is a
transparent deterministic tie-breaker, not a claim of unbiased randomness.

The independent `PanelVoteGate` consumer pins a Recusal deployment and its
final digest. On every ballot it reads the upstream digest and seated status,
uses the transaction caller as voter identity, and rejects non-members and
duplicate votes.

Local evidence currently comprises 48 offline adversarial tests, 12 GenLayer
Direct Mode tests, complete GenVM v0.2.12 lint/validation/schema checks, and
zero-diagnostic SDK-aware typechecks for both contracts. Tests cover malicious
leader output, validator disagreement, prompt injection, malformed output,
missing disclosures, material and ambiguous exclusion, deterministic
replacement, insufficient eligible alternates, immutable finalization,
consumer address/digest failures, unselected alternates, and vote replay.

## Current submission status

**NOT READY for live submission.** Source quality gates pass locally, but the
mandatory external evidence is blocked:

- Repository: `https://github.com/lolaaa00/Recusal` — published. The full
  verification workflow passed at
  `https://github.com/lolaaa00/Recusal/actions/runs/40010902759`.
- Required network: StudioNet `61999`, RPC
  `https://studio.genlayer.com/api` — verified by the local CLI and independent
  live `eth_chainId` request.
- Deployment account: blocked until Lola identifies which listed unlocked
  account is authorized and funded.
- No contract address, finalized transaction, explorer proof, lifecycle
  receipt, consumer deployment, cross-contract live vote, or CI URL exists.

Once those blockers are resolved, follow `docs/DEPLOYMENT.md`, record only
finalized receipts in `evidence/DEPLOYMENT_RECORD.md`, verify deployed-source
parity, and replace this status with actual links. No deployment claim should
be inferred from local tests.
