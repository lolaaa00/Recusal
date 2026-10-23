"""Hard stop unless connected RPC is stable StudioNet 61999.

Run before ANY deployment or contract write. No fallbacks or network switching.
"""

import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request
import urllib.error


ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "network.json").read_text())
EXPECTED = 61999
RPC = "https://studio.genlayer.com/api"


def main():
    if CFG != {"chainId": EXPECTED, "network": "studionet", "rpcUrl": RPC}:
        raise SystemExit("STOP: unexpected network configuration")
    if os.environ.get("GENLAYER_RPC_URL", RPC) != RPC:
        raise SystemExit("STOP: RPC environment override points outside stable StudioNet")
    result = subprocess.run(
        [str(ROOT / "node_modules" / ".bin" / "genlayer"), "--version"],
        check=True, capture_output=True, text=True, cwd=ROOT,
    )
    version = (result.stdout + result.stderr).strip()
    if not re.search(r"(?<!\d)0\.39\.1(?!\d)", version):
        raise SystemExit("STOP: local GenLayer CLI is not 0.39.1: " + version)
    info_result = subprocess.run(
        [str(ROOT / "node_modules" / ".bin" / "genlayer"), "network", "info"],
        check=True, capture_output=True, text=True, cwd=ROOT,
    )
    selected_network = (info_result.stdout + info_result.stderr).lower()
    if "studionet" not in selected_network or RPC not in selected_network or str(EXPECTED) not in selected_network:
        raise SystemExit("STOP: local CLI is not configured for stable StudioNet 61999")
    request = urllib.request.Request(
        RPC,
        data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_chainId", "params": []}).encode(),
        # StudioNet's edge rejects Python's default urllib user-agent with 403.
        # Identify this pinned client explicitly; the request remains read-only.
        headers={
            "Content-Type": "application/json",
            "User-Agent": "recusal-network-guard/genlayer-cli-0.39.1",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"STOP: RPC chain-id request returned HTTP {exc.code}") from None
    except urllib.error.URLError as exc:
        raise SystemExit(f"STOP: RPC chain-id request failed: {exc.reason}") from None
    if "error" in payload or "result" not in payload:
        raise SystemExit("STOP: RPC did not return a verifiable eth_chainId")
    raw = payload["result"]
    actual = int(raw, 16) if isinstance(raw, str) and raw.startswith("0x") else int(raw)
    if actual != EXPECTED:
        raise SystemExit(f"STOP: connected chain is {actual}, expected {EXPECTED}")
    print(f"PASS: local GenLayer CLI 0.39.1, StudioNet chain {actual}, RPC {RPC}")


if __name__ == "__main__":
    main()
