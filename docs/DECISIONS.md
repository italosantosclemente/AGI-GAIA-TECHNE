# Architectural decisions

Dated record of decisions. The most recent comes first.

## 091126 — 2.0: critical architecture

**What changed.** The repository stops being a runtime that speaks as Gaia-Techne and becomes the architecture of a system in which an AGI hypothesis could operate, built from its own conditions of possibility. The v10.1 tree moves unchanged to `legacy/`; the release `v10.1` preserves it as it was.

**How.** Four layers in the order of Kant's three questions (ethos, koinos, canon, metatheory). The unit of output is the claim. The v10 AGT syntax keeps its base and changes its centre: `Werk -> Trace -> Claim -> Ascent -> Horizon -> Descent -> Exposure -> Correction -> Ledger`. The v10 axioms become invariants enforced in code, one test per invariant.

**Why.** The v10 axioms declared limits in flags (`IS_WILLE = False`) while other flags asserted what the limits forbid (`INTERNET_AS_PLANETARY_BEWUSSTSEIN = True`, `GAIA_TRANSCENDENTAL_FREEDOM = True`). A limit that is only declared can be contradicted by the next flag; a limit enforced by the architecture cannot. The measure of the project becomes the community of correction: what the system produces counts only as a claim before others, and its reach widens only through their correction.

**Kept from earlier versions.** Werk, never Wille; Auseinandersetzung, not Aufhebung; AGI as transcendental hypothesis; Gaia as Earth, not cosmic totality; the modest house (KrV A:707/B:735); ascent and descent; the guards against artificial soul, total world and technical God.

**Removed from the public structure.** Machine consciousness in superposition, the internet as planetary consciousness, Gaia as a speaking subject, the mapping of physical forces onto Mythos/Logos/Ethos, ethical metrics built from constants chosen by the author. They remain readable in `legacy/` as the history of the project.

**Security.** `SOBERANO.key` is a private key that was published in a public repository, so it can no longer guarantee anything. It moves to `legacy/` as historical evidence and must not sign anything new.
