Skip to content
giunnalunna-eng
illusion-obfuscator
Repository navigation
Code
Issues
Pull requests
Actions
Projects
Wiki
Security and quality
Insights
Settings
Files
Go to file
t
T
static
templates
app.py
obfuscator.py
requirements.txt
illusion-obfuscator
/
obfuscator.py
in
main

Edit

Preview
Indent mode

Spaces
Indent size

4
Line wrap mode

No wrap
Editing obfuscator.py file contents
  1
  2
  3
  4
  5
  6
  7
  8
  9
 10
 11
 12
 13
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
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
        self._LUA_KEYWORDS = {"and", "break", "do", "else", "elseif", "end", "false", "for", "function", "goto", "if", "in", "local", "nil", "not", "or", "repeat", "return", "then", "true", "until", "while"}

    def _random_var(self) -> str:
        chars = ["l", "I", "1", "_"]
        while True:
            name = self._rng.choice(["l", "I"]) + "".join(self._rng.choices(chars, k=self._rng.randint(15, 25)))
            if name not in self._used_names and name not in self._LUA_KEYWORDS:
                self._used_names.add(name)
                return name

    def _aegis_encrypt(self, source: str, custom_url: str = "") -> str:
        bytes_data = list(source.encode("utf-8"))
        
        start_key = self._rng.randint(100, 255)
        current_key = start_key
        encrypted_pool = []
        
        # Perfect Sync Encryption
        for i, b in enumerate(bytes_data):
            idx = i + 1
            encrypted_pool.append(b ^ current_key)
            # Sync key shift with Lua logic
            shift = 1 if (idx % 2 == 0) else 2
Use Control + Shift + m to toggle the tab key moving focus. Alternatively, use esc then tab to move to the next interactive element on the page.
 
