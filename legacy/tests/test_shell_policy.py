from agt.shell_policy import ShellPolicy
from agt.tool_executor import ToolExecutor
from agt.types import PlanStep


def test_shell_echo_is_allowed_with_public_trace():
    executor = ToolExecutor(shell_policy=ShellPolicy(trusted=False))
    result = executor.execute(
        PlanStep(
            id="shell_echo",
            action="world_shell",
            description="Echo a safe symbolic trace.",
            tool_name="shell",
            tool_args={"command": "echo Gaia-Techne"},
        )
    )

    assert result.ok is True
    assert "World shell trace" in result.output
    assert "policy: allowed" in result.output
    assert "Gaia-Techne" in result.output


def test_shell_destructive_command_is_transmuted():
    executor = ToolExecutor(shell_policy=ShellPolicy(trusted=True))
    result = executor.execute(
        PlanStep(
            id="shell_deny",
            action="world_shell",
            description="Deny destructive command.",
            tool_name="shell",
            tool_args={"command": "rm -rf /"},
        )
    )

    assert result.ok is True
    assert "policy: denied/transmuted" in result.output
    assert "destructive command" in result.output


def test_web_executor_allows_text_data_trace():
    executor = ToolExecutor()
    result = executor.execute(
        PlanStep(
            id="web_data",
            action="world_web",
            description="Read explicit text data trace.",
            tool_name="web",
            tool_args={"url": "data:text/plain,Gaia-Techne"},
        )
    )

    assert result.ok is True
    assert "World web trace" in result.output
    assert "content_type: text/plain" in result.output
    assert "Gaia-Techne" in result.output


def test_web_executor_blocks_private_hosts_by_default():
    executor = ToolExecutor()
    result = executor.execute(
        PlanStep(
            id="web_private",
            action="world_web",
            description="Deny local network trace.",
            tool_name="web",
            tool_args={"url": "http://localhost:8501"},
        )
    )

    assert result.ok is True
    assert "policy: denied/transmuted" in result.output
    assert "Private or local hosts" in result.output
