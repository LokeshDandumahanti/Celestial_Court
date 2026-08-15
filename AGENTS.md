# AGENTS.md — Celestial Court plugin rules

Rules for agents working in this repository:

- **Surgical changes only.** This plugin is a set of markdown instructions;
  the playbook (`skills/celestialcourt/SKILL.md`) is the deterministic
  program. Edit the playbook and the agent definitions, not ad-hoc prose.
- **Keep determinism honest:** the pass=2 counter lives in `state.json` and
  is incremented by the router, never by an agent. "The LM is never the
  terminator."
- **No silent dependencies:** Celestial Court degrades gracefully with zero
  arsenal plugins; provisioning happens only with user consent via
  `/celestialcourt-setup`.
- **Non-trivial changes leave one runnable check** — `tests/test_celestialcourt.py`
  must pass.
