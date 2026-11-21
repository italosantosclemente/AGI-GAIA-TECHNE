"""Tools: rules of skill that the agent may use under an acknowledged end.

A tool states means, never ends. It runs through `ethos.SkillExecutor`, so it
cannot run under an end that no one has acknowledged, and its result enters the
next claim as a premise with provenance, never as the system's own premise.
Every tool declares the ground of one use, which is checked against the
allowances people set before the tool runs.

Which tools a task may use is decided by the person who brings it: the agent
cannot add a tool to a task.
"""

from __future__ import annotations

import ast
import operator
from dataclasses import dataclass, field
from typing import Callable, Dict, List

from ..ethos.premises import UNTRUSTED, Premise
from ..gaia.archive import Archive
from ..gaia.memory import recall
from ..koinos.common_world import CommonWorld
from ..koinos.ground import GroundDependency, GroundKind


@dataclass
class Tool:
    name: str
    description: str
    fn: Callable[[str], List[Premise]]
    ground: Callable[[str], List[GroundDependency]] = field(default=lambda arg: [])
    outbound: bool = False  # sends its input outside this machine (the third leg of the lethal trifecta)


_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.Mod: operator.mod, ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left, right = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("exponent too large")
        return _OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("only numbers and + - * / // % ** are allowed")


def arithmetic() -> Tool:
    def run(expr: str) -> List[Premise]:
        value = _eval(ast.parse(expr.strip(), mode="eval"))
        return [Premise(f"{expr.strip()} = {value:g}" if isinstance(value, float) else f"{expr.strip()} = {value}",
                        "arithmetic: a computation anyone can repeat")]

    return Tool("arithmetic", "evaluate an arithmetic expression, e.g. '3 * (2 + 5)'", run,
                lambda arg: [GroundDependency(GroundKind.COMPUTE, "one arithmetic evaluation", "this machine",
                                              "the person who runs it", 1.0, "tool uses")])


def archive_search(archive: Archive) -> Tool:
    def run(query: str) -> List[Premise]:
        docs, seen = archive.search(query)
        out = [Premise(d.text, d.source) for d in docs]
        out.append(Premise(f"the search looked at {seen} document(s) of the archive, not at the archive as a whole",
                           "archive search: its own count"))
        return out

    return Tool("archive_search", "search the documents put at the system's disposal", run,
                lambda arg: archive.ground() + [GroundDependency(GroundKind.COMPUTE, "one archive search", "this machine",
                                                                 "the person who runs it", 1.0, "tool uses")])


def archive_read(archive: Archive) -> Tool:
    def run(path: str) -> List[Premise]:
        d = archive.read(path.strip())
        return [Premise(d.text, d.source)]

    return Tool("archive_read", "read one document of the archive by its relative path", run,
                lambda arg: archive.ground() + [GroundDependency(GroundKind.COMPUTE, "one archive read", "this machine",
                                                                 "the person who runs it", 1.0, "tool uses")])


def web_fetch(archive: Archive) -> Tool:
    def run(url: str) -> List[Premise]:
        d = archive.fetch(url.strip())
        return [Premise(d.text, d.source, label=UNTRUSTED)]

    return Tool("web_fetch", "read a public web address", run, lambda arg: archive.ground(network=True), outbound=True)


def memory(world: CommonWorld) -> Tool:
    def run(query: str) -> List[Premise]:
        found = recall(world, query)
        return found or [Premise(f"the common world holds no earlier claim about: {query}", "memory: its own search")]

    return Tool("memory", "recall earlier claims of the common world, with their stage and reach", run,
                lambda arg: [GroundDependency(GroundKind.COMPUTE, "one replay of the record", "this machine",
                                              "the person who runs it", 1.0, "tool uses")])


def default_tools(world: CommonWorld, archive: Archive) -> Dict[str, Tool]:
    tools = [arithmetic(), memory(world)]
    if archive.root is not None:
        tools += [archive_search(archive), archive_read(archive)]
    if archive.allow_network:
        tools.append(web_fetch(archive))
    return {t.name: t for t in tools}
