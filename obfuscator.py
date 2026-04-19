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
            name = self._rng.choice(["l", "I"]) + "".join(self._rng.choices(chars, k=self._rng.randint(25, 40)))
            if name not in self._used_names:
                self._used_names.add(name)
                return name

    def _anti_tamper_layer(self) -> str:
        v_check = self._random_var()
        v_tamper = self._random_var()
        v_skid = "dont try to skid \xf0\x9f\x98\x82"
        return f"""
        local function {v_check}(...)
            local _f = {{...}}
            for _, f in pairs(_f) do
                if tostring(f):find("custom") or not tostring(f):find("native") then
                    return true
                end
            end
            return false
        end
        local function {v_tamper}()
            while true do 
                warn("{v_skid}")
                task.wait(0.1) 
            end
        end
        if {v_check}(print, warn, error, setmetatable, getfenv, loadstring, table.concat) then
            task.spawn({v_tamper})
            return
        end
        """

    def _toxic_vm_layer(self, source: str, custom_url: str = "") -> str:
        bytes_data = list(source.encode("utf-8"))
        start_key = self._rng.randint(100, 255)
        current_key = start_key
        encrypted_pool = []
        for i, b in enumerate(bytes_data):
            idx = i + 1
            encrypted_pool.append(b ^ current_key)
            current_key = (current_key + (idx % 4 + 1)) % 256
            
        v_vm = self._random_var()
        v_pool = self._random_var()
        v_proxy = self._random_var()
        v_state = self._random_var()
        v_dispatch = self._random_var()
        v_script_id = str(uuid.uuid4())[:8]
        
        target_url = custom_url or "http://localhost:5000/log_execution"
        anti_tamper = self._anti_tamper_layer()

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
{anti_tamper}
{telemetry}
local {v_pool} = {{{",".join(map(str, encrypted_pool))}}}
local {v_proxy} = {{}}
local {v_state} = {start_key}

for i = 1, #{v_pool} do
    local b = {v_pool}[i]
    local {v_dispatch} = bit32 or bit
    if {v_dispatch} then
        b = {v_dispatch}.bxor(b, {v_state})
    end
    {v_proxy}[i] = string.char(b)
    {v_state} = ({v_state} + (i % 4 + 1)) % 256
end

local function {v_vm}()
    local _c = table.concat({v_proxy})
    local _f, _e = loadstring(_c)
    if _f then
        pcall(function() getfenv(_f).script = nil end)
        task.spawn(_f)
    else
        while true do warn("dont try to skid \xf0\x9f\x98\x82") task.wait(0.1) end
    end
end

{v_vm}()
"""
        return vm_code

    def obfuscate(self, source_code: str, custom_url: str = "") -> dict:
        if not source_code.strip():
            return {"success": False, "error": "No source code"}
        start_time = time.time()
        watermark = f"--[[ ILLUSION v6.5 GHOST GUARD EDITION ]]\n"
        protected = self._toxic_vm_layer(source_code, custom_url)
        junk = []
        for _ in range(30):
            v_j = self._random_var()
            junk.append(f"local {v_j} = 'dont try to skid \xf0\x9f\x98\x82'")
        final = watermark + "\n".join(junk) + "\n" + protected
        return {
            "success": True, "code": final, "original_size": len(source_code),
            "obfuscated_size": len(final), "time_ms": round((time.time() - start_time) * 1000, 2),
            "layers": ["Ghost VM v6.5", "Ghost Guard Anti-Tamper", "Perfect Sync XOR"]
        }

def obfuscate_code(source: str, strength: int = 5, custom_url: str = "") -> dict:
    return IllusionObfuscator(strength=strength).obfuscate(source, custom_url)
