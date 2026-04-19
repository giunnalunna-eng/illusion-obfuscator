document.addEventListener('DOMContentLoaded', () => {
    const btnObf = document.getElementById('btn-obfuscate');
    const input = document.getElementById('code-input');
    const output = document.getElementById('code-output');
    const nameInp = document.getElementById('script-name');
    const pasteToggle = document.getElementById('use-pastefy');
    const historyList = document.getElementById('history-list');
    const liveLogsList = document.getElementById('live-logs');
    const activeCount = document.getElementById('active-count');

    function renderHistory() {
        const history = JSON.parse(localStorage.getItem('obf_history') || '[]');
        historyList.innerHTML = history.length ? history.reverse().map((item, idx) => `
            <div class="log-card">
                <div><div class="log-player">${item.name}</div><div style="font-size:0.6rem;color:#444">${item.date}</div></div>
                <button class="btn-system" onclick="copyHist(${history.length-1-idx})">COPY</button>
            </div>
        `).join('') : '<p style="color:#222;text-align:center;padding:20px;">No local history.</p>';
    }
    renderHistory();

    window.copyHist = (idx) => {
        const history = JSON.parse(localStorage.getItem('obf_history') || '[]');
        navigator.clipboard.writeText(history[idx].code);
        alert('Copied from history!');
    };

    async function fetchLiveLogs() {
        try {
            const res = await fetch('/get_logs');
            const logs = await res.json();
            activeCount.innerText = logs.length;
            if (logs.length > 0) {
                liveLogsList.innerHTML = logs.map(log => `
                    <div class="log-card">
                        <div><div class="log-player">${log.player}</div><div style="font-size:0.6rem;color:#444">Executing: ${log.script}</div></div>
                        <div style="font-size:0.7rem;color:#555">${log.time}</div>
                    </div>
                `).join('');
            }
        } catch {}
    }
    setInterval(fetchLiveLogs, 3000);
    fetchLiveLogs();

    btnObf.addEventListener('click', async () => {
        if (!input.value) return alert('Enter code!');
        btnObf.innerText = "PROCESSING...";
        const res = await fetch('/obfuscate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: input.value, name: nameInp.value || "Untitled", use_pastefy: pasteToggle.checked })
        });
        const data = await res.json();
        if (data.success) {
            output.value = data.code;
            const history = JSON.parse(localStorage.getItem('obf_history') || '[]');
            history.push({ name: nameInp.value || "Untitled", date: new Date().toLocaleString(), code: data.code });
            localStorage.setItem('obf_history', JSON.stringify(history));
            renderHistory();
        }
        btnObf.innerText = "PROTECT & PUBLISH";
    });

    document.getElementById('btn-copy').addEventListener('click', () => {
        if (output.value) { navigator.clipboard.writeText(output.value); alert('Copied!'); }
    });

    document.getElementById('btn-clear').addEventListener('click', () => {
        input.value = ''; output.value = '';
    });
});
