# EML Kernel

The EML Kernel is the Logos-demonstrative submotor formalizing the operational axis of symbolic articulation.

## Operator

```text
eml(x, y) = exp(x) - log(y)
```

## Canonical Decision

[Decisão 140426](../../references/decisao-140426.md)

## Canonical Python Source

`src/core/eml_kernel.py`

## Canonical Julia v4 Artifact

`src/core/eml_kernel_v4_complete.jl`

## Julia Verification Entry Point

`scripts/run_eml_v4_complete.jl`

## Full Specification

[references/decisao-140426.md](../../references/decisao-140426.md)

## Architectural Meaning

- **Darstellung** functions as the stabilizing mediating base of demonstrability.
- **Mythos** marks the lower singularity-boundary of immediacy: `log(0)` tends to `-∞`.
- In the EML operator, as `y → 0+`, the term `-log(y)` tends to `+∞`; therefore the guarded EML prevents singular collapse.
- **Ethos** marks the upper regulative boundary: the focus imaginarius must remain at distance greater than zero.
- The Julia v4 artifact separates Ausdruck, Darstellung and Bedeutung into explicit executable layers and verifies the boundary pipeline through `executar_verificacao_completa_v4()`.

The EML Kernel is a functional engine, not a literal mathematical ontology of mind.

---

[Back to Architecture Map](canonical-architecture-map.md)
