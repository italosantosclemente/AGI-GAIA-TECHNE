from __future__ import annotations

import os
import re
import shlex
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class ShellDecision:
    allowed: bool
    reason: str
    args: List[str]
    risk_level: str
    policy: str
    requires_trusted: bool = False
    builtin_output: Optional[str] = None


class ShellPolicy:
    """
    Audit policy for finite shell action.

    The shell adapter is a world-capability, not private omnipotence. It avoids
    shell=True, records denial reasons, and only expands beyond a small safe
    allowlist when AGT_SHELL_TRUSTED=1 is explicitly set by the operator.
    """

    RESTRICTED_ALLOWLIST = {"echo", "python", "py", "julia"}
    DESTRUCTIVE_ROOTS = {
        "rm",
        "del",
        "erase",
        "format",
        "shutdown",
        "reboot",
        "halt",
        "poweroff",
        "remove-item",
        "rd",
        "rmdir",
        "mkfs",
        "diskpart",
    }
    INLINE_CODE_ARGS = {"-c", "/c", "-command", "-encodedcommand"}

    def __init__(
        self,
        trusted: Optional[bool] = None,
        allow_destructive: Optional[bool] = None,
    ) -> None:
        self.trusted = (
            os.environ.get("AGT_SHELL_TRUSTED") == "1"
            if trusted is None
            else trusted
        )
        self.allow_destructive = (
            os.environ.get("AGT_SHELL_ALLOW_DESTRUCTIVE") == "1"
            if allow_destructive is None
            else allow_destructive
        )

    def assess(self, command: str) -> ShellDecision:
        command = command.strip()
        if not command:
            return self._deny("empty command", [], "low")

        if _has_shell_metacharacter(command):
            return self._deny(
                "shell metacharacters require a human-authored adapter, not raw input",
                [],
                "high",
            )

        try:
            args = shlex.split(command, posix=(os.name != "nt"))
        except ValueError as exc:
            return self._deny(f"could not parse command: {exc}", [], "medium")

        if not args:
            return self._deny("empty command", [], "low")

        root = _normalize_root(args[0])
        if root in self.DESTRUCTIVE_ROOTS and not self.allow_destructive:
            return self._deny(
                "destructive command requires explicit AGT_SHELL_ALLOW_DESTRUCTIVE=1",
                args,
                "high",
            )

        if root == "echo":
            return ShellDecision(
                allowed=True,
                reason="safe builtin echo",
                args=args,
                risk_level="low",
                policy=self._policy_name,
                builtin_output=" ".join(args[1:]),
            )

        if not self.trusted and root not in self.RESTRICTED_ALLOWLIST:
            return ShellDecision(
                allowed=False,
                reason="command is outside the restricted allowlist",
                args=args,
                risk_level="medium",
                policy=self._policy_name,
                requires_trusted=True,
            )

        if not self.trusted and any(arg.lower() in self.INLINE_CODE_ARGS for arg in args[1:]):
            return ShellDecision(
                allowed=False,
                reason="inline code execution requires trusted mode",
                args=args,
                risk_level="medium",
                policy=self._policy_name,
                requires_trusted=True,
            )

        return ShellDecision(
            allowed=True,
            reason="allowed finite shell action",
            args=args,
            risk_level="medium" if self.trusted else "low",
            policy=self._policy_name,
        )

    @property
    def _policy_name(self) -> str:
        return "trusted" if self.trusted else "restricted"

    def _deny(self, reason: str, args: List[str], risk_level: str) -> ShellDecision:
        return ShellDecision(
            allowed=False,
            reason=reason,
            args=args,
            risk_level=risk_level,
            policy=self._policy_name,
        )


def _normalize_root(raw: str) -> str:
    root = raw.strip().strip("\"'").replace("\\", "/").split("/")[-1].lower()
    for suffix in (".exe", ".cmd", ".bat", ".ps1"):
        if root.endswith(suffix):
            return root[: -len(suffix)]
    return root


def _has_shell_metacharacter(command: str) -> bool:
    return bool(re.search(r"(&&|\|\||[|;<>`]|[$]\()", command))
