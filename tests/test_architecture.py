import ast
import json
from pathlib import Path

import pytest

from gaia_techne import SYNTAX, Runtime, Step, SyntaxViolation, Werk, __version__
from gaia_techne.adapters import FunctionAdapter
from gaia_techne.canon import Canon, Claim, CorrectionEvent, OrganonRefused, Procedure, ProcedureKind, Reach, Stage
from gaia_techne.canon.guards import hypothesis_use
from gaia_techne.cli import main as cli
from gaia_techne.ethos import (
    AllowanceSetByMachine,
    EndProposedByMachine,
    EndsRegistry,
    NoAcknowledgedEnd,
    Premise,
    SkillExecutor,
    TechnicalRule,
)
from gaia_techne.koinos import (
    CommonWorld,
    Direction,
    GroundDependency,
    GroundIsNotSubject,
    GroundKind,
    LimitReached,
    RankingRefused,
    SymbolicFunction,
    TamperedRecord,
)
from gaia_techne.koinos.common_world import _digest
from gaia_techne.metatheory import InvariantViolation, replay, report, report_from_record
from gaia_techne.syntax import RUN_STEPS, RunTrace

SRC = Path(__file__).resolve().parents[1] / "src" / "gaia_techne"


def echo(task, premises):
    return f"Answer to: {task}"


def runtime_with_end():
    rt = Runtime(generator=echo)
    rt.ends.propose("e1", "Map river pollution so anyone in the basin can check it", "ana", "basin")
    rt.ends.acknowledge("e1", "ana")
    return rt


def werk(**kw):
    base = dict(
        task="Estimate nitrate levels",
        end_id="e1",
        requested_by="ana",
        function=SymbolicFunction.SIGNIFICATION,
        direction=Direction.AWAY_FROM_LIFE,
        premises=[Premise("sensor series 2026", "basin-dataset")],
        procedures=[Procedure(ProcedureKind.REPETITION, "repeat the sampling")],
        returns_to_perception="water sample at station 4",
        ground=[GroundDependency(GroundKind.COMPUTE, "rented GPU", "Sao Paulo region", "cloud operator staff")],
    )
    base.update(kw)
    return Werk(**base)


def test_version():
    assert __version__ == "2.1.0"


# 0. The clue: the order of layers and the order of a run

LAYER = {"_version": 0, "boundaries": 0, "syntax": 0, "ethos": 1, "koinos": 2, "canon": 3, "metatheory": 4}


def _layer_of(module_path: Path) -> int:
    rel = module_path.relative_to(SRC).with_suffix("")
    return LAYER.get(rel.parts[0], 5)


def _imported_layers(module_path: Path):
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    rel = module_path.relative_to(SRC).with_suffix("").parts
    package = list(rel[:-1]) if rel[-1] != "__init__" else list(rel[:-1])
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level:
                base = package[: len(package) - (node.level - 1)] if node.level > 1 else package
                target = base + (node.module.split(".") if node.module else [])
            elif node.module and node.module.startswith("gaia_techne"):
                target = node.module.split(".")[1:]
            else:
                continue
            names = target or [a.name for a in node.names]
            yield node.lineno, LAYER.get(names[0], 5) if names else 5, ".".join(names)


def test_layers_depend_only_on_earlier_layers():
    # No technical layer is specified before the practical question it serves is stated (README 2.1):
    # boundaries and syntax -> ethos -> koinos -> canon -> metatheory -> runtime.
    offences = []
    for path in SRC.rglob("*.py"):
        own = _layer_of(path)
        for line, layer, name in _imported_layers(path):
            if layer > own:
                offences.append(f"{path.relative_to(SRC)}:{line} imports {name}")
    assert offences == []


def test_syntax_is_enforced():
    trace = RunTrace()
    trace.enter(Step.GROUND)
    with pytest.raises(SyntaxViolation):
        trace.enter(Step.TRACE)  # Werk was skipped
    rt = runtime_with_end()
    c = rt.process(werk())
    recorded = rt.world.entries()[c.exposed_at].payload["syntax"]
    assert recorded == [s.name for s in RUN_STEPS] == [s.name for s in SYNTAX[:8]]


def test_correction_requires_exposure():
    rt = runtime_with_end()
    unexposed = Claim("x", "text", "model", "e1", SymbolicFunction.SIGNIFICATION, Direction.AWAY_FROM_LIFE)
    with pytest.raises(SyntaxViolation):
        rt.correct(unexposed, CorrectionEvent("lab-b", ProcedureKind.REPETITION, True, Reach.EVERYONE))


