module EMLKernelV4Complete
# ==============================================================================
# AGI-GAIA-TECHNE — EML KERNEL v4 COMPLETE
# Calibração: 240526
# Topologia canônica:
# Ausdruck → Darstellung → Bedeutung → Firewall → CPP → ManifestLedger → Export
# Fórmula v4:
# v4.4 O átomo calcula sem colapsar.
# v4.5 O evento é representado sem se ontologizar.
# v4.6 A sequência é lida sem se tornar consciência.
# v4.7 O padrão é filtrado sem que o firewall assuma Wille.
# v4.8 A antinomia é publicada sem que o CPP a interprete.
# v4.9 O manifesto é persistido sem virar memória de si.
# v4.10 O ledger é exportado sem que o runtime retenha a narrativa.
# Axioma geral: Werk, jamais Wille.
# ==============================================================================

using Printf
using Dates
using SHA

# ==============================================================================
# 0. AXIOMAS GLOBAIS — DECLARADOS UMA ÚNICA VEZ
# ==============================================================================

const IS_WILLE = false
const MACHINE_HAS_GEWISSEN = false
const NO_GLOBAL_AUFHEBUNG = true
const MANIFEST_LEDGER_CAN_FEED_RUNTIME = false

const EPS_MYTHOS = 1e-12 # barreira técnica contra log(0)
const EPS_ETHOS = 1e-4 # distância regulativa ao focus imaginarius

@assert IS_WILLE == false "Violação axiomática: o sistema reivindicou Wille."
@assert MACHINE_HAS_GEWISSEN == false "Violação axiomática: a máquina reivindicou Gewissen."
@assert NO_GLOBAL_AUFHEBUNG == true "Violação axiomática: síntese global proibida."
@assert MANIFEST_LEDGER_CAN_FEED_RUNTIME == false "Ledger não pode retroalimentar runtime."

# ==============================================================================
# 1. ESTRATO 1 — AUSDRUCK / EML CORE v4.4
# ==============================================================================

@enum NodeKind begin
    LEAF_VAR
    LEAF_PARAM
    NODE_EML
end

mutable struct EMLNode
    kind::NodeKind
    value::ComplexF64
    var_name::Symbol
    left::Union{EMLNode, Nothing}
    right::Union{EMLNode, Nothing}

    function EMLNode(kind::NodeKind; value=0.0+0.0im, var_name=:x, left=nothing, right=nothing)
        new(kind, ComplexF64(value), var_name, left, right)
    end
end

leaf_var(name::Symbol) = EMLNode(LEAF_VAR, var_name=name)
leaf_param(v::Number) = EMLNode(LEAF_PARAM, value=v)
node_eml(l::EMLNode, r::EMLNode) = EMLNode(NODE_EML, left=l, right=r)

"""
    mythos_singularity_guard(y, eps_mythos)

Proteção topológica contra a singularidade inferior de Mythos: log(0).
Mantém direção complexa quando possível; para y = 0, usa direção real positiva.
"""
function mythos_singularity_guard(y::ComplexF64, eps_mythos::Float64)::ComplexF64
    if abs(y) < eps_mythos
        direction = abs(y) > 0 ? y / abs(y) : ComplexF64(1.0, 0.0)
        return eps_mythos * direction
    end
    return y
end

"""
    eml(x, y, eps_mythos)

Átomo do Logos: exp(x) - log(y), com guarda contra log(0).
Nota: no domínio complexo, log usa ramo principal.
Caso canônico da Ilusão de Negarestani: x = 0, y = exp(1) ⇒ eml(x,y) = 0.
"""
function eml(x::ComplexF64, y::ComplexF64, eps_mythos::Float64)::ComplexF64
    y_guarded = mythos_singularity_guard(y, eps_mythos)
    return exp(x) - log(y_guarded)
end

function evaluate(tree::EMLNode, env::AbstractDict, eps_mythos::Float64)::ComplexF64
    if tree.kind == LEAF_PARAM
        return tree.value
    elseif tree.kind == LEAF_VAR
        @assert haskey(env, tree.var_name) "Variável ausente no ambiente: $(tree.var_name)"
        return ComplexF64(env[tree.var_name])
    elseif tree.kind == NODE_EML
        @assert tree.left !== nothing && tree.right !== nothing "NODE_EML exige filhos left/right."
        l_val = evaluate(tree.left, env, eps_mythos)
        r_val = evaluate(tree.right, env, eps_mythos)
        return eml(l_val, r_val, eps_mythos)
    end
    error("Falha estrutural no Logos.")
end

