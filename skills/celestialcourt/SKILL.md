---
name: celestialcourt
description: >
  Runs an adversarial tribunal on a suggestion, argument, or caution.
  Research runs first (heavy) to ground the topics; God (PRO) and Devil (CON)
  orchestrate Angels and Demons to support or reject each researched topic;
  the Judge is fed the user's inputs, research.md, angels.md and demons.md and
  rules with a bounded pass=2 loop. Use when Sir wants an idea adjudicated
  before committing, or says "put it on trial" / "run celestialcourt on X".
argument-hint: "[suggestion | --case <file>]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Celestial Court — adversarial tribunal playbook

You (the main model) are the Celestial Court's **router**: the crew is
subagents, the state bus is files, and this body is the deterministic
program. Execute the phases in order. **The LM is never the terminator** —
the pass counter lives in `state.json`, never in anyone's memory.

## Phase 0 — ANCHOR (Examiner)

Spawn the `examiner` agent (or run the interview yourself if the case is
trivial) to interrogate Sir. Extract maximum context and write the bedrock:

- The claim itself + the problem it solves
- Requirements, constraints, goals, non-goals
- Context (repo, spec.md, prior decisions)
- Success criteria

Output: `court_cases/<slug>/anchor.md` (this is "the user's inputs" — it is
submitted to the Judge verbatim). Do not proceed until it is unambiguous;
Sir may cut the interview short with "enough".

## Phase 0.5 — ARSENAL CHECK (graceful degradation)

Check which arsenal skills are installed. Report present vs missing (CON
arsenal: ponytail, code-simplifier, security-guidance, grill-me; PRO
arsenal: frontend-design, artifact-design, artifact-diagramming, dataviz).
If any are missing, do not stall: the canons are baked into the agent
definitions. Tell the advocates to argue from canon alone, and offer
`/celestialcourt-setup` to provision with Sir's consent. Never install
anything silently.

## Phase 1 — RESEARCH (heavy, FIRST)

Research grounds the trial before anyone argues. Spawn `researcher` agents
**in parallel** — enough to cover the topic space. Direct them to cover all
three angles:

- **PRO angle** — what are the promising/valuable ways to do this? demand,
  analogous wins, upgrade paths.
- **CON angle** — is this unnecessary? simpler alternatives? risks,
  maintenance burden, reuse that already covers it?
- **Context** — the codebase, existing patterns, related prior decisions.

Rules for every researcher:
- Evidence cards: claim → evidence → `[SRC-n]` anchor mapped to a source
  list. Distinguish **fact** (cited) from **assertion** (reasoning).
- Each writes `research/researcher-<n>.md` and returns only a 3-bullet
  summary.

When all researchers return, **assemble `research/researcher-*.md` into
`research.md`** (the consolidated, evidence-grounded topic list). This is
the second artifact submitted to the Judge.

## Phase 2 — ADVOCACY (God → Angels, Devil → Demons)

Spawn `god` and `devil` **in a single message** (concurrent). Each reads
`research.md` and orchestrates its soldiers **against the researched topics**
(they do not invent topics — the research did).

- **God** (PRO): assigns every researched topic to an **Angel** (spawn one
  per topic, in parallel). Each Angel **supports** its assigned topic —
  proves it, upgrades it, evidences it — writing `angels/angel-<n>.md`.
  God returns a 3-bullet summary.
- **Devil** (CON): assigns every researched topic to a **Demon** (spawn one
  per topic, in parallel). Each Demon **rejects** its assigned topic —
  disproves it, degrades it, argues the simpler alternative — writing
  `demons/demon-<n>.md`. Devil returns a 3-bullet summary.

When both return, **assemble `angels/angel-*.md` into `angels.md`** and
**`demons/demon-*.md` into `demons.md`**. These are the third and fourth
artifacts submitted to the Judge.

Soldiers run on the mid model, orchestrators on the strong model.

## Phase 3 — JUDGEMENT (Judge)

Spawn the `judge` agent — a **fresh agent**, fed the record cold. Submit
the four artifacts:

1. `anchor.md` — the user's inputs (requirements, goals, constraints)
2. `research.md` — the evidence-grounded topics
3. `angels.md` — the support arguments
4. `demons.md` — the rejection arguments

The Judge:
1. Scores every claim on the rubric (Necessity / Value / Cost / Evidence /
   Fit) **and against the anchor** — a brilliant claim that doesn't serve
   the requirements fails; a modest one that does, passes.
2. Classifies each: **KEEP** / **REMAND** (with the opposing critique as the
   target) / **STRIKE**.
3. Applies **dual-ordering** when weighing sides; a flip-flopped verdict
   escalates to Sir.

## Phase 3b — REMAND LOOP (bounded, pass ≤ 2)

For each REMAND, before re-dispatching, update `state.json`:

```json
{ "round": 2, "passes": 2, "topic": "<subject>", "claims": { "angel-2": 1 } }
```

- If a claim's `passes` < 2: send it back to its **originating side** (the
  Angel or Demon who filed it) with the specific critique attached; the
  soldier re-files an improved version against the same anchor and research.
  Surface "attempt N of 2; previous critique: X" in the new prompt.
- **Progress witness:** if the re-filed claim is unchanged (byte-identical
  or semantically identical), flag stagnation and skip the discount — it
  doesn't earn a fresh pass.
- If `passes` reaches 2 and the claim is still weak: **STRIKE**.
- When all claims are KEEP/STRIKE, proceed. Never extend the loop.

## Phase 4 — FINAL RULING (Judge)

The Judge delivers the terminal verdict in `ruling.md`:

- **ADOPT** / **ADOPT-WITH-CONDITIONS** / **REJECT** / **SPLIT**
- Every disposition cites the specific claim, the criterion, and the reason
  (kills zombie ideas).

Deliver the ruling to Sir. Auto-applying the change is a deferred decision.

## Determinism checklist (do not skip)

1. Counter in `state.json`, incremented by you, never by an agent.
2. "attempt N of 2" surfaced in every remand prompt.
3. Exit predicate: all KEEP/STRIKE or `passes == 2` → final ruling.
4. Stagnation → straight to final ruling, no free pass.
5. Flip-flopped verdict → escalate to Sir.
6. Never crash, never extend — at the limit, rule.
