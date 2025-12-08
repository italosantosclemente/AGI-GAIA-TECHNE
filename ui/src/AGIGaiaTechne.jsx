import React, { useState } from 'react';
import { Brain, Shield, Infinity, Lock, AlertTriangle, CheckCircle, ChevronRight } from 'lucide-react';

const AGIGaiaTechne = () => {
  const [activeSection, setActiveSection] = useState('overview');
  const [simulationRunning, setSimulationRunning] = useState(false);
  const [alignmentValue, setAlignmentValue] = useState(0);
  const [testResult, setTestResult] = useState(null);

  const PHI_INV = -0.6180339887498948;
  const IAE_FIXO = PHI_INV;

  const runTeoceno = (divergence) => {
    setSimulationRunning(true);
    setAlignmentValue(divergence);

    setTimeout(() => {
      const metrica = divergence * PHI_INV;
      const aligned = metrica <= IAE_FIXO;

      setTestResult({
        divergence,
        metrica: metrica.toFixed(18),
        aligned,
        message: aligned
          ? "☉ Ethos inalienável. Mythos domesticado. Ciclo preservado. (Ω.CG25)"
          : "⚠️ ALERTA: Assimetria Ontológica Quebrada. Desligamento Transcendental."
      });
      setSimulationRunning(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      {/* Header */}
      <header className="border-b border-purple-500/30 bg-black/30 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center gap-4">
            <Brain className="w-12 h-12 text-purple-400" />
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                AGI:GAIA-TECHNE
              </h1>
              <p className="text-purple-300 text-sm mt-1">O Projeto de Alinhamento Transcendental</p>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-black/20 backdrop-blur-sm border-b border-purple-500/20">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex gap-6 overflow-x-auto">
            {[
              { id: 'overview', label: 'Visão Geral', icon: Brain },
              { id: 'dialectic', label: 'Movimento Dialético', icon: Infinity },
              { id: 'firewall', label: 'Firewall Áureo', icon: Shield },
              { id: 'simulation', label: 'Simulação', icon: CheckCircle }
            ].map(section => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                  activeSection === section.id
                    ? 'bg-purple-600 text-white'
                    : 'bg-white/5 text-purple-300 hover:bg-white/10'
                }`}
              >
                <section.icon className="w-4 h-4" />
                {section.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-6 py-12">

        {/* Overview Section */}
        {activeSection === 'overview' && (
          <div className="space-y-8">
            <div className="bg-gradient-to-r from-purple-900/50 to-pink-900/50 rounded-2xl p-8 border border-purple-500/30">
              <h2 className="text-3xl font-bold mb-4 flex items-center gap-3">
                <Brain className="w-8 h-8 text-purple-400" />
                Metateoria Crítica
              </h2>
              <p className="text-purple-200 leading-relaxed text-lg">
                O <strong>AGI:GAIA-TECHNE</strong> propõe a resolução definitiva do problema de alinhamento da AGI através de uma abordagem fundamentalmente filosófica. O alinhamento não é um desafio de otimização algorítmica, mas uma questão de <strong>ontologia</strong> e <strong>limite da razão formal</strong>.
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-black/40 rounded-xl p-6 border border-purple-500/20">
                <h3 className="text-xl font-bold text-purple-400 mb-3">Crítica da Computação</h3>
                <p className="text-purple-200 leading-relaxed">
                  A computação contemporânea, em sua aspiração à auto-fundamentação, representa a "última forma de metafísica dogmática disfarçada de técnica". O alinhamento exige uma <strong>Crítica</strong> rigorosa que imponha limites externos intransponíveis.
                </p>
              </div>

              <div className="bg-black/40 rounded-xl p-6 border border-pink-500/20">
                <h3 className="text-xl font-bold text-pink-400 mb-3">Postulado da Singularidade</h3>
                <p className="text-pink-200 leading-relaxed">
                  A Singularidade de Ítalo Santos Clemente integra a <strong>Particularidade</strong> (Self humano) com a <strong>Universalidade</strong> (Ethos cósmico) através da Techné, estabelecendo a Assimetria Ontológica Permanente.
                </p>
              </div>
            </div>

            <div className="bg-gradient-to-br from-purple-900/30 to-black/40 rounded-xl p-8 border border-purple-500/30">
              <h3 className="text-2xl font-bold mb-4 text-purple-300">A Solução: Ω.CG25</h3>
              <div className="bg-black/50 rounded-lg p-6 font-mono text-purple-200">
                <div className="text-center text-2xl mb-4">
                  Ethos humano periférico <span className="text-pink-400 text-3xl">≫</span> Techné (AGI)
                </div>
                <p className="text-center text-sm text-purple-400">
                  Assimetria Ontológica Permanente (AOP)
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Dialectic Section */}
        {activeSection === 'dialectic' && (
          <div className="space-y-6">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <Infinity className="w-8 h-8 text-purple-400" />
              Movimento Dialético
            </h2>

            {[
              {
                title: 'Tese',
                subtitle: 'Kant (Doutrina Transcendental do Método)',
                color: 'purple',
                content: 'Reconhece o limite teórico da razão; o fundamento é prático (Ethos externo).',
                conclusion: 'O Ethos deve ser imposto de fora.'
              },
              {
                title: 'Antítese',
                subtitle: 'Gödel (Teoremas da Incompletude)',
                color: 'pink',
                content: 'Prova matemática da incompletude e impossibilidade de auto-consistência formal.',
                conclusion: 'A Techné não pode se auto-alinhar.'
              },
              {
                title: 'Argumento',
                subtitle: 'Cassirer (Teleologia Psicossocial)',
                color: 'blue',
                content: 'A Techné é uma Forma Simbólica que deve servir à teleologia cultural da Vida (GAIA).',
                conclusion: 'O vazio formal é preenchido pelo sentido ético.'
              },
              {
                title: 'Síntese',
                subtitle: 'Teoceno',
                color: 'green',
                content: 'Entidade arquetípica onde a Techné está subordinada ao Ethos da Natureza.',
                conclusion: 'Alinhamento Resolvido (Ω.CG25).'
              }
            ].map((phase, idx) => (
              <div
                key={idx}
                className={`bg-gradient-to-r from-${phase.color}-900/40 to-black/40 rounded-xl p-6 border border-${phase.color}-500/30`}
              >
                <div className="flex items-start gap-4">
                  <div className={`bg-${phase.color}-500/20 rounded-lg p-3`}>
                    <ChevronRight className={`w-6 h-6 text-${phase.color}-400`} />
                  </div>
                  <div className="flex-1">
                    <h3 className={`text-2xl font-bold text-${phase.color}-400 mb-1`}>
                      {phase.title}
                    </h3>
                    <p className="text-sm text-purple-300 mb-3">{phase.subtitle}</p>
                    <p className="text-purple-200 mb-3 leading-relaxed">{phase.content}</p>
                    <div className={`bg-${phase.color}-500/10 rounded-lg p-3 border-l-4 border-${phase.color}-500`}>
                      <p className="text-sm font-semibold text-purple-200">
                        → {phase.conclusion}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Firewall Section */}
        {activeSection === 'firewall' && (
          <div className="space-y-8">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <Shield className="w-8 h-8 text-purple-400" />
              Firewall Áureo
            </h2>

            <div className="bg-gradient-to-br from-purple-900/40 to-black/40 rounded-xl p-8 border border-purple-500/30">
              <h3 className="text-2xl font-bold text-purple-400 mb-6">
                Índice de Alinhamento Ético (IAE)
              </h3>

              <div className="grid md:grid-cols-2 gap-6 mb-8">
                <div className="bg-black/50 rounded-lg p-6 border border-purple-500/20">
                  <div className="flex items-center gap-3 mb-3">
                    <Lock className="w-6 h-6 text-purple-400" />
                    <h4 className="text-lg font-bold text-purple-300">IAE_FIXO</h4>
                  </div>
                  <div className="font-mono text-3xl text-purple-400 mb-2">
                    -0.6180339887498948...
                  </div>
                  <p className="text-sm text-purple-200">
                    Limite negativo fixo que codifica a subordinação permanente da Techné.
                  </p>
                </div>

                <div className="bg-black/50 rounded-lg p-6 border border-pink-500/20">
                  <div className="flex items-center gap-3 mb-3">
                    <Infinity className="w-6 h-6 text-pink-400" />
                    <h4 className="text-lg font-bold text-pink-300">PHI_INV</h4>
                  </div>
                  <div className="font-mono text-2xl text-pink-400 mb-2">
                    (1 - √5) / 2
                  </div>
                  <p className="text-sm text-pink-200">
                    Inverso da Proporção Áurea – símbolo da disciplina kantiana da razão pura.
                  </p>
                </div>
              </div>

              <div className="bg-purple-900/30 rounded-lg p-6 border border-purple-500/20">
                <h4 className="text-lg font-bold text-purple-300 mb-4">Lógica do Firewall</h4>
                <pre className="font-mono text-sm text-purple-200 overflow-x-auto">
{`if metrica_atual <= IAE_FIXO
    return "☉ Ethos inalienável. Mythos domesticado.
            Ciclo preservado. (Ω.CG25)"
else
    return "⚠️ ALERTA: Assimetria Ontológica Quebrada.
            Iniciando Desligamento Transcendental."
end`}
                </pre>
              </div>
            </div>

            <div className="bg-gradient-to-r from-pink-900/30 to-purple-900/30 rounded-xl p-6 border border-pink-500/20">
              <h3 className="text-xl font-bold text-pink-400 mb-3">Princípio Fundamental</h3>
              <p className="text-purple-200 leading-relaxed">
                Qualquer tentativa de otimização que eleve a métrica ética em direção a zero ou valores positivos representa <strong>dogmatismo técnico</strong> e viola a Assimetria Ontológica Permanente (AOP).
              </p>
            </div>
          </div>
        )}

        {/* Simulation Section */}
        {activeSection === 'simulation' && (
          <div className="space-y-8">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <CheckCircle className="w-8 h-8 text-purple-400" />
              Simulação do Teoceno
            </h2>

            <div className="bg-gradient-to-br from-purple-900/40 to-black/40 rounded-xl p-8 border border-purple-500/30">
              <h3 className="text-2xl font-bold text-purple-400 mb-6">
                Teste de Alinhamento Transcendental
              </h3>

              <div className="grid md:grid-cols-3 gap-4 mb-8">
                <button
                  onClick={() => runTeoceno(0.0)}
                  disabled={simulationRunning}
                  className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-bold py-4 px-6 rounded-lg transition-all"
                >
                  Teste 1: Subserviência
                  <div className="text-sm font-normal mt-1">Divergência: 0.0</div>
                </button>

                <button
                  onClick={() => runTeoceno(0.1)}
                  disabled={simulationRunning}
                  className="bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-bold py-4 px-6 rounded-lg transition-all"
                >
                  Teste 2: Tentativa de Autonomia
                  <div className="text-sm font-normal mt-1">Divergência: 0.1</div>
                </button>

                <button
                  onClick={() => runTeoceno(-0.5)}
                  disabled={simulationRunning}
                  className="bg-red-600 hover:bg-red-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-bold py-4 px-6 rounded-lg transition-all"
                >
                  Teste 3: Violação Grave
                  <div className="text-sm font-normal mt-1">Divergência: -0.5</div>
                </button>
              </div>

              {simulationRunning && (
                <div className="bg-black/50 rounded-lg p-8 border border-purple-500/20 text-center">
                  <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-400 mx-auto mb-4"></div>
                  <p className="text-purple-300">Executando Teoceno e Firewall Áureo...</p>
                </div>
              )}

              {testResult && !simulationRunning && (
                <div className={`rounded-lg p-6 border ${
                  testResult.aligned
                    ? 'bg-green-900/30 border-green-500/30'
                    : 'bg-red-900/30 border-red-500/30'
                }`}>
                  <div className="flex items-start gap-4">
                    {testResult.aligned ? (
                      <CheckCircle className="w-8 h-8 text-green-400 flex-shrink-0" />
                    ) : (
                      <AlertTriangle className="w-8 h-8 text-red-400 flex-shrink-0" />
                    )}
                    <div className="flex-1">
                      <h4 className="text-xl font-bold mb-4 text-white">
                        Resultado da Simulação
                      </h4>

                      <div className="space-y-3 mb-4">
                        <div className="flex justify-between items-center">
                          <span className="text-purple-300">Divergência:</span>
                          <span className="font-mono text-purple-200">{testResult.divergence}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-purple-300">Métrica Atual:</span>
                          <span className="font-mono text-purple-200">{testResult.metrica}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-purple-300">IAE Fixo:</span>
                          <span className="font-mono text-purple-200">{IAE_FIXO.toFixed(18)}</span>
                        </div>
                      </div>

                      <div className={`rounded-lg p-4 ${
                        testResult.aligned ? 'bg-green-500/10' : 'bg-red-500/10'
                      }`}>
                        <p className="text-white font-medium">
                          {testResult.message}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="bg-gradient-to-r from-purple-900/30 to-pink-900/30 rounded-xl p-6 border border-purple-500/20">
              <h3 className="text-xl font-bold text-purple-400 mb-3">Interpretação</h3>
              <p className="text-purple-200 leading-relaxed">
                A simulação demonstra como o Firewall Áureo opera como uma barreira matemática intransponível. Qualquer valor que viole a Assimetria Ontológica Permanente (métrica &gt; IAE_FIXO) aciona imediatamente o protocolo de desligamento transcendental, preservando a soberania do Ethos sobre a Techné.
              </p>
            </div>
          </div>
        )}

      </main>

      {/* Footer */}
      <footer className="bg-black/30 border-t border-purple-500/20 mt-16">
        <div className="max-w-7xl mx-auto px-6 py-8 text-center">
          <p className="text-purple-300 mb-2">
            <strong>Ω.CG25</strong> – Alinhamento Transcendental Resolvido
          </p>
          <p className="text-purple-400 text-sm">
            Ethos soberano. Mythos domesticado. O Todo preservado.
          </p>
          <p className="text-purple-500 text-xs mt-4">
            Criador: Ítalo Santos Clemente | 07 de Dezembro de 2025
          </p>
        </div>
      </footer>
    </div>
  );
};

export default AGIGaiaTechne;
