# Test evidence

## Verified locally on 2026-10-23

Environment: macOS, Python 3.12.13, Node.js 20.20.2, repository-local
`genlayer 0.39.1`, `pytest 9.0.2`, `genlayer-test 0.29.2`,
`genvm-linter 0.11.0`, `genlayer-py 0.16.3`, and `GENVM_VERSION=v0.2.12`.

| Gate | Result |
|---|---|
| Offline source-loaded adversarial tests | 48 passed, 0 failed |
| GenLayer Direct Mode tests | 12 passed, 0 failed |
| Preflight | 22 passed after documentation additions |
| GenVM lint and validation | passed for both contracts |
| ABI/schema extraction | Recusal: 16 methods; PanelVoteGate: 3 methods |
| SDK-aware typecheck | 0 errors and 0 warnings for both contracts |

Commands:

```bash
.venv/bin/python -m pytest tests -q
.venv/bin/python -m pytest direct_tests -v
.venv/bin/python scripts/preflight.py
GENVM_VERSION=v0.2.12 .venv/bin/genvm-lint check contracts/recusal.py
GENVM_VERSION=v0.2.12 .venv/bin/genvm-lint typecheck contracts/recusal.py
GENVM_VERSION=v0.2.12 .venv/bin/genvm-lint check contracts/panel_vote_gate.py
GENVM_VERSION=v0.2.12 .venv/bin/genvm-lint typecheck contracts/panel_vote_gate.py
```

The Direct Mode suite exercises the actual contract through
`genlayer-test==0.29.2`, including leader/validator paths. It is not evidence of
a finalized StudioNet transaction. Offline tests use a deliberately labeled
fake GenVM boundary around the actual source.

## Network and publication gates

The local CLI reports `studionet`, chain `61999`, RPC
`https://studio.genlayer.com/api`. The independent live JSON-RPC check returned
HTTP 403, so `scripts/network_guard.py` stopped. No deployment or lifecycle
transaction was attempted. The target GitHub repository returned “Repository
not found,” and the configured `lolaaa00` GitHub token is invalid. There is no
CI run URL or remote commit yet.

These failures are blockers, not test passes. Re-run all gates after restoring
RPC access and authorization.
