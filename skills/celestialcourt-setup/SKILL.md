---
name: celestialcourt-setup
description: >
  Checks which arsenal plugins/skills are installed for Celestial Court, reports the
  gaps, and offers to install them with the user's consent. Use when setting
  up Celestial Court, after /celestialcourt reports missing arsenal, or when Sir asks how to
  strengthen the advocates.
argument-hint: "[--install]"
disable-model-invocation: true
allowed-tools: Read, Grep, Bash
---

# Celestial Court Setup — arsenal provisioning

Celestial Court's advocates work correctly with **zero plugins** — the CON canon
(YAGNI / minimalism / realism / reuse / root-cause) and the PRO mandate are
baked into the agent definitions. The arsenal below is the set of
*sharpening stones* that make each side sharper. This skill provisions them
**with your consent — never silently**.

## 1. CHECK

Inspect what's installed (plugin/skill cache at `~/.claude/plugins/` and
`~/.claude/skills/`, or ask which skills are available). Determine presence
of each:

**CON arsenal (the Devil's side):**
- `ponytail:ponytail`, `ponytail:ponytail-review`, `ponytail:ponytail-audit`
- `code-simplifier` · `security-guidance` · `grill-me`

**PRO arsenal (the God's side):**
- `frontend-design` · `artifact-design` · `artifact-diagramming` · `dataviz`

## 2. REPORT

Print a table: `skill | status (present/missing) | how to install`.

## 3. OFFER (never auto-install)

For each missing skill, give the exact install command and ask for
confirmation before running anything. Reference commands:

- ponytail: `/plugin marketplace add DietrichGebert/ponytail` then
  `/plugin install ponytail@ponytail`
- code-simplifier / security-guidance / frontend-design:
  `/plugin marketplace add anthropics/claude-plugins-official` then
  `/plugin install <name>@claude-plugins-official`
- grill-me / write-a-prd: `/plugin marketplace add reedom/mattpocock-skills`
  then `/plugin install <name>@<marketplace>`
- artifact-design / artifact-diagramming / dataviz: bundled with
  Claude Code — no install needed.

Only run install commands after explicit confirmation. If Sir declines,
confirm clearly that Celestial Court degrades gracefully and the trial proceeds
correctly from canon alone.
