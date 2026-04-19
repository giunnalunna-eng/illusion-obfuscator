document.addEventListener('DOMContentLoaded', () => {
    const btnObf = document.getElementById('btn-obfuscate');
    const btnConf = document.getElementById('btn-confirm-pay');
    const modal = document.getElementById('payment-modal');
    const input = document.getElementById('code-input');
    const output = document.getElementById('code-output');
    const nameInp = document.getElementById('script-name');
    const pasteToggle = document.getElementById('use-pastefy');
    const historyList = document.getElementById('history-list');

    function renderHistory() {
        const history = JSON.parse(localStorage.getItem('obf_history') || '[]');
        historyList.innerHTML = history.reverse().map((item, idx) => `
            <div class="history-item">
                <div><div class="history-name">${item.name}</div><div style="font-size:0.7rem;color:#888;">${item.date}</div></div>
                <button style="background:red;color:white;border:none;padding:5px;border-radius:4px;cursor:pointer;" onclick="navigator.clipboard.writeText(\`${item.code}\`); alert('Copied!')">Copy</button>
            </div>
        `).join('') || '<div style="padding:20px;text-align:center;">No history.</div>';
    }
    renderHistory();

    btnObf.addEventListener('click', () => {
        if (!nameInp.value || !input.value) return alert('Name and Code required!');
        modal.style.display = 'flex';
    });

    btnConf.addEventListener('click', async () => {
        modal.style.display = 'none';
        const res = await fetch('/obfuscate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: input.value, name: nameInp.value, strength: 5, use_pastefy: pasteToggle.checked })
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
