import pytest

from gaia_techne import Runtime, Werk, __version__
from gaia_techne.canon import Canon, Claim, CorrectionEvent, OrganonRefused, Procedure, ProcedureKind, Reach, Stage
from gaia_techne.canon.guards import hypothesis_use
from gaia_techne.ethos import EndProposedByMachine, EndsRegistry, NoAcknowledgedEnd, Premise, SkillExecutor, TechnicalRule
from gaia_techne.koinos import (
    CommonWorld,
    Direction,
    GroundDependency,
    GroundIsNotSubject,
    GroundKind,
    RankingRefused,
    SymbolicFunction,
)
from gaia_techne.metatheory import report


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
    assert __version__ == "2.0.0"


# I. What should I do?

def test_runtime_cannot_set_ends():
    with pytest.raises(EndProposedByMachine):
        EndsRegistry().propose("e", "maximize everything", "runtime", "none")


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
        SymbolicFunction.SIGNIFICATION > SymbolicFunction.EXPRESSION


def test_common_world_is_tamper_evident():
    w = CommonWorld()
    w.record("ana", "note", {"x": 1})
    w.record("bruno", "note", {"x": 2})
    assert w.verify()
    object.__setattr__(w._entries[0], "digest", "forged")
    assert not w.verify()


# III. What can I know?

def test_claim_starts_as_judgment_of_perception():
    c = runtime_with_end().process(werk())
    assert c.stage is Stage.PERCEPTION and c.reach is Reach.SELF


def test_source_cannot_certify_itself():
    rt = runtime_with_end()
    c = rt.process(werk())
    with pytest.raises(OrganonRefused):
        rt.correct(c, CorrectionEvent("model", ProcedureKind.REPETITION, True, Reach.EVERYONE))


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
    assert rt.world.entries()[-1].kind == "derived_end"
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
    rt.canon.verify(c, "ana")
    assert rt.canon.usable(c)
    with pytest.raises(OrganonRefused):
        rt.canon.verify(c, "model")


@pytest.mark.parametrize(
    "text,guard",
    [
        ("The planet thinks through its networks", "soul"),
        ("It has read everything that was ever written", "world"),
        ("The system sets its own goals", "ideal"),
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
        Stage.SHARED < Stage.EXPERIENCE


@pytest.mark.parametrize(
    "text,guard",
    [
        ("The most efficient option is the right one", "technique"),
        ("What can be built must be built", "technique"),
        ("We act in the name of humanity", "humanity"),
        ("Some peoples are less human than others", "humanity"),
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