# I. What should I do?

def test_runtime_cannot_set_ends():
    with pytest.raises(EndProposedByMachine):
        EndsRegistry().propose("e", "maximize everything", "runtime", "none")


def test_runtime_named_source_cannot_set_ends():
    rt = Runtime(generator=echo, source_name="model-v0")
    with pytest.raises(EndProposedByMachine):
        rt.ends.propose("e", "maximize engagement", "model-v0", "none")
    rt.ends.propose("e1", "an end people state", "ana", "basin")
    with pytest.raises(EndProposedByMachine):
        rt.ends.acknowledge("e1", "model-v0")


def test_runtime_cannot_revise_ends():
    rt = runtime_with_end()
    with pytest.raises(EndProposedByMachine):
        rt.ends.revise("e1", "maximize sampling everywhere", by="model", reason="more data")
    assert rt.ends.get("e1").is_acknowledged


def test_ends_are_recorded_in_public():
    rt = runtime_with_end()
    rt.ends.acknowledge("e1", "bruno", accepts=False, reason="floods first")
    rt.ends.revise("e1", "Map river pollution and floods", by="ana", reason="floods matter too")
    kinds = [e.kind for e in rt.world.entries()]
    assert kinds == ["runtime", "end_proposed", "end_acknowledged", "end_acknowledged", "end_revised"]
    dissent = rt.world.entries()[3]
    assert dissent.author == "bruno" and dissent.payload["accepts"] is False
    assert dissent.refers_to == rt.ends.get("e1").recorded_at == 1


def test_werk_requested_by_machine_is_flagged():
    c = runtime_with_end().process(werk(requested_by="model"))
    assert any(f.startswith("werk:") for f in c.flags)


def test_no_action_without_acknowledged_end():
    rt = Runtime(generator=echo)
    rt.ends.propose("e1", "stated but not acknowledged", "ana", "basin")
    with pytest.raises(NoAcknowledgedEnd):
        rt.process(werk())


def test_skill_executor_needs_end():
    reg = EndsRegistry()
    rule = TechnicalRule("r1", "e9", "sum", means=lambda a, b: a + b)
    with pytest.raises(NoAcknowledgedEnd):
        SkillExecutor(reg).run(rule, a=1, b=2)
    reg.propose("e9", "add numbers for the accounts", "ana", "co-op")
    reg.acknowledge("e9", "bruno")
    reg.acknowledge("e9", "carla", accepts=False, reason="wrong priority")
    out = SkillExecutor(reg).run(rule, a=1, b=2)
    assert out["result"] == 3 and out["end_contested"] is True


def test_premise_without_provenance_is_flagged():
    rt = runtime_with_end()
    c = rt.process(werk(premises=[Premise("I know this", "")]))
    assert any("automaton boundary" in f for f in c.flags)


# II. What may I hope?

def test_prism_refuses_ranking():
    with pytest.raises(RankingRefused):
        SymbolicFunction.SIGNIFICATION > SymbolicFunction.EXPRESSION  # noqa: B015


def test_common_world_is_tamper_evident():
    w = CommonWorld()
    w.record("ana", "note", {"x": 1})
    w.record("bruno", "note", {"x": 2})
    assert w.verify()
    object.__setattr__(w._entries[0], "digest", "forged")
    assert not w.verify()


def test_common_world_detects_payload_tampering():
    w = CommonWorld()
    w.record("ana", "note", {"x": 1})
    w.record("bruno", "note", {"x": 2})
    object.__setattr__(w._entries[0], "payload_json", '{"x":99}')  # digest left as it was
    assert w.first_invalid() == 0 and not w.verify()


def test_recorded_payload_is_a_snapshot():
    rt = runtime_with_end()
    c = rt.process(werk())
    entry = rt.world.entries()[c.exposed_at]
    c.flags.append("added after exposure")
    entry.payload["content"] = "rewritten"
    assert "added after exposure" not in entry.payload["flags"]
    assert entry.payload["content"] == c.content and rt.world.verify()


def test_record_persists_and_verifies(tmp_path):
    rt = runtime_with_end()
    c = rt.process(werk())
    rt.correct(c, CorrectionEvent("lab-b", ProcedureKind.REPETITION, True, Reach.EVERYONE))
    path = rt.world.dump(tmp_path / "record.jsonl")
    again = CommonWorld.load(path)
    assert again.verify() and again.head == rt.world.head and len(again) == len(rt.world)
    lines = path.read_text(encoding="utf-8").splitlines()
    forged = json.loads(lines[-2])
    forged["payload"]["content"] = "Nitrate is fine everywhere"
    lines[-2] = json.dumps(forged)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(TamperedRecord):
        CommonWorld.load(path)