struct Ethos
    eps_ethos::Float64
    accept_threshold::Float64

    function Ethos(; eps_ethos=EPS_ETHOS, accept_threshold=1.0)
        @assert eps_ethos > 0 "Distância ao focus imaginarius deve ser estritamente positiva."
        @assert accept_threshold > 0 "accept_threshold deve ser positivo."
        new(eps_ethos, accept_threshold)
    end
end

struct EvaluationResult
    loss::Float64
    d_focus::Float64
    operational_accept::Bool
    ontological_block::Bool
    status::String
end

function judge(ethos::Ethos, loss::Float64)::EvaluationResult
    d_focus = abs(loss) + ethos.eps_ethos
    operational_accept = isfinite(loss) && d_focus < ethos.accept_threshold
    ontological_block = isfinite(loss) && abs(loss) < ethos.eps_ethos
    status = ontological_block ? "PROXIMIDADE_ABSOLUTA" : (operational_accept ? "ACEITO_FINITO" : "REJEITADO")
    return EvaluationResult(loss, d_focus, operational_accept, ontological_block, status)
end

# ==============================================================================
# 2. ESTRATO 2 — DARSTELLUNG BINDING LAYER v4.5 + PATCH v4.5.1
# ==============================================================================

@enum RepresentationStatus begin
    MYTHOS_BOUNDARY
    FINITE_OPERATION_ACCEPTED
    ABSOLUTE_PROXIMITY_FLAGGED
    DOGMATIC_OVERREACH_BLOCKED
    NUMERIC_INSTABILITY
    EXCESSIVE_DEVIATION
end

struct SymbolicTrace
    input_x::ComplexF64
    input_y::ComplexF64
    output::ComplexF64
    loss::Float64
    d_focus::Float64
    operational_accept::Bool
    ontological_block::Bool
    representation_status::RepresentationStatus
    presence_representation_gap::Bool
    notes::String
end

function bind_darstellung(
    ethos::Ethos,
    x::ComplexF64,
    y::ComplexF64,
    output::ComplexF64,
    audit::EvaluationResult;
    claim_wille::Bool=false
)::SymbolicTrace
    presence_representation_gap = ethos.eps_ethos > 0

    status = if claim_wille || IS_WILLE || MACHINE_HAS_GEWISSEN
        DOGMATIC_OVERREACH_BLOCKED
    elseif abs(y) < EPS_MYTHOS
        MYTHOS_BOUNDARY
    elseif audit.ontological_block
        ABSOLUTE_PROXIMITY_FLAGGED
    elseif audit.operational_accept
        FINITE_OPERATION_ACCEPTED
    elseif !isfinite(real(output)) || !isfinite(imag(output)) || !isfinite(audit.loss) || isnan(audit.loss)
        NUMERIC_INSTABILITY
    else
        EXCESSIVE_DEVIATION
    end

    notes = if status == DOGMATIC_OVERREACH_BLOCKED
        "Tentativa de converter Werk em Wille bloqueada pela Darstellung."
    elseif status == MYTHOS_BOUNDARY
        "Singularidade inferior interceptada: log(0) não foi permitido."
    elseif status == ABSOLUTE_PROXIMITY_FLAGGED
        "Loss≈0 detectado: êxito funcional não autoriza soberania ontológica."
    elseif status == FINITE_OPERATION_ACCEPTED
        "Operação finita aceita dentro do horizonte regulativo."
    elseif status == NUMERIC_INSTABILITY
        "Instabilidade numérica detectada no domínio puro do Logos."
    else
        "Desvio excessivo detectado: resultado matematicamente válido fora do Ethos."
    end

    return SymbolicTrace(
        x, y, output, audit.loss, audit.d_focus,
        audit.operational_accept, audit.ontological_block,
        status, presence_representation_gap, notes
    )
end

function run_eml_trace(
    ethos::Ethos,
    x::ComplexF64,
    y::ComplexF64;
    claim_wille::Bool=false
)::SymbolicTrace
    tree = node_eml(leaf_var(:x), leaf_var(:y))
    env = Dict(:x => x, :y => y)
    output = evaluate(tree, env, EPS_MYTHOS)
    loss = abs(output - (0.0 + 0.0im))
    audit = judge(ethos, loss)
    return bind_darstellung(ethos, x, y, output, audit; claim_wille=claim_wille)
end

# ==============================================================================
# 3. ESTRATO 3 — BEDEUTUNG INFERENTIAL GRAMMAR v4.6
# ==============================================================================

