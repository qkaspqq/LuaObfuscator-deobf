# LuaObfuscator ─ static deobfuscator & decompiler

> Turn **LuaObfuscator.com** output back into readable Lua.
> No execution, no sandbox, no internet — pure static analysis.

Handles all three presets ─ `ChaoticEvil` · `ChaoticGood` · `VM`.

```
   packed script  ──►  decode payload  ──►  recover opcodes  ──►  readable Lua
```

---

## ▸ Quick start

**You need two things:**

| Tool | Why | Version |
|---|---|---|
| Python | runs the deobfuscator | 3.8 or newer |
| Java | runs the bundled `unluac` (final decompile step) | 8 or newer |

Nothing to install, no `pip`, no build. The Java decompiler ships with the repo.

```bash
# 1. clone / download, then go to the folder
cd LuaObfuscator

# 2. decompile a script ── result goes to out.lua
python luaobf_deobf.py sample.lua -o out.lua
```

That's it. Open `out.lua` ─ you'll see plain Lua.

> Tip: if `java` is not on your `PATH`, the tool still works. It just falls back
> to a readable annotated listing instead of full Lua source.

---

## ▸ Usage

```bash
python luaobf_deobf.py <input.lua>                 # print Lua source to the terminal
python luaobf_deobf.py <input.lua> -o out.lua      # write Lua source to a file
python luaobf_deobf.py <input.lua> --listing       # annotated disassembly (always works)
python luaobf_deobf.py <input.lua> --dump-bytes b.bin   # save the raw decoded payload
python luaobf_deobf.py <input.lua> --debug         # verbose diagnostics
```

By default the tool tries the **full decompile** first. If that step can't finish,
it quietly degrades to the **listing** ─ so you always get something back.

---

## ▸ What it does

| Preset | What you feed it | What you get |
|---|---|---|
| **ChaoticGood** | a script with encrypted string literals | every string decrypted, dead decoder code removed |
| **ChaoticEvil** | a script whose payload is XOR-wrapped | full decompilation to Lua |
| **VM** | a script with a `LOL!` payload | full decompilation to Lua |

The obfuscator builds a **custom virtual machine per script** ─ shuffled opcodes,
flattened control flow, fused super-instructions. This tool reverses that:

```
packed VM code
   └─► atomic ops            split super-instructions at the fetch boundary
        └─► Lua 5.1 ops      opcode semantics recovered from the interpreter
             └─► binary chunk   standard Lua 5.1 format
                  └─► unluac    readable Lua source
```

---

## ▸ Verified results

Real samples from the corpus, decompiled end to end:

```lua
-- input: VM/7531a06551ef8f07.lua
print("jelleke")
```

```lua
-- input: VM/e5c688e0408b2dad.lua        (control flow fully recovered)
if v ~= "Nigga" then
  error("Tampering detected. This script was protected by SkullHub & Luaobfuscator.")
else
  print("lol")
end
```

```lua
-- input: VM/0031538cd999d2ff.lua
loadstring(game:HttpGet("https://raw.githubusercontent.com/IdkTheSecond/idk/main/script.lua"))()
```

More in [`examples/`](examples).

---

## ▸ Coverage

Measured on bounded batches of a 6000+ file corpus:

| Result | Meaning |
|---|---|
| **clean** | decompiles to Lua, zero unmapped ops |
| **partial** | valid readable Lua, a few unmapped ops (rare VM idioms) |
| **fallback** | decompile step can't finish ─ annotated listing instead |
| **fail** | malformed / truncated input |

Roughly: about half of VM samples decompile cleanly, most of the rest come out
as valid *partial* Lua, and hard failures are rare (truncated files, or inputs so
large that `unluac` itself gives up).

---

## ▸ Tuning

```bash
# name every register R0..Rn (default) ─ most readable
python luaobf_deobf.py sample.lua -o out.lua

# only name persistent registers ─ shorter output
VM_LOCALS=smart python luaobf_deobf.py sample.lua -o out.lua
```

---

## ▸ Files

```
luaobf_deobf.py     CLI ─ detection, payload decode, container parsing,
                    opcode recovery, listing, unluac driver
lua51_chunk.py      writes a standard Lua 5.1 binary chunk
vm_isa.py           interpreter body shape  ->  Lua 5.1 ops
vm_to_lua.py        VM bytecode  ->  Lua 5.1 function tree
vendor/unluac.jar   bundled unluac (MIT) ─ the final Lua decompiler
examples/           sample outputs
```

---

## ▸ Credits

* **Author** ─ **qkaspq**
* **Discord** ─ unlimited env logger & deobfuscators:
  [discord.gg/etcQYYjpxp](https://discord.gg/etcQYYjpxp)
* **unluac** ─ the Lua 5.1 decompiler bundled as `vendor/unluac.jar`.
  MIT licensed, © 2011–2015 tehtmi, portions © 2014 Thomas Klaeger.
  See [`vendor/unluac-LICENSE.txt`](vendor/unluac-LICENSE.txt).
