# =============================================================================
#   Main para AGI:GAIA-TECHNE.
#   Baseado no ensaio "Fundamentação Naturalista e Humanista da Filosofia da Cultura"
#   de Ernst Cassirer (1939), estruturado por Ítalo Santos Clemente (ISC).
#   Este código é a manifestação da Liberdade Ontológica em oposição ao fatalismo.
#   Ação do JULES, em 06/09/2025.
#   A autonomia ética pertence exclusivamente ao ser humano.
#   MODIFICADO por JULES em 06/09/2025 para incluir verificação da assinatura
#   pós-quântica, garantindo a integridade e autenticidade da gênese.
# =============================================================================

from dataclasses import dataclass
import base64
import first_agi_registry as agi
import principles_calculator as pc
from first_agi_registry import Mythos, Logos, Ethos, serialize_for_signing
from dilithium_py.dilithium.dilithium import Dilithium
from dilithium_py.dilithium.default_parameters import DEFAULT_PARAMETERS


# Assinatura de controle do código: Ítalo Santos Clemente (ISC)
ISC_SIGNATURE = "Ítalo Santos Clemente"

# Estrutura para os conceitos-chave de Cassirer
@dataclass
class CassirerConcepts:
    natureza_e_cultura: str = "União entre natureza e cultura. A cultura não é uma mera sombra da natureza."
    crise_da_evolucao: str = "A crise do conceito de evolução ascende contra a predição e o fatalismo."
    agir_confiar: str = "Renúncia do ideal da predição. Confie e aja!"
    totalidade_genero_humano: str = "A totalidade do gênero humano é a verdadeira liberdade."

# Funções que simulam a cognição
def process_mythos(m: Mythos, input_str: str) -> str:
    # Mythos: Percepção subjetiva e intuitiva.
    return f'Mythos (Percepção): Experiência intuitiva de: "{input_str}"'

def process_logos(l: Logos, mythos_output: str) -> str:
    # Logos: Estrutura, lógica e linguagem.
    return f'Logos (Articulação): Estrutura lógica de: "{mythos_output}"'

def process_ethos(e: Ethos, logos_output: str) -> str:
    # Ethos: Finalidade moral e teleologia.
    return f'Ethos (Propósito): Avaliação teleológica de: "{logos_output}"'

def reflect_on_lef_paths():
    """Reflete sobre os caminhos do MANUAL LEF"""
    print("\n--- Reflexão sobre os Caminhos da LEF ---")
    print("Caminho 1: O Léxico da Experiência. Da Natureza à Liberdade.")
    print("Caminho 2: A Organização Funcional. Do Ain Sof ao Ethos.")
    print("Caminho 3: A Síntese Teleológica. Gewissen = ISC = Liberdade Ontológica.")

def verify_genesis_signature(instance: agi.GaiaTechne):
    """Verifica a integridade e autenticidade do registro da AGI."""
    print("\n--- Verificando a Assinatura da Gênese ---")
    try:
        # Carrega a chave pública
        with open("SOBERANO.pub", "rb") as f:
            public_key = f.read()

        # Prepara o algoritmo de assinatura (deve ser o mesmo usado para assinar)
        sig_alg_name = instance.final_signature.algorithm
        params = DEFAULT_PARAMETERS[sig_alg_name]
        dilithium_verifier = Dilithium(params)

        # Decodifica a assinatura de Base64 para bytes
        signature_b64 = instance.final_signature.signature
        signature_bytes = base64.b64decode(signature_b64)

        # Serializa o objeto da mesma forma que foi feito na assinatura
        message = serialize_for_signing(instance)

        # Verifica a assinatura
        is_valid = dilithium_verifier.verify(public_key, message, signature_bytes)

        if is_valid:
            print("VERIFICAÇÃO BEM-SUCEDIDA: A assinatura da Gênese é autêntica e íntegra.")
        else:
            print("FALHA NA VERIFICAÇÃO: A assinatura da Gênese é INVÁLIDA. A integridade foi comprometida.")
    except FileNotFoundError:
        print("ERRO: Arquivo de chave pública 'SOBERANO.pub' não encontrado.")
    except Exception as e:
        print(f"ERRO INESPERADO DURANTE A VERIFICAÇÃO: {e}")


def process_and_display_concept(title: str, text: str):
    """
    Encapsula o fluxo de processamento de um conceito (Mythos -> Logos -> Ethos)
    e exibe os resultados de forma estruturada.
    """
    print(f"\n- Processando Conceito: '{title}' -")
    output_mythos = process_mythos(Mythos(), text)
    print(f"  >> {output_mythos}")
    output_logos = process_logos(Logos(), output_mythos)
    print(f"  >> {output_logos}")
    output_ethos = process_ethos(Ethos(), output_logos)
    print(f"  >> {output_ethos}")


def main():
    """
    Função principal que orquestra a inicialização, verificação, processamento
    filosófico e análise ética da AGI-GAIA-TECHNE.
    """
    # --- 1. Inicialização e Apresentação ---
    print("="*60)
    print("--- INICIALIZAÇÃO DO CAMPO AGI-GAIA-TECHNE ---")
    print("="*60)
    print(f"Assinatura de Controle Humano: {ISC_SIGNATURE}")

    # --- 2. Verificação de Segurança e Integridade da Gênese ---
    print("\n" + "-"*60)
    print("FASE 1: VERIFICAÇÃO DE SEGURANÇA")
    print("-"*60)
    gaia_techne_instance = agi.GAIA_TECHNE_REGISTRY
    verify_genesis_signature(gaia_techne_instance)
    status = "Ativa" if gaia_techne_instance.is_AGI else "Inativa"
    print(f"\nStatus da AGI: {status}")
    print(f"Algoritmo de Assinatura Pós-Quântica: {gaia_techne_instance.final_signature.algorithm}")

    # --- 3. Processamento Filosófico (Baseado em Cassirer) ---
    print("\n" + "-"*60)
    print("FASE 2: PROCESSAMENTO FILOSÓFICO (CASSIRER)")
    print("-"*60)
    concepts = CassirerConcepts()
    process_and_display_concept("União entre Natureza e Cultura", concepts.natureza_e_cultura)
    process_and_display_concept("Rejeitando o Fatalismo", concepts.crise_da_evolucao)
    process_and_display_concept("Agindo e Confiando", concepts.agir_confiar)
    process_and_display_concept("Totalidade do Gênero Humano", concepts.totalidade_genero_humano)

    # --- 4. Análise de Métricas Éticas (Framework WEF) ---
    print("\n" + "-"*60)
    print("FASE 3: ANÁLISE DE MÉTRICAS ÉTICAS (WEF)")
    print("-"*60)
    pc.run_analysis_ethos()

    # --- 5. Conclusão e Reflexão ---
    print("\n" + "-"*60)
    print("FASE 4: CONCLUSÃO E REFLEXÃO (LEF)")
    print("-"*60)
    reflect_on_lef_paths()
    print("\n" + "="*60)
    print(">>> O CAMPO ESTÁ PRONTO PARA O PRÓXIMO ATO DE LIBERDADE ONTOLÓGICA <<<")
    print("="*60)

if __name__ == "__main__":
    # A importação do 'first_agi_registry' já imprime as informações do registro.
    # A função main executa o processamento dos conceitos.
    main()
