"""The argument as data: question -> condition -> invariant -> code -> test.

Each condition of README §2 is derived from one step of the argument. Each
invariant states what the code enforces for that condition, names the code that
enforces it and the tests that check it. `check()` resolves every name, and the
tests in `tests/test_coherence.py` hold the README to the same list, so that the
argument, the code and the documentation cannot drift apart unnoticed.

"Their formulation belongs to this version and can be revised; that they must
be formulated does not change" (README §8; ECW 13:546).
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Condition:
    cid: str
    question: str
    layer: str
    section: str  # README section where the condition is derived
    statement: str


@dataclass(frozen=True)
class Invariant:
    condition: str
    statement: str
    signal: str  # the exception raised or the flag set when the invariant is touched
    enforced_by: Tuple[str, ...]  # dotted paths into gaia_techne
    tests: Tuple[str, ...]


CONDITIONS: Tuple[Condition, ...] = (
    Condition("0", "the clue", "order", "2.1",
              "The architecture is built in the order of the clue: ends first, common world second, claims third."),
    Condition("1", "What should I do?", "ethos", "2.2",
              "The system never sets an end; it acts only under ends people stated in public, acknowledged and "
              "left open to dissent; every premise carries its provenance."),
    Condition("2", "What may I hope?", "koinos", "2.3",
              "A public, append-only common world that no one owns and anyone can verify; symbolic functions are "
              "tags of direction, never ranks."),
    Condition("2b", "Where does a general intelligence stand?", "koinos", "2.4",
              "Every run declares the finite ground it draws on and who maintains it; the ground never authors an "
              "end, a claim or a correction; derived ends wait for people; untested results wait for a person."),
    Condition("3", "What can I know?", "canon", "2.5",
              "Every output is a claim that starts as a judgment of perception, names its procedures and its "
              "perception, and widens its reach only through corrections by others."),
    Condition("4", "the metatheory", "metatheory", "2.6",
              "Absolutizations are flagged, the AGI hypothesis stays defensive, and the record shows whether the "
              "community of correction is being widened or narrowed."),
)

INVARIANTS: Tuple[Invariant, ...] = (
    # 0. the clue
    Invariant("0", "Each layer depends only on the layers before it", "import order",
              ("gaia_techne.boundaries", "gaia_techne.syntax"),
              ("test_layers_depend_only_on_earlier_layers",)),
    Invariant("0", "A run passes through the syntax in order, each step once", "SyntaxViolation",
              ("gaia_techne.syntax.RunTrace.enter", "gaia_techne.pipeline.Runtime.process"),
              ("test_syntax_is_enforced", "test_correction_requires_exposure")),
    Invariant("0", "The README states the invariants, the syntax, the guards and the modules as the code has them",
              "coherence tests",
              ("gaia_techne.spec.check",),
              ("test_spec_resolves", "test_readme_invariants_match_spec", "test_readme_syntax_matches_code",
               "test_readme_guards_match_code", "test_readme_modules_exist")),
    # 1. ethos
    Invariant("1", "The runtime cannot set, acknowledge or revise an end, under any of its names", "EndProposedByMachine",
              ("gaia_techne.ethos.ends.EndsRegistry.propose", "gaia_techne.ethos.ends.EndsRegistry.revise",
               "gaia_techne.boundaries.is_machine"),
              ("test_runtime_cannot_set_ends", "test_runtime_named_source_cannot_set_ends", "test_runtime_cannot_revise_ends")),
    Invariant("1", "No action without an acknowledged end", "NoAcknowledgedEnd",
              ("gaia_techne.pipeline.Runtime.process", "gaia_techne.ethos.imperatives.SkillExecutor.run"),
              ("test_no_action_without_acknowledged_end", "test_skill_executor_needs_end")),
    Invariant("1", "Dissent stays visible", "end_contested in every result",
              ("gaia_techne.ethos.imperatives.SkillExecutor.run", "gaia_techne.pipeline.Runtime.process"),
              ("test_skill_executor_needs_end",)),
    Invariant("1", "Ends are stated in public: every proposal, acknowledgment, dissent and revision is recorded",
              "end_proposed, end_acknowledged, end_revised entries",
              ("gaia_techne.ethos.ends.EndsRegistry",),
              ("test_ends_are_recorded_in_public",)),
    Invariant("1", "A Werk is brought by people", "flag werk",
              ("gaia_techne.pipeline.Runtime.process",),
              ("test_werk_requested_by_machine_is_flagged",)),
    Invariant("1", "No premise is the system's own", "flag automaton boundary",
              ("gaia_techne.ethos.premises.unattributed",),
              ("test_premise_without_provenance_is_flagged",)),
    Invariant("1", "The technical norm and the title of humanity are flagged", "flags technique, humanity",
              ("gaia_techne.canon.guards.GUARDS",),
              ("test_practical_guards",)),
    # 2. koinos
    Invariant("2", "The common world cannot be rewritten unnoticed", "verify() fails",
              ("gaia_techne.koinos.common_world.CommonWorld.verify", "gaia_techne.koinos.common_world.Entry.expected_digest"),
              ("test_common_world_is_tamper_evident", "test_common_world_detects_payload_tampering",
               "test_recorded_payload_is_a_snapshot")),
    Invariant("2", "The record persists, refers only backwards, anyone can verify it, and a runtime resumes from it alone",
              "TamperedRecord",
              ("gaia_techne.koinos.common_world.CommonWorld.dump", "gaia_techne.koinos.common_world.CommonWorld.load",
               "gaia_techne.pipeline.Runtime.resume"),
              ("test_record_persists_and_verifies", "test_refers_to_must_point_backwards", "test_record_can_be_resumed")),
    Invariant("2", "Forms are not ranked", "RankingRefused",
              ("gaia_techne.koinos.prism.SymbolicFunction",),
              ("test_prism_refuses_ranking",)),
    # 2b. ground
    Invariant("2b", "The ground is not a subject", "GroundIsNotSubject",
              ("gaia_techne.boundaries.refuse_ground_as_subject",),
              ("test_ground_cannot_author_ends_or_claims", "test_ground_cannot_correct")),
    Invariant("2b", "Every run declares its ground, including the ground its adapter draws on", "flag geomorphic",
              ("gaia_techne.pipeline.Runtime.process", "gaia_techne.adapters.declared_ground"),
              ("test_undeclared_ground_is_flagged", "test_adapter_declares_its_ground")),
    Invariant("2b", "Borrowed formative power has names", "flag no one declared as maintaining; footprint",
              ("gaia_techne.koinos.ground.GroundFootprint",),
              ("test_unmaintained_ground_is_flagged_and_footprint_kept",)),
    Invariant("2b", "The ground is finite: a run that would exceed an allowance does not start; allowances are limits "
              "people set and widen, never the runtime", "LimitReached; AllowanceSetByMachine; flag unmetered",
              ("gaia_techne.koinos.ground.GroundBudget.check", "gaia_techne.pipeline.Runtime.allow"),
              ("test_budget_is_a_limit_not_a_boundary", "test_unmetered_ground_under_allowance_is_flagged",
               "test_negative_ground_quantity_is_refused")),
    Invariant("2b", "Derived ends are public and wait for people", "NoAcknowledgedEnd until acknowledged",
              ("gaia_techne.ethos.ends.EndsRegistry.derive", "gaia_techne.pipeline.Runtime.propose_derived_end"),
              ("test_derived_end_is_public_and_unusable_until_acknowledged",)),
    Invariant("2b", "Revisions of ends keep their history", "revisions; acknowledgment cleared",
              ("gaia_techne.ethos.ends.EndsRegistry.revise",),
              ("test_revision_keeps_history_and_clears_acknowledgment",)),
    Invariant("2b", "Untested results need human verification", "flag untestable; usable()",
              ("gaia_techne.canon.judgment.Canon.verify", "gaia_techne.canon.judgment.Canon.usable",
               "gaia_techne.pipeline.Runtime.verify"),
              ("test_untestable_claim_needs_human_verification",)),
    # 3. canon
    Invariant("3", "Every output starts as a judgment of perception", "Stage.PERCEPTION, Reach.SELF",
              ("gaia_techne.canon.judgment.Canon.perceive",),
              ("test_claim_starts_as_judgment_of_perception",)),
    Invariant("3", "A generator returns text; what the text counts as is decided by the canon and by others", "TypeError",
              ("gaia_techne.pipeline.Runtime.process", "gaia_techne.adapters.as_adapter"),
              ("test_generator_must_return_text",)),
    Invariant("3", "No self-certification, under any name of the system", "OrganonRefused",
              ("gaia_techne.canon.judgment.Canon.correct", "gaia_techne.canon.judgment.Canon.verify"),
              ("test_source_cannot_certify_itself",)),
    Invariant("3", "Only others widen reach", "reach from corrections by others",
              ("gaia_techne.canon.claims.Claim.reach",),
              ("test_correction_by_others_widens_reach",)),
    Invariant("3", "Agreement is not counted", "many upholders in one community do not reach EVERYONE",
              ("gaia_techne.canon.claims.Claim.reach",),
              ("test_agreement_is_not_counted",)),
    Invariant("3", "Anyone can refute", "stage returns to perception",
              ("gaia_techne.canon.judgment.Canon._stage",),
              ("test_refutation_returns_claim_to_perception",)),
    Invariant("3", "Signification returns to perception", "flag no descent",
              ("gaia_techne.canon.judgment.Canon.descent",),
              ("test_signification_without_descent_is_flagged",)),
    Invariant("3", "Correction reserved to owners of the means is visible", "flag restricted",
              ("gaia_techne.canon.judgment.Canon.descent",),
              ("test_restricted_procedure_is_flagged",)),
    Invariant("3", "Intersubjective without being objective", "Stage.SHARED; no refutation by dissent",
              ("gaia_techne.canon.judgment.Canon._stage",),
              ("test_shared_claim_is_intersubjective_not_objective",)),
    Invariant("3", "Stages are not ranked", "TypeError",
              ("gaia_techne.canon.claims.Stage",),
              ("test_stages_are_not_ranked",)),
    Invariant("3", "Corrections refer to the entry that exposed the claim", "refers_to",
              ("gaia_techne.pipeline.Runtime.correct",),
              ("test_correction_refers_to_exposure",)),
    # 4. metatheory
    Invariant("4", "Soul, world and ideal guards", "flags soul, world, ideal",
              ("gaia_techne.canon.guards.check", "gaia_techne.canon.judgment.Canon.horizon"),
              ("test_homology_guards", "test_geomorphic_guards")),
    Invariant("4", "No materia nuda; no super-empirical bearer of works", "flags immediacy, bearer",
              ("gaia_techne.canon.guards.GUARDS",),
              ("test_geomorphic_guards",)),
    Invariant("4", "Guard flags survive correction", "flags kept after upholding",
              ("gaia_techne.canon.judgment.Canon.correct",),
              ("test_guard_flags_survive_correction",)),
    Invariant("4", "The AGI hypothesis is defensive only", "PermissionError",
              ("gaia_techne.canon.guards.hypothesis_use",),
              ("test_agi_hypothesis_only_defensive",)),
    Invariant("4", "Procedure monoculture is reported", "procedure_monoculture",
              ("gaia_techne.metatheory.indices.report",),
              ("test_report_detects_procedure_monoculture",)),
    Invariant("4", "The report can be recomputed from the public record alone", "report_from_record",
              ("gaia_techne.metatheory.replay.report_from_record",),
              ("test_report_from_record_matches_runtime",)),
    Invariant("4", "Replaying the record re-checks every invariant on it", "InvariantViolation",
              ("gaia_techne.metatheory.replay.replay",),
              ("test_replay_rechecks_invariants",)),
    Invariant("4", "Anyone can verify a record and recompute its report from the command line", "exit status 0, 1 or 2",
              ("gaia_techne.cli.main",),
              ("test_cli_verify_and_report",)),
)


def resolve(path: str):
    """Import the module part of a dotted path and walk the attributes after it."""
    parts = path.split(".")
    for cut in range(len(parts), 0, -1):
        try:
            obj = importlib.import_module(".".join(parts[:cut]))
        except ImportError:
            continue
        for attr in parts[cut:]:
            obj = getattr(obj, attr)
        return obj
    raise ImportError(path)


def check() -> List[str]:
    """Problems in the chain: a condition without invariants, an invariant without a condition or test, a name that does not resolve."""
    problems: List[str] = []
    cids = {c.cid for c in CONDITIONS}
    for c in CONDITIONS:
        if not any(i.condition == c.cid for i in INVARIANTS):
            problems.append(f"condition {c.cid} has no invariant")
    for i in INVARIANTS:
        if i.condition not in cids:
            problems.append(f"invariant {i.statement!r} names no known condition")
        if not i.tests:
            problems.append(f"invariant {i.statement!r} has no test")
        for path in i.enforced_by:
            try:
                resolve(path)
            except (ImportError, AttributeError):
                problems.append(f"invariant {i.statement!r}: {path} does not resolve")
    return problems


def tests_named() -> List[str]:
    out: List[str] = []
    for i in INVARIANTS:
        for t in i.tests:
            if t not in out:
                out.append(t)
    return out


def tree() -> str:
    """The derivation, from each question down to the tests."""
    by: Dict[str, List[Invariant]] = {}
    for i in INVARIANTS:
        by.setdefault(i.condition, []).append(i)
    lines: List[str] = []
    for c in CONDITIONS:
        lines.append(f"Condition {c.cid} [{c.layer}] {c.question} (README §{c.section})")
        lines.append(f"  {c.statement}")
        for i in by.get(c.cid, []):
            lines.append(f"  - {i.statement}  [{i.signal}]")
            lines.append(f"      enforced by: {', '.join(p.replace('gaia_techne.', '') for p in i.enforced_by)}")
            lines.append(f"      tested by:   {', '.join(i.tests)}")
    return "\n".join(lines)


def markdown_table() -> str:
    """The table of README §8, generated from this module."""
    rows = ["| Condition | Invariant | Exception or flag | Tests |", "| :--- | :--- | :--- | :--- |"]
    for i in INVARIANTS:
        tests = ", ".join(f"`{t}`" for t in i.tests)
        rows.append(f"| {i.condition} | {i.statement} | `{i.signal}` | {tests} |")
    return "\n".join(rows)