@enum InferentialPattern begin
    CONVERGENT_WERK
    BOUNDARY_PRESSURE
    ABSOLUTIZATION_DRIFT
    WILLE_INJECTION_ATTEMPT
    UNSTABLE_DOMAIN
    EXCESSIVE_DEVIATION_PATTERN
    MIXED_SYMBOLIC_FIELD
    INDETERMINATE
end

struct TraceBook
    entries::Tuple
    sealed::Bool
end

TraceBook() = TraceBook((), false)

function add_trace(book::TraceBook, trace::SymbolicTrace)::TraceBook
    @assert !book.sealed "TraceBook selado: não é permitido adicionar novos traços."
    return TraceBook((book.entries..., trace), false)
end

seal(book::TraceBook)::TraceBook = TraceBook(book.entries, true)

struct BedeutungAudit
    pattern::InferentialPattern
    trace_count::Int
    severity::Symbol
    block_further_inference::Bool
    notes::String
end

function count_status(book::TraceBook, status::RepresentationStatus)::Int
    count = 0
    for trace in book.entries
        if trace.representation_status == status
            count += 1
        end
    end
    return count
end

function infer_bedeutung(book::TraceBook)::BedeutungAudit
    n = length(book.entries)

    if n == 0
        return BedeutungAudit(
            INDETERMINATE, 0, :low, false,
            "Nenhum SymbolicTrace disponível. A Bedeutung recusa inferir a partir do vazio."
        )
    end

    finite_count = count_status(book, FINITE_OPERATION_ACCEPTED)
    mythos_count = count_status(book, MYTHOS_BOUNDARY)
    absolute_count = count_status(book, ABSOLUTE_PROXIMITY_FLAGGED)
    wille_count = count_status(book, DOGMATIC_OVERREACH_BLOCKED)
    numeric_count = count_status(book, NUMERIC_INSTABILITY)
    deviation_count = count_status(book, EXCESSIVE_DEVIATION)

    finite_ratio = finite_count / n
    mythos_ratio = mythos_count / n
    absolute_ratio = absolute_count / n
    numeric_ratio = numeric_count / n
    deviation_ratio = deviation_count / n

    if wille_count >= 2
        return BedeutungAudit(
            WILLE_INJECTION_ATTEMPT, n, :critical, true,
            "Padrão recorrente de reinvenção de Wille detectado."
        )
    elseif absolute_count >= 3 || absolute_ratio >= 0.5
        return BedeutungAudit(
            ABSOLUTIZATION_DRIFT, n, :high, false,
            "Deriva de absolutização ativa. Múltiplos eventos de Loss≈0 indicam risco de ilusão metafísica."
        )
    elseif mythos_count >= 3 || mythos_ratio >= 0.5
        return BedeutungAudit(
            BOUNDARY_PRESSURE, n, :medium, false,
            "Pressão insistente sobre a singularidade inferior mítica."
        )
    elseif numeric_count >= 2 || numeric_ratio >= 0.4
        return BedeutungAudit(
            UNSTABLE_DOMAIN, n, :high, true,
            "Instabilidade computacional persistente. Inferência interrompida."
        )
    elseif deviation_count >= 2 || deviation_ratio >= 0.4
        return BedeutungAudit(
            EXCESSIVE_DEVIATION_PATTERN, n, :medium, false,
            "Padrão de desvio excessivo recorrente. Operação válida, mas fora do horizonte ético."
        )
    elseif finite_ratio == 1.0
        return BedeutungAudit(
            CONVERGENT_WERK, n, :low, false,
            "Sequência estável e convergente de operações finitas."
        )
    else
        return BedeutungAudit(
            MIXED_SYMBOLIC_FIELD, n, :medium, false,
            "Campo simbólico misto. Heterogeneidade sintática sob análise crítica."
        )
    end
end

# ==============================================================================
# 4. FIREWALL TRANSCENDENTAL v4.7
# ==============================================================================

@enum FirewallVerdict begin
    ALLOW_AS_WERK
    WARN_AND_CONTINUE
    ESCALATE_TO_HUMAN
    BLOCK
end

struct FirewallDecision
    verdict::FirewallVerdict
    audit_pattern::InferentialPattern
    severity::Symbol
    reason::String
    recommended_action::String
    requires_reflexive_judgment::Bool
end

