"""Offline source/network integrity checks. Not equivalent to live deployment verification."""

from pathlib import Path
import ast
import json
import hashlib


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_RPC = "https://studio.genlayer.com/api"
EXPECTED_CHAIN = 61999
REQUIRED = [
    "contracts/recusal.py", "contracts/panel_vote_gate.py", "package.json", "package-lock.json",
    "requirements.txt", "tests/test_recusal.py", "direct_tests/test_recusal_direct.py",
    "docs/ARCHITECTURE.md", "docs/THREAT_MODEL.md", "docs/DEPLOYMENT.md",
    "SECURITY.md", "TEST_EVIDENCE.md", "SUBMISSION.md",
]


def check():
    checks = []
    for item in REQUIRED:
        assert (ROOT / item).is_file(), f"missing {item}"
        checks.append(f"file:{item}")
    package = json.loads((ROOT / "package.json").read_text())
    assert package["devDependencies"]["genlayer"] == "0.39.1"
    lockfile = json.loads((ROOT / "package-lock.json").read_text())
    assert lockfile["packages"]["node_modules/genlayer"]["version"] == "0.39.1"
    checks.append("pinned-local-cli")
    cfg = json.loads((ROOT / "network.json").read_text())
    assert cfg == {"chainId": EXPECTED_CHAIN, "network": "studionet", "rpcUrl": EXPECTED_RPC}
    checks.append("stable-studionet-only")
    gltest_cfg = (ROOT / "gltest.config.yaml").read_text()
    assert "default: studionet" in gltest_cfg and EXPECTED_RPC in gltest_cfg
    checks.append("direct-mode-config-studionet")
    for contract, class_name in (("recusal.py", "Recusal"), ("panel_vote_gate.py", "PanelVoteGate")):
        path = ROOT / "contracts" / contract
        raw = path.read_bytes()
        assert raw.startswith(b'# { "Depends": "py-genlayer:'), f"missing GenVM pin: {contract}"
        tree = ast.parse(raw.decode("utf-8"))
        classes = [x for x in tree.body if isinstance(x, ast.ClassDef)]
        assert len(classes) == 1 and classes[0].name == class_name
        assert any(isinstance(n, ast.FunctionDef) and n.name == "__init__" for n in classes[0].body)
        checks.append("syntax-and-structure:" + contract)
    source = (ROOT / "contracts/recusal.py").read_text()
    assert "run_nondet_unsafe(independently_classify, validator)" in source
    assert "return independently_classify() == proposed" in source
    assert "self.phase = \"BLOCKED\"" in source
    assert "self._frame(self.matter)" in source and 'self._frame(str(int(self.seats)))' in source
    checks += ["independent-decision-replay", "fail-closed-panel", "canonical-panel-commitment"]
    assert not (ROOT / "frontend").exists()
    assert not (ROOT / "backend").exists()
    checks.append("contract-only")
    for item in ("contracts/recusal.py", "contracts/panel_vote_gate.py"):
        digest = hashlib.sha256((ROOT / item).read_bytes()).hexdigest()
        print(f"SHA256 {item}: {digest}")
    for label in checks:
        print("PASS", label)
    print(f"PREFLIGHT PASS: {len(checks)} checks (offline only)")


if __name__ == "__main__":
    check()
