import random, time, uuid

class IllusionXOmega:
    def __init__(self, strength=10):
        self._rng = random.Random(random.randint(1, 999999))
        self._used = set()

    def _rv(self):
        while True:
            n = "lI" + "".join(self._rng.choices(["l", "I", "1", "_"], k=45))
            if n not in self._used: self._used.add(n); return n

    def _void_vm_v11_1(self, source):
        # Dividiamo il codice in blocchi per l'esecuzione incrementale
        source_bytes = list(source.encode("utf-8"))
        chunk_size = self._rng.randint(25, 60)
        chunks = [source_bytes[i:i + chunk_size] for i in range(0, len(source_bytes), chunk_size)]
        
        encrypted_chunks = []
        master_key = self._rng.randint(60, 210)
        
        for chunk in chunks:
            k = self._rng.randint(1, 255)
            enc = [((b ^ k) + master_key) % 256 for b in chunk]
            encrypted_chunks.append({"k": k, "d": enc})

        v_vm = self._rv()
        v_chunks = self._rv()
        v_master = self._rv()
        v_core = self._rv()
        
        chunks_code = ",".join([f"{{k={c['k']},d={{{','.join(map(str, c['d']))}}}}}" for c in encrypted_chunks])
        
        return f"""
--[[ ILLUSION X - VOID v11.1 FIXED ]]
local {v_chunks} = {{{chunks_code}}}
local {v_master} = {master_key}

local function {v_core}()
    local _res = {{}}
    local _ls = loadstring
    local _sc = string.char
    local _tc = table.concat
    
    for i=1, #{v_chunks} do
        local _c = {v_chunks}[i]
        local _k = _c.k
        local _d = _c.d
        local _p = {{}}
        
        for j=1, #_d do
            local b = _d[j]
            b = (b - {v_master}) % 256
            local bit = bit32 or bit
            if bit then b = bit.bxor(b, _k) else b = (b + (256 - _k)) % 256 end
            _p[j] = _sc(b)
        end
        
        _res[i] = _tc(_p)
        _c.d = nil -- Wipe memory
        
        if i % 15 == 0 then task.wait() end
    end
    
    local _final = _tc(_res)
    _res = nil
    
    local _f, _err = _ls(_final)
    if _f then
        task.spawn(_f)
    else
        warn("AEGIS VOID ERROR: " .. tostring(_err))
    end
end

task.spawn({v_core})
"""

    def obfuscate(self, source):
        if not source.strip(): return {"success": False, "error": "No code"}
        start_time = time.time()
        
        # Correzione Junk Code (Ora usa lo stesso nome variabile per la tabella)
        fake_loops = []
        for _ in range(4):
            v = self._rv()
            fake_loops.append(f"local {v} = {{}} for i=1, 200 do table.insert({v}, i) end")

        protected = self._void_vm_v11_1(source)
        final = "--[[ OBFUSCATED BY ILLUSION HUB OBFUSCATOR ]]\n" + "\n".join(fake_loops) + "\n" + protected
        
        return {
            "success": True,
            "code": final,
            "time_ms": round((time.time() - start_time) * 1000, 2)
        }

def obfuscate_code(source, strength=10):
    return IllusionXOmega(strength).obfuscate(source)
