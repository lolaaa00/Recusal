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

**READY.** Source quality gates pass and the mandatory live evidence is complete:

- Repository: `https://github.com/lolaaa00/Recusal` — published. The full
  verification workflow passed at
  `https://github.com/lolaaa00/Recusal/actions/runs/40013996862`.
- Required network: StudioNet `61999`, RPC
  `https://studio.genlayer.com/api` — verified by the local CLI and independent
  live `eth_chainId` request.
- Main Recusal: `0x06da8320F25a48548D7d3cA502Be2E3b6910A255`.
- PanelVoteGate: `0x20B2933f1b459034E81b3C0e9f6933301dE7a52b`.
- Final digest: `a087de8a85fa68df58cc90434ecbdd3d1596a11d6fd0a3b097527cd5d95ab3fc`.
- Finalized lifecycle covers replacement, ambiguity, `BLOCKED`, authorization,
  immutability, valid consumer votes, duplicate/non-member rejection, and
  stale-digest rejection.

Actual receipts, source parity, hashes, setup failures, and the temporarily
paused public explorer are documented in `evidence/DEPLOYMENT_RECORD.md`.
