"""The agent and the models: general as if, a Werk under the same invariants."""

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from gaia_techne import Runtime
from gaia_techne.agent import Agent, Task, parse_plan
from gaia_techne.agent.demo import run as scenario
from gaia_techne.canon import CorrectionEvent, Procedure, ProcedureKind, Reach
from gaia_techne.cli import main as cli
from gaia_techne.ethos import EndProposedByMachine, NoAcknowledgedEnd, Premise
from gaia_techne.gaia import Archive, ArchiveOutsideRoot, recall
from gaia_techne.koinos import Direction, GroundKind, SymbolicFunction
from gaia_techne.metatheory import replay
from gaia_techne.models import AnthropicAdapter, ModelUnavailable, OpenAICompatibleAdapter, ScriptedAdapter


def plan(*steps):
    return json.dumps(list(steps))


def setup(answers, calls=None, archive=None):
    model = ScriptedAdapter(answers=list(answers))
    rt = Runtime(generator=model, source_name="scripted-model")
    rt.ends.propose("e1", "Let anyone in the basin check its water", "ana", "basin")
    rt.ends.acknowledge("e1", "ana")
    if calls is not None:
        rt.allow(GroundKind.COMPUTE, "calls", calls, set_by="ana", end_id="e1")
    return rt, Agent(rt, archive=archive)


def task(**kw):
    base = dict(
        goal="How many samples a year at twice a month for 4 classes?",
        end_id="e1",
        requested_by="ana",
        function=SymbolicFunction.SIGNIFICATION,
        direction=Direction.AWAY_FROM_LIFE,
        procedures=[Procedure(ProcedureKind.REPETITION, "count the log")],
        returns_to_perception="the sample log",
    )
    base.update(kw)
    return Task(**base)


def test_agent_needs_an_acknowledged_end():
    rt = Runtime(generator=ScriptedAdapter(answers=["x"]), source_name="scripted-model")
    rt.ends.propose("e1", "an end", "ana", "basin")
    with pytest.raises(NoAcknowledgedEnd):
        Agent(rt).pursue(task())


def test_agent_plan_and_steps_are_claims_in_the_record():
    rt, agent = setup([plan({"step": "tool", "tool": "arithmetic", "input": "4*2*12"},
                            {"step": "claim", "task": "state the total"}), "96 a year", "96 samples a year"])
    run = agent.pursue(task())
    assert [c.claim_id for c in run.claims] == ["c1", "c2", "c3"] and run.answer.content == "96 samples a year"
    assert any("4*2*12 = 96" in g for g in run.claims[1].grounds)
    assert all(c.exposed_at is not None for c in run.claims)
    assert [c.claim_id for c in replay(rt.world).claims] == ["c1", "c2", "c3"]


def test_agent_cannot_certify_its_answer():
    rt, agent = setup([plan(), "an answer"])
    run = agent.pursue(task())
    assert not rt.canon.usable(run.answer)
    assert any("not usable yet" in q for q in run.open_questions)
    for name in ("scripted-model", "runtime", "model"):
        with pytest.raises(Exception):
            rt.correct(run.answer, CorrectionEvent(name, ProcedureKind.REPETITION, True, Reach.EVERYONE))
    rt.correct(run.answer, CorrectionEvent("bruno", ProcedureKind.REPETITION, True, Reach.FORM_OF_LIFE))
    assert rt.canon.usable(run.answer)


def test_agent_uses_only_the_tools_the_person_allowed():
    rt, agent = setup([plan({"step": "tool", "tool": "arithmetic", "input": "1+1"}), "two"])
    run = agent.pursue(task(tools=["memory"]))
    assert "not among the tools allowed" in run.steps[0]["detail"]
    assert not any("1+1" in g for g in run.answer.grounds)


def test_agent_derived_end_waits_for_people():
    rt, agent = setup([plan({"step": "end", "statement": "publish every sample"}), "an answer"])
    run = agent.pursue(task())
    assert run.waiting and not rt.ends.get("e1.d1").is_acknowledged
    with pytest.raises(EndProposedByMachine):
        rt.ends.acknowledge("e1.d1", "scripted-model")


