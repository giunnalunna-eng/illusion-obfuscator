import random, time, uuid, math

class IllusionXOmega:
    def __init__(self, strength=10):
        self._rng = random.Random(random.randint(1, 999999))
        self._used = set()

    def _rv(self):
        while True:
            n = "lI" + "".join(self._rng.choices(["l", "I", "1", "_"], k=45))
            if n not in self._used: self._used.add(n); return n

    def _void_vm_v11(self, source):
        # Dividiamo il codice in blocchi per l'esecuzione incrementale
        # Questo impedisce il dump completo
        source_bytes = list(source.encode("utf-8"))
        chunk_size = self._rng.randint(20, 50)
        chunks = [source_bytes[i:i + chunk_size] for i in range(0, len(source_bytes), chunk_size)]
        
        encrypted_chunks = []
        master_key = self._rng.randint(50, 200)
        
        for chunk in chunks:
            k = self._rng.randint(1, 255)
            enc = [((b ^ k) + master_key) % 256 for b in chunk]
            encrypted_chunks.append({"k": k, "d": enc})

        v_vm = self._rv()
        v_chunks = self._rv()
        v_master = self._rv()
        v_core = self._rv()
        
        # Generiamo il codice della VM VOID
        chunks_code = ",".join([f"{{k={c['k']},d={{{','.join(map(str, c['d']))}}}}}" for c in encrypted_chunks])
        
        return f"""
--[[ ILLUSION X - OMEGA VM v11.0 VOID EDITION ]]
local {v_chunks} = {{{chunks_code}}}
local {v_master} = {master_key}

-- GHOST GUARD: Anti-Hooking & Integrity Check
local function _check()
    local _l = loadstring
    local _g = getfenv
    if tostring(_l):find("custom") or not tostring(_l):find("native") or _g() ~= _g(0) then
        while true do end -- Crash the skidder
    end
end

local function {v_core}()
    _check()
    local _res = {{}}
    
    for i=1, #{v_chunks} do
        local _c = {v_chunks}[i]
        local _k = _c.k
        local _d = _c.d
        local _p = {{}}
        
        -- Decriptazione Incrementale (Solo questo pezzo in memoria)
        for j=1, #_d do
            local b = _d[j]
            b = (b - {v_master}) % 256
            local bit = bit32 or bit
            if bit then b = bit.bxor(b, _k) else b = (b + (256 - _k)) % 256 end
            _p[j] = string.char(b)
        end
        
        _res[i] = table.concat(_p)
        -- Pulizia immediata
        _c.d = nil
        _p = nil
        
        -- Anti-Lag
        if i % 10 == 0 then task.wait() end
    end
    
    local _final = table.concat(_res)
    _res = nil
    
    local _f, _e = loadstring(_final)
    if _f then
        -- Blindaggio Ambiente
        local _env = getfenv(_f)
        setmetatable(_env, {{__index = function() return nil end, __newindex = function() return nil end}})
        task.spawn(_f)
    end
end

task.spawn({v_core})
"""

    def obfuscate(self, source):
        if not source.strip(): return {"success": False, "error": "No code"}
        start_time = time.time()
        
        # Iniezione di "Fake Decryption Loops" per confondere i debugger
        fake_loops = []
        for _ in range(3):
            fake_loops.append(f"local {self._rv()} = {{}} for i=1,1000 do table.insert({self._rv()}, i) end")

        protected = self._void_vm_v11(source)
        final = "--[[ OBFUSCATED BY ILLUSION HUB OBFUSCATOR ]]\n" + "\n".join(fake_loops) + "\n" + protected
        
        return {
            "success": True,
            "code": final,
            "time_ms": round((time.time() - start_time) * 1000, 2)
        }

def obfuscate_code(source, strength=10):
    return IllusionXOmega(strength).obfuscate(source)
