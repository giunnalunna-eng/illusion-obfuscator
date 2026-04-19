document.addEventListener('DOMContentLoaded', () => {
    const btnObfuscate = document.getElementById('btn-obfuscate');
    const codeInput = document.getElementById('code-input');
    const codeOutput = document.getElementById('code-output');
    const scriptNameInput = document.getElementById('script-name');
    const fileInput = document.getElementById('file-input');
    const btnUploadTrigger = document.getElementById('btn-upload-trigger');
    const liveLogsList = document.getElementById('live-logs');
    const toastContainer = document.getElementById('toast-container');

    function showToast(msg, type = 'info') {
        const toast = document.createElement('div');
        toast.style.cssText = "background: #111; color: #00d4ff; border: 1px solid #00d4ff; padding: 12px 20px; border-radius: 8px; margin-bottom: 10px; font-size: 0.8rem; box-shadow: 0 0 20px rgba(0,212,255,0.2);";
        toast.innerText = msg;
        toastContainer.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    }

    // Gestione Caricamento File .lua
    btnUploadTrigger.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                codeInput.value = event.target.result;
                scriptNameInput.value = file.name.replace(".lua", "");
                showToast(`Loaded ${file.name} successfully!`);
            };
            reader.readAsText(file);
        }
    });

    // Polling Log Sidebar
    async function fetchLiveLogs() {
        try {
            const response = await fetch('/get_logs');
            const logs = await response.json();
            if (logs.length > 0) {
                liveLogsList.innerHTML = logs.map(log => `
                    <div class="log-card">
                        <span class="log-player">${log.player}</span>
                        <div class="log-info">${log.script} | ${log.time}</div>
                    </div>
                `).join('');
            }
        } catch (err) {
            console.error("Log fetch failed");
        }
    }
    setInterval(fetchLiveLogs, 3000);
    fetchLiveLogs();

    // Logica Offuscamento
    btnObfuscate.addEventListener('click', async () => {
        const source = codeInput.value.trim();
        const name = scriptNameInput.value.trim() || "Untitled";

        if (!source) {
            showToast('Enter code or upload a file!', 'error');
            return;
        }

        btnObfuscate.innerText = "PROTECTING...";
        btnObfuscate.disabled = true;

        try {
            const response = await fetch('/obfuscate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code: source,
                    name: name
                })
            });

            const data = await response.json();
            if (data.success) {
                codeOutput.value = data.code;
                showToast('Script Protected & Logged!', 'success');
            } else {
                showToast('Error: ' + data.error, 'error');
            }
        } catch (err) {
            showToast('Server connection failed!', 'error');
        } finally {
            btnObfuscate.innerText = "PROTECT SCRIPT";
            btnObfuscate.disabled = false;
        }
    });

    document.getElementById('btn-copy').addEventListener('click', () => {
        if (codeOutput.value) {
            navigator.clipboard.writeText(codeOutput.value);
            showToast('Result copied!', 'success');
        }
    });

    document.getElementById('btn-clear').addEventListener('click', () => {
        codeInput.value = '';
        codeOutput.value = '';
        showToast('Editor cleared.');
    });
});
