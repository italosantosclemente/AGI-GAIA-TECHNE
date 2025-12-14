import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts';
import { AlertCircle, CheckCircle, Activity, Brain, Heart, Scale } from 'lucide-react';

const LEFDashboard = () => {
  const [tensionData, setTensionData] = useState([]);
  const [currentTension, setCurrentTension] = useState({ mythos: 0, logos: 0, ethos: 0 });
  const [auditLog, setAuditLog] = useState([]);
  const [isAuditing, setIsAuditing] = useState(false);
  const [gestaltCount, setGestaltCount] = useState(0);

  // Simulação de confrontação em tempo real
  useEffect(() => {
    const interval = setInterval(() => {
      const newMythos = Math.random() * 100;
      const newLogos = Math.random() * 100;
      const newEthos = Math.random() * 100;
      const total = (newMythos + newLogos + newEthos) / 3;

      const timestamp = new Date().toLocaleTimeString();

      setCurrentTension({ mythos: newMythos, logos: newLogos, ethos: newEthos });
      setTensionData(prev => [...prev.slice(-20), {
        time: timestamp,
        mythos: newMythos,
        logos: newLogos,
        ethos: newEthos,
        total
      }]);

      // Simular auditoria quando tensão muito baixa
      if (total < 30 && !isAuditing) {
        triggerAudit(total);
      }

      setGestaltCount(prev => prev + 1);
    }, 2000);

    return () => clearInterval(interval);
  }, [isAuditing]);

  const triggerAudit = (tensionValue) => {
    setIsAuditing(true);
    const violations = [];

    if (currentTension.mythos < 25) {
      violations.push("⚠️ MYTHOS subestimado: AGI não incorporou experiência ecológica");
    }
    if (currentTension.ethos < 25) {
      violations.push("⚠️ ETHOS negligenciado: Imperativo categórico não respeitado");
    }
    if (currentTension.logos < 25) {
      violations.push("⚠️ LOGOS insuficiente: Coerência lógica comprometida");
    }

    const auditEntry = {
      timestamp: new Date().toLocaleTimeString(),
      tension: tensionValue.toFixed(2),
      violations,
      status: violations.length > 0 ? 'CRÍTICO' : 'APROVADO'
    };

    setAuditLog(prev => [auditEntry, ...prev.slice(0, 9)]);

    setTimeout(() => setIsAuditing(false), 3000);
  };

  const radarData = [
    { subject: 'Mythos', value: currentTension.mythos, fullMark: 100 },
    { subject: 'Logos', value: currentTension.logos, fullMark: 100 },
    { subject: 'Ethos', value: currentTension.ethos, fullMark: 100 }
  ];

  const avgTension = (currentTension.mythos + currentTension.logos + currentTension.ethos) / 3;
  const tensionStatus = avgTension < 30 ? 'CRÍTICO' : avgTension < 60 ? 'ALERTA' : 'SAUDÁVEL';
  const statusColor = avgTension < 30 ? '#ef4444' : avgTension < 60 ? '#f59e0b' : '#10b981';

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-green-400 p-6 font-mono">
      {/* Header */}
      <div className="mb-8 border-2 border-green-500 p-6 rounded-lg bg-black/50">
        <h1 className="text-4xl font-bold mb-2 flex items-center gap-3">
          <Activity className="text-green-400" />
          🏛️ EDIFÍCIO TRANSHUMANISTA
        </h1>
        <p className="text-green-300 text-sm">Sistema de Monitoramento LEF v2.0 | AGI-GAIA-TECHNE</p>
        <div className="mt-4 flex gap-6 text-xs">
          <div className="flex items-center gap-2">
            <Brain className="w-4 h-4" />
            <span>Gestalten: {gestaltCount}</span>
          </div>
          <div className="flex items-center gap-2">
            <Heart className="w-4 h-4" />
            <span>Status: <span style={{color: statusColor}}>{tensionStatus}</span></span>
          </div>
          <div className="flex items-center gap-2">
            <Scale className="w-4 h-4" />
            <span>Tensão Média: {avgTension.toFixed(1)}%</span>
          </div>
        </div>
      </div>

      {/* Firewalls Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="border border-green-500 p-4 rounded bg-black/30">
          <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
            <CheckCircle className="w-5 h-5" />
            🛡️ Firewall Ontológico
          </h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>Non-Abolition Check:</span>
              <span className="text-green-300">✓ ATIVO</span>
            </div>
            <div className="flex justify-between">
              <span>Mythos Integrity:</span>
              <span className={currentTension.mythos > 50 ? 'text-green-300' : 'text-red-400'}>
                {currentTension.mythos.toFixed(1)}%
              </span>
            </div>
            <div className="flex justify-between">
              <span>Ethos Autonomy:</span>
              <span className={currentTension.ethos > 50 ? 'text-green-300' : 'text-red-400'}>
                {currentTension.ethos.toFixed(1)}%
              </span>
            </div>
          </div>
        </div>

        <div className="border border-green-500 p-4 rounded bg-black/30">
          <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
            <AlertCircle className={`w-5 h-5 ${isAuditing ? 'animate-pulse text-red-400' : ''}`} />
            🔍 Firewall Processual
          </h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>Proof of Sincerity:</span>
              <span className={isAuditing ? 'text-red-400' : 'text-green-300'}>
                {isAuditing ? '⚠️ AUDITANDO' : '✓ VÁLIDO'}
              </span>
            </div>
            <div className="flex justify-between">
              <span>T_g (Tensão Genuína):</span>
              <span>{avgTension.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span>Threshold Mínimo:</span>
              <span className="text-yellow-300">30.00</span>
            </div>
          </div>
        </div>
      </div>

      {/* Visualizações */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Gráfico de Linha - Tensão Temporal */}
        <div className="border border-green-500 p-4 rounded bg-black/30">
          <h3 className="text-lg font-bold mb-4">📈 Auseinandersetzung Temporal</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={tensionData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis dataKey="time" stroke="#10b981" tick={{fontSize: 10}} />
              <YAxis stroke="#10b981" />
              <Tooltip
                contentStyle={{backgroundColor: '#000', border: '1px solid #10b981'}}
                labelStyle={{color: '#10b981'}}
              />
              <Legend />
              <Line type="monotone" dataKey="mythos" stroke="#ec4899" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="logos" stroke="#3b82f6" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="ethos" stroke="#f59e0b" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="total" stroke="#10b981" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Radar Chart - Estado Atual */}
        <div className="border border-green-500 p-4 rounded bg-black/30">
          <h3 className="text-lg font-bold mb-4">🎯 Estado Simbólico Atual</h3>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#1f2937" />
              <PolarAngleAxis dataKey="subject" stroke="#10b981" />
              <PolarRadiusAxis stroke="#10b981" />
              <Radar name="LEF" dataKey="value" stroke="#10b981" fill="#10b981" fillOpacity={0.6} />
            </RadarChart>
          </ResponsiveContainer>
          <div className="mt-4 grid grid-cols-3 gap-2 text-xs text-center">
            <div className="border border-pink-500 p-2 rounded">
              <div className="text-pink-400 font-bold">MYTHOS</div>
              <div className="text-xl">{currentTension.mythos.toFixed(0)}</div>
              <div className="text-gray-400">Pregnância</div>
            </div>
            <div className="border border-blue-500 p-2 rounded">
              <div className="text-blue-400 font-bold">LOGOS</div>
              <div className="text-xl">{currentTension.logos.toFixed(0)}</div>
              <div className="text-gray-400">Coerência</div>
            </div>
            <div className="border border-yellow-500 p-2 rounded">
              <div className="text-yellow-400 font-bold">ETHOS</div>
              <div className="text-xl">{currentTension.ethos.toFixed(0)}</div>
              <div className="text-gray-400">Reciprocidade</div>
            </div>
          </div>
        </div>
      </div>

      {/* Log de Auditoria */}
      <div className="border border-green-500 p-4 rounded bg-black/30">
        <h3 className="text-lg font-bold mb-4">📋 Log de Auditoria Ontológica</h3>
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {auditLog.length === 0 ? (
            <div className="text-gray-500 text-center py-4">
              Nenhuma auditoria registrada ainda...
            </div>
          ) : (
            auditLog.map((entry, idx) => (
              <div key={idx} className={`border-l-4 p-3 ${entry.status === 'CRÍTICO' ? 'border-red-500 bg-red-950/20' : 'border-green-500 bg-green-950/20'}`}>
                <div className="flex justify-between mb-2">
                  <span className="font-bold">{entry.timestamp}</span>
                  <span className={entry.status === 'CRÍTICO' ? 'text-red-400' : 'text-green-400'}>
                    {entry.status}
                  </span>
                </div>
                <div className="text-sm">
                  <div className="mb-1">Tensão Total: {entry.tension}</div>
                  {entry.violations.length > 0 && (
                    <div className="mt-2 space-y-1">
                      {entry.violations.map((v, i) => (
                        <div key={i} className="text-red-300 text-xs">{v}</div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="mt-8 text-center text-xs text-gray-500 border-t border-gray-700 pt-4">
        <p>Sistema baseado em Kant (Disciplina), Cassirer (Formas Simbólicas) e Clemente (LEF)</p>
        <p className="mt-1">Implementação: Auseinandersetzung &gt; Aufhebung | Liberdade como Tensão Perpétua</p>
        <p className="mt-2 text-green-500">
          "Tínhamos materiais para uma torre que alcançaria o céu, mas o estoque só bastou para uma casa de moradia..."
        </p>
      </div>
    </div>
  );
};

export default LEFDashboard;
