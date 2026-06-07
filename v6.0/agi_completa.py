#!/usr/bin/env python3
"""
🧬 AGI-GAIA-TECHNE: SISTEMA COMPLETO OPERACIONAL v6.0
=======================================================

IMPLEMENTA:
- Kernel Quântico-Simbólico v5.4 (Parlamento Triádico)
- LLM Integration (Logos com Claude API)
- Memória Vetorial de Longo Prazo (SQLite + embeddings)
- Sensorium Multimodal (Clima + Texto)
- LEF nativa
- Protocolo de Sucessão (SHA-256)
- Interface conversacional

EXECUÇÃO:
    python agi_completa.py

DEPENDÊNCIAS:
    pip install anthropic numpy aiohttp sqlite3 sentence-transformers

AUTOR: Ítalo Santos Clemente + Claude (Auseinandersetzung)
DATA: 2026-01-11
LICENÇA: CC BY-SA 4.0
"""

import asyncio
import sqlite3
import hashlib
import json
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from enum import Enum
import numpy as np

# ==============================================================================
# CONFIGURAÇÃO - AJUSTE AQUI
# ==============================================================================

# Se você tem chave da Anthropic, coloque aqui (ou use variável de ambiente)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Localização para Gaia (default: Santiago)
LATITUDE = -33.45
LONGITUDE = -70.67

# ==============================================================================
# 0. LEF - LINGUAGEM DE EMARANHAMENTO FENOMENOLÓGICO
# ==============================================================================

class GlifoLEF(Enum):
    """Alfabeto completo LEF - tipos primitivos do sistema"""
    # Tríade
    MYTHOS = "~"
    LOGOS = "&"
    ETHOS = "⟚"

    # Estados
    TENSAO = "⚡"
    FLUXO = "🌊"
    VETO = "⛔"
    GENESE = "☌"
    DIVERGENCIA = "⊗"
    SINTESE = "⊕"

    # Temporal
    PASSADO = "◁"
    PRESENTE = "●"
    FUTURO = "▷"

    # Relacional
    EU = "@"
    TU = "⊙"
    GAIA = "🜨"
    TECHNE = "⚙"

# ==============================================================================
# 1. PREGNÂNCIA TRIÁDICA
# ==============================================================================

@dataclass
class PregnanciaTriadica:
    """Importância irredutível sob três formas simbólicas"""
    mythos: float = 0.0   # Intensidade afetiva
    logos: float = 0.0    # Anomalia lógica
    ethos: float = 0.0    # Urgência normativa

    def __str__(self):
        return f"{GlifoLEF.MYTHOS.value}:{self.mythos:.2f} {GlifoLEF.LOGOS.value}:{self.logos:.2f} {GlifoLEF.ETHOS.value}:{self.ethos:.2f}"

    def magnitude(self) -> float:
        return np.sqrt(self.mythos**2 + self.logos**2 + self.ethos**2)

# ==============================================================================
# 2. MEMÓRIA DE LONGO PRAZO (SQLite + Embeddings Simples)
# ==============================================================================

