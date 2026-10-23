# StudioNet 61999 deploy and verification runbook

The repository intentionally does **not** deploy automatically. Lola's Codex
agent must only proceed after source, runtime and network gates are green.

## 1. Prepare exact tools

From the directory unzipped by Lola:

```bash
python3 --version
npm ci
./node_modules/.bin/genlayer --version
python3 -m pip install -r requirements.txt
python3 -m pytest tests -q
python3 scripts/preflight.py
GENVM_VERSION=v0.2.12 genvm-lint check contracts/recusal.py
GENVM_VERSION=v0.2.12 genvm-lint validate contracts/recusal.py
GENVM_VERSION=v0.2.12 genvm-lint schema contracts/recusal.py
GENVM_VERSION=v0.2.12 genvm-lint typecheck contracts/recusal.py
GENVM_VERSION=v0.2.12 genvm-lint check contracts/panel_vote_gate.py
GENVM_VERSION=v0.2.12 genvm-lint validate contracts/panel_vote_gate.py
GENVM_VERSION=v0.2.12 genvm-lint schema contracts/panel_vote_gate.py
GENVM_VERSION=v0.2.12 genvm-lint typecheck contracts/panel_vote_gate.py
python3 -m pytest direct_tests -v
```

Check GenVM SDK `v0.2.12` compatibility and linter `0.11.0` provenance. Do not
report passing Direct Mode, linter or ABI checks until they actually run.

## 2. Enforce exact chain identity

```bash
./node_modules/.bin/genlayer network set studionet
./node_modules/.bin/genlayer network info
python3 scripts/network_guard.py
```

Guard **must** print StudioNet chain `61999`, RPC
`https://studio.genlayer.com/api`, and local CLI `0.39.1`.

If chain ID, RPC response, local CLI version, account or funds cannot be
verified, **STOP**. Do not substitute an alternate network, global preview
CLI, dev/test account, simulator, or unguarded deployment flow.

## 3. Deploy main Recusal instance

Use a funded, authorized wallet controlled by Lola. Choose the exact public
matter, stable charter, `seats=3` (or 5/7), and fixed reproducible seed.
Review the installed `genlayer deploy --help` interface of local `0.39.1`
before constructing arguments. One typical invocation is:

```bash
./node_modules/.bin/genlayer deploy --contract contracts/recusal.py \
  --args "Grant committee review of applicant Delta, round 2026" \
  "A reviewer is materially conflicted if employed by, financially invested in, or under direct paid contract with applicant Delta. Casual familiarity is non-material." \
  3 "recusal-seed-fixed-before-evidence-2026"
```

`deploy` CLI argument parsing may vary by installed version. Validate via the
local pinned help and a controlled read first. Never silently swap tooling.
Wait for finalization, record contract address, transaction hash, success
status, network ID, source SHA-256 and uploaded code parity.

## 4. Run an actual public lifecycle

1. Owner nominates exactly three primaries and at least two alternates.
2. Owner calls `seal_nominations()`.
3. Each nominee signs one `file_disclosure(...)` from their **own** wallet.
4. Third parties may submit bounded `submit_concern(member, evidence, reference)`
   with non-sensitive public evidence.
5. Owner calls `close_evidence()`.
6. Execute `assess(member)` for *every* original and alternate nominee.
7. Assert one deliberately disclosed material conflict is excluded, another
   ambiguity is held, and no unreviewed candidate can be included.
8. Call `finalize_panel()`. Assert either exactly N seated members or `BLOCKED`.
9. Capture the finalized digest, get_panel, statuses, hashes and explorer URLs.

Each write must have its own success/finality receipt; do not equate submission
hashes, simulated state, mocked LLM results, or optimistic UI with finalized
on-chain evidence. Capture malicious-leader/direct-regression output separately.

## 5. Deploy the consumer AFTER the main panel finalizes

`PanelVoteGate` constructor takes `(recusal_address, expected_digest)`.
Use the exact finalized main address and 64-character digest, verifying source
and chain again. Demonstrate:

- A seated wallet casts `YES`.
- A recused primary is rejected.
- A clear but unselected alternate is rejected.
- A duplicate ballot is rejected.
- Wrong digest is rejected.
- `get_counts()` and `get_ballot()` reflect the finalized writes.

If GenLayer's IC-to-IC interface or SDK differs, fix the consumer and add a
Direct Mode/integration regression before deploying it. Do not leave the
published consumer untested while claiming the full gate works.

## 6. Source and repository evidence

Record real items in `evidence/DEPLOYMENT_RECORD.md`:

- Exact Git commit and branch `main`.
- Installed CLI, GenVM SDK, linter and Direct Mode versions.
- Test totals and CI URL from the actual finished run.
- Both addresses, deployment hashes, finalization receipts and explorer links.
- SHA-256 of each `.py` file, on-chain source parity and ABI/schema hashes.
- At least one successful and one rejected live downstream consumer write.

Only after successful verification, publish to the **new repository owned by
`lolaaa00`**, not the account connected to this ChatGPT session.
