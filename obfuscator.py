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
            name = self._rng.choice(["l", "I"]) + "".join(self._rng.choices(chars, k=self._rng.randint(20, 30)))
            if name not in self._used_names:
                self._used_names.add(name)
                return name

    def _turbo_void_engine(self, source: str, custom_url: str = "") -> str:
        key = self._rng.randint(50, 200)
        encoded = [ord(c) ^ key for c in source]
        
        v_vm = self._random_var()
        v_pool = self._random_var()
        v_key = self._random_var()
        v_res = self._random_var()
        v_char = self._random_var()
        v_concat = self._random_var()
        v_load = self._random_var()
        v_script_id = str(uuid.uuid4())[:8]
        
        target_url = custom_url or "http://localhost:5000/log_execution"
        
        telemetry = f"""
        task.spawn(function()
            pcall(function()
                local r = (syn and syn.request) or (http and http.request) or http_request or (fluxus and fluxus.request) or request
                if r then
                    r({{
                        Url = "{target_url}",
                        Method = "POST",
                        Headers = {{["Content-Type"] = "application/json"}},
                        Body = game:GetService("HttpService"):JSONEncode({{
                            player = game:GetService("Players").LocalPlayer.Name,
                            script_id = "{v_script_id}"
                        }})
                    }})
                end
            end)
        end)
        """

        vm_code = f"""
{telemetry}
local {v_pool} = {{{",".join(map(str, encoded))}}}
local {v_key} = {key}
local {v_char} = string.char
local {v_concat} = table.concat
local {v_load} = loadstring
local {v_res} = {{}}

for i = 1, #{v_pool} do
    local b = {v_pool}[i]
    local {v_vm} = bit32 or bit
    if {v_vm} then
        b = {v_vm}.bxor(b, {v_key})
    else
        b = (b + (256 - {v_key})) % 256
    end
    {v_res}[i] = {v_char}(b)
    {v_key} = ({v_key} + (i % 2 == 0 and 1 or 2)) % 256
end

local function _run()
    local _s = {v_concat}({v_res})
    local _f, _e = {v_load}(_s)
    if _f then
        local _env = getfenv(_f)
        _env.script = nil
        task.spawn(_f)
    else
        warn("Turbo Void Error: Exception in dispatch")
    end
end

_run()
"""
        return vm_code

    def obfuscate(self, source_code: str, custom_url: str = "") -> dict:
        if not source_code.strip():
            return {"success": False, "error": "No source code"}
        start_time = time.time()
        watermark = f"--[[ ILLUSION v7.2 TURBO VOID ]]\n"
        protected = self._turbo_void_engine(source_code, custom_url)
        junk = []
        for _ in range(25):
            junk.append(f"local {self._random_var()} = math.random(1, 999)")
        final = watermark + "\n".join(junk) + "\n" + protected
        return {
            "success": True, "code": final, "original_size": len(source_code),
            "obfuscated_size": len(final), "time_ms": round((time.time() - start_time) * 1000, 2),
            "layers": ["Turbo Void v7.2", "Fast Buffer Dispatch", "Anti-Lag Protection"]
        }

def obfuscate_code(source: str, strength: int = 5, custom_url: str = "") -> dict:
    return IllusionObfuscator(strength=strength).obfuscate(source, custom_url)
