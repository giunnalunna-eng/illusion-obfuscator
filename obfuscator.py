import random, time, uuid

class IllusionXOmega:
    def __init__(self, strength=10):
        self._rng = random.Random(random.randint(1, 999999))
        self._used = set()

    def _rv(self):
        while True:
            n = "lI" + "".join(self._rng.choices(["l", "I", "1", "_"], k=45))
            if n not in self._used: self._used.add(n); return n

    def _omega_vm_v10_1(self, source):
        # 1. Criptazione Veloce a Livello di Byte
        bytes_data = list(source.encode("utf-8"))
        k1 = self._rng.randint(60, 200)
        k2 = self._rng.randint(10, 80)
        
        # Sincronizzazione Chiavi (Turbo)
        encrypted = []
        for i, b in enumerate(bytes_data):
            idx = i + 1
            encrypted.append(((b ^ k1) + k2) % 256)
            k1 = (k1 + (idx % 2 == 0 and 2 or 1)) % 256
            k2 = (k2 + (idx % 3 == 0 and 1 or 2)) % 256

        v_stack = self._rv()
        v_vm = self._rv()
        v_data = self._rv()
        v_instr = self._rv()
        
        # 2. Hardening e Anti-Lag
        # Usiamo un dispatcher a blocchi per velocità massima
        vm_code = f"""
local {v_data} = {{{",".join(map(str, encrypted))}}}
local {v_instr} = {{}}
local k1, k2 = {k1}, {k2} -- Chiave finale sincronizzata

-- OMEGA DISPATCHER v10.1 (Turbo Mode)
for i = 1, #{v_data} do
    local b = {v_data}[i]
    local _k1, _k2 = {k1}, {k2}
    
    -- Ricostruzione Chiave Dinamica (Ottimizzata)
    for j = 1, i do
        _k1 = (_k1 + (j % 2 == 0 and 2 or 1)) % 256
        _k2 = (_k2 + (j % 3 == 0 and 1 or 2)) % 256
    end
    
    b = (b - _k2) % 256
    local bit = bit32 or bit
    if bit then b = bit.bxor(b, _k1) else b = (b + (256 - _k1)) % 256 end
    {v_instr}[i] = string.char(b)

    -- ANTI-FREEZE: Ogni 800 byte facciamo respirare il motore
    if i % 800 == 0 then task.wait() end
end

local function {v_vm}()
    local _s = table.concat({v_instr})
    local _f, _e = loadstring(_s)
    if _f then
        pcall(function() getfenv(_f).script = nil end)
        task.spawn(_f)
    end
    -- Pulizia Tracce
    {v_instr} = nil
    {v_data} = nil
end

task.spawn({v_vm})
"""
        return vm_code

    def obfuscate(self, source):
        if not source.strip(): return {"success": False, "error": "No code"}
        start_time = time.time()
        
        # Junk Code Injection
        junk = [f"local {self._rv()} = {self._rng.randint(1,999)}" for _ in range(20)]
        
        protected = self._omega_vm_v10_1(source)
        final = "--[[ ILLUSION HUB ON TOP ]]\n" + "\n".join(junk) + "\n" + protected
        
        return {
            "success": True,
            "code": final,
            "time_ms": round((time.time() - start_time) * 1000, 2),
            "engine": "ILLUSION OBFUSCATOR"
        }

def obfuscate_code(source, strength=10):
    return IllusionXOmega(strength).obfuscate(source)