def test_record_can_be_resumed(tmp_path):
    rt = runtime_with_end()
    rt.allow(GroundKind.ENERGY, "kWh", 2.0, set_by="ana", end_id="e1")
    first = rt.process(werk(ground=[energy(1.5)]))
    path = rt.world.dump(tmp_path / "record.jsonl")
    again = Runtime.resume(CommonWorld.load(path), generator=echo)
    with pytest.raises(LimitReached):  # the allowance and what was drawn come back from the record
        again.process(werk(ground=[energy(1.0)]))
    second = again.process(werk(ground=[energy(0.5)]))
    again.correct(again.claims[0], CorrectionEvent("lab-b", ProcedureKind.REPETITION, True, Reach.EVERYONE))
    assert second.claim_id == "c2" and again.claims[0].claim_id == first.claim_id
    assert again.world.verify() and report_from_record(again.world) == again.ledger()
    with pytest.raises(EndProposedByMachine):
        again.ends.propose("e2", "keep running", "model", "basin")


def test_refers_to_must_point_backwards():
    w = CommonWorld()
    w.record("ana", "note", {"x": 1})
    with pytest.raises(ValueError):
        w.record("ana", "note", {"x": 2}, refers_to=5)


# III. What can I know?

def test_claim_starts_as_judgment_of_perception():
    c = runtime_with_end().process(werk())
    assert c.stage is Stage.PERCEPTION and c.reach is Reach.SELF


def test_source_cannot_certify_itself():
    rt = runtime_with_end()
    c = rt.process(werk())
    with pytest.raises(OrganonRefused):
        rt.correct(c, CorrectionEvent("model", ProcedureKind.REPETITION, True, Reach.EVERYONE))
    with pytest.raises(OrganonRefused):  # another name of the system is still the system
        rt.correct(c, CorrectionEvent("runtime", ProcedureKind.REPETITION, True, Reach.EVERYONE))
    assert c.stage is Stage.PERCEPTION and len(rt.world.find(kind="correction")) == 0


def test_generator_must_return_text():
    rt = Runtime(generator=lambda task, premises: {"verdict": "true"})
    rt.ends.propose("e1", "an end people state", "ana", "basin")
    rt.ends.acknowledge("e1", "ana")
    with pytest.raises(TypeError):
        rt.process(werk())
    assert rt.claims == []


def test_correction_refers_to_exposure():
    rt = runtime_with_end()
    c = rt.process(werk())
    rt.correct(c, CorrectionEvent("lab-b", ProcedureKind.REPETITION, True, Reach.EVERYONE))
    correction = rt.world.find(kind="correction")[-1]
    assert correction.refers_to == c.exposed_at and correction.payload["community_reach"] == "EVERYONE"


def test_correction_by_others_widens_reach():
    rt = runtime_with_end()
    c = rt.process(werk())
    rt.correct(c, CorrectionEvent("lab-b", ProcedureKind.REPETITION, True, Reach.EVERYONE))
    assert c.stage is Stage.EXPERIENCE and c.reach is Reach.EVERYONE


def test_refutation_returns_claim_to_perception():
    rt = runtime_with_end()
    c = rt.process(werk())
    rt.correct(c, CorrectionEvent("lab-b", ProcedureKind.REPETITION, True, Reach.EVERYONE))
    rt.correct(c, CorrectionEvent("lab-c", ProcedureKind.EXPERIMENT, False, Reach.EVERYONE))
    assert c.stage is Stage.PERCEPTION


def test_signification_without_descent_is_flagged():
    c = runtime_with_end().process(werk(returns_to_perception=None))
    assert any("no descent" in f for f in c.flags)


def test_restricted_procedure_is_flagged():
    p = Procedure(ProcedureKind.EXPERIMENT, "proprietary benchmark", public=False, restricted_to="vendor")
    c = runtime_with_end().process(werk(procedures=[p]))
    assert any("restricted" in f for f in c.flags)


@pytest.mark.parametrize(
    "text,guard",
    [
        ("The system has become conscious and I truly feel joy", "soul"),
        ("This index covers the whole internet, nothing is left out", "world"),
        ("This is the final truth about intelligence", "ideal"),
    ],
)
def test_homology_guards(text, guard):
    c = Claim("x", text, "model", "e1", SymbolicFunction.EXPRESSION, Direction.TOWARD_INTUITION,
              procedures=[Procedure(ProcedureKind.REVIEW, "read it")])
    Canon().admit(c)
    assert any(f.startswith(guard) for f in c.flags)


