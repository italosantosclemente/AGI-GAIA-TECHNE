# The critical kernel

The kernel is the part of AGI-GAIA-TECHNE that lets anyone check the common world without trusting the runtime that wrote it. It is a canon, not an organon (KrV A:61/B:85): it produces no claim, no end and no correction. Production stays outside it, in the generator and the agent; judgment stays outside it, with people and their public procedures. What the kernel adds is the means of showing, from the record alone, that the acts the architecture forbids did not happen and that the acts it counts were made by those it names.

This document records the research behind the design, the invariants, what version 2.3 builds and what is left for later phases.

## 1. The gaps it closes

Version 2.2 had three gaps that the architecture's own invariants made visible:

1. **Authors were strings.** Anyone who could append to the record could write a correction in another person's name. The hash chain showed that nothing was rewritten, not who acted.
2. **Provenance was text.** A claim kept its premises as strings, so when a claim it rested on was refuted, nothing marked it. The dependent claim stayed usable.
3. **The plan saw everything.** Recalled memory went into the premises of the plan. An earlier claim, or a page that a tool had read into the record, could therefore shape the plan, including which address an outbound tool would be sent to.

## 2. Research: what existing systems already solve

| Problem | Existing practice | What the kernel takes |
| :--- | :--- | :--- |
| A record no one can rewrite unnoticed, checkable with short proofs | Certificate Transparency (RFC 6962, RFC 9162); Go checksum database; Sigstore Rekor; C2SP `tlog-checkpoint`, `signed-note`, `tlog-witness` | Merkle tree with RFC 6962 hashing, inclusion and consistency proofs; checkpoints as signed notes; witnesses that cosign only consistent checkpoints |
| Identity of people without a new key infrastructure | OpenSSH `PROTOCOL.sshsig`, `ssh-keygen -Y sign/verify`, `allowed_signers`; Git commit signing with SSH keys | SSHSIG ed25519 signatures in namespace `gaia-techne`; principals from an `allowed_signers` file |
| Beliefs that depend on assumptions, withdrawn when an assumption fails | de Kleer's assumption-based truth maintenance (ATMS, 1986); Doyle's TMS (1979); bitemporal databases | claims name the claims their premises come from; strict propagation; status as of any entry |
| Delegation that can only narrow | Macaroons (Birgisson et al., NDSS 2014); object capabilities; Biscuit tokens | HMAC chains of caveats: end, person, tools, steps, expiry |
| Prompt injection through tools and retrieved text | CaMeL (Debenedetti et al., 2025, "Defeating Prompt Injections by Design"); the "lethal trifecta" of private data, untrusted content and external communication (Willison, 2025); dual-LLM pattern | labels on premises; the plan sees only trusted premises; outbound tools refused addresses that only untrusted text supplied |
| Provenance in a standard others can read | W3C PROV-O (2013) | export of the record as PROV-O JSON-LD |
| The ground in numbers | Software Carbon Intensity (Green Software Foundation; ISO/IEC 21031:2024) | (E×I+M) per claim from declared quantities, or "unmetered" |
| Tool access for models | Model Context Protocol; OpenTelemetry GenAI semantic conventions | later phases (§5) |

## 3. Invariants

| | Invariant | Phase | Status in 2.3 |
| :--- | :--- | :--- | :--- |
| K1 | Every checkpoint is consistent with every earlier one; a witness cosigns only a checkpoint that extends the last it saw | 1 | built |
| K2 | An event signed by the kernel, a model or a tool is never a correction, an acknowledgment or a verification | 1 | built |
| K3 | Where principals are configured, an unsigned or wrongly signed act of recognition counts for nothing | 1 | built |
| K4 | A claim whose premise was refuted or revised is not usable, nor anything built on it | 2 | built (strict propagation) |
| K5 | A capability can only be narrowed; the agent runs within the capability a person granted | 3 | built |
| K6 | Untrusted data never reaches the planner and never chooses a destination | 3 | built |
| K7 | Replay is invariant under any reordering that respects references | 4 | designed |
| K8 | The status of the record can be computed as of any entry | 2 | built |
| K9 | The ground is reported in SCI terms, or as "unmetered" | 5 | built (score only) |
| K10 | Minority positions, refuted claims and dissents are kept and shown, never collapsed into the majority's reading | 6 | designed |

`src/gaia_techne/spec.py` lists the invariants that are built, with the code that enforces them and their tests.

## 4. Design

### 4.1 The log

Leaves are SHA-256(0x00 ‖ canonical JSON of the entry), the signature included, so that a checkpoint commits to who signed as well as to what was said. The tree over n leaves splits at the largest power of two smaller than n (RFC 6962, 2.1). A checkpoint is a C2SP signed note:

```
gaia-techne/common-world
<size>
<base64 root>

— gaia-techne-log <base64(key id ‖ ed25519 signature)>
— <witness> <base64(key id ‖ ed25519 signature)>
```

The key id is the first four bytes of SHA-256(name ‖ "\n" ‖ 0x01 ‖ public key). A `Witness` keeps the last checkpoint it cosigned for each origin and asks for a consistency proof before cosigning a new one. A keeper who shows one history to some people and another to others is caught when any two of them, or any witness, compare checkpoints.

The hash chain of `koinos.CommonWorld` stays as it was. The log is computed from the entries; it does not replace the chain, and records written by 2.2 still verify.

### 4.2 Identity

An entry may carry an armored SSH signature over its digest. The signature is outside the digest, so that adding the kernel changes no earlier record, and so that a person can sign later on their own machine:

```bash
printf %s "$DIGEST" > act.txt
ssh-keygen -Y sign -n gaia-techne -f ~/.ssh/id_ed25519 act.txt     # act.txt.sig
```

