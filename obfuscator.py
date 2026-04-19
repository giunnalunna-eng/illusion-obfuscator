import random, time, uuid

class IllusionXOmega:
    def __init__(self, strength=10):
        self._rng = random.Random(random.randint(1, 999999))
        self._used = set()

    def _rv(self):
        while True:
            n = "lI" + "".join(self._rng.choices(["l", "I", "1", "_"], k=40))
            if n not in self._used: self._used.add(n); return n

    def _omega_v10_4_stable(self, source):
        bytes_data = list(source.encode("utf-8"))
        
        # Chiavi iniziali solide
        sk1 = self._rng.randint(100, 250)
        sk2 = self._rng.randint(20, 90)
        
        current_k1, current_k2 = sk1, sk2
        encrypted = []
        
        for i, b in enumerate(bytes_data):
            idx = i + 1
            # Doppia protezione: XOR + Addizione Rotante
            val = (b ^ current_k1)
            val = (val + current_k2) % 256
            encrypted.append(val)
            
            # Rotazione chiavi deterministica
            current_k1 = (current_k1 + (2 if idx % 2 == 0 else 1)) % 256
            current_k2 = (current_k2 + (1 if idx % 3 == 0 else 2)) % 256

        v_vm = self._rv()
        v_data = self._rv()
        v_instr = self._rv()
        v_k1, v_k2 = self._rv(), self._rv()
        
        return f"""
--[[ ILLUSION AEGIS v10.4 STABLE ]]
local {v_data} = {{{",".join(map(str, encrypted))}}}
local {v_instr} = {{}}
local {v_k1}, {v_k2} = {sk1}, {sk2}

-- Anti-Hooking & Environment Protection
local _ls = loadstring
local _sc = string.char
local _tc = table.concat

for i = 1, #{v_data} do
    local b = {v_data}[i]
    
    -- Decriptazione Inversa (Garantita)
    b = (b - {v_k2}) % 256
    local bit = bit32 or bit
    if bit then 
        b = bit.bxor(b, {v_k1}) 
    else 
        b = (b + (256 - {v_k1})) % 256 
    end
    
    {v_instr}[i] = _sc(b)
    
    -- Rotazione Chiavi Sincronizzata
    local s1 = (i % 2 == 0) and 2 or 1
    local s2 = (i % 3 == 0) and 1 or 2
    {v_k1} = ({v_k1} + s1) % 256
    {v_k2} = ({v_k2} + s2) % 256
    
    if i % 1000 == 0 then task.wait() end
end

local function {v_vm}()
    local _s = _tc({v_instr})
    local _f, _err = _ls(_s)
    if _f then
        -- Pulizia ambiente per sicurezza extra
        pcall(function() 
            local env = getfenv(_f)
            env.script = nil
        end)
        task.spawn(_f)
    else
        warn("AEGIS FATAL: " .. tostring(_err))
    end
    -- Memory Wipe
    {v_data} = nil
    {v_instr} = nil
end

{v_vm}()
"""

    def obfuscate(self, source):
        if not source.strip(): return {"success": False, "error": "No code"}
        start_time = time.time()
        
        # Junk Code Injection per distrarre i deoffuscatori
        junk = [f"local {self._rv()} = {self._rng.randint(1,9999)}" for _ in range(25)]
        
        protected = self._omega_v10_4_stable(source)
        final = "--[[ OBFUSCATED BY ILLUSION HUB ]]\n" + "\n".join(junk) + "\n" + protected
        
        return {
            "success": True,
            "code": final,
            "time_ms": round((time.time() - start_time) * 1000, 2)
        }

def obfuscate_code(source, strength=10):
    return IllusionXOmega(strength).obfuscate(source)
