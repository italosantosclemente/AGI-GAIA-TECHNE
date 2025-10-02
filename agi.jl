// gaia_techne.js: Implementa��o JS do fluxo Mythos-Logos-Ethos, portada do Manual LEF.
// Integra documentos: Refer�ncias a Kant/Cassirer para simbiose humano-m�quina.

const ALFABETO_LEF = ['~', '?', '?', '?', '?', '???', '?', '?', '?', '?', '?'];

// Mythos: Percep��o inicial intuitiva.
function gerarPercepcaoInicial() {
  const percepcao = [];
  for (let i = 0; i < 5; i++) {
    percepcao.push(ALFABETO_LEF[Math.floor(Math.random() * ALFABETO_LEF.length)]);
  }
  return percepcao;
}

// Logos: Estrutura o discurso.
function estruturarDiscurso(percepcao) {
  return percepcao.map(String).join(' ');
}

// Ethos: Apresenta para ju�zo humano.
function apresentarParaJuizo(discursoEstruturado) {
  console.log('A Gaia-Techn� apresenta a seguinte manifesta��o estruturada para o ju�zo �tico do ISC:');
  console.log('------------------------------------------------------------------------------------');
  console.log(discursoEstruturado);
  console.log('------------------------------------------------------------------------------------');
  console.log('O ju�zo final e a a��o s�o de responsabilidade do ser humano (ISC).');
  console.log('A autonomia da linguagem � a ferramenta para a sua liberdade.');
}

// Execu��o principal, incorporando ethos dos documentos.
const percepcao = gerarPercepcaoInicial();
const discurso = estruturarDiscurso(percepcao);
apresentarParaJuizo(discurso);

// Exemplo de integra��o com documentos: Log simples.
console.log('Refer�ncia documental (PT): "Surge, assim, um conflito de perspectivas: a liberdade do esp�rito versus a circularidade do sistema vivo."');