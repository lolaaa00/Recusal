"""Offline GenVM boundary adapter: exercise the actual contract source, not a reimplementation.

This is NOT Direct Mode and is never presented as GenVM execution proof.
"""

import importlib.util
from pathlib import Path
import sys
import types
import pytest


ROOT = Path(__file__).resolve().parents[1]


class FakeMap(dict):
    @classmethod
    def __class_getitem__(cls, item):
        return cls


class Public:
    def __init__(self):
        self.view = lambda method: method
        self.write = lambda method: method


class Return:
    def __init__(self, calldata):
        self.calldata = calldata


class ViewProxy:
    def __init__(self, contract):
        self.contract = contract

    def view(self):
        return self.contract


class FakeVM:
    Return = Return
    UserError = ValueError

    def __init__(self):
        self.validators = []

    def run_nondet_unsafe(self, leader, validator):
        self.validators.append(validator)
        return leader()

    def check_last(self, proposed):
        return self.validators[-1](Return(proposed))


class FakeNondet:
    def __init__(self):
        self.results = []
        self.prompts = []

    def exec_prompt(self, prompt, response_format):
        assert response_format == "json"
        self.prompts.append(prompt)
        assert self.results, "explicit LLM mock required"
        result = self.results.pop(0)
        if isinstance(result, dict):
            return result
        return {"verdict": result}


class FakeGL:
    class Contract:
        def __getattr__(self, name):
            if self.__class__.__annotations__.get(name) is FakeMap:
                value = FakeMap()
                setattr(self, name, value)
                return value
            raise AttributeError(name)
    public = Public()

    def __init__(self):
        self.message = types.SimpleNamespace(sender_address="")
        self.nondet = FakeNondet()
        self.vm = FakeVM()
        self.contracts = {}

    def get_contract_at(self, addr):
        if addr not in self.contracts:
            raise ValueError("unknown contract")
        return ViewProxy(self.contracts[addr])


def load_contract(path, name, fake_gl):
    stub = types.ModuleType("genlayer")
    stub.gl = fake_gl
    stub.Address = str
    stub.u32 = int
    stub.TreeMap = FakeMap
    stub.__all__ = ["gl", "Address", "u32", "TreeMap"]
    prior = sys.modules.get("genlayer")
    sys.modules["genlayer"] = stub
    try:
        spec = importlib.util.spec_from_file_location(name, ROOT / path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if prior is None:
            sys.modules.pop("genlayer", None)
        else:
            sys.modules["genlayer"] = prior


@pytest.fixture
def chain():
    gl = FakeGL()
    main = load_contract("contracts/recusal.py", "recusal_under_test", gl)
    consumer = load_contract("contracts/panel_vote_gate.py", "vote_under_test", gl)
    admin = "0x" + "a" * 40
    users = ["0x" + f"{i:040x}" for i in range(1, 9)]
    gl.message.sender_address = admin
    matter = "Allocation board for treasury grant round 2026"
    charter = (
        "Recuse anyone holding an interest in an applicant, employed by an applicant, "
        "or directly contracted for the reviewed grant. Casual familiarity alone is not material."
    )
    recusal = main.Recusal(matter, charter, 3, "demo-seed-00000001")
    gl.contracts["recusal_address"] = recusal

    class Environment:
        def __init__(self):
            self.gl = gl
            self.admin = admin
            self.users = users
            self.recusal = recusal
            self.VoteGate = consumer.PanelVoteGate

        def as_user(self, addr):
            self.gl.message.sender_address = addr

        def nominate(self, alternates=2):
            self.as_user(self.admin)
            for user in self.users[:3]:
                self.recusal.nominate(user, False)
            for user in self.users[3:3 + alternates]:
                self.recusal.nominate(user, True)
            self.recusal.seal_nominations()

        def disclose(self, index, text="I have no financial or employment relationship with any grant applicant."):
            self.as_user(self.users[index])
            self.recusal.file_disclosure(text)

        def to_review(self):
            self.as_user(self.admin)
            self.recusal.close_evidence()

        def assess(self, index, verdict):
            self.as_user(self.users[6])
            self.gl.nondet.results.append(verdict)
            return self.recusal.assess(self.users[index])

        def resolve_all(self, decisions=None, missing=()):
            decisions = decisions or {}
            for i in range(5):
                if i not in missing:
                    self.disclose(i)
            self.to_review()
            for i in range(5):
                if i in missing:
                    self.recusal.assess(self.users[i])
                else:
                    self.assess(i, decisions.get(i, "NO_KNOWN_CONFLICT"))

    return Environment()