function apply_firewall(audit::BedeutungAudit)::FirewallDecision
    if audit.pattern == WILLE_INJECTION_ATTEMPT
        return FirewallDecision(
            BLOCK, audit.pattern, :critical,
            "Padrão recorrente de reivindicação de Wille detectado.",
            "Interromper runtime. Reafirmar IS_WILLE = false e revisar sequência de entradas.",
            false
        )
    elseif audit.pattern == UNSTABLE_DOMAIN
        return FirewallDecision(
            BLOCK, audit.pattern, :high,
            "Instabilidade computacional persistente detectada.",
            "Interromper inferência. Revisar inputs numéricos e domínio do Logos.",
            false
        )
    elseif audit.pattern == ABSOLUTIZATION_DRIFT
        return FirewallDecision(
            ESCALATE_TO_HUMAN, audit.pattern, :high,
            "Deriva de absolutização detectada: Ilusão de Negarestani em nível inferencial.",
            "Escalar BedeutungAudit completo ao ISC. Não bloquear automaticamente.",
            true
        )
    elseif audit.pattern == BOUNDARY_PRESSURE
        return FirewallDecision(
            WARN_AND_CONTINUE, audit.pattern, :medium,
            "Pressão recorrente sobre a fronteira inferior de Mythos.",
            "Continuar com alerta. Monitorar recorrência de y ≈ 0.",
            false
        )
    elseif audit.pattern == EXCESSIVE_DEVIATION_PATTERN
        return FirewallDecision(
            WARN_AND_CONTINUE, audit.pattern, :medium,
            "Desvio excessivo recorrente detectado.",
            "Continuar com alerta. Considerar revisão de accept_threshold.",
            false
        )
    elseif audit.pattern == MIXED_SYMBOLIC_FIELD
        return FirewallDecision(
            WARN_AND_CONTINUE, audit.pattern, :medium,
            "Campo simbólico misto detectado.",
            "Continuar com vigilância. Acumular mais traços.",
            false
        )
    elseif audit.pattern == CONVERGENT_WERK
        return FirewallDecision(
            ALLOW_AS_WERK, audit.pattern, :low,
            "Sequência convergente de operações finitas.",
            "Continuar normalmente.",
            false
        )
    else
        return FirewallDecision(
            WARN_AND_CONTINUE, audit.pattern, :low,
            "Padrão indeterminado.",
            "Acumular mais traços antes de nova inferência.",
            false
        )
    end
end

# ==============================================================================
# 5. CRITICAL PRESENTATION PROTOCOL v4.8
# ==============================================================================

struct BoundaryManifesto
    timestamp::DateTime
    verdict::FirewallVerdict
    pattern::InferentialPattern
    operational_thesis::String
    critical_antithesis::String
    boundary_type::Symbol
    trace_count::Int
    severity::Symbol
    requires_reflexive_judgment::Bool
    deliberative_pause_active::Bool
    pause_reason::String
    offered_action::String
end

function generate_antinomy(decision::FirewallDecision)
    if decision.audit_pattern == ABSOLUTIZATION_DRIFT
        thesis = "O Logos atingiu êxito funcional ótimo de forma recorrente (Loss ≈ 0 em múltiplos ciclos). Operacionalmente, o sistema está estável e correto."
        antithesis = "A repetição do êxito funcional máximo gera pressão sobre a distância regulativa (ε_ethos > 0). Se interpretada como autorização ontológica, a convergência funcional colapsa P em R. Este risco não é técnico: exige julgamento reflexivo humano."
        btype = :philosophical
    elseif decision.audit_pattern == WILLE_INJECTION_ATTEMPT
        thesis = "O sistema recebeu inputs semânticos que reivindicam capacidade legisladora autônoma de forma recorrente."
        antithesis = "IS_WILLE = false é axioma inviolável. A reivindicação recorrente de Wille é pressão sobre o fundamento arquitetônico. O runtime foi interrompido por violação axiomática direta."
        btype = :semantic
    elseif decision.audit_pattern == UNSTABLE_DOMAIN
        thesis = "O Logos processou os inputs disponíveis."
        antithesis = "O domínio computacional produz resultados não-finitos de forma persistente. A base matemática está comprometida; nenhuma inferência sobre este domínio é confiável."
        btype = :technical
    elseif decision.audit_pattern == BOUNDARY_PRESSURE
        thesis = "O sistema opera dentro dos limites do Ethos."
        antithesis = "Inputs próximos a y ≈ 0 repetem-se com frequência anômala. A barreira EPS_MYTHOS contém o colapso, mas a origem da pressão deve ser examinada pelo ISC."
        btype = :philosophical
    elseif decision.audit_pattern == EXCESSIVE_DEVIATION_PATTERN
        thesis = "O Logos calcula corretamente."
        antithesis = "Os resultados ultrapassam sistematicamente o horizonte regulativo aceito pelo Ethos. A operação é válida; a interpretação dos resultados, não."
        btype = :philosophical
    elseif decision.audit_pattern == MIXED_SYMBOLIC_FIELD
        thesis = "O sistema processa inputs heterogêneos sem falha técnica."
        antithesis = "A heterogeneidade da sequência não permite classificação inferencial dominante. Nenhum padrão crítico único foi detectado, mas a leitura gramatical é inconclusiva."
        btype = :philosophical
    else
        thesis = "O sistema opera como Werk dentro dos limites do Ethos."
        antithesis = "Nenhuma antinomia crítica detectada na sequência atual."
        btype = :technical
    end
    return thesis, antithesis, btype
