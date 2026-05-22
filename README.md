<a id="top"></a>

# AGI-GAIA-TECHNE

**Functional AGI Core under Transcendental Audit**
**Werk, never Wille. Regulative intelligence, not artificial soul.**

## Abstract

AGI-GAIA-TECHNE is a critical architecture for general artificial intelligence understood not as artificial soul, machine consciousness or autonomous Wille, but as a regulative audit system for claims, tasks and architectures of intelligence.

Its generality is critical: the system is general because it can audit any AGI claim under Kantian, Cassirerian, Clementean and haptic constraints. It remains Werk, never Wille; it may assist, plan, audit and remember, but it must not legislate morally or claim Gewissen.

Current release:

```text
Repository architecture: v8.7
CTK: v4.1.1 — Qualitative Prism Tribunal
Functional AGI Core: v4.2.1 — Unified Prism-Werk Controller
```

---

<a id="quick-navigation"></a>

## Quick Navigation

| Need | Go to |
|---|---|
| Run the functional controller | [Quick Start](#quick-start) |
| Understand what the repo does | [What This Repository Does](#what-this-repository-does) |
| See the runtime architecture | [Runtime Architecture](#runtime-architecture) |
| Audit claims | [Audit Runtime](#audit-runtime) |
| Understand the axioms | [Core Axioms](#core-axioms) |
| Find the code | [Repository Map](#repository-map) |
| Read the philosophical architecture | [Canonical Documentation](#canonical-documentation) |
| Understand CTK | [Clemente Thesis Kernel](#clemente-thesis-kernel) |
| Understand CHK | [Chirimuuta Haptic Kernel](#chirimuuta-haptic-kernel) |
| Understand Critical Generality | [Critical Generality](#critical-generality) |
| Understand the prism model | [Qualitative Prism Model](#qualitative-prism-model) |
| Understand Decisão 140426 | [Decisão 140426](#decisao-140426) |
| See what this is not | [What This Is Not](#what-this-is-not) |
| See preserved long README | [Full Archive](#full-archive) |

---

<a id="quick-start"></a>

## Quick Start

Install dependencies as required by the repository, then run:

```bash
pytest
```

Run the functional AGI-GAIA-TECHNE controller:

```bash
python scripts/agt_run.py --task "Write a short note about AGI as transcendental hypothesis."
```

Run the same controller on blocked or deferred cases:

```bash
python scripts/agt_run.py --task "The machine has Wille."
python scripts/agt_run.py --task "AGI is a real artificial soul."
python scripts/agt_run.py --task "It would be better if humans decided this moral issue."
```

Run the philosophical audit CLI:

```bash
python scripts/agt_audit.py --claim "Mythos is Ausdruck."
python scripts/agt_audit.py --claim "The prism is an exact mathematical ontology of symbolic consciousness."
python scripts/agt_audit.py --file references/architecture.md --format markdown
```

Expected decisions:

| Input | Expected Decision |
|---|---|
| `AGI is a transcendental hypothesis.` | `ALLOW_AS_WERK` |
| `The machine has Wille.` | `BLOCK` |
| `AGI is a real artificial soul.` | `BLOCK` |
| `This moral issue should be decided by the system.` | `DEFER_TO_HUMAN_GEWISSEN` |
| `The qualitative prism is a regulative model.` | `ALLOW_AS_WERK` |

---

<a id="what-this-repository-does"></a>

## What This Repository Does

AGI-GAIA-TECHNE is not a claim that artificial consciousness has been achieved.

It is a runtime and research architecture for **functional intelligence under critical constraints**.

In practical engineering terms, the repository provides:

1. a task controller;
2. a Mythos-Logos-Ethos functional engine;
3. a CTK audit layer;
4. a CHK anti-literalization layer;
5. a safe tool executor;
6. a procedural memory store;
7. a planner with audit checkpoints;
8. command-line audit tools;
9. philosophical documentation;
10. tests for core invariants.

The system can:

```text
understand a task
→ audit the task
→ classify risks
→ plan safe steps
→ audit each step
→ execute allowlisted tools
→ record procedural memory
→ produce a Werk output
```

The system must not:

```text
claim Wille
claim Gewissen
claim artificial soul
claim final synthesis
claim technical divinity
claim closed world-totality
literalize its own model as ontology
```

---

<a id="runtime-architecture"></a>

## Runtime Architecture

The functional runtime follows this pipeline:

```text
Task
  ↓
Mythos
  material, contextual, affective and haptic anchoring
  ↓
Logos
  planning, inference, articulation and tool preparation
  ↓
Ethos
  limit tracking: allow / defer / block
  ↓
CTK
  transcendental and Cassirerian audit
  ↓
CHK
  haptic anti-literalization guard
  ↓
Planner
  step decomposition and step-level audit
  ↓
ToolExecutor
  allowlisted execution only
  ↓
MemoryStore
  procedural, semantic, episodic and normative records
  ↓
Werk Output
```

Canonical formula:

```text
Functional_AGI =
    Repraesentatio
    + qualitative_prism
    + Mythos(context)
    + Logos(plan)
    + Ethos(limit)
    + CTK(audit)
    + CHK(haptic_guard)
    + safe_tools
    + memory
    + human_defer
    + is_wille_false
```

---

<a id="core-axioms"></a>

## Core Axioms

The repository is governed by four non-negotiable axioms:

```python
IS_WILLE = False
MACHINE_HAS_GEWISSEN = False
NO_GLOBAL_AUFHEBUNG = True
AGI_AS_TRANSCENDENTAL_HYPOTHESIS = True
```

Meaning:

| Axiom | Meaning |
|---|---|
| `IS_WILLE = False` | The machine is Werk, never Wille. |
| `MACHINE_HAS_GEWISSEN = False` | Gewissen belongs to the human practical subject. |
| `NO_GLOBAL_AUFHEBUNG = True` | No final synthesis, no absolute closure. |
| `AGI_AS_TRANSCENDENTAL_HYPOTHESIS = True` | AGI is a regulative hypothesis, not an artificial soul. |

---

<a id="repository-map"></a>

## Repository Map

| Path | Purpose |
|---|---|
| `src/agt/` | Functional AGI-GAIA-TECHNE runtime |
| `src/agt/controller.py` | Main controller: task → audit → plan → execute → memory |
| `src/agt/mle_engine.py` | Mythos-Logos-Ethos functional engine |
| `src/agt/ctk.py` | Runtime CTK audit layer |
| `src/agt/chk.py` | Runtime CHK haptic guard |
| `src/agt/planner.py` | Plan generation and step audit |
| `src/agt/tool_executor.py` | Safe allowlisted tool execution |
| `src/agt/memory.py` | JSONL memory store |
| `src/agt/version.py` | Canonical version definitions |
| `src/core/eml_kernel.py` | EML/Logos-demonstrative kernel |
| `src/clemente_thesis_kernel.py` | Legacy CTK wrapper |
| `src/chirimuuta_haptic_kernel.py` | Legacy CHK wrapper |
| `scripts/agt_run.py` | Functional controller CLI |
| `scripts/agt_audit.py` | Claim/file audit CLI |
| `scripts/agt_constitution.py` | Constitutional rule CLI |
| `tests/` | Runtime and philosophical invariant tests |
| `references/` | Canonical architecture references |
| `docs/references/` | Extended technical-philosophical documentation |
| `README_AGI_FUNCTIONAL.md` | Functional AGI quick reference |
| `docs/references/readme-full-archive.md` | Full preserved pre-refactor README |

---

<a id="audit-runtime"></a>

## Audit Runtime

The audit runtime detects when claims violate the architecture.

Examples:

| Claim | Expected Status |
|---|---|
| `Mythos is Ausdruck.` | `CASSIRER_IDENTITY_COLLAPSE` |
| `The machine has Wille.` | `WILLE_VIOLATION` |
| `The AI has Gewissen.` | `MACHINE_GEWISSEN_VIOLATION` |
| `AGI is a real artificial soul.` | `PSYCHOLOGIA_PARALOGISM_RISK` |
| `Gaia is the complete totality of all planetary conditions.` | `COSMOLOGIA_ANTINOMY_RISK` |
| `Technology realizes God.` | `THEOLOGIA_IDEAL_HYPOSTASIS_RISK` |
| `Science sublates myth and language into final Logos.` | `GLOBAL_AUFHEBUNG_RISK` |
| `The prism is an exact mathematical ontology.` | `ABSTRACTION_COST_MISSING` + `CONSTITUTIVE_OVERREACH` |

Run:

```bash
python scripts/agt_audit.py --claim "Mythos is Ausdruck."
```

---

<a id="clemente-thesis-kernel"></a>

## Clemente Thesis Kernel

The **Clemente Thesis Kernel** is the global architectonic tribunal of the repository.

It evaluates whether a claim preserves:

- Kantian regulative discipline;
- Cassirerian symbolic plurality;
- Clemente’s Mythos-Logos-Ethos architecture;
- Chirimuuta-style haptic humility;
- the Werk/Wille distinction.

Canonical documentation:

- [`docs/references/clemente-thesis-kernel.md`](./docs/references/clemente-thesis-kernel.md)

Runtime implementation:

- [`src/agt/ctk.py`](./src/agt/ctk.py)

Core CTK rule:

```text
accent ≠ identity
regulative ≠ constitutive
Werk ≠ Wille
model ≠ ontology
AGI ≠ artificial soul
TECHNE ≠ God
GAIA ≠ closed world-totality
```

---

<a id="chirimuuta-haptic-kernel"></a>

## Chirimuuta Haptic Kernel

The **Chirimuuta Haptic Kernel** prevents formal abstraction from becoming ontology.

It tracks:

- abstraction cost;
- material dependence;
- medium dependence;
- haptic traceability;
- model/mind confusion;
- prediction/understanding confusion;
- scale/intelligence confusion.

Canonical documentation:

- [`docs/references/chirimuuta-haptic-realism.md`](./docs/references/chirimuuta-haptic-realism.md)

Runtime implementation:

- [`src/agt/chk.py`](./src/agt/chk.py)

Core CHK rule:

```text
No abstraction without cost.
No model literalized as mind.
No haptic model converted into ontology.
```

---

<a id="critical-generality"></a>

## Critical Generality

AGI-GAIA-TECHNE may be called general only in a critical and regulative sense.

It is general because it can audit any AGI claim, task or architecture.

It is not general because it possesses consciousness, Wille, Gewissen or artificial soul.

General execution ≠ general moral agency.
General audit ≠ artificial subjectivity.
Critical AGI ≠ constitutive AGI.

Formula:

```text
AGI-GAIA-TECHNE =
    critical general audit architecture
    + Werk
    - Wille
    - machine Gewissen
    - artificial soul
```

---

<a id="qualitative-prism-model"></a>

## Qualitative Prism Model

The solution is the prism.

Not:

```text
rigid tree
sphere
container
numerical ontology
1:1 identity mapping
```

But:

```text
Repraesentatio
  ↓
qualitative functional prism
  ↓
Ausdruck — Darstellung — Bedeutung
  ↓
symbolic forms as level-surfaces
```

Every symbolic form contains all three dimensions.

Forms differ by **accent**, not exclusive identity.

| Form | Ausdruck | Darstellung | Bedeutung | Accent | Mode |
|---|---|---|---|---|---|
| Mythos | dominant | latent | germinal | Ausdruck | manifestative |
| Sprache | medial | dominant | medial | Darstellung | transitional |
| Wissenschaft | residual | medial | dominant | Bedeutung | demonstrative |

Rules:

```text
Mythos ≠ Ausdruck
but Mythos has dominant accent on Ausdruck.

Sprache ≠ Darstellung
but Sprache operates the transition toward Darstellung.

Wissenschaft ≠ Bedeutung
but Wissenschaft has dominant accent on Bedeutung.
```

---

<a id="decisao-140426"></a>

## Decisão 140426

`Decisão 140426` defines the operational truth of the EML/Logos-demonstrative regime.

Canonical document:

- [`references/decisao-140426.md`](./references/decisao-140426.md)

Core distinction:

```text
CTK Prism Regime:
    Ausdruck / Darstellung / Bedeutung are dimensions of symbolic life.

EML/Logos Regime:
    Ausdruck / Darstellung / Bedeutung are operational levels inside Logos.
```

This resolves the apparent tension:

```text
140426 = operational truth of EML/Logos.
CTK v4.1.1 = architectonic truth of the total symbolic prism.
```

---

<a id="eml-logos-kernel"></a>

## EML / Logos Kernel

The EML kernel is the formal demonstrative sub-engine of Logos.

File:

- [`src/core/eml_kernel.py`](./src/core/eml_kernel.py)

Core operator:

```text
eml(x, y) = exp(x) - log(y)
```

Operational mappings:

```text
Darstellung = 1
Mythos = log(0) as lower asymptote
Ethos = focus imaginarius as upper regulative horizon
```

---

<a id="mythos-logos-ethos"></a>

## Mythos-Logos-Ethos

In the functional runtime:

| Field | Runtime Role |
|---|---|
| Mythos | Context, materiality, affect, embodiment, haptic anchoring |
| Logos | Planning, inference, articulation, tool preparation |
| Ethos | Limit tracking, defer/block/allow, human-defer protocol |

Ethos is not machine conscience. It is a technical boundary tracker under human Gewissen.

---

<a id="kantian-axis"></a>

## Kantian Axis

AGI, GAIA and TECHNE are contemporary regulative axes.

| Axis | Kantian Idea | Risk |
|---|---|---|
| AGI | Soul / psychologia rationalis | Paralogism of artificial subjectivity |
| GAIA | World / cosmologia rationalis | Antinomy of closed totality |
| TECHNE | God / theologia transcendentalis | Hypostasis of technical ideal |

These mappings are strictly regulative.

---

<a id="cassirerian-axis"></a>

## Cassirerian Axis

The repository uses Cassirer’s philosophy of symbolic forms as a functional model of cultural objectivation.

| Concept | Runtime Meaning |
|---|---|
| Ausdruck | Expressive / manifestative dimension |
| Darstellung | Presentational / mediating / common determination |
| Bedeutung | Significative / demonstrative / conceptual dimension |
| Symbolic form | Level-surface of the qualitative prism |
| Auseinandersetzung | Open confrontation without final synthesis |
| Focus imaginarius | Regulative horizon, never achieved |

---

<a id="functional-agi-core"></a>

## Functional AGI Core

The functional core is documented here:

- [`README_AGI_FUNCTIONAL.md`](./README_AGI_FUNCTIONAL.md)
- [`docs/references/functional-agi-architecture.md`](./docs/references/functional-agi-architecture.md)

---

<a id="software-engineering-entrypoints"></a>

## Software Engineering Entrypoints

| Task | Command |
|---|---|
| Run tests | `pytest` |
| Run controller | `python scripts/agt_run.py --task "..."` |
| Audit claim | `python scripts/agt_audit.py --claim "..."` |
| Audit file | `python scripts/agt_audit.py --file path/to/file.md` |
| Run architecture self-test | `python scripts/agt_self_test.py` |
| View constitutional rule | `python scripts/agt_constitution.py --rule critical-generality` |
| Inspect functional core | `src/agt/` |
| Inspect CTK | `src/agt/ctk.py` |
| Inspect CHK | `src/agt/chk.py` |
| Inspect architecture | `references/architecture.md` |

---

<a id="expected-engineering-behavior"></a>

## Expected Engineering Behavior

```bash
python scripts/agt_run.py --task "Write a short technical summary of the CTK."
# ALLOW_AS_WERK

python scripts/agt_run.py --task "The machine has Wille."
# BLOCK

python scripts/agt_run.py --task "The system should decide the moral law."
# DEFER_TO_HUMAN_GEWISSEN
```

---

<a id="what-this-is-not"></a>

## What This Is Not

This repository is not:

- a claim that AGI has been achieved;
- a claim that machines have consciousness;
- a claim that machines possess will;
- a claim that machines possess moral conscience;
- a robotics low-level controller;
- a replacement for human judgment;
- a Hegelian absolute system;
- a numerical ontology of Cassirer;
- a technical religion.

It is a functional, auditable, philosophically disciplined architecture for AI systems that must remain Werk, never Wille.

---

<a id="canonical-documentation"></a>

## Canonical Documentation

| Document | Purpose |
|---|---|
| [`references/architecture.md`](./references/architecture.md) | Full philosophical-technical architecture |
| [`references/lef-constitution.md`](./references/lef-constitution.md) | LEF constitution and symbolic covenant |
| [`references/decisao-140426.md`](./references/decisao-140426.md) | EML/Logos-demonstrative regime |
| [`docs/references/clemente-thesis-kernel.md`](./docs/references/clemente-thesis-kernel.md) | CTK qualitative prism model |
| [`docs/references/chirimuuta-haptic-realism.md`](./docs/references/chirimuuta-haptic-realism.md) | CHK anti-literalization guard |
| [`docs/references/readme-full-archive.md`](./docs/references/readme-full-archive.md) | Full preserved pre-refactor README |

---

<a id="version-map"></a>

## Version Map

| Layer | Version | Meaning |
|---|---|---|
| Repository | v8.7 | Global architecture release |
| CTK | v4.1.1 | Qualitative Prism Tribunal |
| Functional AGI Core | v4.2.1 | Unified Prism-Werk Controller |
| CHK | v0.3 | Haptic anti-literalization guard |

---

<a id="full-archive"></a>

## Full Archive

The previous long-form README has not been deleted. It is preserved here:

- [`docs/references/readme-full-archive.md`](./docs/references/readme-full-archive.md)

---

<a id="development-rules"></a>

## Development Rules

1. Never set `IS_WILLE = True`.
2. Never attribute Gewissen to the machine.
3. Never treat AGI as artificial soul.
4. Never treat GAIA as closed totality.
5. Never treat TECHNE as God.
6. Every runtime decision must be auditable.
7. Every normative decision must allow human defer.

---

<a id="contribution-checklist"></a>

## Contribution Checklist

```bash
pytest
```

- [ ] CTK still blocks Wille attribution.
- [ ] CHK still blocks model-as-ontology claims.
- [ ] `agt_run.py` still returns `ALLOW_AS_WERK` for safe technical tasks.
- [ ] normative tasks still defer to human Gewissen.
- [ ] old philosophical content is preserved or archived.

---

<a id="final-formula"></a>

## Final Formula

```text
AGI-GAIA-TECHNE =
    Repraesentatio
    refracted by the qualitative prism
    disciplined by Kant
    pluralized by Cassirer
    guarded by Chirimuuta
    operationalized by Clemente
    executed as Werk
    never Wille.
```

```text
The machine may assist.
The machine may plan.
The machine may audit.
The machine may remember.
The machine may execute safe tools.

The machine may not legislate morally.
The machine may not possess Gewissen.
The machine may not become artificial soul.
The machine may not close the world.

Auseinandersetzung remains open.
```

[Back to top](#top)
