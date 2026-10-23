# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

"""Independent IC consumer: only finalized Recusal panel seats can cast votes."""

from genlayer import *


class PanelVoteGate(gl.Contract):
    recusal_address: Address
    expected_digest: str
    yes_count: u32
    no_count: u32
    ballots: TreeMap[str, str]

    def __init__(self, recusal_address: Address, expected_digest: str):
        assert len(expected_digest) == 64, "64-character final panel digest required"
        assert all(ch in "0123456789abcdef" for ch in expected_digest), "lowercase hex digest required"
        self.recusal_address = recusal_address
        self.expected_digest = expected_digest
        self.yes_count = u32(0)
        self.no_count = u32(0)
        # Storage mapping is zero-initialized; do not assign a bare TreeMap().

    def _key(self, member: Address) -> str:
        if isinstance(member, bytes):
            return "0x" + member.hex()
        return str(member).lower()

    @gl.public.write
    def cast_vote(self, choice: str) -> None:
        assert choice in ("YES", "NO"), "invalid vote"
        voter = gl.message.sender_address
        key = self._key(voter)
        assert not self.ballots.get(key, ""), "already voted"
        upstream = gl.get_contract_at(self.recusal_address)
        assert upstream.view().get_panel_digest() == self.expected_digest, "panel digest mismatch"
        assert upstream.view().is_seated(voter), "voter not on cleared panel"
        self.ballots[key] = choice
        if choice == "YES":
            self.yes_count = u32(int(self.yes_count) + 1)
        else:
            self.no_count = u32(int(self.no_count) + 1)

    @gl.public.view
    def get_counts(self) -> dict:
        return {"yes": int(self.yes_count), "no": int(self.no_count)}

    @gl.public.view
    def get_ballot(self, member: Address) -> str:
        return self.ballots.get(self._key(member), "")