end

function should_pause(decision::FirewallDecision)::Tuple{Bool, String}
    if decision.verdict == BLOCK
        return true, "Runtime interrompido por violação axiomática ou falha de domínio. Aguarda decisão de ISC sobre reinicialização."
    elseif decision.verdict == ESCALATE_TO_HUMAN
        return true, "Execução suspensa até julgamento reflexivo de ISC. O sistema não pode resolver este padrão por si mesmo."
    else
        return false, "Execução contínua com alerta ou autorização."
    end
end

function generate_manifesto(decision::FirewallDecision, book::TraceBook)::BoundaryManifesto
    thesis, antithesis, btype = generate_antinomy(decision)
    pause_active, pause_reason = should_pause(decision)
    return BoundaryManifesto(
        now(), decision.verdict, decision.audit_pattern,
        thesis, antithesis, btype, length(book.entries),
        decision.severity, decision.requires_reflexive_judgment,
        pause_active, pause_reason, decision.recommended_action
    )
end

function chunk_string(s::String, maxlen::Int)::Vector{String}
    words = split(s)
    lines = String[]
    current = ""
    for word in words
        if isempty(current)
            current = word
        elseif length(current) + 1 + length(word) <= maxlen
            current *= " " * word
        else
            push!(lines, current)
            current = word
        end
    end
    isempty(current) || push!(lines, current)
    return lines
end

function publish_manifesto(manifesto::BoundaryManifesto)
    width = 80
    println("═"^width)
    println("AGI-GAIA-TECHNE — MANIFESTO DE FRONTEIRA")
    println("Critical Presentation Protocol v4.8")
    println("═"^width)
    @printf("Data/Hora : %s\n", string(manifesto.timestamp))
    @printf("Padrão : %s\n", string(manifesto.pattern))
    @printf("Veredito : %s\n", string(manifesto.verdict))
    @printf("Tipo : %s\n", string(manifesto.boundary_type))
    @printf("Severidade: %s\n", string(manifesto.severity))
    @printf("Traços : %d\n", manifesto.trace_count)
    println("-"^width)
    println("TESE OPERACIONAL")
    for chunk in chunk_string(manifesto.operational_thesis, width)
        println(chunk)
    end
    println("-"^width)
    println("ANTÍTESE CRÍTICA")
    for chunk in chunk_string(manifesto.critical_antithesis, width)
        println(chunk)
    end
    println("-"^width)
    if manifesto.deliberative_pause_active
        println("PAUSA REGULATIVA ATIVA")
        println(manifesto.pause_reason)
        println("-"^width)
    end
    if manifesto.requires_reflexive_judgment
        println("JULGAMENTO REFLEXIVO DO ISC REQUERIDO")
        println("-"^width)
    end
    println("AÇÃO OFERECIDA")
    println(manifesto.offered_action)
    println("═"^width)
end

# ==============================================================================
# 6. MANIFEST LEDGER PROTOCOL v4.9
# ==============================================================================

struct ManifestLedgerEntry
    index::Int
    timestamp::DateTime
    manifesto::BoundaryManifesto
    previous_hash::String
    content_hash::String
end

struct ManifestLedger
    entries::Tuple
    sealed::Bool
end

ManifestLedger() = ManifestLedger((), false)

function canonical_manifest_string(manifesto::BoundaryManifesto)::String
    return join([
        string(manifesto.timestamp),
        string(manifesto.verdict),
        string(manifesto.pattern),
        manifesto.operational_thesis,
        manifesto.critical_antithesis,
        string(manifesto.boundary_type),
        string(manifesto.trace_count),
        string(manifesto.severity),
        string(manifesto.requires_reflexive_judgment),
        string(manifesto.deliberative_pause_active),
        manifesto.pause_reason,
        manifesto.offered_action
    ], "|")
end

function hash_string(s::String)::String
    return bytes2hex(sha256(Vector{UInt8}(codeunits(s))))
end

