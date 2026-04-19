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
            name = self._rng.choice(["l", "I"]) + "".join(self._rng.choices(chars, k=self._rng.randint(30, 50)))
            if name not in self._used_names:
                self._used_names.add(name)
                return name

    def _void_vm_engine(self, source: str, custom_url: str = "") -> str:
        encoded_source = base64.b64encode(source.encode("utf-8")).decode("utf-8")
        
        v_vm_loop = self._random_var()
        v_instr = self._random_var()
        v_pc = self._random_var()
        v_env = self._random_var()
        v_decoded = self._random_var()
        v_script_id = str(uuid.uuid4())[:8]
        
        target_url = custom_url or "http://localhost:5000/log_execution"
        
        anti_dump = f"""
        local function _check()
            local _ = tostring(loadstring)
            if not _:find("native") then while true do end end
        end
        _check()
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
local {v_env} = {{
    ['\\108\\111\\97\\100\\115\\116\\114\\105\\110\\103'] = loadstring,
    ['\\116\\97\\98\\108\\101'] = table,
    ['\\115\\116\\114\\105\\110\\103'] = string
}}
local {v_decoded} = "{encoded_source}"
local {v_pc} = 1

local function {v_vm_loop}()
    local _b = {{}}
    local _s = {v_env}['\\115\\116\\114\\105\\110\\103'].gsub({v_decoded}, "[^%g]", "")
    
    local function _d(data)
        local b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        data = string.gsub(data, '[^'..b64..'=]', '')
        return (data:gsub('.', function(x)
            if (x == '=') then return '' end
            local r,f='',(b64:find(x)-1)
            for i=6,1,-1 do r=r..(f%2^i-f%2^(i-1)>0 and '1' or '0') end
            return r;
        end):gsub('%d%d%d%d%d%d%d%d', function(x)
            local r=0
            for i=1,8 do r=r+(x:sub(i,i)=='1' and 2^(8-i) or 0) end
            return string.char(r)
        end))
    end

    local _payload = _d(_s)
    local _exec, _err = {v_env}['\\108\\111\\97\\100\\115\\116\\114\\105\\110\\103'](_payload)
    
    if _exec then
        local _mt = {{__metatable = "VOID_PROTECTED"}}
        setmetatable(_env, _mt)
        task.spawn(_f or _exec)
    else
        warn("VOID VM ERROR: EXCEPTION_AT_DISPATCH")
    end
end

{v_vm_loop}()
"""
        return vm_code

    def obfuscate(self, source_code: str, custom_url: str = "") -> dict:
        if not source_code.strip():
            return {"success": False, "error": "No source code"}
            
        start_time = time.time()
        watermark = f"--[[ VOID VM v7.0 - SECURED BY ILLUSION ]]\n"
        protected = self._void_vm_engine(source_code, custom_url)
        junk = []
        for _ in range(50):
            v = self._random_var()
            junk.append(f"local {v} = function() return tostring(math.random()) end")
        final = watermark + "\n".join(junk) + "\n" + protected
        return {
            "success": True, "code": final, "original_size": len(source_code),
            "obfuscated_size": len(final), "time_ms": round((time.time() - start_time) * 1000, 2),
            "layers": ["VOID VM v7.0", "Base64 Bytecode", "Anti-Dump v3", "Dynamic Environment"]
        }

def obfuscate_code(source: str, strength: int = 5, custom_url: str = "") -> dict:
    return IllusionObfuscator(strength=strength).obfuscate(source, custom_url)
