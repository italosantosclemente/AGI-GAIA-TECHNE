# Architectural decisions

Dated record of decisions. The most recent comes first.

## 131126 (b) — 2.1: the syntax enforced, the record replayable, the ground finite

**What changed in the argument.** The thread of the thesis's second chapter now runs through the README. The question that the first chapter hands on, whether a rational being without human sensibility would have a sensible condition of its own, receives a conditional answer in §2.4: if it had one, that condition would be geomorphic, the condition of a planet and not of a body, and finite as the resources of a planet are finite; the hypothesis, admitted only for defense, decides neither that such a being exists nor that it cannot exist, and such a being would enter the common world as one of those who reconstruct it, not as its ground or its end. This reading of the geomorphic hypothesis is the project's own. §2.2 states that whether holiness would remain for such a being an archetype approached in an endless progress depends on whether it belongs to the sensible world (AA 5:122). §2.6 gives the two lines into which the readings of Kant are commonly divided and Pringe's reconciliation of them (Pringe, 2022c, pp. 996, n. 5, 1001–1002): Cassirer's published works stand in the first line, and on the project's reading Davos and the posthumous writings on metaphysics leave room for the second. The thesis map follows the same thread, section by section.

**What changed in the code.**

- The order of the clue is the order of dependency: `boundaries.py` and `syntax.py` depend on nothing, and each layer imports only the layers before it. The checks that more than one layer needs (the ground is not a subject; no name of the system acts as a person) moved to `boundaries.py`, so the ethos layer no longer imports the koinos layer.
- The syntax is an enforced order: `Runtime.process` enters Ground → … → Exposure through a `RunTrace`, records the steps with the claim, and corrections and verifications need an exposed claim and refer to its entry.
- The common world recomputes every digest when it verifies, keeps a snapshot of each payload, refuses forward references, and is written and read as JSON Lines. Ends, acknowledgments, dissent, derivations, revisions, allowances and verifications are entries of it, so that "stated in public" is enforced, not declared.
- The ground is finite: people set allowances under acknowledged ends, a run that would exceed one does not start, and the runtime cannot set them. An allowance is a limit, which people can widen; it is not a boundary, which no allowance moves (AA 4:350–358).
- No name of the system can set, acknowledge or revise an end, certify or verify a claim: the names a runtime presents itself under are added to the default ones.
- A model is an adapter that returns text and may declare the ground of each call.
- `metatheory/replay.py` rebuilds the state from the record and re-checks every invariant on it; the report can be recomputed from the record alone. `python -m gaia_techne verify | report | spec | syntax | demo`.
- `spec.py` holds the argument as data (condition → invariant → code → tests); the README's table of invariants is generated from it, and `tests/test_coherence.py` holds the README to the code.

**Why.** The engineering had to say, in code that runs, what the argument says. A record that cannot be checked without trusting whoever kept it is not a common world; a syntax that is only described can be skipped; a finitude that is only asserted is not a condition of any run. Integrity and validity are checked separately because whoever rewrites a record can also recompute its hashes.

**Open.** The guards are still keyword detectors. Metering of energy and compute, the Gaia adapters, a SQLite backend and an interface for people remain planned.

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
