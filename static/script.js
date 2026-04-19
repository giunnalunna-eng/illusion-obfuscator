document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('btn-obfuscate');
    const input = document.getElementById('code-input');
    const output = document.getElementById('code-output');

    btn.addEventListener('click', async () => {
        if (!input.value) return;
        btn.innerText = "Processing...";
        const res = await fetch('/obfuscate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: input.value })
        });
        const data = await res.json();
        if (data.success) {
            output.value = data.code;
        }
        btn.innerText = "OBFUSCATE SCRIPT";
    });
});
