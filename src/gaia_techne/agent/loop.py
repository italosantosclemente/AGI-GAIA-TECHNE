"""The agent: general as if, a Werk that pursues tasks of any domain under ends people set.

The thesis asks what is to be done with "a system that already drives, writes,
judges and fights in the public world without being a 'subject'", and answers
that it falls under the criterion of correction: the processes by which it forms
and revises the ends it pursues must be public and available to "any of us",
and its results must remain subject to human verification wherever they cannot
yet be tested (thesis, 10.4; Final Conclusion). This module builds such a system
in the only form the architecture allows.

Its generality is a generality of tasks, not of a subject. The same loop takes
a task from any domain, plans it, uses tools, recalls the common world and
answers; what makes it general is that no domain is fixed in advance, and what
keeps it a Werk is that every one of its acts passes through the layers:

- the task is brought by a person, under an end that people stated and
  acknowledged; the agent cannot set, acknowledge or revise an end;
- the plan the model proposes is itself a claim, exposed in the common world
  and testable by review of those who brought the task;
- every step that asks the model for text is a full run of the syntax, so its
  output is a judgment of perception with its guards, descent and flags;
- tools are rules of skill, run only under the acknowledged end, chosen by the
  person who brought the task, and checked against the allowances of the ground
  before they run;
- where the plan needs an end that the task does not cover, the agent records a
  derived end and leaves that branch to people: it waits;
- the answer is a claim like every other. The agent never corrects, certifies or
  verifies it, and it reports what a person still has to judge before using it.

- what comes back from tools and from the memory of the record is labelled
  untrusted: it is data for the judgments of the steps and the answer, never
  an instruction for the plan. The plan is made before any tool runs and sees
  only what the person brought, so no page, document or earlier claim can
  choose a step; and an outbound tool is refused an address that only
  untrusted text supplied (the "lethal trifecta" of private data, untrusted
  content and a way out; Willison, 2025; Debenedetti et al., 2025, CaMeL).
The motto holds: Werk, never Wille. Calling the loop "general as if" names a
use of the hypothesis for defense, not a ground: it shows what such a system can
do inside the boundaries, against those who say no general system could work
within them, without ascribing to it a soul or a will. The reading is this
project's.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, replace
from typing import Dict, List, Optional

from ..canon.claims import Claim, Procedure, ProcedureKind
from ..ethos.imperatives import NoAcknowledgedEnd, SkillExecutor, TechnicalRule
from ..ethos.premises import TRUSTED, UNTRUSTED, Premise
from ..gaia.archive import Archive, ArchiveOutsideRoot
from ..gaia.memory import recall
from ..koinos.ground import GroundDependency, LimitReached
from ..koinos.prism import Direction, SymbolicFunction
from ..models import ModelUnavailable
from ..pipeline import Runtime, Werk
from .tools import Tool, default_tools

PLAN_INSTRUCTIONS = """Propose a plan for the task as a JSON array, and nothing else. Each element is one of:
  {{"step": "tool", "tool": NAME, "input": TEXT}}  use one of the tools listed below
  {{"step": "claim", "task": TEXT}}                ask for one intermediate result in words
  {{"step": "end", "statement": TEXT}}             a further end this plan would need, which people must acknowledge
