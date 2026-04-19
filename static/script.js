document.addEventListener('DOMContentLoaded', () => {
    const btnObf = document.getElementById('btn-obfuscate');
    const input = document.getElementById('code-input');
    const output = document.getElementById('code-output');
    const nameInp = document.getElementById('script-name');
    const pasteToggle = document.getElementById('use-pastefy');

    btnObf.addEventListener('click', async () => {
        if (!input.value) return alert('Enter code!');
        btnObf.innerText = "Processing...";
        const res = await fetch('/obfuscate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                code: input.value, 
                name: nameInp.value || "Script", 
                use_pastefy: pasteToggle.checked 
            })
        });
        const data = await res.json();
        if (data.success) {
            output.value = data.code;
            alert('Success!');
        }
        btnObf.innerText = "OBFUSCATE";
    });

    document.getElementById('btn-copy').addEventListener('click', () => {
        if (output.value) { navigator.clipboard.writeText(output.value); alert('Copied!'); }
    });

    document.getElementById('btn-clear').addEventListener('click', () => {
        input.value = ''; output.value = '';
    });
});
