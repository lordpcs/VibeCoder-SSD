#!/usr/bin/env python3
"""
SDD CLI Tool: System-Driven Development validator, compiler, and invariant verifier.
"""
import sys
import os
import json
import glob
import re
from pathlib import Path

# Fix Windows console utf-8 encoding issues
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Try importing yaml, or provide fallback YAML parser for simple structures
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Try importing jsonschema
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

def find_project_root():
    current = Path.cwd()
    for p in [current, current.parent, current.parent.parent]:
        if (p / "specs" / "system-blueprint.yaml").exists() or (p / "Dockerfile").exists():
            return p
    return current

PROJECT_ROOT = find_project_root()
SPECS_DIR = PROJECT_ROOT / "specs"

def load_yaml(file_path):
    if not os.path.exists(file_path):
        return None
    if HAS_YAML:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        # Minimal line-based parser fallback for blueprint info
        result = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if ":" in line and not line.startswith("#"):
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if v:
                    result[k] = v
        return result

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def cmd_lint():
    print("🔍 [SDD LINT] Validating System Specifications and Contracts...")
    errors = 0
    warnings = 0

    # 1. Check system-blueprint.yaml
    blueprint_path = SPECS_DIR / "system-blueprint.yaml"
    if not blueprint_path.exists():
        print(f"❌ Missing required blueprint: {blueprint_path}")
        errors += 1
    else:
        bp = load_yaml(blueprint_path)
        if bp:
            print(f"✅ Blueprint valid: {bp.get('project', {}).get('name', 'System Blueprint')}")
        else:
            print(f"⚠️ Could not fully parse blueprint: {blueprint_path}")
            warnings += 1

    # 2. Check task-schema.json
    schema_path = SPECS_DIR / "contracts" / "task-schema.json"
    task_schema = None
    if not schema_path.exists():
        print(f"❌ Missing task schema: {schema_path}")
        errors += 1
    else:
        try:
            task_schema = load_json(schema_path)
            print("✅ SDD Task Schema loaded successfully.")
        except Exception as e:
            print(f"❌ Error in task schema JSON: {e}")
            errors += 1

    # 3. Check OpenAPI contract
    openapi_path = SPECS_DIR / "contracts" / "api-v1.yaml"
    if openapi_path.exists():
        print("✅ OpenAPI 3.1 specification present.")
    else:
        print(f"⚠️ OpenAPI spec not found at {openapi_path}")
        warnings += 1

    # 4. Validate all task files in specs/tasks/
    task_files = list(SPECS_DIR.glob("tasks/**/*.json"))
    for tf in task_files:
        if "template" in tf.name:
            continue
        try:
            task_data = load_json(tf)
            if task_schema and HAS_JSONSCHEMA:
                jsonschema.validate(instance=task_data, schema=task_schema)
                print(f"✅ Valid Task Manifest: {tf.relative_to(PROJECT_ROOT)} ({task_data.get('title')})")
            else:
                # Basic check
                required = ["task_id", "title", "intent_vibe", "target_component", "acceptance_criteria"]
                missing = [r for r in required if r not in task_data]
                if missing:
                    print(f"❌ Task {tf.name} missing fields: {missing}")
                    errors += 1
                else:
                    print(f"✅ Basic validation passed: {tf.relative_to(PROJECT_ROOT)}")
        except Exception as e:
            print(f"❌ Schema validation failed for {tf.name}: {e}")
            errors += 1

    print("------------------------------------------------------------")
    if errors == 0:
        print(f"🎉 SDD Validation Passed: 0 errors, {warnings} warning(s).")
        return 0
    else:
        print(f"💥 SDD Validation Failed: {errors} error(s), {warnings} warning(s).")
        return 1