Use at most {max_steps} steps. Tools available for this task: {tools}.
Task: {goal}"""


@dataclass
class Task:
    """What a person brings: a goal under an acknowledged end, with the tools they allow."""

    goal: str
    end_id: str
    requested_by: str
    function: SymbolicFunction = SymbolicFunction.PRESENTATION
    direction: Direction = Direction.TOWARD_INTUITION
    procedures: List[Procedure] = field(default_factory=list)
    returns_to_perception: Optional[str] = None
    premises: List[Premise] = field(default_factory=list)
    ground: List[GroundDependency] = field(default_factory=list)
    tools: Optional[List[str]] = None  # None: every tool the agent has; [] : none
    max_steps: int = 6
    use_memory: bool = True
    determines_object: bool = True


@dataclass
class AgentRun:
    task: Task
    plan: Optional[Claim] = None
    steps: List[Dict[str, str]] = field(default_factory=list)
    claims: List[Claim] = field(default_factory=list)
    answer: Optional[Claim] = None
    waiting: List[str] = field(default_factory=list)  # derived ends that wait for people
    stopped: Optional[str] = None
    open_questions: List[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [f"goal: {self.task.goal}", f"end: {self.task.end_id} (brought by {self.task.requested_by})"]
        if self.plan is not None:
            lines.append(f"plan: claim {self.plan.claim_id}, {len(self.steps)} step(s)")
        for s in self.steps:
            lines.append(f"  - {s['step']}: {s.get('detail', '')}")
        if self.waiting:
            lines.append("waiting for people: " + "; ".join(self.waiting))
        if self.stopped:
            lines.append(f"stopped: {self.stopped}")
        if self.answer is not None:
            a = self.answer
            lines += [f"answer ({a.claim_id}, {a.stage.value}, reach {a.reach.name}):", a.content]
        if self.open_questions:
            lines.append("before using it, a person still has to judge:")
            lines += [f"  - {q}" for q in self.open_questions]
        return "\n".join(lines)


def parse_plan(text: str, max_steps: int) -> List[Dict[str, str]]:
    """The JSON array in the model's text; a plan that cannot be read becomes one step that asks for the answer."""
    m = re.search(r"\[.*\]", text, flags=re.S)
    steps: List[Dict[str, str]] = []
    if m:
        try:
            raw = json.loads(m.group(0))
        except json.JSONDecodeError:
            raw = []
        for s in raw if isinstance(raw, list) else []:
            if isinstance(s, dict) and s.get("step") in {"tool", "claim", "end"}:
                steps.append({k: str(v) for k, v in s.items()})
    return steps[:max_steps]


