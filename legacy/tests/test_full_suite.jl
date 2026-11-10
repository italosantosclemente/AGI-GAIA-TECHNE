using Test

@testset "AGI-GAIA-TECHNE Full Test Suite" begin
    include("../carregar_alfabeto.jl")
    ALFABETO_LEF = carregar_alfabeto()
    include("test_analitica_vida_simbolica.jl")
    include("test_gerador_narrativas.jl")
    include("test_calculate_harmony_index.jl")
    include("test_eco_semente.jl")
    include("test_conjecture.jl")
    include("test_techne_score_calculator.jl")
end
