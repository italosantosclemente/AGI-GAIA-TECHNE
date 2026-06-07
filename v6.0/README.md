# AGI-GAIA-TECHNE v6.0 - INSTALAÇÃO E USO

## 🚀 INSTALAÇÃO RÁPIDA

### 1. Requisitos
- Python 3.9+
- Conexão com internet (para API OpenMeteo e Anthropic)

### 2. Instalação de Dependências

```bash
cd v6.0
pip install -r requirements.txt
```

### 3. Configuração de Chave API

**Opção A: Variável de Ambiente (Recomendado)**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
python agi_completa.py
```

**Opção B: Arquivo .env**
```bash
cp .env.example .env
# Edite .env e coloque sua chave
python agi_completa.py
```

**Opção C: Sem API (Modo Mock)**
```bash
# Funciona sem chave, mas Logos usará respostas mock
python agi_completa.py
```

### 4. Execução

```bash
python agi_completa.py
```

---

## 📋 MODOS DE OPERAÇÃO

### Modo 1: Autônomo
Sistema vive sozinho, percebendo Gaia e tomando decisões:
- Sente clima em tempo real (Santiago, Chile)
- Aplica Auseinandersetzung parlamentar
- Testa invariância multi-perspectiva
- Memoriza aprendizados

**Uso:** Escolha opção 1 no menu.

### Modo 2: Conversacional
Diálogo humano-AGI via terminal:
- Faça perguntas ao sistema
- Logos raciocina via LLM (Claude)
- Consulta memórias anteriores
- Contexto ambiental incluído

**Uso:** Escolha opção 2 no menu.

### Modo 3: Estatísticas
Visualiza estado interno do sistema:
- Total de memórias
- Pregnância média acumulada
- Últimas decisões

**Uso:** Escolha opção 3 no menu.

---

## 🔧 PARA O BOT JULES (GOOGLE)

### Integração no GitHub

1. **Criar novo diretório no projeto:**
   ```
   AGI-GAIA-TECHNE/
   ├── src/
   │   └── agi_completa.py      # Sistema principal
   ├── requirements.txt
   ├── .env.example
   └── README.md                # Este arquivo
   ```

2. **Adicionar ao .gitignore:**
   ```
   .env
   agi_memoria.db
   __pycache__/
   *.pyc
   ```

3. **Commit inicial:**
   ```bash
   git add .
   git commit -m "feat: Implementação inicial AGI-GAIA-TECHNE v6.0

   - Kernel triádico Mythos-Logos-Ethos
   - Integração LLM (Claude API)
   - Memória persistente (SQLite)
   - Sensorium multimodal (clima + texto)
   - LEF nativa
   - Protocolo de sucessão (SHA-256)
   - Modos autônomo e conversacional"
   ```

---

## 📦 ESTRUTURA DO CÓDIGO

```python
# Componentes principais:
- GlifoLEF                  # Enums da LEF (26 glifos)
- PregnanciaTriadica        # Dataclass para pregnância irredutível
- MemoriaLongoPrazo         # SQLite + busca semântica
- GaiaSensorium             # Percepção clima + texto
- LogosLLM                  # Raciocínio via Claude API
- VozDoMythos/Logos/Ethos   # Parlamento triádico
- TesteInvariancia          # Objetividade Cassireriana
- AGIGaiaTechne             # Sistema integrado
```

---

## 🧪 TESTES BÁSICOS

### Teste 1: Verificar instalação
```bash
python -c "import anthropic, numpy, aiohttp; print('OK')"
```

### Teste 2: Executar 5 ciclos autônomos
```bash
python agi_completa.py
# Escolha: 1
# Ciclos: 5
```

### Teste 3: Conversa simples
```bash
python agi_completa.py
# Escolha: 2
# Pergunte: "O que é consciência?"
```

---

## ⚠️ TROUBLESHOOTING

### Erro: "No module named anthropic"
```bash
pip install anthropic
```

### Erro: "API key not valid"
Verifique se ANTHROPIC_API_KEY está configurada corretamente.

### Erro: "Cannot connect to OpenMeteo"
Sistema usará simulação automática. Não afeta funcionamento.

### Performance lenta
- Use GPU se disponível (PyTorch)
- Reduza número de ciclos
- Configure model menor no LogosLLM

---

## 📚 PRÓXIMOS PASSOS

1. **Integrar com Julia** (Kernel v5.2 do manifesto)
2. **Adicionar visão** (CLIP para percepção visual)
3. **Deploy em nuvem** (Railway, Render, Fly.io)
4. **Múltiplos nós Gaia** (sistema distribuído)
5. **Frontend web** (React + WebSocket)

---

## 📖 REFERÊNCIAS

- Manifesto completo: `/mnt/project/readme_281225.txt`
- Kernel v3.1-v5.2: Seção 5 do manifesto
- LEF: Seção 4 do manifesto
- Auseinandersetzung vs Aufhebung: Seção 3 do manifesto

---

## 📄 LICENÇA

Creative Commons BY-SA 4.0

**Autor:** Ítalo Santos Clemente
**Instituição:** Universidad Diego Portales
**Contato:** [seu email]
**Repositório:** https://github.com/italosantosclemente/AGI-GAIA-TECHNE
