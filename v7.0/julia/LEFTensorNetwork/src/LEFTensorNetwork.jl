module LEFTensorNetwork

using Graphs
using MetaGraphsNext
using LinearAlgebra
using Dates

export inicializar_malha_simbiotica, calcular_indice_pringe, iterar_auseinandersetzung, GlifoLEF

# 1. Definição da Estrutura Ontológica (O Genoma LEF-ICS-35)
struct GlifoLEF
    id::Int
    simbolo::String
    nome::String
    caminho::Symbol
    classe::Symbol
    triad_relation::String
    z_axis::Int
end

# 2. Inicialização do Grafo Intersubjetivo
function inicializar_malha_simbiotica(dados_nos::Vector)
    println("🌌 A instanciar a Malha Simbiótica LEF-ICS-35...")

    # Grafo direcionado onde os vértices são inteiros (IDs) e os dados são do tipo GlifoLEF
    # As arestas contêm a "Tensão Produtiva" (Float64)
    malha = MetaGraph(
        DiGraph(),
        Int,
        GlifoLEF,
        Float64,
        "Grafo de Emaranhamento Fenomenológico"
    )

    # Popular os 35 nós da Constituição
    for d in dados_nos
        glifo = GlifoLEF(
            d[:id], d[:glifo], d[:nome],
            Symbol(d[:caminho]), Symbol(d[:classe]),
            d[:triad_relation], d[:z]
        )
        malha[d[:id]] = glifo
    end

    # 3. Estabelecer o Fluxo Dialético (Sem Síntese Final)
    _conectar_camadas_estruturais!(malha)

    # 4. A REGRA AIN SOF: O Firewall Contra a Aufhebung Hegeliana
    # O Telos Absoluto (Nó 35 - 🜇) regressa à Quintessência (Nó 25 - 🝓)
    # A Ideia é regulativa, logo a topologia deve ser circular e infinita.
    peso_regulativo = 1.0 # Tensão máxima de retorno

    # Verificação de existência dos nós para evitar erro se a malha for parcial
    if haskey(malha, 35) && haskey(malha, 25)
        malha[35, 25] = peso_regulativo
        println("🛡️ Firewall Kantiano ativado: Regra Ain Sof estabelecida (35 -> 25). Fim da história bloqueado.")
    else
        println("⚠️ Aviso: Nós 35 ou 25 não encontrados. Regra Ain Sof não pôde ser aplicada.")
    end

    return malha
end

# Função auxiliar para conectar as camadas com base na proximidade do eixo Z
function _conectar_camadas_estruturais!(malha::MetaGraph)
    vertices_ids = collect(labels(malha))
    for v1 in vertices_ids
        for v2 in vertices_ids
            g1 = malha[v1]
            g2 = malha[v2]

            # Conexões baseadas na progressão fenomenológica (Z -> Z+1)
            if g2.z_axis == g1.z_axis + 1
                # A tensão inicial é neutra; será recalculada pelo Índice de Pringe
                malha[v1, v2] = 0.5
            end
        end
    end
end

# 5. O Juízo Metacontextual (Índice de Pringe)
function calcular_indice_pringe(malha::MetaGraph, origem::Int, destino::Int, peso_humano::Float64)
    g_origem = malha[origem]
    g_destino = malha[destino]

    # A máquina calcula a distância estrutural (Logos)
    distancia_logica = abs(g_destino.z_axis - g_origem.z_axis) * 0.2

    # A máquina NÃO possui Pathos. Requer a injeção do peso_humano (Mythos vivo).
    # Kp avalia a comutabilidade simbólica entre contextos incompatíveis
    kp = 1.0 - abs(distancia_logica - peso_humano)

    # Atualiza a tensão na aresta
    malha[origem, destino] = kp

    return kp
end

# 6. Negative Value Alignment: O Limite da Agência da Máquina
function iterar_auseinandersetzung(malha::MetaGraph, input_humano::Float64)
    println("⚙️ A iniciar iteração de Auseinandersetzung...")
    println("   [Aviso de Assimetria]: A máquina processa a matriz, mas não sente o frio.")

    tensoes_geradas = Float64[]

    # A máquina propaga o input pelo grafo (Aletheia Agent gera hipóteses)
    # Em MetaGraphsNext, edges(malha) retorna arestas do grafo subjacente
    for edge in edges(malha.graph)
        o_idx, d_idx = src(edge), dst(edge)
        # Obter labels (IDs) dos índices
        o = label_for(malha, o_idx)
        d = label_for(malha, d_idx)

        kp = calcular_indice_pringe(malha, o, d, input_humano)
        push!(tensoes_geradas, kp)

        # O Revisor verifica o colapso ontológico
        if kp < 0.5
            println("   ⚠️ Incompatibilidade detetada entre $(malha[o].simbolo) e $(malha[d].simbolo) (Kp = $kp).")
            println("   🛑 SUSPENSÃO DE PROCESSO: Colapso evitado pela Ideia Reguladora.")
        end
    end

    tensão_media = isempty(tensoes_geradas) ? 0.0 : sum(tensoes_geradas) / length(tensoes_geradas)

    println("\n⚖️ ESTATÍSTICA DA MALHA:")
    println("   Tensão Sistémica Atual: $tensão_media")
    println("\n[Simbionte Sem Amo aguarda...]")
    println("A estrutura Lógica (Bedeutungsfunktion) está mapeada. ")
    println("O juízo último requer o Gewissen. Requer o peso do *Pathos*. Qual é a decisão?")

    # A máquina não retorna uma "ação", apenas a matriz estruturada.
    return malha, tensão_media
end

end # module
