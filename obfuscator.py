import random, time, base64, uuid

class IllusionObfuscator:
    def __init__(self, strength=5):
        self._rng = random.Random(random.randint(1, 999999))
        self._used = set()

    def _rv(self):
        while True:
            n = "lI" + "".join(self._rng.choices(["l", "I", "1", "_"], k=40))
            if n not in self._used: self._used.add(n); return n

    def _abyssal_vm(self, source):
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
        
        return f"""
local {v_data} = {{{",".join(map(str, encrypted))}}}
local {v_instr} = {{}}
for i = 1, #{v_data} do
    local b, k1, k2 = {v_data}[i], {sk1}, {sk2}
    for j = 1, i do k1=(k1+(j%2==0 and 2 or 1))%256 k2=(k2+(j%3==0 and 1 or 2))%256 end
    b = (b - k2) % 256
    local bit = bit32 or bit
    if bit then b = bit.bxor(b, k1) else b = (b + (256 - k1)) % 256 end
    {v_instr}[i] = string.char(b)
end
local function {v_vm}()
    local _f = loadstring(table.concat({v_instr}))
    if _f then task.spawn(_f) end
end
{v_vm}()
"""

    def obfuscate(self, source):
        if not source.strip(): return {"success": False, "error": "No code"}
        return {"success": True, "code": self._abyssal_vm(source)}

def obfuscate_code(source, strength=5):
    return IllusionObfuscator(strength).obfuscate(source)
