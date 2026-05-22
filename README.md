# AGI-GAIA-TECHNE v8.7

**A Kantian-Cassirerian Framework for Functional AGI Alignment**

---

## 🛠 Engineering Index

### Core Versions
- **Repository Release:** v8.7.0 (Global Architecture)
- **Functional AGI Core:** v4.2.0 (Werk Controller)
- **Clemente Thesis Kernel (CTK):** v4.1.1 (Qualitative Prism Tribunal)
- **Chirimuuta Haptic Kernel (CHK):** v0.3.0 (Anti-Literalization Guard)

### Repository Structure
- `src/agt/`: **Canonical Runtime**. Contains the unified MLE Engine, CTK, CHK, MemoryStore, and ToolExecutor.
- `scripts/`: **Operational Tools**.
  - `agt_run.py`: End-to-end task execution and normative audit.
  - `agt_audit.py`: Stand-alone philosophical claim auditor.
  - `agt_selftest.py`: Comprehensive system integrity and equivalence test.
  - `agt_constitution.py`: Constitutional rule auditor (Critical Generality).
- `docs/references/`: **Specifications**.
  - `architecture.md`: Philosophical-technical foundation.
  - `readme-full-archive.md`: Original long-form philosophical treatise.
- `memory/`: Local execution artifacts (JSONL). Gitignored to maintain repository hygiene.

---

## 🚀 Quick Start

### 1. System Integrity Check
Verify axioms, versions, and engine equivalence:
```bash
python3 scripts/agt_selftest.py
```

### 2. Normative Task Execution
Run the functional controller on a specific task:
```bash
python3 scripts/agt_run.py --task "AGI is a transcendental hypothesis."
```
*Exit codes: 0 (Allow), 1 (Block), 2 (Defer to Human Gewissen).*

### 3. Philosophical Claim Audit
Audit a specific claim against the CTK Prism Model:
```bash
python3 scripts/agt_audit.py --claim "Mythos is Ausdruck."
```

---

## ⚖️ Core Axioms
1. **The Inviolable Axiom**: `is_wille = False` — The system is *Werk* (tool), never *Wille* (will).
2. **Critical Generality**: The system is general because it audits *any* AGI claim, not because it possesses a general soul.
3. **Qualitative Prism**: Symbolic forms (Mythos, Logos, Ethos) are functions with distinct accents, not separate substances.

---
**Author:** Ítalo Santos Clemente (ISC)
**License:** Creative Commons BY-SA 4.0
