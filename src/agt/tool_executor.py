from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Callable, Dict, List

from .types import PlanStep, StepResult


class ToolExecutor:
    """
    Safe allowlisted tool executor.
    """

    SAFE_EXTENSIONS = {".txt", ".md", ".json", ".yaml", ".yml", ".log"}
    SAFE_ROOTS = {"memory", "outputs"}

    def __init__(self) -> None:
        self.tools: Dict[str, Callable[..., Any]] = {
            "draft_text": self._draft_text,
            "echo": self._echo,
            "read_text_file": self._read_text_file,
            "write_text_file_sandboxed": self._write_text_file_sandboxed,
            "audit_file": self._audit_file,
            "summarize_file": self._summarize_file,
            "run_pytest_command_dry": self._run_pytest_command_dry,
            "repo_path_inspect": self._repo_path_inspect,
        }

    def execute(self, step: PlanStep) -> StepResult:
        if step.action == "audit_blocked_step":
            return StepResult(
                step_id=step.id,
                ok=False,
                output=None,
                error=f"Step blocked by CTK/CHK audit. Statuses: {', '.join(step.audit_statuses)}",
            )

        if not step.tool_name:
            return StepResult(
                step_id=step.id,
                ok=True,
                output=f"No tool needed for {step.action}.",
            )

        tool = self.tools.get(step.tool_name)

        if tool is None:
            return StepResult(
                step_id=step.id,
                ok=False,
                output=None,
                error=f"Tool not allowed: {step.tool_name}",
            )

        try:
            return StepResult(
                step_id=step.id,
                ok=True,
                output=tool(**step.tool_args),
            )

        except Exception as exc:
            return StepResult(
                step_id=step.id,
                ok=False,
                output=None,
                error=str(exc),
            )

    def _draft_text(self, prompt: str) -> str:
        return (
            "Draft produced as Werk, not Wille.\n\n"
            f"Task: {prompt}\n\n"
            "1. Identify the problem.\n"
            "2. State the regulative frame.\n"
            "3. Propose an operational next step.\n"
            "4. Preserve human review when normative judgment is involved."
        )

    def _echo(self, text: str) -> str:
        return text

    def _read_text_file(self, filepath: str) -> str:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        return path.read_text(encoding="utf-8")

    def _write_text_file_sandboxed(self, filepath: str, content: str) -> Dict[str, Any]:
        target = Path(filepath)
        # Normalize and check sandbox
        try:
            full_path = target.resolve()
            cwd = Path.cwd().resolve()
            rel_path = full_path.relative_to(cwd)

            root_dir = rel_path.parts[0]
            if root_dir not in self.SAFE_ROOTS:
                raise PermissionError(f"Access denied: {filepath} is outside safe roots {self.SAFE_ROOTS}")

            if target.suffix not in self.SAFE_EXTENSIONS:
                raise ValueError(f"Extension not allowed: {target.suffix}")

            if ".." in str(target):
                raise ValueError("Double dots not allowed in path.")
        except Exception as e:
             raise PermissionError(f"Sandbox violation: {str(e)}")

        target.parent.mkdir(parents=True, exist_ok=True)

        # Atomic-ish write
        temp_path = target.with_suffix(target.suffix + ".tmp")
        temp_path.write_text(content, encoding="utf-8")
        temp_path.replace(target)

        return {
            "ok": True,
            "path": str(rel_path),
            "bytes_written": len(content.encode("utf-8")),
            "sandboxed": True
        }

    def _audit_file(self, filepath: str) -> Dict[str, Any]:
        from .ctk import ClementeThesisKernel
        ctk = ClementeThesisKernel()
        content = self._read_text_file(filepath)
        result = ctk.evaluate(content)
        return {
            "filepath": filepath,
            "statuses": result.statuses,
            "severity": result.severity.value,
            "ok": result.ok
        }

    def _summarize_file(self, filepath: str) -> str:
        content = self._read_text_file(filepath)
        lines = content.splitlines()
        summary = f"File: {filepath}\nLines: {len(lines)}\nSize: {len(content)} bytes\n"
        summary += "Preview:\n" + "\n".join(lines[:10])
        return summary

    def _run_pytest_command_dry(self) -> Dict[str, Any]:
        cmd = ["python3", "-m", "pytest", "--collect-only", "-q"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        collected = 0
        for line in result.stdout.splitlines():
            if "tests collected" in line:
                try:
                    collected = int(line.split()[0])
                except:
                    pass

        return {
            "ok": result.returncode == 0,
            "mode": "dry",
            "command": " ".join(cmd),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "collected_tests": collected
        }

    def _repo_path_inspect(self, root: str = ".", max_depth: int = 3) -> Dict[str, Any]:
        base = Path(root)
        ignored = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "node_modules"}

        entries = []
        def walk(path: Path, depth: int):
            if depth > max_depth:
                return
            try:
                for item in path.iterdir():
                    if item.name in ignored:
                        continue

                    entry = {
                        "path": str(item.relative_to(base)),
                        "type": "directory" if item.is_dir() else "file",
                        "size_bytes": item.stat().st_size if item.is_file() else 0,
                        "modified_at": item.stat().st_mtime
                    }
                    entries.append(entry)
                    if item.is_dir():
                        walk(item, depth + 1)
            except PermissionError:
                pass

        walk(base, 1)
        return {
            "root": str(base),
            "max_depth": max_depth,
            "entries": entries
        }
