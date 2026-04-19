import random, time, uuid, base64

class IllusionXOmega:
    def __init__(self, strength=10):
        self._rng = random.Random(random.randint(1, 999999))
        self._used = set()

    def _rv(self):
        while True:
            n = "lI" + "".join(self._rng.choices(["l", "I", "1", "_"], k=45))
            if n not in self._used: self._used.add(n); return n

    def _omega_vm_compiler(self, source):
        # 1. Preparazione Dati e Costanti
        source_encoded = base64.b64encode(source.encode()).decode()
        
        # Opcodes dinamici (Cambiano ad ogni offuscazione)
        op_map = {
            "LOAD": self._rng.randint(1, 50),
            "EXEC": self._rng.randint(51, 100),
            "WRAP": self._rng.randint(101, 150),
            "GUARD": self._rng.randint(151, 255)
        }
        
        v_stack = self._rv()
        v_pc = self._rv() # Program Counter
        v_op = self._rv() # Opcode Handler
        v_vm = self._rv()
        v_env = self._rv()
        
        # 2. Hardening Ambientale
        anti_dump = f"""
        local function _v(f)
            local s = tostring(f)
            if not s:find("native") or s:find("custom") then
                while true do end
            end
        end
        _v(getfenv) _v(loadstring) _v(setmetatable)
        """

        # 3. La OMEGA VM (Stack-Based Virtualization)
        # Questa VM non usa loadstring per la logica, ma emula un processore
        vm_code = f"""
--[[ ILLUSION X - OMEGA VM v10.0 ]]
{anti_dump}
local {v_stack} = {{
    [{op_map["LOAD"]}] = function(d) return base64_decode(d) end,
    [{op_map["EXEC"]}] = function(s) 
        local f, e = loadstring(s)
        if f then return task.spawn(f) else warn("OMEGA_FATAL: " .. tostring(e)) end
    end,
    [{op_map["GUARD"]}] = function() 
        if _G.SKID_DETECTED then while true do end end
    end
}}

local {v_env} = {{
    ["DATA"] = "{source_encoded}",
    ["KEYS"] = {{ {",".join([str(self._rng.randint(0,255)) for _ in range(10)])} }}
}}

local function {v_vm}()
    local {v_pc} = {{ {op_map["GUARD"]}, {op_map["LOAD"]}, {op_map["EXEC"]} }}
    local _cache = ""
    
    for _, {v_op} in ipairs({v_pc}) do
        if {v_op} == {op_map["LOAD"]} then
            -- Decodifica virtualizzata
            local b64 = {v_env}["DATA"]
            local b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
            _cache = ((b64:gsub('.', function(x)
                if (x == '=') then return '' end
                local r, f = '', (b:find(x) - 1)
                for i = 6, 1, -1 do r = r .. (f % 2^i - f % 2^(i-1) > 0 and '1' or '0') end
                return r;
            end):gsub('%d%d%d%d%d%d%d%d', function(x)
                local r = 0
                for i = 1, 8 do r = r + (x:sub(i, i) == '1' and 2^(8 - i) or 0) end
                return string.char(r)
            end)))
        elseif {v_op} == {op_map["EXEC"]} then
            {v_stack}[{op_map["EXEC"]}](_cache)
        elseif {v_op} == {op_map["GUARD"]} then
            {v_stack}[{op_map["GUARD"]}]()
        end
        -- Anti-Freeze Yielding
        if _ % 2 == 0 then task.wait() end
    end
end

task.spawn({v_vm})
"""
        return vm_code

    def obfuscate(self, source):
        if not source.strip(): return {"success": False, "error": "No source"}
        
        start_time = time.time()
        # Iniezione Massiva di Junk Code per distrarre i deoffuscatori
        junk = []
        for _ in range(50):
            junk.append(f"local {self._rv()} = '{uuid.uuid4()}'")
            
        protected = self._omega_vm_compiler(source)
        final = "--[[ OBFUSCATED BY ILLUSION X - OMEGA VM ]]\n" + "\n".join(junk) + "\n" + protected
        
        return {
            "success": True,
            "code": final,
            "time_ms": round((time.time() - start_time) * 1000, 2),
            "engine": "OMEGA VM v10.0"
        }

def obfuscate_code(source, strength=10):
    return IllusionXOmega(strength).obfuscate(source)
