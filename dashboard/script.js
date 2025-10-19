let harmonyData = [];
let harmonyChart;
let metricsChart;

async function fetchMetrics(leapFactor, conjecture = '') {
    const response = await fetch(`http://localhost:5000/metrics?leap=${leapFactor}&conjecture=${encodeURIComponent(conjecture)}`);
    return await response.json();
}

async function fetchNarrative(conjecture) {
    const response = await fetch(`http://localhost:5000/narrative?conjecture=${encodeURIComponent(conjecture)}`);
    return await response.json();
}

function updateCharts(metrics) {
    harmonyData.push(metrics.harmony[metrics.harmony.length - 1]);
    if (harmonyData.length > 10) harmonyData.shift();

    if (harmonyChart) {
        harmonyChart.data.labels = Array(harmonyData.length).fill().map((_, i) => i);
        harmonyChart.data.datasets[0].data = harmonyData;
        harmonyChart.update();
    } else {
        const ctxHarmony = document.getElementById('harmonyChart').getContext('2d');
        harmonyChart = new Chart(ctxHarmony, {
            type: 'line',
            data: {
                labels: Array(harmonyData.length).fill().map((_, i) => i),
                datasets: [{ label: 'Harmony Index', data: harmonyData, borderColor: 'blue' }]
            }
        });
    }

    if (metricsChart) {
        metricsChart.data.datasets[0].data = [metrics.techné, metrics.iae, metrics.ethos];
        metricsChart.data.datasets[0].backgroundColor = metrics.iae > 1.5 ? 'red' : 'green';
        metricsChart.update();
    } else {
        const ctxMetrics = document.getElementById('metricsChart').getContext('2d');
        metricsChart = new Chart(ctxMetrics, {
            type: 'bar',
            data: {
                labels: ['Techné Score', 'IAE', 'Ethos Strength'],
                datasets: [{ data: [metrics.techné, metrics.iae, metrics.ethos], backgroundColor: metrics.iae > 1.5 ? 'red' : 'green' }]
            }
        });
    }

    document.getElementById('gauge').innerHTML = metrics.iae > 1.5 ? '<span class="alert">Critical (IAE > 1.50)</span>' : metrics.iae < 1.0 ? 'Safe' : 'Warning';
}

async function submitConjecture() {
    const conjecture = document.getElementById('conjecture-input').value;
    const metrics = await fetchMetrics(document.getElementById('synergy-slider').value, conjecture);
    const narrative = await fetchNarrative(conjecture);
    document.getElementById('narrative-output').innerText = narrative.text;
    updateCharts(metrics);
}

function runSimulation() {
    submitConjecture(); // Reuse conjecture logic for simulations
}

function triggerVeto() {
    fetch('http://localhost:5000/veto', { method: 'POST' })
        .then(() => alert('Ethos Veto Activated! Logged to ethos_log.json'));
}

// Real-time updates
setInterval(() => {
    // only update if there is no conjecture
    if (document.getElementById('conjecture-input').value === '') {
        submitConjecture()
    }
}, 5000);

// Initial load
submitConjecture();