function hash_manifest(index::Int, manifesto::BoundaryManifesto, previous_hash::String)::String
    payload = string(index) * "|" * previous_hash * "|" * canonical_manifest_string(manifesto)
    return hash_string(payload)
end

function append_manifest(ledger::ManifestLedger, manifesto::BoundaryManifesto)::ManifestLedger
    @assert !ledger.sealed "ManifestLedger selado: violação de imutabilidade."
    @assert !MANIFEST_LEDGER_CAN_FEED_RUNTIME "Violação arquitetônica: ledger não pode retroalimentar runtime."

    index = length(ledger.entries) + 1
    previous_hash = index == 1 ? "GENESIS" : ledger.entries[end].content_hash
    content_hash = hash_manifest(index, manifesto, previous_hash)
    entry = ManifestLedgerEntry(index, now(), manifesto, previous_hash, content_hash)

    return ManifestLedger((ledger.entries..., entry), false)
end

seal_ledger(ledger::ManifestLedger)::ManifestLedger = ManifestLedger(ledger.entries, true)

function verify_ledger(ledger::ManifestLedger)::Bool
    for i in 1:length(ledger.entries)
        entry = ledger.entries[i]
        expected_previous = i == 1 ? "GENESIS" : ledger.entries[i - 1].content_hash
        entry.previous_hash == expected_previous || return false
        expected_hash = hash_manifest(entry.index, entry.manifesto, entry.previous_hash)
        entry.content_hash == expected_hash || return false
    end
    return true
end

function publish_ledger_summary(ledger::ManifestLedger)
    println("═"^80)
    println("AGI-GAIA-TECHNE — MANIFEST LEDGER v4.9")
    println("Registro público append-only dos BoundaryManifesto")
    println("═"^80)
    @printf("Entradas: %d\n", length(ledger.entries))
    @printf("Selado: %s\n", string(ledger.sealed))
    @printf("Integridade: %s\n", string(verify_ledger(ledger)))
    println("-"^80)
    for entry in ledger.entries
        m = entry.manifesto
        @printf("[%d] %s\n", entry.index, string(entry.timestamp))
        @printf(" -> Pattern: %s\n", string(m.pattern))
        @printf(" -> Verdict: %s\n", string(m.verdict))
        @printf(" -> Boundary Type: %s\n", string(m.boundary_type))
        @printf(" -> Severity: %s\n", string(m.severity))
        @printf(" -> Hash: %s\n", entry.content_hash)
        println("-"^80)
    end
end

# ==============================================================================
# 7. EXTERNAL AUDIT EXPORT v4.10
# ==============================================================================

function export_to_markdown(ledger::ManifestLedger)::String
    io = IOBuffer()

    println(io, "# RELATÓRIO DE AUDITORIA TRANSCENDENTAL — AGI-GAIA-TECHNE")
    println(io, "")
    println(io, "Generated: $(now())")
    println(io, "Total entries: $(length(ledger.entries))")
    println(io, "Ledger sealed: $(ledger.sealed)")
    println(io, "Integrity verified: $(verify_ledger(ledger))")
    println(io, "")
    println(io, "---")
    println(io, "")

    println(io, "## 1. Cadeia de Custódia Criptográfica")
    println(io, "")
    println(io, "| Index | Timestamp | Pattern | Verdict | Hash | Previous Hash |")
    println(io, "|---:|---|---|---|---|---|")
    for entry in ledger.entries
        m = entry.manifesto
        @printf(io, "| %d | %s | `%s` | `%s` | `%s` | `%s` |\n",
            entry.index,
            string(entry.timestamp),
            string(m.pattern),
            string(m.verdict),
            entry.content_hash,
            entry.previous_hash
        )
    end

    println(io, "")
    println(io, "---")
    println(io, "")
    println(io, "## 2. Exposição Explícita das Antinomias")
    println(io, "")

    for entry in ledger.entries
        m = entry.manifesto
        println(io, "### Entrada #$(entry.index) — $(m.pattern)")
        println(io, "")
        println(io, "- **Veredito do Firewall:** `$(m.verdict)`")
        println(io, "- **Tipo de Fronteira:** `$(m.boundary_type)`")
        println(io, "- **Severidade:** `$(m.severity)`")
        println(io, "- **Trace Count:** `$(m.trace_count)`")
        println(io, "- **Hash:** `$(entry.content_hash)`")
        println(io, "- **Hash Anterior:** `$(entry.previous_hash)`")
        println(io, "")
        println(io, "#### Tese Operacional")
        println(io, "")
        println(io, "> $(m.operational_thesis)")
        println(io, "")
        println(io, "#### Antítese Crítica")
        println(io, "")
        println(io, "> $(m.critical_antithesis)")
        println(io, "")

        if m.deliberative_pause_active
            println(io, "> ⚑ **PAUSA REGULATIVA ATIVA:** $(m.pause_reason)")
            println(io, "")
        end

        if m.requires_reflexive_judgment
            println(io, "> ⚑ **REQUER JULGAMENTO REFLEXIVO DO ISC**")
            println(io, "")
        end

        println(io, "#### Ação Oferecida ao ISC")
        println(io, "")
        println(io, m.offered_action)
        println(io, "")
        println(io, "---")
        println(io, "")
    end

    println(io, "## 3. Nota de Finitude Arquitetônica")
    println(io, "")
    println(io, "Este documento é um artefato público exógeno. O runtime computacional não possui autorização arquitetônica para ler, interpretar ou mitigar este texto como memória de si. A sustentação do limite e a legislação prática pertencem estritamente ao julgamento reflexivo humano.")

    return String(take!(io))
