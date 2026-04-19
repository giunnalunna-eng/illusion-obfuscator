document.addEventListener('DOMContentLoaded', () => {
    const btnObf = document.getElementById('btn-obfuscate');
    const btnConf = document.getElementById('btn-confirm-pay');
    const modal = document.getElementById('payment-modal');
    const input = document.getElementById('code-input');
    const output = document.getElementById('code-output');
    const nameInp = document.getElementById('script-name');
    const historyList = document.getElementById('history-list');

    function renderHistory() {
        const history = JSON.parse(localStorage.getItem('obf_history') || '[]');
        historyList.innerHTML = history.reverse().map((item, idx) => `
            <div class="history-card">
                <div><div style="font-weight:700">${item.name}</div><div style="font-size:0.7rem;color:#555">${item.date}</div></div>
                <button style="background:red;border:none;color:white;padding:5px 10px;border-radius:5px;cursor:pointer" onclick="navigator.clipboard.writeText(\`${item.code}\`); alert('Copied!')">Copy</button>
            </div>
        `).join('') || '<p style="color:#555">No history found.</p>';
    }
    renderHistory();

    btnObf.addEventListener('click', () => {
        if (!nameInp.value || !input.value) return alert('Name and code are required!');
        modal.style.display = 'flex';
    });

    btnConf.addEventListener('click', async () => {
        modal.style.display = 'none';
        const res = await fetch('/obfuscate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                code: input.value, 
                name: nameInp.value, 
                strength: 5, 
                use_pastefy: document.getElementById('use-pastefy').checked 
            })
        });
        const data = await res.json();
        if (data.success) {
            output.value = data.code;
            const history = JSON.parse(localStorage.getItem('obf_history') || '[]');
            history.push({ name: nameInp.value, date: new Date().toLocaleString(), code: data.code });
            localStorage.setItem('obf_history', JSON.stringify(history));
            renderHistory();
        }
    });
});
