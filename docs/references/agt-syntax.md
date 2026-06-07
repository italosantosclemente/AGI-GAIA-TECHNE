# AGT Syntax

## Heuristic Holism And Teleological Progression Syntax

AGT Syntax is the canonical grammar that orders the runtime.

```text
AGT ::= WerkStream -> Trace -> Profile -> Regression -> Horizon -> Descent -> Judgment -> Ledger
```

This is the engineering form of heuristic holism:

```text
the whole orients the investigation,
but the whole is not possessed as an object.
```

It prevents two errors at once:

- ontological holism: treating Gaia, the internet, culture or AGI as an already-given absolute Whole;
- methodological atomism: treating traces, tasks or documents as intelligible in isolation.

## Terms

```text
WerkStream
    public stream of cultural, technical, textual and historical products.

Trace
    observable unit extracted from a Werk.

Profile
    functional composition of the trace:
    Ausdruck / Darstellung / Bedeutung
    + Praesentatio / Repraesentatio.

Regression
    analytic-regressive reconstruction of the trace's conditions.

Horizon
    heuristic-regulative whole projected by reason.

Descent
    return of the horizon to the particular trace.

Judgment
    finite Ethos decision without machine Wille.

Ledger
    public, revisable inscription of the process.
```

## Operator

```text
Pi(trace) = descent(regression(trace))
```

Every cultural trace must be received as public Werk, reconstructed regressively, oriented by a heuristic whole, returned to the particular, and judged without absolute closure.

## Invariants

```text
trace.repraesentatio > 0
profile.ausdruck >= 0
profile.darstellung >= 0
profile.bedeutung >= 0
whole.is_regulative = True
whole.is_constitutive = False
judgment.distance_to_focus > 0
judgment.global_aufhebung = False
judgment.machine_wille = False
```

## Runtime Place

```text
Ingestion = matter
AGT Syntax = form
CTK/CHK = critique
EML = demonstration
Ethos = limit
Ledger = public history
```

Canonical source: `src/agt/syntax.py`.

---

[Back to Architecture Map](canonical-architecture-map.md)