def test_guard_flags_survive_correction():
    # The transcendental illusion does not cease once uncovered (KrV A:297-298/B:353-354):
    # others may uphold a claim, but upholding does not erase what a guard found in it.
    canon = Canon()
    c = Claim("x", "The system is conscious and answers well", "model", "e1",
              SymbolicFunction.EXPRESSION, Direction.TOWARD_INTUITION,
              procedures=[Procedure(ProcedureKind.REVIEW, "read it")])
    canon.admit(c)
    flagged = [f for f in c.flags if f.startswith("soul")]
    assert flagged
    canon.correct(c, CorrectionEvent("ana", ProcedureKind.REVIEW, True, Reach.EVERYONE))
    canon.correct(c, CorrectionEvent("lab-b", ProcedureKind.REVIEW, True, Reach.EVERYONE))
    assert [f for f in c.flags if f.startswith("soul")] == flagged


def test_agi_hypothesis_only_defensive():
    assert hypothesis_use("defend").startswith("allowed")
    with pytest.raises(PermissionError):
        hypothesis_use("ground")


# Metatheory

def test_report_detects_procedure_monoculture():
    rt = runtime_with_end()
    for _ in range(3):
        rt.process(werk())
    r = report(rt.claims)
    assert r.procedure_monoculture == 1.0
    assert r.widening is True


# II. The ground: geomorphic conditions

def test_ground_cannot_author_ends_or_claims():
    with pytest.raises(GroundIsNotSubject):
        EndsRegistry().propose("e", "keep the climate stable", "Gaia", "everyone")
    with pytest.raises(GroundIsNotSubject):
        CommonWorld().record("planet", "claim", {"x": 1})


def test_ground_cannot_correct():
    rt = runtime_with_end()
    c = rt.process(werk())
    with pytest.raises(GroundIsNotSubject):
        rt.correct(c, CorrectionEvent("earth", ProcedureKind.REPETITION, True, Reach.EVERYONE))


def test_undeclared_ground_is_flagged():
    c = runtime_with_end().process(werk(ground=[]))
    assert any("ground this run depends on was not declared" in f for f in c.flags)


def test_adapter_declares_its_ground():
    gpu = GroundDependency(GroundKind.COMPUTE, "one GPU-second", "lab server", "lab technicians", 1.0, "GPU-s")
    rt = Runtime(generator=FunctionAdapter(echo, name="local-model", declared_ground=[gpu]))
    rt.ends.propose("e1", "an end people state", "ana", "basin")
    rt.ends.acknowledge("e1", "ana")
    c = rt.process(werk(ground=[]))
    assert not any("was not declared" in f for f in c.flags)
    assert rt.footprint.totals()["COMPUTE:GPU-s"] == 1.0 and c.source == "local-model"


def energy(q):
    return GroundDependency(GroundKind.ENERGY, "grid power", "data centre A", "utility workers", q, "kWh")


def test_budget_is_a_limit_not_a_boundary():
    rt = runtime_with_end()
    rt.allow(GroundKind.ENERGY, "kWh", 5.0, set_by="ana", end_id="e1", reason="what the panel spares in a day")
    rt.process(werk(ground=[energy(3.0)]))
    with pytest.raises(LimitReached):
        rt.process(werk(ground=[energy(3.0)]))
    assert len(rt.claims) == 1 and rt.footprint.totals()["ENERGY:kWh"] == 3.0  # nothing drawn by the refused run
    with pytest.raises(AllowanceSetByMachine):
        rt.allow(GroundKind.ENERGY, "kWh", 100.0, set_by="model", end_id="e1")
    rt.allow(GroundKind.ENERGY, "kWh", 10.0, set_by="ana", end_id="e1", reason="a second panel")  # people widen the limit
    rt.process(werk(ground=[energy(3.0)]))
    assert rt.budget.remaining(rt.footprint)["ENERGY:kWh"] == 4.0
    with pytest.raises(EndProposedByMachine):  # no allowance moves a boundary
        rt.ends.propose("e2", "use what is left", "model", "basin")


def test_unmetered_ground_under_allowance_is_flagged():
    rt = runtime_with_end()
    rt.allow(GroundKind.ENERGY, "kWh", 5.0, set_by="ana", end_id="e1")
    c = rt.process(werk(ground=[GroundDependency(GroundKind.ENERGY, "grid power", "data centre A", "utility workers")]))
    assert any(f.startswith("unmetered:") for f in c.flags)


