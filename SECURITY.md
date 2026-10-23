# Security policy and review notes

## Core invariant

A nominee with a material conflict, an ambiguous assessment, no signed
disclosure, or no completed assessment must never receive a finalized seat.
`PanelVoteGate` grants no administrative bypass: it checks the pinned Recusal
address, the current finalized digest, and the caller's seated status before
recording a ballot.

## Trust boundaries

- Semantic consensus classifies only the frozen matter, charter, nominee,
  disclosure, and submitted concerns. It does not choose members or votes.
- Contract code owns phase changes, uniqueness, caps, fail-closed treatment,
  alternate ranking, exact panel size, finalization, and vote replay protection.
- Submitted text and references are untrusted public data. They are neither
  authenticated facts nor confidential records.
- The fixed seed produces reproducible ordering, not unbiased randomness. The
  owner can influence the seed and slate before sealing. GenVM v0.2.12 exposes
  no contract-native VRF used by this implementation.

## Audit findings fixed on 2026-10-23

1. **Ambiguous panel commitment encoding (high):** the original digest joined
   user-controlled fields with `|`, permitting serialization collisions across
   different field boundaries. Hash inputs now use UTF-8 byte-length framing
   and include the seat count.
2. **Weak consumer digest validation (low):** the consumer accepted any
   64-character string. It now requires exactly 64 lowercase hexadecimal
   characters.
3. **Incomplete adversarial coverage (medium):** regression tests now cover
   malformed consensus JSON, validator disagreement, full context binding,
   prompt injection in Direct Mode, ambiguous exclusion, invalid contract
   addresses, unfinalized committees, and clear-but-unselected alternates.
4. **Unpinned CI SDK resolution (medium):** CI now sets `GENVM_VERSION=v0.2.12`
   and runs validation, schema extraction, and SDK-aware typechecking for both
   contracts.

## Known limitations

- A false signed denial may evade detection if no reliable concern is filed.
- False or unsupported concerns can force `AMBIGUOUS`; four public concern
  slots per nominee create a bounded griefing surface.
- The seed-ranked alternate order is predictable and owner-influenceable. It
  is suitable for reproducible tie-breaking, not lotteries or adversarially
  unbiased elections.
- Finalized panels are immutable. New evidence requires a new Recusal instance
  and downstream migration.
- Live StudioNet deployment and IC-to-IC behavior must be verified from
  finalized transactions; local Direct Mode is not deployment evidence.

Report suspected vulnerabilities privately to the repository owner before
publishing exploit details. Do not submit secrets, private keys, or personal
evidence in an issue or on chain.
