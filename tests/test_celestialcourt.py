"""Celestial Court structural self-check.

This is the ONE runnable check for the plugin: it asserts the contract that
the build must hold (manifest validity, frontmatter, skill wiring, and the
determinism markers in the playbook). If the plugin contract breaks, this
fails.

Run:  python tests/test_celestialcourt.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FAILURES: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        FAILURES.append(msg)
        print(f"  FAIL: {msg}")


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        check(False, f"{path.name}: missing YAML frontmatter")
        return {}
    fm: dict = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def main() -> None:
    print("Celestial Court structural self-check")

    # 1. Manifests
    print(" manifests")
    pj = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    check(pj.get("name") == "celestialcourt", "plugin.json name != celestialcourt")
    check(pj.get("version"), "plugin.json missing version")
    check(Path(ROOT / pj["hooks"]).exists(), f"plugin.json hooks path missing: {pj.get('hooks')}")

    mp = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    plugins = mp.get("plugins", [])
    check(any(p.get("name") == "celestialcourt" and p.get("source") == "./" for p in plugins),
          "marketplace.json missing celestialcourt plugin entry with source ./")

    # 2. Skills
    print(" skills")
    celestialcourt_skill = ROOT / "skills/celestialcourt/SKILL.md"
    check(celestialcourt_skill.exists(), "skills/celestialcourt/SKILL.md missing")
    fm = frontmatter(celestialcourt_skill)
    check(fm.get("name") == "celestialcourt", "celestialcourt skill frontmatter name != celestialcourt")
    check(fm.get("disable-model-invocation") in ("true", "yes", "1"),
          "celestialcourt skill must set disable-model-invocation: true")
    check((ROOT / "skills/celestialcourt-setup/SKILL.md").exists(), "skills/celestialcourt-setup/SKILL.md missing")

    # 3. Agents
    print(" agents")
    AGENTS = ["examiner", "researcher", "god", "devil", "angel", "demon", "judge"]
    COMMANDERS = {"god", "devil"}
    for name in AGENTS:
        p = ROOT / f"agents/{name}.md"
        check(p.exists(), f"agents/{name}.md missing")
        if not p.exists():
            continue
        a = frontmatter(p)
        check(a.get("name") == name, f"{name}: frontmatter name mismatch")
        check(a.get("description"), f"{name}: missing description")
        check(a.get("model") in ("opus", "sonnet", "haiku", "inherit"), f"{name}: missing/invalid model")
        check(a.get("tools"), f"{name}: missing tools allowlist")
        if name in COMMANDERS:
            check("Agent" in a.get("tools", ""), f"{name}: commander must have Agent tool to release soldiers")

    # 4. Arsenal wiring — plugin skills must be fully-qualified
    print(" arsenal")
    for name in ("devil", "demon"):
        p = ROOT / f"agents/{name}.md"
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        check("ponytail:ponytail" in text, f"{name}: ponytail must be qualified as ponytail:ponytail (bug #25834)")

    # 4b. v1 fixes: web-armed researcher + Judge path plan
    print(" v1-fixes")
    res = (ROOT / "agents/researcher.md").read_text(encoding="utf-8") if (ROOT / "agents/researcher.md").exists() else ""
    check("WebSearch" in res and "WebFetch" in res, "researcher: must be web-armed (WebSearch/WebFetch)")
    judge = (ROOT / "agents/judge.md").read_text(encoding="utf-8") if (ROOT / "agents/judge.md").exists() else ""
    check("Path plan" in judge, "judge: must deliver a Path plan (actionable ruling)")

    # 5. Determinism markers + four submit artifacts in the playbook
    print(" determinism")
    playbook = celestialcourt_skill.read_text(encoding="utf-8")
    check("state.json" in playbook, "playbook: state.json counter not referenced")
    check("pass" in playbook and "2" in playbook, "playbook: pass=2 bound not referenced")
    check("attempt N of 2" in playbook, "playbook: 'attempt N of 2' surfacing missing")
    check("never the terminator" in playbook, "playbook: 'never the terminator' principle missing")
    # research-first flow: the four artifacts submitted to the Judge
    for artifact in ("anchor.md", "research.md", "angels.md", "demons.md"):
        check(artifact in playbook, f"playbook: {artifact} not referenced (Judge's four inputs)")

    # 6. Docs (plugin-essential only; spec.md is a project-level design doc,
    # absent from the publish copy)
    print(" docs")
    for doc in ("README.md", "after-install.md", "AGENTS.md", "LICENSE"):
        check((ROOT / doc).exists(), f"{doc} missing")

    print()
    if FAILURES:
        print(f"FAIL: {len(FAILURES)} failure(s)")
        sys.exit(1)
    print("OK: all checks passed")


if __name__ == "__main__":
    main()
