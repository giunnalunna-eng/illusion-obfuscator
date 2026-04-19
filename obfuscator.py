import random, time, uuid

class IllusionObfuscator:
    def __init__(self, strength=5):
        self._rng = random.Random(random.randint(1, 999999))
        self._used = set()

    def _rv(self):
        while True:
            n = "lI" + "".join(self._rng.choices(["l", "I", "1", "_"], k=40))
            if n not in self._used: self._used.add(n); return n

    def _abyssal_vm_fast(self, source, custom_url=""):
        bytes_data = list(source.encode("utf-8"))
        k1, k2 = self._rng.randint(60, 180), self._rng.randint(5, 50)
        sk1, sk2 = k1, k2
        encrypted = []
        for i, b in enumerate(bytes_data):
            idx = i + 1
            encrypted.append(((b ^ k1) + k2) % 256)
            k1 = (k1 + (2 if idx % 2 == 0 else 1)) % 256
            k2 = (k2 + (1 if idx % 3 == 0 else 2)) % 256

        v_data, v_instr, v_vm = self._rv(), self._rv(), self._rv()
        
        # Aggiunto sistema di micro-pause (task.wait) per evitare il freeze
        return f"""
--[[ AEGIS FAST-LOAD v9.6 ]]
local {v_data} = {{{",".join(map(str, encrypted))}}}
local {v_instr} = {{}}
local k1, k2 = {sk1}, {sk2}

for i = 1, #{v_data} do
    local b = {v_data}[i]
    b = (b - k2) % 256
    local bit = bit32 or bit
    if bit then b = bit.bxor(b, k1) else b = (b + (256 - k1)) % 256 end
    {v_instr}[i] = string.char(b)
    
    -- Sincronizzazione chiavi
    for j = 1, 1 do 
        k1=(k1+(i%2==0 and 2 or 1))%256 
        k2=(k2+(i%3==0 and 1 or 2))%256 
    end

    -- ANTI-FREEZE: Ogni 500 caratteri lo script fa una micro-pausa
    if i % 500 == 0 then
        task.wait()
    end
end

local function {v_vm}()
    local _s = table.concat({v_instr})
    local _f, _e = loadstring(_s)
    if _f then
        task.spawn(_f)
    else
        warn("VM Error: " .. tostring(_e))
    end
end
{v_vm}()
"""

    def obfuscate(self, source):
        if not source.strip(): return {"success": False, "error": "No code"}
        return {"success": True, "code": self._abyssal_vm_fast(source)}

def obfuscate_code(source, strength=5):
    return IllusionObfuscator(strength).obfuscate(source)
