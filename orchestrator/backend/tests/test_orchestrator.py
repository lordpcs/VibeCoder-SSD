import asyncio
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from app.core.sdd_compiler import SDDCompiler
from app.core.dispatcher import TaskDispatcher
from app.schemas.task import TaskDefinition, TaskStatus
from app.api.routes_agents import check_tool, KNOWN_TOOLS

async def test_sdd_compiler():
    print("Testing SDDCompiler...")
    compiler = SDDCompiler()
    bp = compiler.get_blueprint()
    assert bp is not None, "Blueprint should load"
    assert "components" in bp, "Blueprint must contain components"

    val = compiler.validate_specs()
    assert val.valid is True, f"Validation failed: {val.errors}"

    compiled = compiler.compile_prompt_from_vibe(
        intent_vibe="Test feature authentication vibe",
        target_component="agentic-orchestrator",
        assigned_agent="mock-runner"
    )
    assert compiled.task_id.startswith("task_"), "Task ID format invalid"
    assert "Test feature authentication vibe" in compiled.compiled_prompt
    print("✅ SDDCompiler tests passed.")

async def test_dispatcher_mock_run():
    print("Testing TaskDispatcher with Mock Runner...")
    dispatcher = TaskDispatcher()
    task_def = TaskDefinition(
        task_id="task_test_mock_001",
        title="Test Mock Task Execution",
        intent_vibe="Simulate execution in test suite",
        target_component="agentic-orchestrator",
        assigned_agent="mock-runner",
        acceptance_criteria=["Criterion 1 holds"],
        verification_commands=["python bin/sdd.py invariants"]
    )

    result = await dispatcher.submit_task(task_def)
    assert result.status in [TaskStatus.QUEUED, TaskStatus.RUNNING]

    # Wait for execution to finish
    for _ in range(30):
        await asyncio.sleep(0.3)
        current = dispatcher.get_task("task_test_mock_001")
        if current and current.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            break

    final_task = dispatcher.get_task("task_test_mock_001")
    assert final_task is not None
    assert final_task.status == TaskStatus.COMPLETED, f"Task did not complete: {final_task.status} ({final_task.error_message})"
    assert len(final_task.verification_results) > 0, "Should have verification results"
    assert final_task.verification_results[0].passed is True, "Verification command should pass"
    print("✅ TaskDispatcher mock execution & verification gates passed.")

def test_tool_checks():
    print("Testing toolchain detection...")
    python_status = check_tool({"name": "Python", "command": "python", "version_arg": "--version", "purpose": "Testing"})
    assert python_status.installed is True
    print(f"✅ Python tool detection passed: {python_status.version}")

async def main():
    await test_sdd_compiler()
    test_tool_checks()
    await test_dispatcher_mock_run()
    print("🎉 All Orchestrator unit & integration tests succeeded!")

if __name__ == "__main__":
    asyncio.run(main())
