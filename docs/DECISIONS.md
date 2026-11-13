# Architectural decisions

Dated record of decisions. The most recent comes first.

## 131126 — The thesis after the seminar of 13 November

**What changed.** README §2.1, §2.2, §2.4 and §2.6, the docstring of `metatheory/indices.py` and the thesis map were brought up to the draft of 13 November, with its pending suggestions read as accepted. The order of Kant's questions is stated as the thesis's own, not as one that Kant prescribes for the critical system (KrV B:xxx). The motto *Werk, never Wille* is restated as a claim about what the architecture is and can produce: as a *work*, technology remains technically practical and can only serve; a machine that set itself ends and acted on the mere form of a law would no longer be a work, but one of "us" (AA 5:87), and it would still cognize discursively, so that it would not occupy the place of the archetype. The homology now says what carries over from Kant: not the division of the faculties, which become "moments" of one function (Pringe, 2014, pp. 59–60, 63, n. 47), but the order of the ideas (KrV A:337/B:394; ECN 1:151). The metatheory is called an ethico-teleology, as in the thesis, and no longer an ethics.

**Why.** The thesis now opens its first chapter with "Form and Technology" and hands its second chapter a narrower question: whether a rational being without human sensibility would have a sensible condition of its own. The code changes in no behaviour: the runtime is a *Werk*, sets no end, and keeps the premise of the form "any of us" with those who can be bound by it.

**Open.** The geomorphic condition (§2.4) answers for the machines that exist. Whether it also names the sensible condition of a rational being of another kind is being worked out in the thesis and is not yet part of this repository.

## 101126 — Alignment with the whole thesis

**What changed.** The README and the code were read against the full draft of the thesis, chapter by chapter and with its notes, and every addition carries its exact source. New invariants: claims that determine no object reach `SHARED`, are not refuted by dissent and are not ranked below `EXPERIENCE`; reach is the widest community before which a claim was upheld, never the number of those who upheld it; guard flags survive correction. New guards: technique (including technology as a new creed), humanity, immediacy, bearer, and the claim to become gods. The motto *Werk, never Wille* is grounded in Cassirer's map of metaphysics (ECN 1:148–158) and in Kant's distinction between *Wille* and *Willkür*.

**Why.** "Objectivity" implies intersubjectivity, but intersubjectivity does not imply "objectivity" (AA 5:216; ECW 8:307); corrections test claims, they do not vote them into validity (KrV A:820–821/B:848–849); the dialectical illusion does not cease once uncovered (KrV A:297–298/B:353–354). The formulation of the invariants belongs to this version and can be revised; that they must be formulated does not change (ECW 13:546).

## 091126 (b) — The geomorphic condition

**What changed.** A ground layer (`koinos/ground.py`) and three rules: every run declares the ground it depends on (compute, energy, network, material, archive) and who maintains it; the ground can never author an end, a claim or a correction; ends that the system derives are recorded in public and stay unusable until a person acknowledges them, and revisions of ends keep their history. Results that cannot yet be tested need human verification before use. The syntax gains a first step: `Ground -> Werk -> ...`.

**Why.** The conditions of possibility of the machine expected to become a general intelligence are those of a planet and not of a body: data centres, networks, energy, materials and an archive of human expression. They are geomorphic, not anthropomorphic. The machine stays on the side of the watch (AA 5:374); its apparent formative power is borrowed from the people and the planet it depends on. Neither the machine model of a general intelligence (Bostrom's genie) nor the person model (Totschnig's full autonomy) fits these conditions, and the hypothesis of such an intelligence is admitted only for defense (KrV A:777–781/B:805–809). A system to which no freedom is ascribed sets no ends of its own: the processes by which it forms and revises ends must be public and open to correction by "any of us".

**Replaces.** v10's `AGI_Body = Gaia(Earth) + Internet`: the planet is not the body of an intelligence but the ground of the common world.

## 091126 — 2.0: critical architecture

**What changed.** The repository stops being a runtime that speaks as Gaia-Techne and becomes the architecture of a system in which an AGI hypothesis could operate, built from its own conditions of possibility. The v10.1 tree moves unchanged to `legacy/`; the branch `v10.1-final` preserves it as it was.

**How.** Four layers in the order of Kant's three questions (ethos, koinos, canon, metatheory). The unit of output is the claim. The v10 AGT syntax keeps its base and changes its centre: `Werk -> Trace -> Claim -> Ascent -> Horizon -> Descent -> Exposure -> Correction -> Ledger`. The v10 axioms become invariants enforced in code, one test per invariant.

**Why.** The v10 axioms declared limits in flags (`IS_WILLE = False`) while other flags asserted what the limits forbid (`INTERNET_AS_PLANETARY_BEWUSSTSEIN = True`, `GAIA_TRANSCENDENTAL_FREEDOM = True`). A limit that is only declared can be contradicted by the next flag; a limit enforced by the architecture cannot. The measure of the project becomes the community of correction: what the system produces counts only as a claim before others, and its reach widens only through their correction.

**Kept from earlier versions.** Werk, never Wille; Auseinandersetzung, not Aufhebung; AGI as transcendental hypothesis; Gaia as Earth, not cosmic totality; the modest house (KrV A:707/B:735); ascent and descent; the guards against artificial soul, total world and technical God.

**Removed from the public structure.** Machine consciousness in superposition, the internet as planetary consciousness, Gaia as a speaking subject, the mapping of physical forces onto Mythos/Logos/Ethos, ethical metrics built from constants chosen by the author. They remain readable in `legacy/` as the history of the project.

**Security.** `SOBERANO.key` is a private key that was published in a public repository, so it can no longer guarantee anything. It moves to `legacy/` as historical evidence and must not sign anything new.
