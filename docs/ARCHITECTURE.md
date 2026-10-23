# Mechanism and state-machine invariants

## Why this needs GenLayer

Ordinary committee membership is a binary ACL. Recusal instead asks a bounded,
context-sensitive question: *does a documented relationship between a nominee
and a frozen matter cross the recusal charter's materiality threshold?*
LLMs handle the semantic relation and validators independently repeat it;
deterministic code retains exclusive control over seat assignment, rank,
membership, and consumer voting rights.

## Immutable inputs

- `matter`: exact decision context. Never replace once deployed.
- `charter`: explicit conflict scope and materiality rule. Never mutate.
- `seats`: odd number 3, 5, or 7. Never mutate.
- `seed`: fixed at creation before the evidence horizon. Never mutate.
- primary and alternate pools: unique wallet addresses; freeze on nomination seal.
- each candidate's own signed disclosure: exactly once during EVIDENCE phase.
- submitted concerns: one per filer/nominee, up to four per nominee, immutable after evidence closure.

## Consensus boundary

An `assess(member)` invocation after the evidence freeze builds a prompt from
the public charter/matter, the nominee's signed statement and the exact
recorded concerns. Each party invokes `gl.nondet.exec_prompt(...,
response_format="json")`, extracts *only* one allowlisted verdict and performs
no state mutation inside the nondeterministic block. A custom validator
rejects malformed leader output and independently runs the same inference,
requiring exact category equality. Rationale prose and scores are not
settlement inputs. `run_nondet_unsafe` rejects errors, which prompts consensus
retry/rotation rather than silently granting eligibility.

Supported classes:

- `MATERIAL_CONFLICT`
- `NON_MATERIAL_RELATIONSHIP`
- `NO_KNOWN_CONFLICT`
- `AMBIGUOUS`

The relation is only as trustworthy as the admitted evidence. It is **not** a
cryptographic proof of a person's off-chain identity or employment and does
not attest that an allegation URL was independently fetched or authenticated.
An unsubstantiated contested claim should be treated as `AMBIGUOUS`.

## Deterministic selection

The contract refuses finalization unless every nominee is assessed. It retains
cleared primaries in their sealed sequence. It computes each eligible alternate's
rank as:

`SHA256(frame(seed) || frame(matter) || frame(lowercase_wallet))`

where `frame(x) = utf8_byte_length(x) + ":" + x`. The same canonical framing
is used for the final panel commitment, which also binds the seat count. This
prevents field-boundary collisions that delimiter concatenation permits.

It sorts by `(rank, lowercase_wallet)` ascending and takes only the required
number to fill vacancies. The algorithm never queries an LLM for nominees,
quorum thresholds, replacement order, or tie breaking.

The `seed` is a **pre-fixed reproducible tie-breaker, not a VRF** or guaranteed
unbiasable source of randomness. The nominating owner can influence seed and
candidate pool at creation. A production election requiring unpredictable,
unbiasable choice would require independently verifiable randomness and a
separate threat model; this project does not claim that property.

If fewer than `seats` clear nominees remain, no partial panel is usable:
the case becomes terminal `BLOCKED`, `is_seated` returns false for everyone,
and `get_panel_digest` returns empty.

## Consumers and identity

The optional separate `PanelVoteGate` receives the real Recusal contract
address and the expected 64-hex-character digest from `get_panel_digest()`
after finalization. Before writing a ballot, it reads both the upstream digest
and `is_seated(caller_wallet)` via a GenLayer view call. Every wallet votes
at most once. It has no administrative bypass and cannot accept votes from
merely *nominated* candidates or cleared alternates that were not seated.

## Commitments and partial trust

The panel digest binds `matter`, `charter`, `seed`, `seats`, and the ordered
seated wallet list using canonical length prefixes. It is a state commitment,
not a signed attestation or standalone proof
of finalization outside the original deployment. Consumers must verify the
address, method result, digest and finalized source/network. Panel decisions
are final only after the parent Recusal transaction itself is finalized on
StudioNet; consumer deployment must wait for that finality.