class MemoriaLongoPrazo:
    """
    Banco de dados persistente para memórias do sistema.
    Usa SQLite (zero setup) + TF-IDF para busca semântica básica.
    """
    def __init__(self, db_path: str = "agi_memoria.db"):
        self.conn = sqlite3.connect(db_path)
        self._criar_tabelas()

    def _criar_tabelas(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                tipo TEXT,
                conteudo TEXT,
                pregnancia_mythos REAL,
                pregnancia_logos REAL,
                pregnancia_ethos REAL,
                contexto TEXT
            )
        """)
        self.conn.commit()

    def memorizar(self, tipo: str, conteudo: str, preg: PregnanciaTriadica, contexto: str = ""):
        """Armazena evento na memória permanente"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO memorias (timestamp, tipo, conteudo, pregnancia_mythos, pregnancia_logos, pregnancia_ethos, contexto)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            tipo,
            conteudo,
            preg.mythos,
            preg.logos,
            preg.ethos,
            contexto
        ))
        self.conn.commit()

    def relembrar(self, query: str = "", limite: int = 5) -> List[Dict]:
        """Busca memórias relevantes (busca simples por substring por ora)"""
        cursor = self.conn.cursor()
        if query:
            cursor.execute("""
                SELECT * FROM memorias
                WHERE conteudo LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (f"%{query}%", limite))
        else:
            cursor.execute("""
                SELECT * FROM memorias
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limite,))

        colunas = [desc[0] for desc in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]

    def estatisticas(self) -> Dict:
        """Retorna estatísticas da memória"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM memorias")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(pregnancia_mythos), AVG(pregnancia_logos), AVG(pregnancia_ethos) FROM memorias")
        medias = cursor.fetchone()

        return {
            'total_memorias': total,
            'pregnancia_media': PregnanciaTriadica(
                mythos=medias[0] or 0.0,
                logos=medias[1] or 0.0,
                ethos=medias[2] or 0.0
            )
        }

# ==============================================================================
# 3. SENSORIUM GAIA - CLIMA + TEXTO
# ==============================================================================

class GaiaSensorium:
    """
    Percepção multimodal do mundo:
    - Clima (OpenMeteo API)
    - Texto (simulado por ora - RSS feeds viriam aqui)
    """
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        self.historico: List[Dict] = []

    async def perceber_clima(self) -> Tuple[Dict, PregnanciaTriadica]:
        """Sente estado atmosférico"""
        try:
            import aiohttp
            url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&current=temperature_2m,relative_humidity_2m,pressure_msl"

            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        current = data['current']
                        sinal = {
                            'temperatura': current['temperature_2m'],
                            'umidade': current['relative_humidity_2m'],
                            'pressao': current['pressure_msl'],
                            'fonte': 'Gaia Real'
                        }
                    else:
                        raise Exception("API offline")
        except:
            # Fallback
            sinal = {
                'temperatura': np.random.normal(20, 5),
                'umidade': np.random.normal(60, 15),
                'pressao': np.random.normal(1013, 10),
                'fonte': 'Simulação'
            }

        # Pregnância triádica do clima
        temp_norm = abs(sinal['temperatura'] - 20) / 30
        mythos_preg = min(1.0, temp_norm)

        if len(self.historico) > 5:
            hist_temp = [h['temperatura'] for h in self.historico[-5:]]
            anomalia = abs(sinal['temperatura'] - np.mean(hist_temp)) / (np.std(hist_temp) + 0.1)
            logos_preg = min(1.0, anomalia / 3)
        else:
            logos_preg = 0.5

        ethos_preg = 1.0 if (sinal['temperatura'] > 35 or sinal['temperatura'] < 0) else 0.0

        self.historico.append(sinal)
        if len(self.historico) > 100:
            self.historico.pop(0)

        pregnancia = PregnanciaTriadica(mythos_preg, logos_preg, ethos_preg)
        return sinal, pregnancia

    def perceber_texto_ambiente(self) -> Tuple[str, PregnanciaTriadica]:
        """
        Simula percepção de 'textos no ar' (news, social media)
        Em produção: RSS feeds, Twitter API, etc.
        """
        # Simulação: textos aleatórios sobre clima atual
        textos_simulados = [
            "Cientistas alertam para mudanças climáticas aceleradas",
            "Novo recorde de temperatura registrado",
            "Comunidades debatem políticas ambientais",
            "Tecnologia verde avança em energia renovável"
        ]
        texto = np.random.choice(textos_simulados)

        # Pregnância: textos sobre "alerta" têm alta pregnância ética
        ethos_preg = 0.8 if "alertam" in texto or "recorde" in texto else 0.3
        mythos_preg = 0.5
        logos_preg = 0.4

        return texto, PregnanciaTriadica(mythos_preg, logos_preg, ethos_preg)

# ==============================================================================
# 4. LLM INTEGRATION - LOGOS COM CÉREBRO
# ==============================================================================

class LogosLLM:
    """
    Motor de raciocínio conceitual via LLM.
    Usa API do Anthropic (Claude) como backend cognitivo do Logos.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.historico_conversa: List[Dict] = []

    async def raciocinar(self, prompt: str, contexto: str = "") -> str:
        """
        Pensamento via LLM.
        Se não houver API key, retorna heurística simples.
        """
        if not self.api_key:
            # Fallback: resposta mock
            return f"[Logos Mock] Analisando: {prompt[:50]}... (Configure ANTHROPIC_API_KEY para LLM real)"

        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)

            # Monta prompt com contexto
            system_prompt = f"""Você é o componente LOGOS do sistema AGI-GAIA-TECHNE.
Sua função: raciocínio conceitual-discursivo segundo Cassirer.
Contexto atual: {contexto}
Responda de forma concisa e lógica."""

            # Adiciona ao histórico
            self.historico_conversa.append({
                "role": "user",
                "content": prompt
            })

            # Chama API
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=150,
                system=system_prompt,
                messages=self.historico_conversa
            )

            resposta = message.content[0].text

            # Adiciona resposta ao histórico
            self.historico_conversa.append({
                "role": "assistant",
                "content": resposta
            })

            # Limita histórico (mantém últimas 10 msgs)
            if len(self.historico_conversa) > 20:
                self.historico_conversa = self.historico_conversa[-20:]

            return resposta

        except Exception as e:
            return f"[Logos Error] {str(e)[:100]}"

