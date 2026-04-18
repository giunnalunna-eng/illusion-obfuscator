/* ===== ILLUSION OBFUSCATOR - UI LOGIC v7 ===== */

document.addEventListener('DOMContentLoaded', () => {
    // Nav elements
    const navObfuscator = document.getElementById('nav-obfuscator');
    const navDashboard = document.getElementById('nav-dashboard');
    const navAccount = document.getElementById('nav-account');
    
    const obfuscatorView = document.getElementById('obfuscator-view');
    const dashboardView = document.getElementById('dashboard-view');
    const accountView = document.getElementById('account-view');
    const pageTitle = document.getElementById('page-title');

    // Account elements
    const inputUsername = document.getElementById('username');
    const inputCustomUrl = document.getElementById('custom-url');
    const btnSaveSettings = document.getElementById('btn-save-settings');

    // Obfuscator elements
    const codeInput = document.getElementById('code-input');
    const codeOutput = document.getElementById('code-output');
    const btnObfuscate = document.getElementById('btn-obfuscate');
    const btnCopy = document.getElementById('btn-copy');
    const btnClear = document.getElementById('btn-clear');
    const pills = document.querySelectorAll('.pill');

    // Dashboard elements
    const logsTable = document.getElementById('logs-table');
    const totalExecs = document.getElementById('total-execs');
    
    let currentStrength = 5;

    // --- Persistence & Account ---
    const loadSettings = () => {
        const settings = JSON.parse(localStorage.getItem('illusion_settings') || '{}');
        if (settings.username) inputUsername.value = settings.username;
        if (settings.custom_url) inputCustomUrl.value = settings.custom_url;
        showToast('Account data loaded!');
    };

    const saveSettings = () => {
        const settings = {
            username: inputUsername.value.trim(),
            custom_url: inputCustomUrl.value.trim()
        };
        localStorage.setItem('illusion_settings', JSON.stringify(settings));
        showToast('Account & Settings saved successfully!', 'success');
    };

    btnSaveSettings.onclick = saveSettings;
    loadSettings();

    // --- Navigation ---
    const switchView = (view) => {
        navObfuscator.classList.remove('active');
        navDashboard.classList.remove('active');
        navAccount.classList.remove('active');
        
        obfuscatorView.style.display = 'none';
        dashboardView.style.display = 'none';
        accountView.style.display = 'none';

        if (view === 'obfuscator') {
            navObfuscator.classList.add('active');
            obfuscatorView.style.display = 'block';
            pageTitle.innerText = 'Obfuscation';
        } else if (view === 'dashboard') {
            navDashboard.classList.add('active');
            dashboardView.style.display = 'block';
            pageTitle.innerText = 'Dashboard (Logs)';
            refreshDashboard();
        } else {
            navAccount.classList.add('active');
            accountView.style.display = 'block';
            pageTitle.innerText = 'Account & Settings';
        }
    };

    navObfuscator.onclick = (e) => { e.preventDefault(); switchView('obfuscator'); };
    navDashboard.onclick = (e) => { e.preventDefault(); switchView('dashboard'); };
    navAccount.onclick = (e) => { e.preventDefault(); switchView('account'); };

    // --- Obfuscator Logic ---
    pills.forEach(pill => {
        pill.onclick = () => {
            pills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            currentStrength = parseInt(pill.dataset.level);
        };
    });

    btnObfuscate.onclick = async () => {
        const code = codeInput.value.trim();
        const settings = JSON.parse(localStorage.getItem('illusion_settings') || '{}');
        const customUrl = settings.custom_url || '';

        if (!code) return showToast('Enter code!', 'error');

        btnObfuscate.innerText = 'PROTECTING...';
        btnObfuscate.disabled = true;

        try {
            const res = await fetch('/obfuscate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    code, 
                    strength: currentStrength,
                    custom_url: customUrl
                })
            });
            const data = await res.json();
            if (data.success) {
                codeOutput.value = data.code;
                showToast('Protected!', 'success');
            } else {
                showToast(data.error || 'Failed', 'error');
            }
        } catch (err) {
            showToast('Connect error!', 'error');
        } finally {
            btnObfuscate.innerText = 'OBFUSCATE SCRIPT';
            btnObfuscate.disabled = false;
        }
    };

    // --- Dashboard Logic ---
    const refreshDashboard = async () => {
        try {
            const logRes = await fetch('/get_logs');
            const logs = await logRes.json();
            updateLogsTable(logs);
            totalExecs.innerText = logs.length;
        } catch (err) {
            console.error('Dashboard sync error', err);
        }
    };

    const updateLogsTable = (logs) => {
        const header = `<div class="table-header"><span>Player Name</span><span>Script ID</span><span>Time</span></div>`;
        const rows = logs.map(log => `
            <div class="table-row">
                <span style="color: #9d4edd; font-weight: bold;">${log.player}</span>
                <span style="font-family: monospace; font-size: 0.8rem;">${log.script_id}</span>
                <span>${log.time}</span>
            </div>
        `).join('');
        logsTable.innerHTML = header + (rows || '<div class="table-row">No executions yet</div>');
    };

    setInterval(() => {
        if (dashboardView.style.display === 'block') refreshDashboard();
    }, 5000);

    // Copy/Clear
    btnCopy.onclick = () => {
        navigator.clipboard.writeText(codeOutput.value);
        showToast('Copied!');
    };

    btnClear.onclick = () => {
        if (confirm('Clear everything?')) {
            codeInput.value = '';
            codeOutput.value = '';
        }
    };

    function showToast(msg, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerText = msg;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }
});
