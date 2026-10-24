# Build and deployment status — 2026-10-24

Status: **READY**.

- Repository: <https://github.com/lolaaa00/Recusal>
- StudioNet chain: `61999`; RPC: `https://studio.genlayer.com/api`
- Main: `0x06da8320F25a48548D7d3cA502Be2E3b6910A255`
- Consumer: `0x20B2933f1b459034E81b3C0e9f6933301dE7a52b`
- Digest: `a087de8a85fa68df58cc90434ecbdd3d1596a11d6fd0a3b097527cd5d95ab3fc`
- Offline pytest: **48 passed**; Direct Mode: **12 passed**; preflight: **22 passed**.
- GenVM v0.2.12 lint/validate/schema: passed for both; typecheck: zero diagnostics.
- CI: <https://github.com/lolaaa00/Recusal/actions/runs/40013996862> passed.

Live evidence covers normal finalization, material-conflict exclusion,
deterministic replacement, ambiguity, insufficient replacements (`BLOCKED`),
immutable finalization, owner authorization, eligible replacement voting,
recused and unresolved voter rejection, duplicate rejection, and stale digest
rejection. Full receipts and source hashes are in
`evidence/DEPLOYMENT_RECORD.md`.

Known limitation: <https://genlayer-explorer.vercel.app> returned
`DEPLOYMENT_PAUSED` during final verification. Finalized RPC receipts remain
reproducible with the pinned CLI; no working explorer deep link is claimed
while that public frontend is unavailable.
