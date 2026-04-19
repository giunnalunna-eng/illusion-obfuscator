import random, time, uuid

class IllusionXOmega:
    def __init__(self, strength=10):
        self._rng = random.Random(random.randint(1, 999999))
        self._used = set()

    def _rv(self):
        while True:
            n = "lI" + "".join(self._rng.choices(["l", "I", "1", "_"], k=40))
            if n not in self._used: self._used.add(n); return n

    def _omega_v10_3_shield(self, source):
        bytes_data = list(source.encode("utf-8"))
        
        # 1. Criptazione e Shuffle (Rimescolamento)
        sk1, sk2 = self._rng.randint(60, 200), self._rng.randint(10, 80)
        
        # Creiamo una mappa di posizioni mescolate
        indices = list(range(len(bytes_data)))
        self._rng.shuffle(indices)
        
        # Criptiamo i byte seguendo l'ordine mescolato
        shuffled_encrypted = [0] * len(bytes_data)
        current_k1, current_k2 = sk1, sk2
        
        for i, original_idx in enumerate(indices):
            idx = i + 1
            b = bytes_data[original_idx]
            val = ((b ^ current_k1) + current_k2) % 256
            shuffled_encrypted[i] = val
            
            # Rotazione chiavi
            current_k1 = (current_k1 + (2 if idx % 2 == 0 else 1)) % 256
            current_k2 = (current_k2 + (1 if idx % 3 == 0 else 2)) % 256

        v_data = self._rv()
        v_map = self._rv()
        v_vm = self._rv()
        v_instr = self._rv()
        
        # Il Loader deve conoscere la mappa per rimettere i byte in ordine
        # Usiamo un algoritmo di ricostruzione della mappa basato su seed per risparmiare spazio
        seed = self._rng.randint(1, 999999)
        
        return f"""
--[[ ILLUSION OBFUSCATOR ]]
local {v_data} = {{{",".join(map(str, shuffled_encrypted))}}}
local {v_instr} = {{}}
local k1, k2 = {sk1}, {sk2}

-- Ricostruzione Mappa di Shuffle (Seed: {seed})
local function _get_map(n, s)
    local m = {{}} for i=1,n do m[i]=i end
    local r = math.randomseed(s)
    for i=n, 2, -1 do
        local j = math.random(i)
        m[i], m[j] = m[j], m[i]
    end
    return m
end

local {v_map} = _get_map(#{v_data}, {seed})
local _final_bytes = {{}}

-- Anti-Hooking Check
local _sc = string.char
if tostring(_sc) ~= "blank" and not tostring(_sc):find("native") then
    print("Security Breach Detected")
    return
end

for i = 1, #{v_data} do
    local b = {v_data}[i]
    
    -- Decriptazione
    b = (b - k2) % 256
    local bit = bit32 or bit
    if bit then b = bit.bxor(b, k1) else b = (b + (256 - k1)) % 256 end
    
    -- Riposizionamento (Un-shuffle)
    _final_bytes[{v_map}[i]] = _sc(b)
    
    -- Rotazione Chiavi
    k1 = (k1 + (i % 2 == 0 and 2 or 1)) % 256
    k2 = (k2 + (i % 3 == 0 and 1 or 2)) % 256
    
    if i % 1500 == 0 then task.wait() end
end

local function {v_vm}()
    local _s = table.concat(_final_bytes)
    local _f = loadstring(_s)
    if _f then
        task.spawn(_f)
    end
    -- Zero-Trace Memory Wipe
    _final_bytes = nil
    {v_data} = nil
    {v_map} = nil
end
{v_vm}()
"""

    def obfuscate(self, source):
        if not source.strip(): return {"success": False, "error": "No code"}
        start_time = time.time()
        protected = self._omega_v10_3_shield(source)
        return {
            "success": True,
            "code": protected,
            "time_ms": round((time.time() - start_time) * 1000, 2)
        }

def obfuscate_code(source, strength=10):
    return IllusionXOmega(strength).obfuscate(source)
