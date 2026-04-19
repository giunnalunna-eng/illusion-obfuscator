import random
import string
import hashlib
import time
import base64
import uuid

class IllusionObfuscator:
    def __init__(self, strength=5, seed=None):
        self.strength = strength
        self.seed = seed or random.randint(1, 999999)
        self._rng = random.Random(self.seed)
        self._used_names = set()

    def _random_var(self) -> str:
        chars = ["l", "I", "1", "_"]
        while True:
            name = self._rng.choice(["l", "I"]) + "".join(self._rng.choices(chars, k=self._rng.randint(35, 50)))
            if name not in self._used_names:
                self._used_names.add(name)
                return name

    def _vantablack_vm_engine(self, source: str, custom_url: str = "") -> str:
        bytes_data = list(source.encode("utf-8"))
        
        start_key1 = self._rng.randint(50, 150)
        start_key2 = self._rng.randint(10, 100)
        current_key1 = start_key1
        current_key2 = start_key2
        encrypted = []
        
        # Sincronizzazione perfetta della rotazione chiavi
        for i, b in enumerate(bytes_data):
            idx = i + 1
            # Criptazione a due strati
            val = b ^ current_key1
            val = (val + current_key2) % 256
            encrypted.append(val)
            
            # Rotazione chiavi identica a quella Lua
            shift1 = 1 if (idx % 2 == 0) else 2
            shift2 = 3 if (idx % 3 == 0) else 1
            current_key1 = (current_key1 + shift1) % 256
            current_key2 = (current_key2 + shift2) % 256

        v_vm = self._random_var()
        v_data = self._random_var()
        v_key1 = self._random_var()
        v_key2 = self._random_var()
        v_iter = self._random_var()
        v_env = self._random_var()
        v_script_id = str(uuid.uuid4())[:8]
        
        target_url = custom_url or "http://localhost:5000/log_execution"
        
        vm_code = f"""
local {v_data} = {{{",".join(map(str, encrypted))}}}
local {v_key1} = {start_key1}
local {v_key2} = {start_key2}
local {v_iter} = {{}}

for i = 1, #{v_data} do
    local b = {v_data}[i]
    -- Decriptazione invertita rispetto a Python
    b = (b - {v_key2}) % 256
    local _bit = bit32 or bit
    if _bit then
        b = _bit.bxor(b, {v_key1})
    else
        b = (b + (256 - {v_key1})) % 256
    end
    {v_iter}[i] = string.char(b)
    
    -- Rotazione chiavi
    local shift1 = (i % 2 == 0) and 1 or 2
    local shift2 = (i % 3 == 0) and 3 or 1
    {v_key1} = ({v_key1} + shift1) % 256
    {v_key2} = ({v_key2} + shift2) % 256
end

local function {v_vm}()
    local _s = table.concat({v_iter})
    local _exec, _err = loadstring(_s)
    if _exec then
        getfenv(_exec).script = nil
        task.spawn(_exec)
    else
        warn("Vantablack Error: " .. tostring(_err))
    end
end

{v_vm}()
"""
        return vm_code

    def obfuscate(self, source_code: str, custom_url: str = "") -> dict:
        if not source_code.strip():
            return {"success": False, "error": "No source code"}
        start_time = time.time()
        watermark = f"--[[ VANTABLACK v8.1 SYNC ]]\n"
        protected = self._vantablack_vm_engine(source_code, custom_url)
        junk = []
        for _ in range(10):
            junk.append(f"local {self._random_var()} = math.random(1, 100)")
        final = watermark + "\n".join(junk) + "\n" + protected
        return {
            "success": True, "code": final, "original_size": len(source_code),
            "obfuscated_size": len(final), "time_ms": round((time.time() - start_time) * 1000, 2),
            "layers": ["Vantablack v8.1", "Perfect Sync Rotation"]
        }

def obfuscate_code(source: str, strength: int = 5, custom_url: str = "") -> dict:
    return IllusionObfuscator(strength=strength).obfuscate(source, custom_url)
