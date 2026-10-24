# Verified StudioNet deployment record

Verified on 2026-10-24 against StudioNet chain `61999` and RPC
`https://studio.genlayer.com/api` with repository-local `genlayer 0.39.1`.
The authorized account was `probe2`
(`0xe36aeec44999a1c347782b4459bedd98329b9147`).

## Deployments

| Artifact | Address | Deployment transaction | Final state |
|---|---|---|---|
| Recusal (main) | `0x06da8320F25a48548D7d3cA502Be2E3b6910A255` | `0x85e5b90408e2516d4cdc050474474e34a663347e2d74f2e3089d108de1ff6949` | `FINALIZED` panel |
| PanelVoteGate | `0x20B2933f1b459034E81b3C0e9f6933301dE7a52b` | `0x1b96bbbd5ca9289ac97a6b26c0d930a8f4d6b675f74d5cf8e5308ee264accbfc` | `{yes: 1, no: 1}` |
| Recusal (insufficient-replacement proof) | `0xd58A80e5EC395C6aa2a43c23873D9bD0Ff3bC927` | `0xa67574ed5f8898b30fda2e31d069df8fc2f926048b7ff896cfb5a70ec95666bf` | `BLOCKED` |
| PanelVoteGate (stale-digest proof) | `0xD3C95D23ce4a04f0Bc1F9659fBA606455684eF56` | `0x2c13536650633e919cdbecb39e210a29a60239c334f8b256e8dd1782b4279d5b` | mismatch rejection only |

Explorer base: <https://genlayer-explorer.vercel.app>. It returned
`DEPLOYMENT_PAUSED` when checked on 2026-10-24, so finalized RPC receipts are
the authoritative reproducible evidence; no working deep-link format is
claimed.

Main constructor arguments: matter `Grant committee review of applicant
Delta, round 2026`; charter `A reviewer is materially conflicted if employed
by, financially invested in, or under direct paid contract with applicant
Delta. Casual familiarity is non-material.`; seats `3`; seed
`recusal-seed-fixed-before-evidence-2026`.

The finalized digest is
`a087de8a85fa68df58cc90434ecbdd3d1596a11d6fd0a3b097527cd5d95ab3fc`.
The ordered panel is:

1. `0x19fbc43de9f8dbce33fba7ad34e9f4ee49e565e1`
2. `0xaa18ecd158aec67c75a51768b747cb3247a21689`
3. `0xe36aeec44999a1c347782b4459bedd98329b9147`

## Main lifecycle receipts

| Operation | Transaction | Verified result |
|---|---|---|
| nominate five members | `0x06b466e14ee25d22028130ff56f5bc12fd0cf8d2c7d22dc74ffa32b9de34444c`, `0xb82b092c88c7345db998388aed67c0ddb71d3b96e2efd7b0677d3f8f48e90827`, `0x7f414c97c376ffb909c60efc8577afd389c967c3ec959a2b3413a2c410a5deed`, `0x9f41e4af29367ae1ec55d126410704c4e4843911ceb7fd6b8a983518ab7401c1`, `0x8877378079486776c1ad4c32569c5f8072eb90d63eb4ad207aee84a3192627f1` | accepted |
| seal nominations | `0x0601313180acbb7bda06fac182abce3d845ac38b69ae789adc5413f7d9be0005` | phase `EVIDENCE` |
| conflicted disclosure | `0xd1349c0851c63c11727a7141f71ffd63cd70e12f081e6f4388ce4b30347d560b` | accepted |
| clear disclosures | `0xb7116baefe3c0a7f78a6399df0edd15bec8037e0284f365056e43f8f8a02561b`, `0x9072a851788bc68fd419d96ce00ebc0640de931b8a1aa27f8c5408024c0429db`, `0xbb3b640a679c6049308ec12d9903a94b5821c8cfe1ce14039aff1a64f1a6693d` | accepted |
| close evidence | `0x465f6c7c6d6f06a07a35fe76cbcf338e56e8d59b08fdcda9f0be50fc4a3e3339` | phase `REVIEW` |
| assess five nominees | `0x72703bf881ff2c0f686074aa3c8fbf846c6b5a03310d721c535a19260a183c92`, `0xada96d17352b2026b0a647ac997639a2472248460f9770b4a6ff9c87b205f76c`, `0xdf5851e2bf6b5b3abb7a09087d6c4dbd8151ea683bc2e24fbb3d96f3a6b2bff7`, `0xe9e5e02c7bde5ff1c3dd0886e3381867aa734409b1eb36a00672ef9b840f690e`, `0x2f66b8cd5111efa93f774df267809ad83d0f124b5ac3f295f527dd70b6c009c2` | `MATERIAL_CONFLICT`, three `NO_KNOWN_CONFLICT`, `AMBIGUOUS` |
| finalize panel | `0xa5ec6805396a97c5c89f3260675b5d45a7edf8784af5df478877cb42a13c78ff` | `FINALIZED`; clear alternate replaces conflicted primary |
| repeat finalization | `0xbb0dd6a2cceba0cbbf6acdb0158bbeff74a3b319ccc3f140be2d50b526fe391d` | finalized receipt, execution `ERROR: invalid phase` |
| unauthorized admin call | `0x91bf1d86c3e2bf5d6cd9e4248a8c3fa824bdf79777c10b9a97fa6f726a44ae1c` | finalized receipt, execution `ERROR: only owner` |

