document.addEventListener('DOMContentLoaded', () => {
    // Effetto Particelle Blu
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    let particles = [];
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2;
            this.speedX = Math.random() * 0.5 - 0.25;
            this.speedY = Math.random() * 0.5 - 0.25;
        }
        update() {
            this.x += this.speedX; this.y += this.speedY;
            if (this.x > canvas.width) this.x = 0; if (this.x < 0) this.x = canvas.width;
            if (this.y > canvas.height) this.y = 0; if (this.y < 0) this.y = canvas.height;
        }
        draw() {
            ctx.fillStyle = 'rgba(0, 212, 255, 0.5)';
            ctx.beginPath(); ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2); ctx.fill();
        }
    }
    for (let i = 0; i < 80; i++) particles.push(new Particle());
    function animate() {
        ctx.clearRect(0,0,canvas.width, canvas.height);
        particles.forEach(p => { p.update(); p.draw(); });
        requestAnimationFrame(animate);
    }
    animate();

    // Logica Offuscamento
    const btn = document.getElementById('btn-obfuscate');
    const input = document.getElementById('code-input');
    const output = document.getElementById('code-output');

    btn.addEventListener('click', async () => {
        if (!input.value) return;
        btn.innerText = "Protecting...";
        const res = await fetch('/obfuscate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                code: input.value, 
                use_pastefy: document.getElementById('use-pastefy').checked,
                name: document.getElementById('script-name').value || "Script"
            })
        });
        const data = await res.json();
        if (data.success) {
            output.value = data.code;
        }
        btn.innerText = "PROTECT SCRIPT";
    });
});
