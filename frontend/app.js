async function fetchMetrics() {
    try {
        const response = await fetch('/api/v1/health');
        if (!response.ok) throw new Error('Network response error');
        const data = await response.json();

        document.getElementById('connection').innerText = 'CONNECTED (200 OK)';
        document.getElementById('metrics').innerText = JSON.stringify(data, null, 4);
    } catch (error) {
        document.getElementById('connection').innerText = 'DISCONNECTED';
        document.getElementById('connection').style.color = '#c0392b';
        document.getElementById('metrics').innerText = 'Failed to fetch metrics from backend service.';
    }
}
fetchMetrics();