def cmd_compile_prompt(task_file):
    path = Path(task_file)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    if not path.exists():
        print(f"❌ Task file not found: {path}")
        return 1

    task = load_json(path)
    blueprint = load_yaml(SPECS_DIR / "system-blueprint.yaml") or {}
    invariants = load_yaml(SPECS_DIR / "invariants" / "system-invariants.yaml") or {}

    prompt = f"""# ==============================================================================
# STRUCTURED SDD AGENT INSTRUCTION PACKET
# ==============================================================================
TASK_ID: {task.get('task_id')}
TITLE: {task.get('title')}
TARGET_COMPONENT: {task.get('target_component')}
ASSIGNED_AGENT: {task.get('assigned_agent', 'claude-code')}

## 1. USER INTENT / VIBE
{task.get('intent_vibe')}

## 2. AFFECTED FILES & BLAST RADIUS
{json.dumps(task.get('affected_files', []), indent=2)}

## 3. ACCEPTANCE CRITERIA (MANDATORY INVARIANTS)
"""
    for i, ac in enumerate(task.get('acceptance_criteria', []), 1):
        prompt += f"{i}. {ac}\n"

    prompt += "\n## 4. AUTOMATED POST-TASK VERIFICATION GATES\n"
    for cmd in task.get('verification_commands', []):
        prompt += f"- `{cmd}`\n"

    prompt += """
## 5. SYSTEM INVARIANTS
- Container user is non-root 'node'. Never hardcode absolute host paths.
- Do NOT commit API keys or auth secrets.
- Backward compatibility: Preserves existing CLI tools (c, cx, rw, lg, pn, b).
- Implement changes cleanly. Run verification commands before returning.
"""
    print(prompt)
    return 0

def cmd_verify_invariants():
    print("🛡️ [SDD INVARIANTS] Checking deterministic architectural rules...")
    violations = 0

    # Invariant 1: Check Dockerfile enforces non-root user
    dockerfile = PROJECT_ROOT / "Dockerfile"
    if dockerfile.exists():
        content = dockerfile.read_text(encoding='utf-8')
        if "USER node" in content:
            print("✅ Invariant 1 [Passed]: Dockerfile enforces non-root user 'node'.")
        else:
            print("❌ Invariant 1 [Failed]: Dockerfile must specify 'USER node'.")
            violations += 1

    # Invariant 2: Check for leaked keys in git tracked/workspace files
    forbidden_patterns = [r"sk-ant-[a-zA-Z0-9_-]{20,}", r"sk-[a-zA-Z0-9_-]{20,}", r"ghp_[a-zA-Z0-9_-]{20,}"]
    leaks = False
    for ext in ["*.py", "*.json", "*.yaml", "*.yml", "*.sh", "*.md"]:
        for file_p in PROJECT_ROOT.glob(ext):
            if ".git" in str(file_p) or ".env" in file_p.name:
                continue
            try:
                txt = file_p.read_text(encoding='utf-8', errors='ignore')
                for pat in forbidden_patterns:
                    if re.search(pat, txt):
                        print(f"❌ Invariant 2 [Failed]: Potential credential leak in {file_p.name}")
                        violations += 1
                        leaks = True
            except Exception:
                pass
    if not leaks:
        print("✅ Invariant 2 [Passed]: No hardcoded credentials detected.")

    # Invariant 3: Verification script exists
    verify_sh = PROJECT_ROOT / "verify.sh"
    if verify_sh.exists():
        print("✅ Invariant 3 [Passed]: Toolchain verification script present.")
    else:
        print("❌ Invariant 3 [Failed]: verify.sh is missing.")
        violations += 1

    print("------------------------------------------------------------")
    if violations == 0:
        print("🎉 All Architectural Invariants Satisfied.")
        return 0
    else:
        print(f"💥 Invariant check failed with {violations} violation(s).")
        return 1

def main():
    if len(sys.argv) < 2:
        print("Usage: sdd <command> [args]")
        print("Commands:")
        print("  lint                 Validate blueprint, contracts, and tasks")
        print("  compile-prompt <file> Synthesize full prompt packet from task manifest")
        print("  verify-invariants    Assert architectural and security invariants")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "lint":
        sys.exit(cmd_lint())
    elif cmd in ["compile", "compile-prompt"]:
        if len(sys.argv) < 3:
            print("Error: Specify a task JSON file (e.g. sdd compile-prompt specs/tasks/example-auth-task.json)")
            sys.exit(1)
        sys.exit(cmd_compile_prompt(sys.argv[2]))
    elif cmd in ["verify-invariants", "invariants"]:
        sys.exit(cmd_verify_invariants())
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