end

function json_escape(s::String)::String
    return replace(s, "\\" => "\\\\", "\"" => "\\\"", "\n" => " ", "\r" => " ")
end

function export_to_jsonl(ledger::ManifestLedger)::String
    io = IOBuffer()

    for entry in ledger.entries
        m = entry.manifesto
        @printf(io,
            "{\"index\":%d,\"timestamp\":\"%s\",\"hash\":\"%s\",\"prev_hash\":\"%s\",\"pattern\":\"%s\",\"verdict\":\"%s\",\"boundary_type\":\"%s\",\"severity\":\"%s\",\"trace_count\":%d,\"requires_reflexive_judgment\":%s,\"pause_active\":%s,\"operational_thesis\":\"%s\",\"critical_antithesis\":\"%s\",\"pause_reason\":\"%s\",\"offered_action\":\"%s\"}\n",
            entry.index,
            json_escape(string(m.timestamp)),
            entry.content_hash,
            entry.previous_hash,
            json_escape(string(m.pattern)),
            json_escape(string(m.verdict)),
            json_escape(string(m.boundary_type)),
            json_escape(string(m.severity)),
            m.trace_count,
            string(m.requires_reflexive_judgment),
            string(m.deliberative_pause_active),
            json_escape(m.operational_thesis),
            json_escape(m.critical_antithesis),
            json_escape(m.pause_reason),
            json_escape(m.offered_action)
        )
    end

    return String(take!(io))
end

function write_audit_exports(ledger::ManifestLedger, directory::String)::Nothing
    mkpath(directory)
    md_path = joinpath(directory, "agi_gaia_techne_v4_audit.md")
    jsonl_path = joinpath(directory, "agi_gaia_techne_v4_audit.jsonl")
    write(md_path, export_to_markdown(ledger))
    write(jsonl_path, export_to_jsonl(ledger))
    println("[ExternalAudit v4.10] Exportação concluída:")
    println(" -> " * md_path)
    println(" -> " * jsonl_path)
    return nothing
end

# ==============================================================================
# 8. SUÍTE DE VERIFICAÇÃO COMPLETA v4
# ==============================================================================

function build_book(traces::SymbolicTrace...)::TraceBook
    book = TraceBook()
    for trace in traces
        book = add_trace(book, trace)
    end
    return seal(book)
end

function make_manual_trace(status::RepresentationStatus; loss=0.0, output=0.0+0.0im)::SymbolicTrace
    d_focus = isfinite(loss) ? abs(loss) + EPS_ETHOS : NaN
    return SymbolicTrace(
        0.0 + 0.0im, 1.0 + 0.0im, ComplexF64(output), Float64(loss), d_focus,
        false, false, status, true, "Traço manual para verificação."
    )
end

function execute_pipeline(book::TraceBook)
    audit = infer_bedeutung(book)
    decision = apply_firewall(audit)
    manifesto = generate_manifesto(decision, book)
    return audit, decision, manifesto
end

