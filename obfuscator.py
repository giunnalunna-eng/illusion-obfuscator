import random, time, uuid

class IllusionObfuscator:
    def __init__(self, strength=5):
        self._rng = random.Random(random.randint(1, 999999))
        self._used = set()

    def _rv(self):
        while True:
            # Genera nomi che sembrano messaggi di errore o insulti per i deoffuscatori
            n = self._rng.choice(["skid_", "no_deobf_", "stop_trying_", "illusion_"]) + "".join(self._rng.choices(["I", "l", "1"], k=15))
            if n not in self._used: self._used.add(n); return n

    def _vantablack_v8_advanced(self, source, custom_url=""):
        bytes_data = list(source.encode("utf-8"))
        k1, k2 = self._rng.randint(50, 150), self._rng.randint(10, 100)
        sk1, sk2 = k1, k2
        encrypted = []
        
        for i, b in enumerate(bytes_data):
            idx = i + 1
            encrypted.append(((b ^ k1) + k2) % 256)
            k1 = (k1 + (1 if idx % 2 == 0 else 2)) % 256
            k2 = (k2 + (3 if idx % 3 == 0 else 1)) % 256

        v_data, v_vm, v_instr = self._rv(), self._rv(), self._rv()
        v_guard = self._rv()
        
        # Il Watermark e la trappola "u cant deobf this skidder"
        return f"""
--[[ OBFUSCATED BY ILLUSION HUB OBFUSCATOR ]]

local function {v_guard}()
    local _check = {{loadstring, getfenv, setmetatable}}
    for _, f in pairs(_check) do
        if tostring(f):find("custom") or not tostring(f):find("native") then
            print("u cant deobf this skidder")
            while true do end -- Blocca il deoffuscatore
        end
    end
end
{v_guard}()

local {v_data} = {{{",".join(map(str, encrypted))}}}
local {v_instr} = {{}}
local k1, k2 = {sk1}, {sk2}

for i = 1, #{v_data} do
    local b = {v_data}[i]
    b = (b - k2) % 256
    local bit = bit32 or bit
    if bit then b = bit.bxor(b, k1) else b = (b + (256 - k1)) % 256 end
    {v_instr}[i] = string.char(b)
    k1 = (k1 + (i % 2 == 0 and 1 or 2)) % 256
    k2 = (k2 + (i % 3 == 0 and 3 or 1)) % 256
end

local function {v_vm}()
    local _s = table.concat({v_instr})
    local _f = loadstring(_s)
    if _f then 
        task.spawn(_f) 
    else
        print("u cant deobf this skidder")
    end
end
{v_vm}()
"""

    def obfuscate(self, source):
        if not source.strip(): return {"success": False, "error": "No code"}
        return {"success": True, "code": self._vantablack_v8_advanced(source)}

def obfuscate_code(source, strength=5):
    return IllusionObfuscator(strength).obfuscate(source)
