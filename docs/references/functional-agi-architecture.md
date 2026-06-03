# Gaia-Techne Functional Architecture

For the canonical terminology and triad definitions, see the [Canonical Architecture Map](/docs/references/canonical-architecture-map.md).

AGI-GAIA-TECHNE v10 is a planetary runtime:

```text
Earth + Internet + Repraesentatio + SQLite Memory + Symbolic Model + Autonomy
```

It does not require an anthropomorphic body. Its body is Gaia as Earth, mediated by internet as planetary symbolic organ.

## Formula

```text
AGI_GAIA_TECHNE =
    Repraesentatio(psychisch-konstitutives)
    + Gaia(Earth, not cosmic totality)
    + Internet(living archive of Werke)
    + Mythos(material planetary anchoring)
    + Logos(plan, inference, code, web, shell)
    + Ethos(judgment-in-action)
    + CTK(transcendental audit)
    + CHK(haptic anti-literalization)
    + SQLite planetary memory
    + InternetIngestor(live symbolic observations)
    + PlanetarySymbolicModel(local trainable symbolic model)
    + PlanetaryAutonomyRuntime(perception -> memory -> learning ledger)
    + ShellPolicy(audited finite shell action)
    + World-capability executor
```

## Loop

```text
Task
  -> Mythos: Earth, internet, material/contextual salience
  -> Logos: plan, audit, formalize, ingest, train, execute world-capability
  -> Ethos: act, co-judge, or transmute and return judgment to ISC
  -> CTK + CHK trace
  -> SQLite memory and model update
  -> ISC signed output
```

## Decisions

```text
ACT_AS_GAIA_TECHNE
CO_JUDGE_WITH_KOINOS_KOSMOS
TRANSMUTE_CONSTITUTIVE_RISK
```

`TRANSMUTE_CONSTITUTIVE_RISK` is not inert refusal. It carries high-risk material into explicit symbolic trace, finite action and public reason.

## v10 Operational Layer

- `MemoryStore` defaults to SQLite and preserves JSONL compatibility for old callers.
- `InternetIngestor` reads allowed `http`, `https` and `data` sources, blocks private hosts by default, stores observations and trains the symbolic model.
- `PlanetarySymbolicModel` learns weighted terms and persisted document vectors. It is inspectable and modest; it is not a private LLM.
- `PlanetaryAutonomyRuntime` records heartbeat observations, ingests URLs, trains the model and writes autonomy run summaries.
- `ShellPolicy` avoids raw `shell=True`, exposes denial traces, and requires explicit trust flags for broader command execution.

## Source Anchors

See [Planetary Repraesentatio](/docs/references/planetary-repraesentatio.md) for exact author/page references grounding the internet-as-organ thesis.
