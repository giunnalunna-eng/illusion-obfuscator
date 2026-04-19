import random, time, uuid

class IllusionXOmega:
    def __init__(self, strength=10):
        self._rng = random.Random(random.randint(1, 999999))
        self._used = set()

    def _rv(self):
        while True:
            n = "lI" + "".join(self._rng.choices(["l", "I", "1", "_"], k=40))
            if n not in self._used: self._used.add(n); return n

    def _omega_vm_v10_2(self, source):
        bytes_data = list(source.encode("utf-8"))
        
        # Chiavi iniziali (Devono rimanere costanti per l'inizio del loop Lua)
        sk1 = self._rng.randint(60, 200)
        sk2 = self._rng.randint(10, 80)
        
        current_k1 = sk1
        current_k2 = sk2
        encrypted = []
        
        # Criptazione Lineare (Velocissima)
        for i, b in enumerate(bytes_data):
            idx = i + 1
            # Xor + Add shift
            val = b ^ current_k1
            val = (val + current_k2) % 256
            encrypted.append(val)
            
            # Rotazione chiavi IDENTICA a quella che faremo in Lua
            current_k1 = (current_k1 + (2 if idx % 2 == 0 else 1)) % 256
            current_k2 = (current_k2 + (1 if idx % 3 == 0 else 2)) % 256

        v_vm = self._rv()
        v_data = self._rv()
        v_instr = self._rv()
        v_k1 = self._rv()
        v_k2 = self._rv()
        
        # Il Loader Lua O(n) - Estremamente veloce
        return f"""
local {v_data} = {{{",".join(map(str, encrypted))}}}
local {v_instr} = {{}}
local {v_k1} = {sk1}
local {v_k2} = {sk2}

for i = 1, #{v_data} do
    local b = {v_data}[i]
    
    -- Decriptazione invertita rispetto a Python
    b = (b - {v_k2}) % 256
    local bit = bit32 or bit
    if bit then 
        b = bit.bxor(b, {v_k1}) 
    else 
        b = (b + (256 - {v_k1})) % 256 
    end
    
    {v_instr}[i] = string.char(b)
    
    -- Rotazione chiavi (Lineare, no lag)
    local s1 = (i % 2 == 0) and 2 or 1
    local s2 = (i % 3 == 0) and 1 or 2
    {v_k1} = ({v_k1} + s1) % 256
    {v_k2} = ({v_k2} + s2) % 256

    -- Anti-Lag: solo ogni 1500 caratteri per massima velocità
    if i % 1500 == 0 then task.wait() end
end

local function {v_vm}()
    local _s = table.concat({v_instr})
    local _f, _e = loadstring(_s)
    if _f then
        pcall(function() getfenv(_f).script = nil end)
        task.spawn(_f)
    else
        warn("OMEGA ERROR: " .. tostring(_e))
    end
end
{v_vm}()
"""

    def obfuscate(self, source):
        if not source.strip(): return {"success": False, "error": "No code"}
        start_time = time.time()
        protected = self._omega_vm_v10_2(source)
        final = "--[[ OBFUSCATED BY ILLUSION OBFUSCATOR ]]\n" + protected
        return {
            "success": True,
            "code": final,
            "time_ms": round((time.time() - start_time) * 1000, 2)
        }

def obfuscate_code(source, strength=10):
    return IllusionXOmega(strength).obfuscate(source)
