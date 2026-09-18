import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from app.config import PROJECT_ROOT, SPECS_DIR
from app.schemas.spec import BlueprintSchema, SpecValidationResult, ValidationError, CompilePromptResponse

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

class SDDCompiler:
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = project_root
        self.specs_dir = project_root / "specs"

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        content = path.read_text(encoding='utf-8')
        if HAS_YAML:
            return yaml.safe_load(content) or {}
        # Fallback dictionary parser
        data: Dict[str, Any] = {}
        for line in content.splitlines():
            line = line.strip()
            if ":" in line and not line.startswith("#"):
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip().strip('"').strip("'")
        return data

    def _load_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_blueprint(self) -> Dict[str, Any]:
        bp_path = self.specs_dir / "system-blueprint.yaml"
        return self._load_yaml(bp_path)

    def get_invariants(self) -> Dict[str, Any]:
        inv_path = self.specs_dir / "invariants" / "system-invariants.yaml"
        return self._load_yaml(inv_path)

    def get_task_schema(self) -> Dict[str, Any]:
        schema_path = self.specs_dir / "contracts" / "task-schema.json"
        return self._load_json(schema_path)

    def validate_specs(self) -> SpecValidationResult:
        errors: List[ValidationError] = []
        warnings: List[ValidationError] = []

        # 1. Blueprint check
        bp_path = self.specs_dir / "system-blueprint.yaml"
        if not bp_path.exists():
            errors.append(ValidationError(file="specs/system-blueprint.yaml", message="Blueprint file not found"))
        else:
            bp = self.get_blueprint()
            if not bp or "components" not in bp:
                warnings.append(ValidationError(file="specs/system-blueprint.yaml", message="Blueprint missing 'components' definition", severity="warning"))

        # 2. Task Schema check
        schema_path = self.specs_dir / "contracts" / "task-schema.json"
        if not schema_path.exists():
            errors.append(ValidationError(file="specs/contracts/task-schema.json", message="Task schema definition not found"))

        # 3. Tasks validation
        task_files = list(self.specs_dir.glob("tasks/**/*.json"))
        task_schema = self.get_task_schema()
        for tf in task_files:
            if "template" in tf.name:
                continue
            try:
                task_data = self._load_json(tf)
                if task_schema and HAS_JSONSCHEMA:
                    jsonschema.validate(instance=task_data, schema=task_schema)
                else:
                    for req in ["task_id", "title", "intent_vibe", "target_component", "acceptance_criteria"]:
                        if req not in task_data:
                            errors.append(ValidationError(file=str(tf.relative_to(self.project_root)), message=f"Missing required property '{req}'"))
            except Exception as e:
                errors.append(ValidationError(file=str(tf.relative_to(self.project_root)), message=str(e)))

        return SpecValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            blueprint_summary=self.get_blueprint().get("project")
        )

    def compile_prompt_from_vibe(
        self,
        intent_vibe: str,
        target_component: str,
        target_spec: Optional[str] = "specs/contracts/api-v1.yaml",
        assigned_agent: str = "claude-code",
        affected_files: Optional[List[str]] = None
    ) -> CompilePromptResponse:
        blueprint = self.get_blueprint()
        invariants = self.get_invariants()
        
        # Generate slug and task_id
        timestamp_str = time.strftime("%Y%m%d")
        slug = "_".join(intent_vibe.lower().split()[:3])
        slug = "".join(c for c in slug if c.isalnum() or c == "_")
        task_id = f"task_{timestamp_str}_{slug or 'vibe_mission'}"

        # Find component details from blueprint
        comp_details = {}
        for c in blueprint.get("components", []):
            if c.get("id") == target_component:
                comp_details = c
                break

        # Synthesize acceptance criteria
        criteria = [
            f"Fulfill feature intent: {intent_vibe}",
            f"Adhere to component architecture in {comp_details.get('path', target_component)}",
            "Maintain zero linter and type-checker regressions",
            "Keep container user non-root ('node') with no leaked API tokens"
        ]

        verification_commands = ["python bin/sdd.py lint"]
        if comp_details.get("runtime", "").startswith("React") or comp_details.get("path", "").startswith("orchestrator/dashboard"):
            verification_commands.append("npm test --if-present")

        manifest = {
            "task_id": task_id,
            "title": f"{target_component.title()}: {intent_vibe[:60]}",
            "intent_vibe": intent_vibe,
            "target_component": target_component,
            "target_spec": target_spec,
            "affected_files": affected_files or [f"{comp_details.get('path', 'src/')}**/*"],
            "assigned_agent": assigned_agent,
            "constraints": {
                "max_iterations": 3,
                "strict_types": True,
                "preserve_tests": True,
                "timeout_seconds": 300
            },
            "acceptance_criteria": criteria,
            "verification_commands": verification_commands
        }

        compiled_prompt = f"""# ==============================================================================
# STRUCTURED SDD AGENT INSTRUCTION PACKET
# ==============================================================================
TASK_ID: {task_id}
TITLE: {manifest['title']}
TARGET_COMPONENT: {target_component} ({comp_details.get('name', 'General')})
ASSIGNED_AGENT: {assigned_agent}

## 1. USER INTENT / VIBE
{intent_vibe}

## 2. AFFECTED BLAST RADIUS
{json.dumps(manifest['affected_files'], indent=2)}

## 3. ACCEPTANCE CRITERIA (MANDATORY INVARIANTS)
"""
        for i, ac in enumerate(criteria, 1):
            compiled_prompt += f"{i}. {ac}\n"

        compiled_prompt += "\n## 4. AUTOMATED POST-TASK VERIFICATION GATES\n"
        for cmd in verification_commands:
            compiled_prompt += f"- `{cmd}`\n"

        compiled_prompt += """
## 5. SYSTEM ARCHITECTURAL INVARIANTS
- Non-root user 'node'. Do NOT commit credentials or hardcode absolute host directories.
- Preserve existing CLI shortcuts and verified toolchain (Claude, Codex, Bun, PNPM, Tmux).
- Execute clean changes and satisfy all verification gates.
"""

        return CompilePromptResponse(
            task_id=task_id,
            compiled_prompt=compiled_prompt,
            synthesized_manifest=manifest
        )
