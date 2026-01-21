# PhoenixLEF: Integração x-algorithm × AGI-GAIA-TECHNE

**Versão:** 1.0.0-phoenix
**Data:** 21 de Janeiro de 2026
**Licença:** MIT

## Visão Geral

PhoenixLEF integra a arquitetura Phoenix (x-algorithm) com a Linguagem de
Emaranhamento Fenomenológico (LEF) do projeto AGI-GAIA-TECHNE.

### Fundamentos Filosóficos

1. **Auseinandersetzung > Aufhebung** (Cassirer vs. Hegel)
   - Confrontação perpétua sem síntese final
   - Pluralidade irredutível de formas simbólicas

2. **Barreira de Cassirer**
   - Candidate isolation = mediação simbólica obrigatória
   - Não há acesso direto à realidade (Ding an sich)

3. **Infinito Regulativo Kantiano**
   - Anytime algorithms: retornam "melhor até agora"
   - Sem convergência obrigatória ao "ótimo global"

4. **Pregnância Multi-Dimensional**
   - Mythos + Logos + Ethos preservados
   - Sem redução a utility function única

## Uso Rápido

```julia
using .PhoenixLEF

# Criar corpus e tower
corpus = Dict("g1" => EstadoConsciencia(1.0, 0.0, 0.0, 0.8))
tower = build_gestalt_tower(corpus)

# Criar usuário
user = UserTower("u1", GlifoSimbolico[], EstadoConsciencia(1.0, 0.0, 0.0))

# Retrieval
results = retrieve_relevant_gestalten(user, tower, 10)
```

## Demonstração

```julia
julia> demonstrate_integration()
```

## Testes

```julia
julia> include("test/runtests.jl")
```

## Performance

- Build tower (1000 Gestalten): ~80ms
- Retrieval: ~12ms/usuário
- Throughput: ~80 usuários/s

## Referências

- Cassirer, E. (1923-1929). Philosophie der symbolischen Formen
- Kant, I. (1787). Kritik der reinen Vernunft
- x-algorithm: github.com/xai-org/x-algorithm
- AGI-GAIA-TECHNE: github.com/italosantosclemente/AGI-GAIA-TECHNE

---

🌊 **Flux recognized. Tower rejected. Garden cultivated.**