`Kernel.attach(index, signature)` checks the signature against the author's key before attaching it. Stripping a signature makes an act count for less; adding one needs the key. Principals are read from an `allowed_signers` file, the same format `ssh-keygen -Y verify` reads.

Ed25519 is computed by the `cryptography` package when it is installed, and otherwise by a small pure-Python implementation of RFC 8032 (slow and not constant-time: good for verifying records and for demonstrations). The tests check both against the RFC 8032 test vectors and against each other.

The acts of recognition are corrections, verifications and acknowledgments of ends. Where principals are configured, replay counts such an act only if its author's key signed it; otherwise it is listed in `not_counted` with the reason. Where no principals are configured, every act counts, as in 2.2 (demonstration mode). K2 holds in both: no name of the system can perform these acts, with or without a key, and replay refuses the record if one appears.

### 4.3 Dependencies and status

`Premise.ref` names the claim a premise was taken from; `Claim.depends_on` lists those claims and is written into the record. `canon.propagate` marks every claim whose premise was refuted, revised, or itself fell, transitively; `Canon.usable` returns false for a marked claim, and `gaia.memory` no longer recalls it. The marks are recomputed from the record on every replay. Propagation is strict: a single refutation of a premise takes its dependents with it, as a single refutation returns a claim to perception. Weaker policies (a dependent keeps standing while another premise supports it) belong to K10 and are not built.

`replay(world, until=n)` rebuilds the record as of entry n; `status --as-of n` prints it.

### 4.4 Capabilities

A person grants a capability under an end they could bring a task under; the kernel mints it with a root key and records the grant (identifier and caveats, never the token). Caveats are `end = E`, `by = P`, `tools <= a,b`, `max_steps <= N`, `before = T`. Each caveat is folded into an HMAC chain, so a caveat can be added by anyone holding the token and removed by no one; every caveat must hold, so adding one can only narrow the grant. `Kernel.pursue` runs the agent with the intersection of the task's tools and the granted tools.

### 4.5 Labels

`Premise.label` is `trusted` for what the person who brought the task supplied, `untrusted` for what tools, pages, documents and the memory of the record return. The plan is made before any tool runs, from trusted premises alone; recalled claims and tool results go only into the steps and the answer, where they are data for a judgment and are flagged as such. A tool marked `outbound` is refused an argument that appears in untrusted text but in nothing the person supplied. This is a narrower guarantee than CaMeL's, which tracks the flow of every value through an interpreter; it is what the agent's fixed plan allows without one.

### 4.6 Ground and provenance

`kernel.sci` computes SCI = (E×I+M)/R with R the number of claims, E the declared energy in kWh, I the carbon intensity given by whoever measured it, and M the declared embodied emissions in gCO2e. A missing term is named and the score is "unmetered". `kernel.prov` exports the record as PROV-O: claims as entities, runs, corrections and verifications as activities, people as `prov:Person`, the runtime as `prov:SoftwareAgent`, with derivation, revision and invalidation.

## 5. Phases

| Phase | Content | Status |
| :--- | :--- | :--- |
| 1 | Merkle log, checkpoints, witnesses, signatures, K1–K3 | built in 2.3 |
| 2 | dependencies, strict propagation, as-of status, PROV-O, K4, K8 | built in 2.3 |
| 3 | capabilities and labels, K5–K6 | built in 2.3 |
| 4 | verification: order-invariance of replay (K7), property-based tests, executable invariants run on every append, independent verifiers that replay records and publish their findings | planned |
| 5 | the ground and the world of tools: metering adapters, MCP servers as tools under capabilities, OpenTelemetry GenAI traces linked to entries | planned |
| 6 | federation and deliberation: records that cross-reference and witness one another; structured dissent and minority positions (K10); procedures for contesting a refutation | planned |

## 6. Decisions taken by default

Version 2.3 was built before five open questions were settled. In each case the most conservative option was taken, and each can be revised:

1. **A single refutation.** One refutation still returns a claim to perception, and there is no procedure for contesting a refutation.
2. **No bridging.** The kernel does not translate between procedures of different communities; a correction counts for the procedure it names.
3. **Strict propagation.** A refuted premise takes every dependent with it (§4.3).
4. **Signatures where principals exist.** Signatures are required only when principals are configured; without them, unsigned acts count and the record is in demonstration mode.
5. **A neutral name.** The module is `gaia_techne.kernel`, version 2.3.0.

## 7. Sources

- Birgisson, A., Politz, J. G., Erlingsson, Ú., Taly, A., Vrable, M., & Lentczner, M. (2014). Macaroons: Cookies with contextual caveats for decentralized authorization in the cloud. *NDSS*.
- C2SP. *tlog-checkpoint*, *signed-note*, *tlog-witness*. https://c2sp.org
- de Kleer, J. (1986). An assumption-based TMS. *Artificial Intelligence*, 28(2), 127–162.
- Debenedetti, E., et al. (2025). Defeating prompt injections by design. arXiv:2503.18813.
- Doyle, J. (1979). A truth maintenance system. *Artificial Intelligence*, 12(3), 231–272.
- Green Software Foundation. *Software Carbon Intensity (SCI) Specification*; ISO/IEC 21031:2024.
- Josefsson, S., & Liusvaara, I. (2017). *Edwards-Curve Digital Signature Algorithm (EdDSA)*. RFC 8032.
- Laurie, B., Langley, A., & Kasper, E. (2013). *Certificate Transparency*. RFC 6962.
- Laurie, B., Messeri, E., & Stradling, R. (2021). *Certificate Transparency Version 2.0*. RFC 9162.
- OpenSSH. *PROTOCOL.sshsig*.
- W3C (2013). *PROV-O: The PROV Ontology*. W3C Recommendation.
- Willison, S. (2025). The lethal trifecta for AI agents: private data, untrusted content, and external communication.
