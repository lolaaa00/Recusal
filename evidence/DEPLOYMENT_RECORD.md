# Verified deployment record — to be completed by Lola's Codex agent

Status: **NOT DEPLOYED**. The fields below intentionally remain pending.

| Evidence | Value |
|---|---|
| Target owner/repo | `lolaaa00/recusal` |
| Network | stable StudioNet, chain `61999` |
| RPC | `https://studio.genlayer.com/api` |
| Local CLI | `genlayer@0.39.1` (verified) |
| Configured network | `studionet`, chain `61999`, exact RPC (verified by local CLI only) |
| Live RPC chain identity | verified: `eth_chainId=0xf22f` (`61999`) |
| Main source SHA-256 | recorded in `evidence/LOCAL_CHECKS.md` |
| Consumer source SHA-256 | recorded in `evidence/LOCAL_CHECKS.md` |
| Main contract address | pending |
| Consumer contract address | pending |
| Main deployment transaction / finality | pending |
| Consumer deployment transaction / finality | pending |
| Full lifecycle transaction/receipt links | pending |
| Actual Direct Mode results | 12 passed locally |
| GenVM lint/validate/schema/typecheck results | passed for both; zero type diagnostics |
| CI commit and run URL | blocked: target repo not found; GitHub auth valid |
| Source vs deployed bytes match | pending |
| Consumer accepted/rejected writes | pending |
| Final review readiness | pending |

No deployment has been attempted. The network guard now passes, but the active
CLI account is `probe2`; it has not been assumed to be Lola's authorized and
funded deployment account. This fact must not be converted into deployment
evidence.
