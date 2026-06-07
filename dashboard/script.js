const API_BASE = window.location.protocol === 'file:' ? 'http://localhost:5000' : '';

let harmonyData = [];
let harmonyChart;
let metricsChart;

const elements = {
    synergySlider: document.getElementById('synergy-slider'),
    synergyValue: document.getElementById('synergy-value'),
    statusPill: document.getElementById('status-pill'),
    techneValue: document.getElementById('techne-value'),
    iaeValue: document.getElementById('iae-value'),
    harmonyValue: document.getElementById('harmony-value'),
    ethosValue: document.getElementById('ethos-value'),
    conjectureInput: document.getElementById('conjecture-input'),
    narrativeOutput: document.getElementById('narrative-output'),
    summaryOutput: document.getElementById('summary-output'),
    flagsOutput: document.getElementById('flags-output'),
    documentCount: document.getElementById('document-count'),
    principalDocuments: document.getElementById('principal-documents'),
    runButton: document.getElementById('run-button'),
    submitButton: document.getElementById('submit-button'),
    vetoButton: document.getElementById('veto-button'),
};

async function fetchJson(path) {
    const response = await fetch(`${API_BASE}${path}`);
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
}

function currentQuery() {
    const leap = elements.synergySlider.value;
    const conjecture = encodeURIComponent(elements.conjectureInput.value);
    return `leap=${leap}&conjecture=${conjecture}`;
}

async function fetchMetrics() {
    return fetchJson(`/metrics?${currentQuery()}`);
}

async function fetchNarrative() {
    return fetchJson(`/narrative?conjecture=${encodeURIComponent(elements.conjectureInput.value)}`);
}

async function fetchSummary() {
    return fetchJson(`/summary?${currentQuery()}`);
}

async function fetchDocuments() {
    return fetchJson('/documents');
}

function formatMetric(value) {
    return Number(value || 0).toFixed(4);
}

function updateStatus(state) {
    elements.statusPill.textContent = state.status_label || 'MONITORAMENTO';
    elements.statusPill.dataset.status = state.status || 'monitoring';
}

function updateMetricCards(state) {
    elements.techneValue.textContent = formatMetric(state.techne);
    elements.iaeValue.textContent = formatMetric(state.iae);
    elements.harmonyValue.textContent = formatMetric(state.harmony);
    elements.ethosValue.textContent = formatMetric(state.ethos);
}

function updateCharts(state) {
    harmonyData.push(state.harmony);
    if (harmonyData.length > 12) harmonyData.shift();
    if (!window.Chart) return;

    const labels = harmonyData.map((_, index) => index + 1);
    if (harmonyChart) {
        harmonyChart.data.labels = labels;
        harmonyChart.data.datasets[0].data = harmonyData;
        harmonyChart.update();
    } else {
        const ctxHarmony = document.getElementById('harmonyChart').getContext('2d');
        harmonyChart = new Chart(ctxHarmony, {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'Índice de Harmonia',
                    data: harmonyData,
                    borderColor: '#287c68',
                    backgroundColor: 'rgba(40, 124, 104, 0.12)',
                    tension: 0.25,
                    fill: true,
                }],
            },
            options: { responsive: true, maintainAspectRatio: false },
        });
    }

    const metricData = [state.techne, state.iae, state.harmony, state.ethos];
    const metricColors = ['#2f5f98', '#b64747', '#287c68', '#8a6b19'];
    if (metricsChart) {
        metricsChart.data.datasets[0].data = metricData;
        metricsChart.update();
    } else {
        const ctxMetrics = document.getElementById('metricsChart').getContext('2d');
        metricsChart = new Chart(ctxMetrics, {
            type: 'bar',
            data: {
                labels: ['Techné', 'IAE', 'Harmonia', 'Ethos'],
                datasets: [{ data: metricData, backgroundColor: metricColors }],
            },
            options: { responsive: true, maintainAspectRatio: false },
        });
    }
}

function updateSummary(payload) {
    elements.summaryOutput.textContent = payload.summary;
    const flags = payload.state.risk_flags || [];
    elements.flagsOutput.innerHTML = flags.length
        ? flags.map(flag => `<span>${flag}</span>`).join('')
        : '<span>SEM_RISCO_EXTRA</span>';
}

function renderDocuments(payload) {
    const documents = payload.documents || [];
    const pinnedPaths = [
        'SOBERANO.key',
        'SOBERANO.pub',
        'docs/README_RELEASE_1_3_LEGACY.md',
        'README.md',
        'principles_calculator.py',
        'gaia_techne_framework.py',
        'backend/app.py',
    ];
    const pinned = pinnedPaths
        .map(path => documents.find(doc => doc.path === path))
        .filter(Boolean);
    const largestPrincipal = documents.filter(doc => doc.importance === 5).slice(-8).reverse();
    const principal = [...pinned, ...largestPrincipal]
        .filter((doc, index, list) => list.findIndex(item => item.path === doc.path) === index)
        .slice(0, 10);
    elements.documentCount.textContent = `${documents.length} arquivos`;
    elements.principalDocuments.innerHTML = principal.map(doc => `
        <article class="document-row">
            <strong>${doc.path}</strong>
            <span>${doc.date} · ${doc.layer}</span>
            <p>${doc.role}</p>
        </article>
    `).join('');
}

async function submitConjecture() {
    elements.synergyValue.textContent = Number(elements.synergySlider.value).toFixed(1);
    const [metrics, narrative, summary] = await Promise.all([
        fetchMetrics(),
        fetchNarrative(),
        fetchSummary(),
    ]);
    updateStatus(metrics);
    updateMetricCards(metrics);
    updateCharts(metrics);
    updateSummary(summary);
    elements.narrativeOutput.textContent = narrative.text;
}

async function loadDocuments() {
    const documents = await fetchDocuments();
    renderDocuments(documents);
}

async function triggerVeto() {
    await fetch(`${API_BASE}/veto`, { method: 'POST' });
    elements.statusPill.textContent = 'VETO ETHOS';
    elements.statusPill.dataset.status = 'critical';
}

elements.runButton.addEventListener('click', submitConjecture);
elements.submitButton.addEventListener('click', submitConjecture);
elements.vetoButton.addEventListener('click', triggerVeto);
elements.synergySlider.addEventListener('input', () => {
    elements.synergyValue.textContent = Number(elements.synergySlider.value).toFixed(1);
});

setInterval(() => {
    if (document.visibilityState === 'visible') {
        submitConjecture().catch(() => {
            elements.statusPill.textContent = 'OFFLINE';
            elements.statusPill.dataset.status = 'critical';
        });
    }
}, 5000);

loadDocuments().catch(() => {
    elements.documentCount.textContent = 'inventário indisponível';
});
submitConjecture().catch(() => {
    elements.statusPill.textContent = 'OFFLINE';
    elements.statusPill.dataset.status = 'critical';
});