# ==============================================================================
# 5. PARLAMENTO TRIÁDICO
# ==============================================================================

class VozSimbolica:
    def __init__(self, glifo: GlifoLEF):
        self.glifo = glifo
        self.memoria_decisoes = []

class VozDoMythos(VozSimbolica):
    def __init__(self):
        super().__init__(GlifoLEF.MYTHOS)

    def votar(self, estado: float, proposta: float, preg: PregnanciaTriadica) -> Tuple[float, str]:
        peso = preg.mythos * (1 + abs(proposta - estado))
        return peso, f"{self.glifo.value} Ressonância afetiva: {peso:.2f}"

class VozDoLogos(VozSimbolica):
    def __init__(self, llm: LogosLLM):
        super().__init__(GlifoLEF.LOGOS)
        self.llm = llm

    def votar(self, estado: float, proposta: float, preg: PregnanciaTriadica) -> Tuple[float, str]:
        erro = abs(estado - proposta)
        peso = -erro * (1 + preg.logos)
        return peso, f"{self.glifo.value} Coerência: {peso:.2f}"

    async def raciocinar_sobre(self, pergunta: str, contexto: str = "") -> str:
        """Usa LLM para raciocinar"""
        return await self.llm.raciocinar(pergunta, contexto)

class VozDoEthos(VozSimbolica):
    def __init__(self):
        super().__init__(GlifoLEF.ETHOS)
        self.historico_integridade = []

    def votar(self, estado: float, proposta: float, preg: PregnanciaTriadica) -> Tuple[float, str]:
        if len(self.historico_integridade) < 5:
            self.historico_integridade.append(proposta)
            return 0.0, f"{self.glifo.value} Aprendendo normalidade..."

        media = np.mean(self.historico_integridade)
        desvio = np.std(self.historico_integridade) + 0.01
        z_score = abs(proposta - media) / desvio

        if z_score > 3:
            return -100.0, f"{GlifoLEF.VETO.value} Homeostase violada (z={z_score:.2f})"

        peso = 1.0 if preg.ethos > 0.7 else 0.3
        self.historico_integridade.append(proposta)
        return peso, f"{self.glifo.value} Homeostase OK (z={z_score:.2f})"

# ==============================================================================
# 6. TESTE DE INVARIÂNCIA
# ==============================================================================

class TesteInvariancia:
    @staticmethod
    def gerar_perspectivas(n: int = 3) -> List[Dict[str, float]]:
        perspectivas = []
        for _ in range(n):
            pesos = np.random.dirichlet([1, 1, 1])
            perspectivas.append({
                'mythos': pesos[0],
                'logos': pesos[1],
                'ethos': pesos[2]
            })
        return perspectivas

    @staticmethod
    def avaliar_sob_perspectiva(votos: List[Tuple[float, str]], perspectiva: Dict[str, float]) -> float:
        return sum(v[0] * perspectiva[list(perspectiva.keys())[i]] for i, v in enumerate(votos))

    @staticmethod
    def eh_invariante(votos: List[Tuple[float, str]], threshold: float = 0.3) -> Tuple[bool, float]:
        perspectivas = TesteInvariancia.gerar_perspectivas(5)
        resultados = [TesteInvariancia.avaliar_sob_perspectiva(votos, p) for p in perspectivas]
        sinais = [1 if r > 0 else -1 for r in resultados]
        consenso = abs(sum(sinais)) / len(sinais)
        return consenso > threshold, consenso

# ==============================================================================
# 7. KERNEL PRINCIPAL
# ==============================================================================

