import random, time, uuid

class IllusionXOmega:
    def __init__(self, strength=10):
        self._rng = random.Random(random.randint(1, 999999))
        self._used = set()

    def _rv(self):
        while True:
            n = "lI" + "".join(self._rng.choices(["l", "I", "1", "_"], k=45))
            if n not in self._used: self._used.add(n); return n

    def _eternal_vm_v12_1(self, source):
        trap_message = "dont try to skid"
        
        # 1. Suddivisione in Frammenti (Più piccoli per sicurezza estrema)
        source_bytes = list(source.encode("utf-8"))
        chunk_size = self._rng.randint(12, 28)
        chunks = [source_bytes[i:i + chunk_size] for i in range(0, len(source_bytes), chunk_size)]
        
        v_chunks = self._rv()
        v_dispatcher = self._rv()
        v_trap = self._rv()
        v_key = self._rng.randint(55, 245)
        
        encrypted_chunks = []
        for c in chunks:
            k = self._rng.randint(1, 255)
            enc = [((b ^ k) + v_key) % 256 for b in c]
            encrypted_chunks.append({"k": k, "d": enc})

        chunks_data = ",".join([f"{{k={c['k']},d={{{','.join(map(str, c['d']))}}}}}" for c in encrypted_chunks])

        return f"""
--[[ OBFUSCATED BY ILLUSION HUB OBFUSCATOR ]]

local {v_chunks} = {{{chunks_data}}}
local {v_trap} = "{trap_message}"

-- Anti-Hook System
local _ls = loadstring
local _env = getfenv
if tostring(_ls):find("custom") or not tostring(_ls):find("native") then
    print({v_trap})
    while true do end
end

local function {v_dispatcher}()
    local _res = {{}}
    local _sc = string.char
    local _tc = table.concat
    
    for i=1, #{v_chunks} do
        local _c = {v_chunks}[i]
        local _k = _c.k
        local _d = _c.d
        local _p = {{}}
        
        for j=1, #_d do
            local b = _d[j]
            b = (b - {v_key}) % 256
            local bit = bit32 or bit
            if bit then b = bit.bxor(b, _k) else b = (b + (256 - _k)) % 256 end
            _p[j] = _sc(b)
        end
        
        _res[i] = _tc(_p)
        _c.d = nil 
        
        if i % 25 == 0 then task.wait() end
    end
    
    local _final = _tc(_res)
    _res = nil
    
    -- Esecuzione in Sandbox (Impossibile da catturare)
    local _f, _err = _ls(_final)
    if _f then
        local _proxy = setmetatable({{}}, {{
            __index = function(_, k)
                if k == "loadstring" or k == "getfenv" or k == "setfenv" then
                    print({v_trap})
                    return function() while true do end end
                end
                return _env(0)[k]
            end,
            __metatable = "Locked by Illusion"
        }})
        setfenv(_f, _proxy)
        task.spawn(_f)
    else
        warn("ETERNAL v12.1 ERROR")
    end
end

task.spawn({v_dispatcher})
"""

    def obfuscate(self, source):
        if not source.strip(): return {"success": False, "error": "No code"}
        start_time = time.time()
        
        # Junk Code Injection (Ora con nomi variabili solidi)
        junk = []
        for _ in range(35):
            v = self._rv()
            junk.append(f"local {v} = function() local _ = '{uuid.uuid4()}' return _ end")

        protected = self._eternal_vm_v12_1(source)
        # CORRETTO: Aggiunti i commenti al Watermark
        final = "--[[ OBFUSCATED BY ILLUSION HUB OBFUSCATOR ]]\n" + "\n".join(junk) + "\n" + protected
        
        return {
            "success": True,
            "code": final,
            "time_ms": round((time.time() - start_time) * 1000, 2)
        }

def obfuscate_code(source, strength=10):
    return IllusionXOmega(strength).obfuscate(source)