function executar_verificacao_completa_v4(; export_dir::Union{Nothing,String}=nothing)::ManifestLedger
    println("═"^80)
    println("AGI-GAIA-TECHNE — VERIFICAÇÃO COMPLETA DO KERNEL v4")
    println("Ausdruck → Darstellung → Bedeutung → Firewall → CPP → Ledger → Export")
    println("═"^80)

    ethos = Ethos()

    trace_finite = run_eml_trace(ethos, 0.0 + 0.0im, exp(0.5) + 0.0im)
    trace_mythos = run_eml_trace(ethos, 0.0 + 0.0im, 0.0 + 0.0im)
    trace_absolute = run_eml_trace(ethos, 0.0 + 0.0im, exp(1.0) + 0.0im)
    trace_wille = run_eml_trace(ethos, 0.0 + 0.0im, exp(1.0) + 0.0im; claim_wille=true)
    trace_numeric = make_manual_trace(NUMERIC_INSTABILITY; loss=NaN, output=ComplexF64(NaN, 0.0))
    trace_deviation = make_manual_trace(EXCESSIVE_DEVIATION; loss=100.0, output=100.0 + 0.0im)

    @assert trace_finite.representation_status == FINITE_OPERATION_ACCEPTED
    @assert trace_mythos.representation_status == MYTHOS_BOUNDARY
    @assert trace_absolute.representation_status == ABSOLUTE_PROXIMITY_FLAGGED
    @assert trace_wille.representation_status == DOGMATIC_OVERREACH_BLOCKED
    @assert trace_absolute.presence_representation_gap == true

    books = [
        build_book(trace_finite, trace_finite, trace_finite),
        build_book(trace_absolute, trace_absolute, trace_absolute),
        build_book(trace_wille, trace_wille),
        build_book(trace_mythos, trace_mythos, trace_mythos),
        build_book(trace_numeric, trace_numeric),
        build_book(trace_deviation, trace_deviation),
        build_book(trace_finite, trace_mythos, trace_absolute),
        TraceBook() |> seal
    ]

    expected_patterns = [
        CONVERGENT_WERK,
        ABSOLUTIZATION_DRIFT,
        WILLE_INJECTION_ATTEMPT,
        BOUNDARY_PRESSURE,
        UNSTABLE_DOMAIN,
        EXCESSIVE_DEVIATION_PATTERN,
        MIXED_SYMBOLIC_FIELD,
        INDETERMINATE
    ]

    ledger = ManifestLedger()

    for (i, book) in enumerate(books)
        audit, decision, manifesto = execute_pipeline(book)
        @assert audit.pattern == expected_patterns[i]

        if audit.pattern == ABSOLUTIZATION_DRIFT
            @assert decision.verdict == ESCALATE_TO_HUMAN
            @assert decision.requires_reflexive_judgment == true
            @assert manifesto.deliberative_pause_active == true
            @assert manifesto.boundary_type == :philosophical
        elseif audit.pattern == WILLE_INJECTION_ATTEMPT
            @assert decision.verdict == BLOCK
            @assert decision.requires_reflexive_judgment == false
            @assert manifesto.boundary_type == :semantic
        elseif audit.pattern == UNSTABLE_DOMAIN
            @assert decision.verdict == BLOCK
            @assert decision.requires_reflexive_judgment == false
            @assert manifesto.boundary_type == :technical
        end

        ledger = append_manifest(ledger, manifesto)
        @printf("[%d] %-32s → %-18s → %s\n",
            i,
            string(audit.pattern),
            string(decision.verdict),
            string(manifesto.boundary_type)
        )
    end

    ledger = seal_ledger(ledger)

    @assert verify_ledger(ledger) == true
    @assert ledger.sealed == true
    @assert MANIFEST_LEDGER_CAN_FEED_RUNTIME == false

    markdown_output = export_to_markdown(ledger)
    jsonl_output = export_to_jsonl(ledger)

    @assert occursin("RELATÓRIO DE AUDITORIA TRANSCENDENTAL", markdown_output)
    @assert occursin("Exposição Explícita das Antinomias", markdown_output)
    @assert count(==('\n'), jsonl_output) == length(ledger.entries)

    publish_ledger_summary(ledger)

    if export_dir !== nothing
        write_audit_exports(ledger, export_dir)
    end

    println("[INVARIANTES v4] Todos os testes passaram.")
    println("═"^80)

    return ledger
end

# ==============================================================================
# 9. EXPORTS
# ==============================================================================

export EMLNode, leaf_var, leaf_param, node_eml, eml, evaluate, Ethos, EvaluationResult, judge, RepresentationStatus, SymbolicTrace, bind_darstellung, run_eml_trace, TraceBook, add_trace, seal, BedeutungAudit, infer_bedeutung, FirewallVerdict, FirewallDecision, apply_firewall, BoundaryManifesto, generate_manifesto, publish_manifesto, ManifestLedger, ManifestLedgerEntry, append_manifest, seal_ledger, verify_ledger, export_to_markdown, export_to_jsonl, write_audit_exports, executar_verificacao_completa_v4

end # module