def test_agent_stops_at_the_allowance_of_the_ground():
    rt, agent = setup([plan({"step": "claim", "task": "a"}, {"step": "claim", "task": "b"}), "x", "y", "z"], calls=2)
    run = agent.pursue(task())
    assert run.answer is None and run.stopped and "allowance" in run.stopped
    assert rt.footprint.totals()["COMPUTE:calls"] == 2.0


def test_unreadable_plan_still_answers():
    assert parse_plan("I would rather just answer.", 5) == []
    rt, agent = setup(["I would rather just answer.", "the answer"])
    run = agent.pursue(task())
    assert run.steps == [] and run.answer.content == "the answer"


def test_memory_recalls_only_what_the_record_allows():
    rt, agent = setup([plan(), "Nitrate at station 4 exceeded the limit", plan(), "Nitrate at station 4 is fine"])
    first = agent.pursue(task(goal="nitrate station 4"))
    rt.correct(first.answer, CorrectionEvent("lab", ProcedureKind.REPETITION, True, Reach.EVERYONE))
    found = recall(rt.world, "nitrate station")
    assert found and "holds for everyone" in found[0].source and "reach EVERYONE" in found[0].source
    rt.correct(first.answer, CorrectionEvent("lab-2", ProcedureKind.REPETITION, False, Reach.EVERYONE))
    assert all(first.answer.content != p.text for p in recall(rt.world, "nitrate station"))


def test_archive_keeps_provenance_and_its_boundary(tmp_path):
    (tmp_path / "plan.md").write_text("Stations 2, 4 and 7 are sampled monthly.", encoding="utf-8")
    archive = Archive(str(tmp_path))
    docs, seen = archive.search("stations sampled")
    assert seen == 1 and docs[0].source == "archive: plan.md"
    with pytest.raises(ArchiveOutsideRoot):
        archive.read("../outside.txt")
    with pytest.raises(ArchiveOutsideRoot):
        archive.fetch("https://example.org")  # no public address was put at the system's disposal


def _stub(response):
    class Handler(BaseHTTPRequestHandler):
        seen = []

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["content-length"])))
            Handler.seen.append((dict(self.headers), body))
            data = json.dumps(response).encode()
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *a):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, Handler


def test_models_speak_http_and_declare_their_ground():
    server, h = _stub({"choices": [{"message": {"content": "a claim from a local model"}}]})
    try:
        m = OpenAICompatibleAdapter(base_url=f"http://127.0.0.1:{server.server_port}/v1", model="m")
        assert m.generate("t", [Premise("p", "s")]) == "a claim from a local model"
        assert h.seen[0][1]["messages"][0]["role"] == "system" and "[source: s]" in h.seen[0][1]["messages"][1]["content"]
        dep = m.ground()[0]
        assert dep.kind is GroundKind.COMPUTE and dep.unit == "calls" and dep.quantity == 1
    finally:
        server.shutdown()
    server, h = _stub({"content": [{"type": "text", "text": "a claim from the Messages API"}]})
    try:
        a = AnthropicAdapter(api_key="k", url=f"http://127.0.0.1:{server.server_port}/v1/messages")
        assert a.generate("t", []) == "a claim from the Messages API"
        assert {k.lower(): v for k, v in h.seen[0][0].items()}["x-api-key"] == "k"
    finally:
        server.shutdown()
    with pytest.raises(ModelUnavailable):
        OpenAICompatibleAdapter(base_url="http://127.0.0.1:9/v1", timeout=1).generate("t", [])


def test_agent_scenario_and_cli(tmp_path, capsys):
    result = scenario(out=lambda *a: None)
    assert result.answer is not None and result.waiting
    ledger = tmp_path / "agent.jsonl"
    assert cli(["agent", "--ledger", str(ledger)]) == 0
    assert cli(["verify", str(ledger)]) == 0
    assert cli(["agent", "a goal"]) == 2  # no end, no person: the agent does not start