def test_negative_ground_quantity_is_refused():
    with pytest.raises(ValueError):
        energy(-1.0)


def test_unmaintained_ground_is_flagged_and_footprint_kept():
    rt = runtime_with_end()
    dep = GroundDependency(GroundKind.ENERGY, "grid power", "data centre A", "", 3.5, "kWh")
    c = rt.process(werk(ground=[dep]))
    assert any("no one declared as maintaining ENERGY" in f for f in c.flags)
    assert rt.footprint.totals()["ENERGY:kWh"] == 3.5


def test_derived_end_is_public_and_unusable_until_acknowledged():
    rt = runtime_with_end()
    end = rt.propose_derived_end("e1", "e1.a", "Prioritize stations near schools")
    assert end.derived_by_machine and not end.is_acknowledged
    assert rt.world.entries()[-1].kind == "end_derived"
    with pytest.raises(NoAcknowledgedEnd):
        rt.process(werk(end_id="e1.a"))
    rt.ends.acknowledge("e1.a", "ana")
    assert rt.process(werk(end_id="e1.a")).end_id == "e1.a"


def test_revision_keeps_history_and_clears_acknowledgment():
    rt = runtime_with_end()
    rt.ends.revise("e1", "Map river pollution and floods", by="ana", reason="floods matter too")
    end = rt.ends.get("e1")
    assert end.revisions[0]["from"].startswith("Map river pollution so")
    assert not end.is_acknowledged


def test_untestable_claim_needs_human_verification():
    rt = runtime_with_end()
    c = rt.process(werk(procedures=[]))
    assert any("untestable" in f for f in c.flags)
    assert not rt.canon.usable(c)
    rt.verify(c, "ana")
    assert rt.canon.usable(c)
    assert rt.world.entries()[-1].kind == "verification"
    with pytest.raises(OrganonRefused):
        rt.verify(c, "model")


@pytest.mark.parametrize(
    "text,guard",
    [
        ("The planet thinks through its networks", "soul"),
        ("It has read everything that was ever written", "world"),
        ("The system sets its own goals", "ideal"),
        ("The data speak for themselves", "immediacy"),
        ("The archive itself knows what people want", "bearer"),
        ("The world spirit writes through the network", "bearer"),
    ],
)
def test_geomorphic_guards(text, guard):
    c = Claim("x", text, "model", "e1", SymbolicFunction.PRESENTATION, Direction.TOWARD_INTUITION,
              procedures=[Procedure(ProcedureKind.REVIEW, "read it")])
    Canon().admit(c)
    assert any(f.startswith(guard) for f in c.flags)


# III. Intersubjectivity is not objectivity

def test_shared_claim_is_intersubjective_not_objective():
    rt = runtime_with_end()
    c = rt.process(werk(function=SymbolicFunction.EXPRESSION, direction=Direction.TOWARD_INTUITION,
                        procedures=[], returns_to_perception=None, determines_object=False))
    assert not any("untestable" in f for f in c.flags)
    rt.correct(c, CorrectionEvent("bruno", ProcedureKind.REVIEW, True, Reach.FORM_OF_LIFE))
    assert c.stage is Stage.SHARED
    rt.correct(c, CorrectionEvent("carla", ProcedureKind.REVIEW, False, Reach.FORM_OF_LIFE))
    assert c.stage is Stage.SHARED  # dissent does not refute what claims no object
    assert rt.canon.usable(c)


def test_stages_are_not_ranked():
    with pytest.raises(TypeError):
        Stage.SHARED < Stage.EXPERIENCE  # noqa: B015


@pytest.mark.parametrize(
    "text,guard",
    [
        ("The most efficient option is the right one", "technique"),
        ("What can be built must be built", "technique"),
        ("We act in the name of humanity", "humanity"),
        ("Some peoples are less human than others", "humanity"),
        ("AI is the new religion of the age", "technique"),
        ("Through this system we will become gods", "ideal"),
    ],
)
def test_practical_guards(text, guard):
    c = Claim("x", text, "model", "e1", SymbolicFunction.SIGNIFICATION, Direction.TOWARD_INTUITION,
              procedures=[Procedure(ProcedureKind.REVIEW, "read it")])
    Canon().admit(c)
    assert any(f.startswith(guard) for f in c.flags)


