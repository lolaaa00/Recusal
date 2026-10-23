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

The local CLI and independent live JSON-RPC guard both verify `studionet`, chain
`61999`, RPC `https://studio.genlayer.com/api`. StudioNet's edge rejected
Python's default user-agent; the guard now identifies the pinned client and
receives `eth_chainId = 0xf22f` (61999). No deployment or lifecycle transaction
has yet been attempted because no listed unlocked account has been identified
as Lola's authorized deployment account. GitHub authentication for `lolaaa00`
is valid, but the target repository does not yet exist. There is no CI run URL
or remote commit yet.

These missing authorizations are blockers, not test passes. Re-run all gates
immediately before deployment.
