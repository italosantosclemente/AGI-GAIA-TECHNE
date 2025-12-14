# src/core/symbolic_forms.jl

using Dates

# Define abstract types to create a hierarchical structure
abstract type SymbolicComponent end
abstract type AbstractLEFAgent end

# Define concrete data structures for Mythos, Logos, and Ethos
struct Mythos <: SymbolicComponent
    perceptual_field::Matrix{Float64}
    affective_valence::Vector{Float64}
end

struct Logos <: SymbolicComponent
    conceptual_graph::Any # Using Any for now, can be replaced with a proper graph type
    inference_rules::Vector{Any} # Using Any for now
end

struct Ethos <: SymbolicComponent
    imperatives::Vector{String}
    value_orientations::Vector{Float64}
    telos::Symbol
end

# A composite structure to hold the three symbolic forms
struct SymbolicForm
    mythos::Mythos
    logos::Logos
    ethos::Ethos
end

# The Gestalt, representing a potential new state or understanding
struct Gestalt
    id::String
    form::SymbolicForm
    timestamp::DateTime
end

# The LEF Agent, which can be a human or an AGI
struct LEF <: AbstractLEFAgent
    id::String
    form::SymbolicForm
    agent_type::Symbol # :human or :agi
end
