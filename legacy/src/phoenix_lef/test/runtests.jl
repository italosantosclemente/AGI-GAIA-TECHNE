using Test
using LinearAlgebra
using Dates

include("../PhoenixLEF.jl")
using .PhoenixLEF

@testset "PhoenixLEF: Suite Completa" begin

    @testset "EstadoConsciencia: Invariantes" begin
        e = EstadoConsciencia(3.0, 4.0, 0.0)
        @test norm(e.psi) ≈ 1.0 atol=1e-10

        @test_throws ErrorException EstadoConsciencia(0.0, 0.0, 0.0)

        e2 = EstadoConsciencia(1.0, 0.0, 0.0, 1.5)
        @test e2.invariancia == 1.0
    end

    @testset "EstadoConsciencia: Operações" begin
        e1 = EstadoConsciencia(1.0, 0.0, 0.0, 0.5)
        e2 = EstadoConsciencia(0.0, 1.0, 0.0, 0.7)

        e3 = e1 + e2
        @test norm(e3.psi) ≈ 1.0 atol=1e-10

        e4 = 2.0 * e1
        @test norm(e4.psi) ≈ 1.0 atol=1e-10

        @test fidelidade(e1, e1) ≈ 1.0
    end

    @testset "Two-Tower: Retrieval" begin
        corpus = Dict(
            "g1" => EstadoConsciencia(1.0, 0.0, 0.0, 0.8),
            "g2" => EstadoConsciencia(0.0, 1.0, 0.0, 0.6),
            "g3" => EstadoConsciencia(0.0, 0.0, 1.0, 0.9)
        )

        tower = build_gestalt_tower(corpus)
        @test size(tower.embeddings) == (3, 3)

        user_state = EstadoConsciencia(1.0, 0.0, 0.0, 0.5)
        user = UserTower("test", GlifoSimbolico[], user_state)

        results = retrieve_relevant_gestalten(user, tower, 2)
        @test length(results) == 2
        @test results[1][1] == "g1"
    end

    @testset "Scoring Multi-Dimensional" begin
        weights = PregnanciaWeights(1.0, 1.0, 1.0)
        @test weights.mythos ≈ 1/3

        e = EstadoConsciencia(1.0, 0.0, 0.0, 0.0)
        score = score_multi_dimensional(e, weights)
        @test score.mythos_score ≈ 1.0
        @test score.logos_score ≈ 0.0
    end

    @testset "Firewall Ontológico" begin
        e_low = EstadoConsciencia(1.0, 0.0, 0.0, 0.1)
        e_high = EstadoConsciencia(1.0, 0.0, 0.0, 0.9)

        filtros = default_primitive_filters()
        candidatos = [("low", e_low, 0.5), ("high", e_high, 0.5)]

        filtered = apply_firewall_pipeline(candidatos, filtros, FiltroEtico[])
        @test length(filtered) == 1
        @test filtered[1][1] == "high"
    end

    @testset "Hash Embeddings" begin
        emb = hash_embedding_invariante("teste", 5)
        @test norm(emb) ≈ 1.0 atol=1e-10

        emb1 = hash_embedding_invariante("teste", 5, UInt64(0x123))
        emb2 = hash_embedding_invariante("teste", 5, UInt64(0x123))
        @test emb1 ≈ emb2
    end

    @testset "Integração End-to-End" begin
        # Definir funções auxiliares localmente ou via export
        corpus = PhoenixLEF.create_sample_corpus(50)
        tower = build_gestalt_tower(corpus)
        user = PhoenixLEF.create_sample_user()

        candidatos = retrieve_relevant_gestalten(user, tower, 20)
        @test length(candidatos) > 0

        weights = PregnanciaWeights(0.4, 0.3, 0.3)
        scored = [(id, e, score_multi_dimensional(e, weights)) for (id, e, _) in candidatos]

        candidatos_filtrar = [(id, e, sc.pregnancia) for (id, e, sc) in scored]
        filtered = apply_firewall_pipeline(candidatos_filtrar)

        @test length(filtered) ≤ length(candidatos)
    end

    @testset "Propriedades Filosóficas" begin
        # Auseinandersetzung: diversidade preservada
        corpus = Dict(
            "mythos1" => EstadoConsciencia(1.0, 0.0, 0.0),
            "mythos2" => EstadoConsciencia(0.9, 0.1, 0.0),
            "logos" => EstadoConsciencia(0.0, 1.0, 0.0)
        )
        tower = build_gestalt_tower(corpus)
        user = UserTower("u1", GlifoSimbolico[], EstadoConsciencia(1.0, 0.0, 0.0))

        results = retrieve_relevant_gestalten(user, tower, 3, diversity_penalty=0.7)
        pilares = Set([argmax(abs2.(r[2].psi)) for r in results])
        @test length(pilares) ≥ 2

        # Barreira de Cassirer: scoring isolado
        e1 = EstadoConsciencia(1.0, 0.0, 0.0, 0.5)
        weights = PregnanciaWeights()
        score1 = score_multi_dimensional(e1, weights)
        score2 = score_multi_dimensional(e1, weights)
        @test score1.pregnancia == score2.pregnancia
    end
end

println("\n" * "="^70)
println("✅ TODOS OS TESTES PASSARAM")
println("="^70)
println("🌊 Flux validated. Architecture robust.")
