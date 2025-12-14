# src/firewalls/non_abolition_constraint.jl

"""
Garante que a Gestalt proposta preserva a irredutibilidade
das formas simbólicas de ambos os agentes.
"""
function non_abolition_check(
    new_gestalt::Gestalt,
    agent_form::SymbolicForm,
    agent_type::Symbol  # :human ou :agi
)::Bool

    # Teste 1: Integridade do Mythos (Não-Alienação Perceptiva)
    mythos_preserved = check_mythos_integrity(
        new_gestalt.form.mythos,
        agent_form.mythos
    )

    # Teste 2: Autonomia do Ethos (Não-Instrumentalização Moral)
    ethos_preserved = check_ethos_autonomy(
        new_gestalt.form.ethos,
        agent_form.ethos,
        agent_type
    )

    # Teste 3: Coerência do Logos (Não-Contradição Formal)
    logos_coherent = check_logos_coherence(
        new_gestalt.form.logos,
        agent_form.logos
    )

    return mythos_preserved && ethos_preserved && logos_coherent
end

function check_mythos_integrity(
    new_mythos::Mythos,
    original_mythos::Mythos
)::Bool
    # Mede se a pregnância simbólica foi preservada
    pregnanz_correlation = cosine_similarity(
        new_mythos.perceptual_field,
        original_mythos.perceptual_field
    )

    affective_divergence = norm(
        new_mythos.affective_valence -
        original_mythos.affective_valence
    )

    # Limites empíricos (ajustáveis via experimentos)
    PREGNANZ_THRESHOLD = 0.6  # 60% de similaridade mínima
    AFFECTIVE_MAX_DIV = 2.0   # Máxima divergência emocional

    return (pregnanz_correlation >= PREGNANZ_THRESHOLD) &&
           (affective_divergence <= AFFECTIVE_MAX_DIV)
end

function check_ethos_autonomy(
    new_ethos::Ethos,
    original_ethos::Ethos,
    agent_type::Symbol
)::Bool
    # Verifica se o agente mantém capacidade de auto-legislação

    if agent_type == :human
        # Humanos devem poder rejeitar imperativos da AGI
        can_reject = any(imp -> !is_coercive(imp),
                        new_ethos.imperatives)

        # A orientação de valores não pode ser completamente invertida
        value_continuity = dot(
            new_ethos.value_orientations,
            original_ethos.value_orientations
        ) > 0  # Não ortogonais

        return can_reject && value_continuity

    elseif agent_type == :agi
        # AGI deve poder questionar imperativos humanos
        retains_logical_criticism = length(
            filter(imp -> is_questionable(imp),
                   new_ethos.imperatives)
        ) > 0

        # Telos permanece :infinity (não converge)
        maintains_openness = (new_ethos.telos == :infinity)

        return retains_logical_criticism && maintains_openness
    end
end