## Consumer receipts

| Operation | Transaction | Verified result |
|---|---|---|
| replacement member votes `YES` | `0x368a7b7af5e6124cdeca40ab7b07e04f95f8bc0cc90d1ef0f0b9a2d431f0ef91` | accepted |
| seated primary votes `NO` | `0x73067729b1964f6e14b770bb0a457f28d9f10106b0a3b5608e1f0e60587dce7e` | accepted |
| duplicate vote | `0xbffab85f7a6f5420433febda77755998402f7a3eebbbb35da12c8258e920f7ba` | `ERROR: already voted` |
| recused primary votes | `0xbf67ab452e48ff4d27b554340f48be062c3e15983f34bf635d30bc0efa63a9bb` | `ERROR: voter not on cleared panel` |
| ambiguous alternate votes | `0x3d1f737cf18782138dd7c80b5fcd6e15a04258bd736f48220e942e0e0bc677f2` | `ERROR: voter not on cleared panel` |
| stale-digest gate vote | `0x800538773510a9f1f6590c31ec62779ea460f78405b6e48b2334a6d3c0fd6742` | `ERROR: panel digest mismatch` |

The ambiguous test wallet received `0.1 GEN` solely for its rejection write:
transfer `0x340466fc7e9b7dbc4af829d14cb187843033b1346e25935542842f7fe150cf17`.

## Insufficient replacements and setup failures

The valid three-seat proof assessed three primaries and one alternate as
`AMBIGUOUS`, then finalized to `BLOCKED` in
`0xbee6b4098af4a589328506ab8bfaeab7036b655d8e7218d952f01582c67b3518`.
`get_config()` returned `phase: BLOCKED` and an empty digest.

Two setup failures are retained rather than hidden: a one-seat deployment
(`0xbc68e29fc98911a9203ebed0694d05d3004fad904078ca0ab053d4fa5aedcaa1`)
failed with `3, 5 or 7 seats`; an all-zero digest was parsed by the CLI as an
integer (`0x29cd79ce51a0fa4274af42ac85c0f0301444eb909049acf402499c5a117479df`).
Neither failed address is presented as a deployed contract.

## Source and publication integrity

| Source | SHA-256 |
|---|---|
| `contracts/recusal.py` | `69e3ca2bb03fb5627ee8bf80c41506f20d8779bd6678518fb641b59518a58109` |
| `contracts/panel_vote_gate.py` | `14c5c80e1d96294c83ffd647b402f2b1cb4756925730cb60215561abfb3d4b29` |

`genlayer code` retrieved the live contract sources and they matched the
audited local files; `genlayer schema` exposed the expected 16-method Recusal
and 3-method consumer ABIs. Contract sources did not change after deployment.
Repository: <https://github.com/lolaaa00/Recusal>.
