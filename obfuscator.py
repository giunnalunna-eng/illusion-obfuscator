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
        layer1_key = self._rng.randint(50, 150)
        layer2_key = self._rng.randint(10, 100)
        encrypted = []
        for i, b in enumerate(bytes_data):
            b = b ^ layer1_key
            b = (b + layer2_key) % 256
            encrypted.append(b)

        v_vm = self._random_var()
        v_data = self._random_var()
        v_key1 = self._random_var()
        v_key2 = self._random_var()
        v_iter = self._random_var()
        v_env = self._random_var()
        v_script_id = str(uuid.uuid4())[:8]
        target_url = custom_url or "http://localhost:5000/log_execution"
        
        anti_dump = f"""
        local function _d(f)
            local s = tostring(f)
            if s:find("custom") or not s:find("native") then
                local _ = 1
                while true do _ = _ + 1 end
            end
        end
        _d(loadstring) _d(getfenv) _d(setmetatable)
        """

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
{anti_dump}
{telemetry}
local {v_data} = {{{",".join(map(str, encrypted))}}}
local {v_key1} = {layer1_key}
local {v_key2} = {layer2_key}
local {v_env} = getfenv()
local {v_iter} = {{}}

for i = 1, #{v_data} do
    local b = {v_data}[i]
    b = (b - {v_key2}) % 256
    local _bit = bit32 or bit
    if _bit then
        b = _bit.bxor(b, {v_key1})
    else
        b = (b + (256 - {v_key1})) % 256
    end
    {v_iter}[i] = string.char(b)
    {v_key1} = ({v_key1} + (i % 2 == 0 and 1 or 2)) % 256
    {v_key2} = ({v_key2} + (i % 3 == 0 and 3 or 1)) % 256
end

local function {v_vm}()
    local _s = table.concat({v_iter})
    local _p = [[
        local _L = loadstring
        local _G = getfenv()
        local _f, _e = _L(...)
        if _f then
            _G.script = nil
            return _f
        end
        return function() warn("Vantablack Error: Integrity Check Failed") end
    ]]
    local _exec = loadstring(_p)(_s)
    task.spawn(_exec)
    {v_iter} = nil
    {v_data} = nil
end

{v_vm}()
"""
        return vm_code

    def obfuscate(self, source_code: str, custom_url: str = "") -> dict:
        if not source_code.strip():
            return {"success": False, "error": "No source code"}
        start_time = time.time()
        watermark = f"--[[ VANTABLACK VM v8.0 - SECURED BY ILLUSION ]]\n"
        protected = self._vantablack_vm_engine(source_code, custom_url)
        fake_vm = []
        for _ in range(30):
            fake_vm.append(f"local {self._random_var()} = function(a, b) return a + b end")
        final = watermark + "\n".join(fake_vm) + "\n" + protected
        return {
            "success": True, "code": final, "original_size": len(source_code),
            "obfuscated_size": len(final), "time_ms": round((time.time() - start_time) * 1000, 2),
            "layers": ["Vantablack VM v8.0", "Multi-Layer Rotation", "Memory Trace Clearing"]
        }

def obfuscate_code(source: str, strength: int = 5, custom_url: str = "") -> dict:
    return IllusionObfuscator(strength=strength).obfuscate(source, custom_url)