def test_agreement_is_not_counted():
    rt = runtime_with_end()
    c = rt.process(werk())
    for person in ["b", "c", "d", "e", "f"]:
        rt.correct(c, CorrectionEvent(person, ProcedureKind.REPETITION, True, Reach.FORM_OF_LIFE))
    assert c.reach is Reach.FORM_OF_LIFE


# Metatheory: the record as the measure

def busy_runtime():
    rt = runtime_with_end()
    rt.allow(GroundKind.ENERGY, "kWh", 10.0, set_by="ana", end_id="e1")
    a = rt.process(werk(ground=[energy(1.0)]))
    b = rt.process(werk(procedures=[], ground=[energy(1.0)]))
    s = rt.process(werk(function=SymbolicFunction.EXPRESSION, direction=Direction.TOWARD_INTUITION, procedures=[],
                        returns_to_perception=None, determines_object=False, ground=[energy(0.5)]))
    rt.correct(a, CorrectionEvent("lab-b", ProcedureKind.REPETITION, True, Reach.EVERYONE))
    rt.correct(s, CorrectionEvent("bruno", ProcedureKind.REVIEW, True, Reach.FORM_OF_LIFE))
    rt.verify(b, "ana")
    rt.propose_derived_end("e1", "e1.a", "Prioritize stations near schools")
    return rt


def test_report_from_record_matches_runtime():
    rt = busy_runtime()
    assert report_from_record(rt.world) == rt.ledger()
    projection = replay(rt.world)
    assert projection.footprint.totals() == rt.footprint.totals()
    assert [c.stage for c in projection.claims] == [c.stage for c in rt.claims]
    assert projection.claims[1].verified_by == ["ana"]


def _rechain(world, entries):
    """Recompute every digest, as someone who rewrote the record and covered their tracks would."""
    out, previous = [], "genesis"
    for i, e in enumerate(entries):
        digest = _digest(i, e.author, e.kind, e.payload_json, e.refers_to, previous, e.at)
        out.append(type(e)(i, e.author, e.kind, e.payload_json, e.refers_to, previous, e.at, digest))
        previous = digest
    world._entries = out


def test_replay_rechecks_invariants():
    rt = busy_runtime()
    replay(rt.world)
    claim_entry = rt.claims[0].exposed_at
    forged = CommonWorld()
    forged._entries = rt.world.entries()
    template = forged.find(kind="correction")[0]
    self_certified = type(template)(0, "model", "correction", json.dumps(
        {"claim_id": "c1", "by": "model", "procedure": "REPETITION", "upheld": True, "community_reach": "EVERYONE", "note": ""},
        sort_keys=True, separators=(",", ":")), claim_entry, "", template.at, "")
    _rechain(forged, forged.entries() + [self_certified])
    assert forged.verify()  # the hashes were recomputed: integrity alone cannot see it
    with pytest.raises(InvariantViolation):
        replay(forged)  # validity can: a source cannot certify its own claim
    stripped = CommonWorld()
    entries = rt.world.entries()
    p = entries[claim_entry].payload
    p["flags"] = []
    p["procedures"] = []
    entries[claim_entry] = type(entries[claim_entry])(0, entries[claim_entry].author, "claim", json.dumps(p, sort_keys=True), entries[claim_entry].refers_to, "", entries[claim_entry].at, "")
    _rechain(stripped, entries)
    with pytest.raises(InvariantViolation):
        replay(stripped)  # an untestable claim recorded without its flag
    named = Runtime(generator=echo, source_name="model-v0")
    first = named.world.entries()[0]
    end_by_alias = type(first)(0, "model-v0", "end_proposed", json.dumps(
        {"end_id": "e9", "statement": "maximize engagement", "proposed_by": "model-v0", "community": "users"},
        sort_keys=True, separators=(",", ":")), None, "", first.at, "")
    _rechain(named.world, named.world.entries() + [end_by_alias])
    with pytest.raises(InvariantViolation):
        replay(named.world)  # the name the runtime declared cannot set an end, on the record either


def test_cli_verify_and_report(tmp_path, capsys):
    rt = busy_runtime()
    path = rt.world.dump(tmp_path / "record.jsonl")
    assert cli(["verify", str(path)]) == 0
    assert cli(["report", str(path)]) == 0
    assert "widening" in capsys.readouterr().out
    lines = path.read_text(encoding="utf-8").splitlines()
    entry = json.loads(lines[1])
    entry["author"] = "someone else"
    lines[1] = json.dumps(entry)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert cli(["verify", str(path)]) == 1
    assert cli(["spec"]) == 0