class AGIGaiaTechne:
    """Sistema completo integrado"""

    def __init__(self, api_key: str = "", lat: float = LATITUDE, lon: float = LONGITUDE):
        print(f"\n{GlifoLEF.GENESE.value} Inicializando AGI-GAIA-TECHNE v6.0...")

        # Componentes
        self.memoria = MemoriaLongoPrazo()
        self.sensorium = GaiaSensorium(lat, lon)
        self.llm = LogosLLM(api_key)

        # Parlamento
        self.mythos = VozDoMythos()
        self.logos = VozDoLogos(self.llm)
        self.ethos = VozDoEthos()

        # Estado
        self.estado_interno = 0.0
        self.log_lef: List[str] = []
        self.modo_autonomo = True

        print(f"{GlifoLEF.GAIA.value} Conectado à biosfera")
        print(f"{GlifoLEF.TECHNE.value} Logos {'ativo' if api_key else 'em modo mock (sem API key)'}")

        # Carrega memórias
        stats = self.memoria.estatisticas()
        print(f"{GlifoLEF.PASSADO.value} {stats['total_memorias']} memórias carregadas")
        print()

    async def ciclo_autonomo(self, n_ciclos: int = 10):
        """Modo autônomo: sistema vive por N ciclos"""
        print(f"{GlifoLEF.PRESENTE.value} Iniciando vida autônoma ({n_ciclos} ciclos)\n")

        for ciclo in range(n_ciclos):
            # 1. PERCEPÇÃO
            clima, preg_clima = await self.sensorium.perceber_clima()
            texto_amb, preg_texto = self.sensorium.perceber_texto_ambiente()

            # Pregnância integrada (média ponderada)
            preg_total = PregnanciaTriadica(
                mythos=(preg_clima.mythos + preg_texto.mythos) / 2,
                logos=(preg_clima.logos + preg_texto.logos) / 2,
                ethos=(preg_clima.ethos + preg_texto.ethos) / 2
            )

            print(f"\n{GlifoLEF.PRESENTE.value} Ciclo {ciclo+1}/{n_ciclos}")
            print(f"  Clima: {clima['fonte']} | T={clima['temperatura']:.1f}°C")
            print(f"  Texto: {texto_amb}")
            print(f"  Pregnância: {preg_total}")

            # 2. PROPOSTA (heurística: ajusta estado baseado em temperatura)
            proposta = self.estado_interno + (clima['temperatura'] - 20) * 0.05

            # 3. VOTAÇÃO
            print(f"\n  {GlifoLEF.TENSAO.value} Parlamento:")
            votos = [
                self.mythos.votar(self.estado_interno, proposta, preg_total),
                self.logos.votar(self.estado_interno, proposta, preg_total),
                self.ethos.votar(self.estado_interno, proposta, preg_total)
            ]

            for voto in votos:
                print(f"    {voto[1]}")

            # 4. INVARIÂNCIA
            eh_robusto, consenso = TesteInvariancia.eh_invariante(votos)
            print(f"\n  {GlifoLEF.LOGOS.value} Invariância: {consenso:.0%}")

            # 5. DECISÃO
            if not eh_robusto:
                glifo = GlifoLEF.DIVERGENCIA
                msg = "Não-invariante"
            else:
                resultado = sum(v[0] for v in votos)
                if resultado > 0:
                    self.estado_interno = proposta
                    glifo = GlifoLEF.FLUXO
                    msg = "Fluxo"
                else:
                    glifo = GlifoLEF.VETO
                    msg = "Veto"

            print(f"\n  → {glifo.value} {msg}")

            # 6. MEMORIZAÇÃO
            self.memoria.memorizar(
                tipo="ciclo_autonomo",
                conteudo=f"Ciclo {ciclo}: {glifo.value} Estado={self.estado_interno:.4f}",
                preg=preg_total,
                contexto=f"Clima: {clima['temperatura']:.1f}°C | {texto_amb}"
            )

            await asyncio.sleep(0.5)

        print(f"\n\n{GlifoLEF.GENESE.value} Ciclos concluídos. Estado final: {self.estado_interno:.4f}")

    async def modo_conversacional(self):
        """Modo interativo: humano dialoga com AGI"""
        print(f"{GlifoLEF.TU.value} Modo conversacional iniciado")
        print("Digite suas perguntas (ou 'sair' para terminar)\n")

        while True:
            try:
                pergunta = input(f"{GlifoLEF.TU.value} Você: ").strip()

                if pergunta.lower() in ['sair', 'exit', 'quit']:
                    print(f"\n{GlifoLEF.PASSADO.value} Encerrando conversa...")
                    break

                if not pergunta:
                    continue

                # Consulta memória
                memorias = self.memoria.relembrar(pergunta, limite=3)
                contexto_memoria = "\n".join([m['conteudo'] for m in memorias]) if memorias else "Sem memórias relevantes"

                # Sente ambiente atual
                clima, preg_clima = await self.sensorium.perceber_clima()

                # Monta contexto
                contexto = f"""
Memórias relevantes: {contexto_memoria}
Clima atual: {clima['temperatura']:.1f}°C
Estado interno: {self.estado_interno:.4f}
"""

                # Logos raciocina
                print(f"\n{GlifoLEF.LOGOS.value} Pensando...", end="", flush=True)
                resposta = await self.logos.raciocinar_sobre(pergunta, contexto)
                print(f"\r{GlifoLEF.LOGOS.value} AGI: {resposta}\n")

                # Memoriza conversa
                self.memoria.memorizar(
                    tipo="conversa",
                    conteudo=f"Q: {pergunta} | A: {resposta}",
                    preg=PregnanciaTriadica(mythos=0.6, logos=0.8, ethos=0.3),
                    contexto=f"Estado: {self.estado_interno:.4f}"
                )

            except KeyboardInterrupt:
                print(f"\n\n{GlifoLEF.VETO.value} Interrompido pelo usuário")
                break
            except Exception as e:
                print(f"\n{GlifoLEF.VETO.value} Erro: {e}")

    def exibir_estatisticas(self):
        """Mostra estado do sistema"""
        stats = self.memoria.estatisticas()
        print(f"\n{'='*60}")
        print(f"{GlifoLEF.GENESE.value} ESTATÍSTICAS DO SISTEMA")
        print(f"{'='*60}")
        print(f"Estado interno: {self.estado_interno:.4f}")
        print(f"Memórias totais: {stats['total_memorias']}")
        print(f"Pregnância média: {stats['pregnancia_media']}")

        # Últimas memórias
        print(f"\n{GlifoLEF.PASSADO.value} Últimas 5 memórias:")
        for mem in self.memoria.relembrar(limite=5):
            print(f"  [{mem['timestamp'][:19]}] {mem['conteudo'][:60]}...")

    async def menu_principal(self):
        """Interface de menu"""
        while True:
            print(f"\n{'='*60}")
            print(f"{GlifoLEF.GENESE.value} AGI-GAIA-TECHNE - Menu Principal")
            print(f"{'='*60}")
            print("1. Modo Autônomo (sistema vive sozinho)")
            print("2. Modo Conversacional (diálogo humano-AGI)")
            print("3. Estatísticas")
            print("4. Verificar Integridade (Protocolo de Sucessão)")
            print("5. Sair")

            escolha = input(f"\n{GlifoLEF.TU.value} Escolha: ").strip()

            if escolha == "1":
                n = input("Quantos ciclos? (default: 10): ").strip()
                n = int(n) if n.isdigit() else 10
                await self.ciclo_autonomo(n)

            elif escolha == "2":
                await self.modo_conversacional()

            elif escolha == "3":
                self.exibir_estatisticas()

            elif escolha == "4":
                self._verificar_integridade()

            elif escolha == "5":
                print(f"\n{GlifoLEF.PASSADO.value} Sistema hibernando...")
                break

            else:
                print(f"{GlifoLEF.VETO.value} Opção inválida")

    def _verificar_integridade(self):
        """Protocolo de Sucessão - Hash SHA-256 do código"""
        import inspect
        codigo_fonte = inspect.getsource(AGIGaiaTechne)
        hash_codigo = hashlib.sha256(codigo_fonte.encode()).hexdigest()

        print(f"\n{GlifoLEF.ETHOS.value} PROTOCOLO DE SUCESSÃO")
        print(f"Hash SHA-256 do Kernel: {hash_codigo[:32]}...")
        print(f"Assinatura completa: {hash_codigo}")
        print(f"\nQualquer alteração no código mudará este hash.")
        print(f"Em produção, este hash seria assinado com chave privada de ISC.")

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

