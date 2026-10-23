# Locally observed verification (2026-10-23)

Environment: isolated Python 3.12 with `pytest==9.0.2`, `genlayer-test==0.29.2`
and `genvm-linter==0.11.0`; pinned GenVM SDK v0.2.12 extracted by Direct Mode.

```text
python -m pytest tests -q
48 passed in 0.21s

python -m pytest direct_tests -q
12 passed in 0.87s

python scripts/preflight.py
PREFLIGHT PASS: 22 checks (offline only)

genvm-lint check contracts/recusal.py
Lint passed (3 checks)
Validation passed — Recusal: 16 methods (9 view, 7 write)

genvm-lint check contracts/panel_vote_gate.py
Lint passed (3 checks)
Validation passed — PanelVoteGate: 3 methods (2 view, 1 write)

genvm-lint schema contracts/recusal.py
Schema extracted; 4 constructor params; 16 methods

genvm-lint schema contracts/panel_vote_gate.py
Schema extracted; 2 constructor params; 3 methods

GENVM_VERSION=v0.2.12 genvm-lint typecheck contracts/recusal.py
0 errors, 0 warnings, 0 information messages

GENVM_VERSION=v0.2.12 genvm-lint typecheck contracts/panel_vote_gate.py
0 errors, 0 warnings, 0 information messages
```

Contract SHA-256, calculated from the exact contract files after those checks:

```text
recusal.py         69e3ca2bb03fb5627ee8bf80c41506f20d8779bd6678518fb641b59518a58109
panel_vote_gate.py 14c5c80e1d96294c83ffd647b402f2b1cb4756925730cb60215561abfb3d4b29
```

These are test-runtime and static checks only. The configured local CLI and
independent live guard verify StudioNet 61999 at the exact required RPC. No RPC
write, deployment, wallet signature, CI run, source-to-deployed-code match, or
finalization was performed. Live IC-to-IC
integration remains pending for Lola's authorized environment. Never convert
these results into claims of production or StudioNet deployment success.
