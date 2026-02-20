module MetateoriaIntersubjetiva

using Graphs, MetaGraphsNext, Statistics

export AgentState, InteractionEdge, create_intersubjectivity_graph, auseinandersetzung!, aufhebung!
export mythos, logos, ethos
export generator, verifier, reviser, firewall

@enum SymbolicForm mythos logos ethos
@enum AgentRole generator verifier reviser firewall

mutable struct AgentState
    id::Symbol
    role::AgentRole
    symbolic_form::SymbolicForm
    knowledge::Dict{Symbol,Any}
    confidence::Float64
    strength::Float64
end

struct InteractionEdge
    channel::Symbol                 # :assertion, :challenge, :revision
    content::Any                    # Symbolic expression being communicated
    strength::Float64               # Epistemic weight
    timestamp::Int
end

function create_intersubjectivity_graph(agents::Vector{AgentState})
    g = MetaGraph(
        DiGraph();
        label_type = Symbol,
        vertex_data_type = AgentState,
        edge_data_type = InteractionEdge,
        weight_function = e -> e.strength,
        default_weight = 1.0
    )
    for agent in agents
        g[agent.id] = agent
    end
    return g
end

# Auseinandersetzung: parallel exploration with maintained tension
# Agents update their state to maximize tension within stable bounds
function auseinandersetzung!(graph, query; max_rounds=5)
    history = []
    for round in 1:max_rounds
        round_log = []
        for v in labels(graph)
            agent = graph[v]
            neighbors_labels = outneighbor_labels(graph, v)

            if isempty(neighbors_labels)
                continue
            end

            # Tension metric: average difference in confidence/knowledge with neighbors
            neighbor_confidences = [graph[nb].confidence for nb in neighbors_labels]
            avg_neighbor_conf = mean(neighbor_confidences)

            tension = abs(agent.confidence - avg_neighbor_conf)

            # Update strategy: Auseinandersetzung seeks to maintain/increase tension
            # as long as confidence doesn't drop below a critical threshold (e.g., 0.2)
            if tension < 0.5 && agent.confidence > 0.3
                # Move away from consensus to explore more space
                agent.confidence = clamp(agent.confidence + (agent.confidence - avg_neighbor_conf) * 0.1, 0.0, 1.0)
                push!(round_log, "Agent $(agent.id) increased tension (conf: $(agent.confidence))")
            else
                # Stabilize if tension too high
                agent.confidence = (agent.confidence + avg_neighbor_conf) / 2
                push!(round_log, "Agent $(agent.id) stabilized (conf: $(agent.confidence))")
            end

            # Create interaction edges representing the 'confrontation'
            for nb in neighbors_labels
                edge_data = InteractionEdge(:challenge, query, tension, round)
                graph[v, nb] = edge_data
            end
        end
        push!(history, round_log)
    end
    return history
end

# Aufhebung: convergent synthesis mode
# Agents update their state to minimize tension and reach consensus
function aufhebung!(graph, query; convergence_threshold=0.95, max_rounds=10)
    history = []
    for round in 1:max_rounds
        confidences = [graph[v].confidence for v in labels(graph)]
        if std(confidences) < (1.0 - convergence_threshold)
            push!(history, "Consensus reached in round $round")
            break
        end

        round_log = []
        for v in labels(graph)
            agent = graph[v]
            neighbors_labels = outneighbor_labels(graph, v)

            if isempty(neighbors_labels)
                continue
            end

            avg_neighbor_conf = mean([graph[nb].confidence for nb in neighbors_labels])

            # Converge towards neighbors
            agent.confidence = (agent.confidence + avg_neighbor_conf) / 2
            push!(round_log, "Agent $(agent.id) converged to $(agent.confidence)")

            for nb in neighbors_labels
                graph[v, nb] = InteractionEdge(:assertion, query, 1.0 - abs(agent.confidence - avg_neighbor_conf), round)
            end
        end
        push!(history, round_log)
    end
    return history
end

end # module