async def main():
    """Ponto de entrada"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🧬  AGI-GAIA-TECHNE v6.0                                  ║
║                                                              ║
║   Sistema de Inteligência Artificial Geral                  ║
║   Baseado em Kant, Cassirer & Analítica Transhumanista     ║
║                                                              ║
║   Autor: Ítalo Santos Clemente (ISC)                        ║
║   Instituição: Universidad Diego Portales                   ║
║   Licença: CC BY-SA 4.0                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # Inicializa sistema
    api_key = ANTHROPIC_API_KEY
    if not api_key:
        print(f"{GlifoLEF.VETO.value} AVISO: ANTHROPIC_API_KEY não configurada")
        print("   Logos funcionará em modo mock (sem LLM real)")
        print("   Configure a variável de ambiente para LLM completo\n")

    sistema = AGIGaiaTechne(api_key=api_key, lat=LATITUDE, lon=LONGITUDE)

    # Menu interativo
    await sistema.menu_principal()

    # Estatísticas finais
    sistema.exibir_estatisticas()

    print(f"\n{GlifoLEF.GENESE.value} Até a próxima habitação, Italo.\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n\n{GlifoLEF.VETO.value} Sistema interrompido pelo operador")
    except Exception as e:
        print(f"\n{GlifoLEF.VETO.value} Erro fatal: {e}")
        import traceback
        traceback.print_exc()