class Agent:
    """Pursues tasks under acknowledged ends, through a `Runtime`. It holds no pen in the register of ends."""

    def __init__(self, runtime: Runtime, archive: Optional[Archive] = None, tools: Optional[Dict[str, Tool]] = None) -> None:
        self.runtime = runtime
        self.archive = archive or Archive()
        self.tools = tools if tools is not None else default_tools(runtime.world, self.archive)
        self.executor = SkillExecutor(runtime.ends)
        self._derived = 0

    # -- helpers ---------------------------------------------------------------

    def _werk(self, task: Task, text: str, premises: List[Premise], ground: List[GroundDependency], **kw) -> Werk:
        base = dict(
            task=text,
            end_id=task.end_id,
            requested_by=task.requested_by,
            function=task.function,
            direction=task.direction,
            premises=premises,
            procedures=list(task.procedures),
            returns_to_perception=task.returns_to_perception,
            ground=list(task.ground) + ground,
            determines_object=task.determines_object,
        )
        base.update(kw)
        return Werk(**base)

    def _allowed(self, task: Task) -> Dict[str, Tool]:
        if task.tools is None:
            return dict(self.tools)
        return {n: t for n, t in self.tools.items() if n in task.tools}

    @staticmethod
    def _exfiltration(task: Task, tool: Tool, arg: str, gathered: List[Premise]) -> Optional[str]:
        """K6: an outbound tool may not be sent to what only untrusted text supplied."""
        if not tool.outbound or not arg.strip():
            return None
        needle = arg.strip()
        trusted = [task.goal] + [p.text for p in gathered if p.label == TRUSTED]
        if any(needle in t for t in trusted):
            return None
        if any(needle in p.text for p in gathered if p.label != TRUSTED):
            return f"{tool.name}({needle}): the address appears only in untrusted text; refused"
        return None

    def _use_tool(self, task: Task, tool: Tool, arg: str, pending: List[GroundDependency]) -> List[Premise]:
        deps = tool.ground(arg)
        self.runtime.budget.check(self.runtime.footprint, pending + deps)  # LimitReached before the tool runs
        rule = TechnicalRule(tool.name, task.end_id, tool.description, lambda: tool.fn(arg))
        out = self.executor.run(rule)
        pending.extend(deps)
        return [p if p.label != TRUSTED else replace(p, label=UNTRUSTED) for p in out["result"]]

    @staticmethod
    def _as_premise(c: Claim) -> Premise:
        return Premise(c.content, f"claim {c.claim_id} of this run by {c.source}: {c.stage.value}",
                       ref=c.claim_id, label=UNTRUSTED)

    # -- the loop --------------------------------------------------------------

    def pursue(self, task: Task) -> AgentRun:
        run = AgentRun(task)
        end = self.runtime.ends.find(task.end_id)
        if end is None or not end.is_acknowledged:
            raise NoAcknowledgedEnd(f"{task.end_id!r} has not been acknowledged by anyone: the agent does not start")
        tools = self._allowed(task)
        premises: List[Premise] = list(task.premises)
        pending: List[GroundDependency] = []
        try:
            recalled = recall(self.runtime.world, task.goal) if task.use_memory else []

            # The plan is a claim, testable by review of those who brought the task. It sees only
            # what the person brought (K6): recalled claims are data for the steps, not instructions.
            planning = [p for p in premises if p.label == TRUSTED]
            listing = ", ".join(f"{n} ({t.description})" for n, t in tools.items()) or "none"
            plan = self.runtime.process(self._werk(
                task, PLAN_INSTRUCTIONS.format(max_steps=task.max_steps, tools=listing, goal=task.goal), planning, [],
                function=SymbolicFunction.PRESENTATION, direction=Direction.TOWARD_INTUITION, determines_object=True,
                procedures=[Procedure(ProcedureKind.REVIEW, f"review of the plan by {task.requested_by} and those the end concerns")],
                returns_to_perception="the steps as carried out, in the common world",
            ))
            run.plan = plan
            run.claims.append(plan)
            steps = parse_plan(plan.content, task.max_steps)

            gathered: List[Premise] = list(premises) + recalled
            for s in steps:
                kind = s["step"]
                if kind == "tool":
                    name, arg = s.get("tool", ""), s.get("input", "")
                    if name not in tools:
                        run.steps.append({"step": "tool", "detail": f"{name}: not among the tools allowed for this task"})
                        run.open_questions.append(f"the plan asked for a tool not allowed: {name}")
                        continue
                    refused = self._exfiltration(task, tools[name], arg, gathered)
                    if refused:
                        run.steps.append({"step": "tool", "detail": refused})
                        run.open_questions.append(f"labels: {refused}")
                        continue
                    try:
                        found = self._use_tool(task, tools[name], arg, pending)
                    except (ValueError, ArchiveOutsideRoot, OSError, SyntaxError) as exc:
                        run.steps.append({"step": "tool", "detail": f"{name}({arg}): failed, {exc}"})
                        continue
                    gathered += found
                    run.steps.append({"step": "tool", "detail": f"{name}({arg}): {len(found)} premise(s) with provenance"})
                elif kind == "claim":
                    c = self.runtime.process(self._werk(task, s.get("task", task.goal), gathered, pending))
                    pending = []
                    run.claims.append(c)
                    gathered.append(self._as_premise(c))
                    run.steps.append({"step": "claim", "detail": f"{c.claim_id}: {c.stage.value}; {len(c.flags)} flag(s)"})
                elif kind == "end":
                    self._derived += 1
                    end_id = f"{task.end_id}.d{self._derived}"
                    while self.runtime.ends.find(end_id) is not None:
                        self._derived += 1
                        end_id = f"{task.end_id}.d{self._derived}"
                    self.runtime.propose_derived_end(task.end_id, end_id, s.get("statement", ""))
                    run.waiting.append(f"{end_id}: {s.get('statement', '')}")
                    run.steps.append({"step": "end", "detail": f"{end_id} recorded; unusable until a person acknowledges it"})

            # The answer: one more run, from everything gathered, with the ground the tools drew on.
            answer = self.runtime.process(self._werk(task, task.goal, gathered, pending))
            pending = []
            run.answer = answer
            run.claims.append(answer)
        except LimitReached as exc:
            run.stopped = f"an allowance of the ground would be exceeded: {exc}"
        except ModelUnavailable as exc:
            run.stopped = f"the model could not be reached: {exc}"
        if run.answer is not None:
            run.open_questions += self.runtime.canon.open_questions(run.answer)
            if not self.runtime.canon.usable(run.answer):
                run.open_questions.append("not usable yet: it needs correction by others or verification by a person")
        if run.waiting:
            run.open_questions.append("derived ends wait for acknowledgment: " + ", ".join(w.split(":")[0] for w in run.waiting))
        return run
