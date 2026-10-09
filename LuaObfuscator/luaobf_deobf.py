#!/usr/bin/env python3

import argparse
import os
import re
import subprocess
import sys

MAGIC = "LOL!"

_LUA_SIMPLE_ESCAPES = {
    "a": 7, "b": 8, "f": 12, "n": 10, "r": 13, "t": 9, "v": 11,
    "\\": 92, '"': 34, "'": 39, "\n": 10,
}


def unescape_lua_string(raw: str) -> bytes:
    out = bytearray()
    i = 0
    n = len(raw)
    while i < n:
        ch = raw[i]
        if ch != "\\":
            out.extend(ch.encode("utf-8", "surrogateescape"))
            i += 1
            continue
        i += 1
        if i >= n:
            break
        e = raw[i]
        if e == "z":
            i += 1
            while i < n and raw[i] in " \t\r\n\v\f":
                i += 1
            continue
        if e == "x":
            i += 1
            hx = raw[i:i + 2]
            if len(hx) == 2 and all(c in "0123456789abcdefABCDEF" for c in hx):
                out.append(int(hx, 16))
                i += 2
                continue
            out.append(ord("x"))
            continue
        if e.isdigit():
            j = i
            digits = ""
            while j < n and raw[j].isdigit() and len(digits) < 3:
                digits += raw[j]
                j += 1
            out.append(int(digits) & 0xFF)
            i = j
            continue
        if e in _LUA_SIMPLE_ESCAPES:
            out.append(_LUA_SIMPLE_ESCAPES[e])
            i += 1
            continue
        if e == "\n":
            out.append(10)
            i += 1
            continue
        out.extend(e.encode("utf-8", "surrogateescape"))
        i += 1
    return bytes(out)


_STRING_LITERAL_RE = re.compile(r'"((?:[^"\\]|\\.)*)"', re.S)


def iter_string_literals(src: str):
    for m in _STRING_LITERAL_RE.finditer(src):
        yield m.start(), m.end(), m.group(1)


def xor_decode(data: bytes, key: bytes) -> bytes:
    if not key:
        return data
    out = bytearray(len(data))
    klen = len(key)
    for i in range(len(data)):
        out[i] = data[i] ^ key[(i + 1) % klen]
    return bytes(out)


def _payload_from_literal_bytes(blob: bytes):
    if blob[:4] == MAGIC.encode():
        return blob.decode("latin-1")
    return None


def find_payload(src: str, debug: bool = False):
    literals = list(iter_string_literals(src))
    info = {"literals": len(literals)}

    for _s, _e, raw in literals:
        blob = unescape_lua_string(raw)
        got = _payload_from_literal_bytes(blob)
        if got is not None:
            info["mode"] = "plain"
            return got, info

    idx = src.find(MAGIC)
    if idx >= 0:
        end = src.find('"', idx)
        raw = src[idx:end if end >= 0 else len(src)]
        got = _payload_from_literal_bytes(unescape_lua_string(raw))
        if got is not None:
            info["mode"] = "plain"
            return got, info

    call_re = re.compile(
        r'([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*"((?:[^"\\]|\\.)*)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*\)',
        re.S,
    )
    for m in call_re.finditer(src):
        data = unescape_lua_string(m.group(2))
        key = unescape_lua_string(m.group(3))
        if len(data) < 64:
            continue
        dec = xor_decode(data, key)
        got = _payload_from_literal_bytes(dec)
        if got is not None:
            info["mode"] = "xor"
            info["helper"] = m.group(1)
            info["key"] = key
            return got, info

    info["mode"] = None
    return None, info


_HEX_DIGITS = set("0123456789abcdefABCDEF")


def detect_rle_marker(body: str) -> str:
    for i in range(1, len(body), 2):
        ch = body[i]
        if ch not in _HEX_DIGITS:
            return ch
    return "Q"


def decode_hex_rle(payload: str) -> bytes:
    body = payload[len(MAGIC):]
    marker = detect_rle_marker(body)
    out = bytearray()
    repeat = None
    i = 0
    n = len(body)
    while i + 1 <= n:
        pair = body[i:i + 2]
        if len(pair) < 2:
            break
        if pair[1] == marker:
            repeat = int(pair[0])
        else:
            try:
                b = int(pair, 16)
            except ValueError:
                raise ValueError(f"bad hex pair {pair!r} at {i}")
            if repeat is not None:
                out.extend(bytes([b]) * repeat)
                repeat = None
            else:
                out.append(b)
        i += 2
    return bytes(out)


def find_xor_helper(src: str):
    for m in re.finditer(r"local function (\w+)\s*\((\w+)\s*,\s*(\w+)\s*\)", src):
        body = src[m.end():m.end() + 400]
        if "%256" in body and "#" in body:
            return m.group(1)
    return None


def _lua_quote(b: bytes) -> str:
    out = ['"']
    for ch in b:
        if ch == 34:
            out.append('\\"')
        elif ch == 92:
            out.append("\\\\")
        elif 32 <= ch < 127:
            out.append(chr(ch))
        elif ch == 10:
            out.append("\\n")
        elif ch == 13:
            out.append("\\r")
        elif ch == 9:
            out.append("\\t")
        else:
            out.append(f"\\{ch}")
    out.append('"')
    return "".join(out)


def deobfuscate_strings(src: str, debug: bool = False):
    helper = find_xor_helper(src)
    if helper is None:
        return None, {"mode": None}

    call_re = re.compile(
        re.escape(helper) + r'\s*\(\s*"((?:[^"\\]|\\.)*)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*\)',
        re.S,
    )
    count = 0

    def repl(m):
        nonlocal count
        data = unescape_lua_string(m.group(1))
        key = unescape_lua_string(m.group(2))
        count += 1
        return _lua_quote(xor_decode(data, key))

    out = call_re.sub(repl, src)
    out = _drop_dead_prelude(out, helper)
    return out, {"mode": "strings", "helper": helper, "count": count}


def _skip_block(src: str, start: int) -> int:
    depth = 0
    tok = re.compile(r"\b(if|function|do|repeat|end|until)\b")
    for m in tok.finditer(src, start):
        w = m.group(1)
        if w in ("if", "function", "do", "repeat"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return m.end()
    return len(src)


def _drop_dead_prelude(out: str, helper: str) -> str:
    m = re.search(r"local function " + re.escape(helper) + r"\s*\(", out)
    if m:
        end = _skip_block(out, m.start())
        out = out[:m.start()] + out[end:]

    for _ in range(40):
        changed = False
        for m in re.finditer(r"local (\w+)=([^;\n]*);", out):
            name = m.group(1)
            rest = out[:m.start()] + out[m.end():]
            if not re.search(r"\b" + re.escape(name) + r"\b", rest):
                out = out[:m.start()] + out[m.end():]
                changed = True
                break
        if not changed:
            break
    return out


def _fmt_const(v):
    if isinstance(v, str):
        return _lua_quote(v.encode("latin-1", "replace"))
    return repr(v)


_IDENT_RE = re.compile(r"[A-Za-z_]\w*")


def _strip_outer_parens(expr: str) -> str:
    s = expr.strip()
    while s.startswith("(") and s.endswith(")"):
        depth = 0
        ok = True
        for i, c in enumerate(s):
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0 and i != len(s) - 1:
                    ok = False
                    break
        if not ok:
            break
        s = s[1:-1].strip()
    return s


def _split_top(expr: str, keyword: str):
    parts, depth, i, last = [], 0, 0, 0
    n = len(expr)
    while i < n:
        c = expr[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif depth == 0 and expr.startswith(keyword, i):
            before_ok = i == 0 or not (expr[i - 1].isalnum() or expr[i - 1] == "_")
            j = i + len(keyword)
            after_ok = j >= n or not (expr[j].isalnum() or expr[j] == "_")
            if before_ok and after_ok:
                parts.append(expr[last:i])
                i = j
                last = i
                continue
        i += 1
    parts.append(expr[last:])
    return parts


def _split_cmp(expr: str, op: str):
    depth = 0
    i = 0
    n = len(expr)
    while i < n:
        c = expr[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif depth == 0 and expr.startswith(op, i):
            return expr[:i], expr[i + len(op):]
        i += 1
    return None


def eval_arith(expr: str, env):
    expr = expr.strip()
    if expr == "":
        return None

    def sub(m):
        name = m.group(0)
        if name in env:
            return repr(env[name])
        if name in ("true", "false"):
            return name
        raise KeyError(name)

    try:
        e = _IDENT_RE.sub(sub, expr)
    except KeyError:
        return None
    e = e.replace("^", "**")
    if not re.fullmatch(r"[0-9eE+\-*/%().\s]+", e):
        return None
    try:
        return eval(e, {"__builtins__": {}}, {})
    except Exception:
        return None


def eval_cond(expr: str, env):
    expr = _strip_outer_parens(expr)
    if not expr:
        return None
    ors = _split_top(expr, "or")
    if len(ors) > 1:
        vals = [eval_cond(p, env) for p in ors]
        if any(v is True for v in vals):
            return True
        if any(v is None for v in vals):
            return None
        return False
    ands = _split_top(expr, "and")
    if len(ands) > 1:
        vals = [eval_cond(p, env) for p in ands]
        if any(v is False for v in vals):
            return False
        if any(v is None for v in vals):
            return None
        return True
    if re.match(r"^not\b", expr):
        v = eval_cond(re.sub(r"^not\b", "", expr, count=1), env)
        return None if v is None else (not v)
    for op in ("==", "~=", "<=", ">=", "<", ">"):
        parts = _split_cmp(expr, op)
        if parts:
            l = eval_arith(parts[0], env)
            r = eval_arith(parts[1], env)
            if l is None or r is None:
                return None
            return {"==": l == r, "~=": l != r, "<=": l <= r,
                    ">=": l >= r, "<": l < r, ">": l > r}[op]
    v = eval_arith(expr, env)
    return None if v is None else bool(v)


def _num(v):
    return str(int(v)) if isinstance(v, float) and v.is_integer() else (
        str(v) if isinstance(v, int) else repr(v))


_FOLD_CACHE = {}


def fold_constants(s: str) -> str:
    hit = _FOLD_CACHE.get(s)
    if hit is not None:
        return hit
    out = _fold_constants_impl(s)
    if len(_FOLD_CACHE) > 96:
        _FOLD_CACHE.clear()
    _FOLD_CACHE[s] = out
    return out


def _fold_constants_impl(s: str) -> str:
    for _ in range(40):
        m = re.search(r"\(([0-9+\-*/% .]+)\)", s)
        if not m:
            break
        try:
            v = eval(m.group(1).replace("^", "**"), {"__builtins__": {}}, {})
        except Exception:
            break
        if not isinstance(v, (int, float)):
            break
        s = s[:m.start()] + _num(v) + s[m.end():]

    def _fold_bracket(m):
        try:
            v = eval(m.group(1).replace("^", "**"), {"__builtins__": {}}, {})
        except Exception:
            return m.group(0)
        if not isinstance(v, (int, float)):
            return m.group(0)
        return "[" + _num(v) + "]"

    for _ in range(10):
        s2 = re.sub(r"\[([0-9+\-*/% .]+)\]", _fold_bracket, s)
        if s2 == s:
            break
        s = s2
    return s


_BLOCK_OPEN = {"if", "function", "do", "repeat"}
_BLOCK_TOKENS = re.compile(r"\b(if|function|do|repeat|end|until)\b")
_COMPARE = re.compile(r"\b([A-Za-z_]\w*)\s*(?:<=|>=|==|~=|<|>)\s*[\(\d]")


def _block_ends(src: str):
    ends, stack = {}, []
    for m in _BLOCK_TOKENS.finditer(src):
        if m.group(1) in _BLOCK_OPEN:
            stack.append(m.start())
        elif stack:
            ends[stack.pop()] = m.end()
    return ends


def _find_dispatch(src: str):
    from bisect import bisect_left, bisect_right
    from collections import Counter

    ends = _block_ends(src)
    hits = [(m.start(), m.group(1)) for m in _COMPARE.finditer(src)]
    starts = [h[0] for h in hits]

    best = None
    for m in re.finditer(r"while true do", src):
        blk_end = ends.get(m.end() - 2)
        if blk_end is None or blk_end - m.start() < 80:
            continue
        lo = bisect_left(starts, m.start())
        hi = bisect_right(starts, blk_end)
        if hi - lo < 3:
            continue
        opvar, cnt = Counter(hits[i][1] for i in range(lo, hi)).most_common(1)[0]
        if cnt < 3:
            continue
        if best is None or cnt > best[0]:
            best = (cnt, src[m.start():blk_end], opvar)
    if best is None:
        return None, None
    return best[1], best[2]


def _wb(s, i):
    return i >= len(s) or not (s[i].isalnum() or s[i] == "_")


_THEN_TOK = re.compile(r"\(|\)|\bthen\b")


def _top_then(s, pos):
    depth = 0
    for m in _THEN_TOK.finditer(s, pos):
        t = m.group(0)
        if t == "(":
            depth += 1
        elif t == ")":
            depth -= 1
        elif depth == 0:
            return m.start()
    return -1


_BLK_TOK = re.compile(r"\(|\)|\b(if|elseif|else|then|end|while|for|do|function|repeat|until)\b")
_OPENER = {"if", "do", "function", "repeat"}
_CLOSER = {"end", "until"}


_BRANCH_CACHE = {}


def _split_branches(s, i):
    key = (s, i)
    hit = _BRANCH_CACHE.get(key)
    if hit is not None:
        return hit
    res = _split_branches_uncached(s, i)
    if len(_BRANCH_CACHE) > 128:
        _BRANCH_CACHE.clear()
    _BRANCH_CACHE[key] = res
    return res


def _split_branches_uncached(s, i):
    res = []
    pos = i + 2
    while True:
        tp = _top_then(s, pos)
        if tp < 0:
            return res, len(s)
        cond = s[pos:tp].strip()
        bstart = tp + 4
        depth = 0
        dp = dk = None
        for m in _BLK_TOK.finditer(s, bstart):
            t = m.group(1) or m.group(0)
            if t == "(":
                depth += 1
            elif t == ")":
                depth -= 1
            elif t in _OPENER:
                depth += 1
            elif t in _CLOSER:
                if depth == 0:
                    dp, dk = m.start(), "end"
                    break
                depth -= 1
            elif t in ("elseif", "else") and depth == 0:
                dp, dk = m.start(), t
                break
        if dp is None:
            return res, len(s)
        res.append((cond, s[bstart:dp].strip()))
        if dk == "end":
            return res, dp + 3
        if dk == "else":
            estart = dp + 4
            depth = 0
            for m in _BLK_TOK.finditer(s, estart):
                t = m.group(1) or m.group(0)
                if t == "(":
                    depth += 1
                elif t == ")":
                    depth -= 1
                elif t in _OPENER:
                    depth += 1
                elif t in _CLOSER:
                    if depth == 0:
                        res.append((None, s[estart:m.start()].strip()))
                        return res, m.start() + 3
                    depth -= 1
            return res, len(s)
        pos = dp + len("elseif")


def _rebuild(branches, j):
    parts = []
    for idx in range(j, len(branches)):
        cond, body = branches[idx]
        body = fold_constants(body.strip())
        if idx == j:
            parts.append("if " + cond + " then " + body)
        elif cond is not None:
            parts.append("elseif " + cond + " then " + body)
        else:
            parts.append("else " + body)
    parts.append("end")
    return " ".join(parts)


def _mentions(text, var):
    return re.search(r"\b" + re.escape(var) + r"\b", text) is not None


def _owner_index(blk, opvar, instr):
    if instr:
        m = re.search(r"\b" + re.escape(opvar) + r"\s*=\s*" + re.escape(instr) +
                      r"\s*\[\s*1\s*\]", blk)
        if m:
            mm = re.search(r"\bif\b", blk[m.end():])
            if mm:
                return m.end() + mm.start()
    m = re.search(r"\(?" + re.escape(opvar) + r"\s*(?:<=|>=|==|~=|<|>)", blk)
    if not m:
        return None
    start = m.start()
    depth = 0
    owner = start
    for t in re.finditer(r"\b(if|end|until)\b", blk[:start]):
        if t.group(1) == "if":
            if depth == 0:
                owner = t.start()
            else:
                depth -= 1
        else:
            depth += 1
    return owner


def _eval_dispatch(s, i, env, opvar, depth=0):
    while i < len(s) and s[i] in " \t\r\n":
        i += 1
    if not (s.startswith("if", i) and _wb(s, i + 2)):
        return None
    branches, _end = _split_branches(s, i)
    if not branches:
        return None
    for j, (cond, body) in enumerate(branches):
        if cond is not None and opvar not in cond:
            if len(branches) == 1 and _mentions(body, opvar):
                sub = _eval_dispatch(fold_constants(body.strip()), 0, env, opvar,
                                     depth + 1)
                if sub is not None:
                    return sub
            return _rebuild(branches, j)
        ok = cond is None or (eval_cond(cond, env) is True)
        if not ok:
            continue
        b = fold_constants(body.strip())
        if b.startswith("if") and _wb(b, 2) and depth < 60:
            tp = _top_then(b, 2)
            if opvar in b[2:tp] or _mentions(b, opvar):
                sub = _eval_dispatch(b, 0, env, opvar, depth + 1)
                if sub is not None:
                    return sub
        return b
    return None


def _detect_instr(src, blk, opvar):
    if opvar:
        m = re.search(r"\b" + re.escape(opvar) + r"\s*=\s*([A-Za-z_]\w*)\[\s*1\s*\]", blk)
        if m:
            return m.group(1)
        m = re.search(r"\b" + re.escape(opvar) + r"\s*=\s*([A-Za-z_]\w*)\[", blk)
        if m:
            return m.group(1)
    return None


def _detect_regs(blk, isa, instr):
    from collections import Counter
    c = Counter()
    if instr:
        for body in isa.values():
            for mm in re.finditer(r"\b([A-Za-z_]\w*)\[\s*" + re.escape(instr) +
                                  r"\s*\[\s*[234]\s*\]\s*\]", body):
                c[mm.group(1)] += 1
    if not c:
        return _regs_var(blk, instr)
    return c.most_common(1)[0][0]


def recover_isa(src: str):
    blk, opvar = _find_dispatch(src)
    if blk is None:
        return {}, None, None, None
    instr = _detect_instr(src, blk, opvar)
    owner = _owner_index(blk, opvar, instr)
    if owner is None:
        return {}, opvar, instr, None
    isa = {}
    for k in range(0, 256):
        body = _eval_dispatch(blk, owner, {opvar: k}, opvar)
        if body:
            isa[k] = body
    regs = _detect_regs(blk, isa, instr)
    return isa, opvar, instr, regs


_PATTERNS = [
    (r"^do return\b", "RETURN"),
    (r"^local \w+=\w+\[\w+\[2\]\];do return \w+\(", "TAILCALL"),
    (r"^return \w+\[\w+\[2\]\]$", "RETURN1"),
    (r"\[\w+\[2\]\]=(\w+)\[\w+\[3\] \+ (\d+)\]$", "MOVE_OFF"),
    (r"\[\w+\[2\]\]=\w+\(\w+\[\w+\[3\]\],", "CLOSURE"),
    (r"for \w+=\w+\[2\],\w+\[3\] do \w+\[\w+\]=nil;end", "LOADNIL"),
    (r"for \w+=1,\w+\[3\] do \w+\[\w+\]=\w+\[\w+ \+ \w+\];end", "SETLIST"),
    (r"\]\(\)$", "CALL0"),
    (r"\]\(\w+\(\w+,\w+ \+ 1", "CALL"),
    (r"local \w+=\w+\[\w+\[2\]\];local \w+=\{\w+\[\w+\]\(%", "CALL"),
    (r"local \w+=\w+\[\w+\[2\]\];local \w+=\{\w+\[\w+\]\(", "CALL"),
    (r"\]\([^)]*\)$", "CALL"),
    (r"\{\w+\[\w+\[2\]\]\(", "CALL"),
    (r"\[\w+ \+ 1[^;]*\]=\w+;\w+\[\w+\]=\w+\[\w+\[4\]\]$", "SELF"),
    (r"\[\w+\[2\]\]\[\w+\[3\]\]=", "SETTABLE"),
    (r"\[\w+\[2\]\]=\w+\[\w+\[3\]\]\[\w+\[4\]\]$", "GETTABLE"),
    (r"\[\w+\[2\]\]=\{\}$", "NEWTABLE"),
    (r"\[\w+\[2\]\]\(\w+\[\w+ \+ 1\]\)$", "CALL"),
    (r"\[\w+\[2\]\]\(\)$", "CALL0"),
    (r"\[\w+\[3\]\]=\w+\[\w+\[2\]\]$", "SETUPVAL"),
    (r"\[\w+\[2\]\]=#\w+\[\w+\[3\]\]$", "LEN"),
    (r"\[\w+\[2\]\]= not \w+\[\w+\[3\]\]$", "NOT"),
    (r"\[\w+\[2\]\]= ?-\w+\[\w+\[3\]\]$", "UNM"),
    (r"\[\w+\[2\]\]=\w+\[\w+\[3\]\]~=0$", "LOADBOOL"),
    (r"\[\w+\[2\]\]= ?\.\. ?", "CONCAT"),
    (r"\[\w+\[2\]\]=\w+\[\w+\[3\]\] \+ \w+\[4\]$", "ADD"),
    (r"\[\w+\[2\]\]=\w+\[\w+\[3\]\] -\w+\[4\]$", "SUB"),
    (r"\[\w+\[2\]\]=\w+\[\w+\[3\]\] \* \w+\[4\]$", "MUL"),
    (r"\[\w+\[2\]\]=\w+\[\w+\[3\]\]/\w+\[4\]$", "DIV"),
    (r"\[\w+\[2\]\]=\w+\[\w+\[3\]\] ?% ?\w+\[4\]$", "MOD"),
    (r"\[\w+\[2\]\]=\w+\[\w+\[3\]\] \^ \w+\[4\]$", "POW"),
    (r"\[\w+\[2\]\]=\w+\[\w+\[3\]\]==\w+\[4\]$", "EQ"),
    (r"\[\w+\[2\]\]=\w+\[\w+\[3\]\]<\w+\[4\]$", "LT"),
    (r"\[\w+\[2\]\]=\w+\[\w+\[3\]\]<=\w+\[4\]$", "LE"),
    (r"\[\w+\[2\]\]=\w+\[\w+\[3\]\]$", "@RHSTABLE"),
    (r"\[\w+\[2\]\]=\w+\[3\]$", "LOADK"),
    (r"^v?\w+\[\w+\[3\]\];$", "CLOSE"),
    (r"^v?\w+=\w+\[3\]$", "JMP"),
    (r"=\w+\(\w+,\w+,\w+\)$", "CLOSURE"),
    (r"^\w+\[\w+\[2\]\]=", "SET"),
]


def _regs_var(blk: str, instr: str):
    from collections import Counter
    c = Counter(re.findall(r"\b(\w+)\[", blk))
    c.pop(instr, None)
    return c.most_common(1)[0][0] if c else None


def classify_op(body: str, regs: str = None, globals_var: str = None):
    b = body.strip().rstrip(";").strip()
    for pat, name in _PATTERNS:
        if not re.search(pat, b, re.S):
            continue
        if name == "@RHSTABLE":
            mm = re.search(r"=\s*(\w+)\[", b)
            return "MOVE" if (mm and regs and mm.group(1) == regs) else "GETGLOBAL"
        return name
    return "op"


def _opnd(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return f"R{v}"
    return _fmt_const(v)


def render_ins(ins, name: str) -> str:
    a, b, c = ins["A"], ins["B"], ins["C"]
    A = _opnd(a)
    B = _opnd(b)
    C = _opnd(c)
    if name == "RETURN":
        return "return"
    if name == "RETURN1":
        return f"return {A}"
    if name == "LOADNIL":
        return f"{A}..{B} = nil"
    if name == "LOADK":
        return f"{A} = {_fmt_const(b)}"
    if name == "LOADBOOL":
        return f"{A} = ({_fmt_const(b)} ~= 0)"
    if name == "GETGLOBAL":
        return f"{A} = _ENV[{_fmt_const(b)}]"
    if name == "SETGLOBAL":
        return f"_ENV[{_fmt_const(b)}] = {A}"
    if name == "GETTABLE":
        return f"{A} = {B}[{C}]"
    if name == "SETTABLE":
        return f"{B}[{C}] = {A}"
    if name == "NEWTABLE":
        return f"{A} = {{}}"
    if name == "MOVE":
        return f"{A} = {B}"
    if name == "CALL":
        return f"{A}({_opnd((a + 1) if isinstance(a, int) else a)})"
    if name == "CALL0":
        return f"{A}()"
    if name == "SETUPVAL":
        return f"upval[{B}] = {A}"
    if name == "GETUPVAL":
        return f"{A} = upval[{B}]"
    if name == "JMP":
        return f"goto {b}"
    if name == "CLOSURE":
        return f"{A} = closure(proto, {C})"
    if name == "CLOSE":
        return f"close upvalues >= {A}"
    if name == "CONCAT":
        return f"{A} = {B} .. ..."
    if name in ("ADD", "SUB", "MUL", "DIV", "MOD", "POW", "EQ", "LT", "LE"):
        sym = {"ADD": "+", "SUB": "-", "MUL": "*", "DIV": "/", "MOD": "%",
               "POW": "^", "EQ": "==", "LT": "<", "LE": "<="}[name]
        return f"{A} = {B} {sym} {C}"
    if name == "LEN":
        return f"{A} = #{B}"
    if name == "NOT":
        return f"{A} = not {B}"
    if name == "UNM":
        return f"{A} = -{B}"
    if name == "SET":
        return f"{A} = ..."
    return f"; {name}"


def lift_chunk(chunk, isa, regs, indent=0, out=None):
    out = out if out is not None else []
    pad = "  " * indent
    out.append(f"{pad}; --- chunk: params={chunk['numparams']} "
               f"consts={len(chunk['consts'])} code={sum(1 for c in chunk['code'] if c)} ---")
    for i, k in enumerate(chunk["consts"]):
        out.append(f"{pad}; K{i} = {_fmt_const(k)}")
    for i, ins in enumerate(chunk["code"]):
        if ins is None:
            continue
        body = isa.get(ins["op"], "")
        name = classify_op(body, regs)
        if name == "op":
            snippet = fold_constants(body).replace("\n", " ")
            if len(snippet) > 160:
                snippet = snippet[:160] + " ..."
            out.append(f"{pad}[{i:4}] op{ins['op']:<6} {snippet}")
        else:
            out.append(f"{pad}[{i:4}] {name:<10} {render_ins(ins, name)}")
    for i, p in enumerate(chunk["protos"]):
        out.append(f"{pad}; --- proto[{i}] ---")
        lift_chunk(p, isa, regs, indent + 1, out)
    return out


def _pc_and_code(body: str, instr: str, code_hint: str = None):
    if not instr or not body:
        return None, code_hint
    m = re.search(r"\b" + re.escape(instr) + r"\s*=\s*(\w+)\[(\w+)\]", body)
    if m:
        return m.group(2), m.group(1)
    return None, code_hint


def split_op_steps(body: str, instr: str, code: str = None):
    pc, code = _pc_and_code(body, instr, code)
    if not pc or not code:
        return [body.strip()]
    fetch = re.compile(re.escape(instr) + r"\s*=\s*" + re.escape(code) + r"\[" + re.escape(pc) + r"\]\s*;")
    parts, last = [], 0
    for m in fetch.finditer(body):
        parts.append(body[last:m.start()])
        last = m.end()
    parts.append(body[last:])
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        p = re.sub(r"\b" + re.escape(pc) + r"\s*=\s*" + re.escape(pc) + r"\s*\+\s*[0-9()+\-* .]+;\s*$", "", p).strip()
        if p:
            out.append(p)
    return out


class Reader:
    def __init__(self, data: bytes, pos: int = 0):
        self.d = data
        self.p = pos

    def byte(self):
        v = self.d[self.p]
        self.p += 1
        return v

    def u16(self):
        lo, hi = self.d[self.p], self.d[self.p + 1]
        self.p += 2
        return hi * 256 + lo

    def u32(self):
        b = self.d[self.p:self.p + 4]
        self.p += 4
        return b[3] * 16777216 + b[2] * 65536 + b[1] * 256 + b[0]

    def double(self):
        import struct
        raw = self.u32() | (self.u32() << 32)
        return struct.unpack("<d", raw.to_bytes(8, "little"))[0]

    def string(self):
        ln = self.u32()
        if ln == 0:
            return ""
        s = self.d[self.p:self.p + ln]
        self.p += ln
        return s.decode("latin-1")


MODE_BYTE_BYTE = 0
MODE_WORD = 1
MODE_SWORD = 2
MODE_SWORD_BYTE = 3


def const_at(consts, idx):
    if idx is None:
        return None
    if not isinstance(idx, int) or idx < 1 or idx > len(consts):
        raise ValueError(f"const index {idx} out of range (have {len(consts)})")
    return consts[idx - 1]


def read_chunk(r: Reader, depth: int = 0):
    consts = []
    nconst = r.u32()
    for _ in range(nconst):
        t = r.byte()
        if t == 1:
            consts.append(r.byte() != 0)
        elif t == 2:
            consts.append(r.double())
        elif t == 3:
            consts.append(r.string())
        else:
            consts.append(None)

    numparams = r.byte()

    code = []
    ncode = r.u32()
    for _ in range(ncode):
        desc = r.byte()
        if (desc & 1) != 0:
            code.append(None)
            continue
        mode = (desc >> 1) & 0x3
        mask = (desc >> 3) & 0x7
        op = r.u16()
        a = r.u16()
        b = c = None
        a_raw = b_raw = c_raw = None
        if mode == MODE_BYTE_BYTE:
            b = r.u16()
            c = r.u16()
        elif mode == MODE_WORD:
            b = r.u32()
        elif mode == MODE_SWORD:
            b = r.u32() - (1 << 16)
        elif mode == MODE_SWORD_BYTE:
            b = r.u32() - (1 << 16)
            c = r.u16()
        a_raw, b_raw, c_raw = a, b, c
        if mask & 0x1:
            a = const_at(consts, a)
        if mask & 0x2:
            b = const_at(consts, b)
        if mask & 0x4:
            c = const_at(consts, c)
        code.append({"op": op, "A": a, "B": b, "C": c,
                     "A_raw": a_raw, "B_raw": b_raw, "C_raw": c_raw,
                     "mode": mode, "mask": mask, "desc": desc})

    protos = []
    nproto = r.u32()
    for _ in range(nproto):
        protos.append(read_chunk(r, depth + 1))

    return {
        "consts": consts,
        "numparams": numparams,
        "code": code,
        "protos": protos,
    }


def deserialize(data: bytes):
    r = Reader(data)
    chunk = read_chunk(r)
    chunk["consumed"] = r.p
    chunk["size"] = len(data)
    return chunk


def _unluac_classpath():
    here = os.path.dirname(os.path.abspath(__file__))
    cp = os.path.join(here, "vendor")
    return cp if os.path.isdir(os.path.join(cp, "unluac")) else None


def decompile_vm(src: str, data: bytes):
    import tempfile
    import vm_to_lua as V

    blob, fn = V.vm_to_lua_chunk(src, data)
    cp = _unluac_classpath()
    if not cp:
        raise RuntimeError("unluac classes not found under vendor/unluac")
    with tempfile.TemporaryDirectory() as td:
        luac = os.path.join(td, "chunk.luac")
        with open(luac, "wb") as f:
            f.write(blob)
        p = subprocess.run(["java", "-cp", cp, "unluac.Main", luac],
                           capture_output=True, text=True, errors="replace")
    if p.returncode != 0 or "Exception" in p.stderr:
        tail = (p.stderr.strip().splitlines() or ["unluac failed"])[-1]
        raise RuntimeError(tail)
    return p.stdout, fn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--output")
    ap.add_argument("--dump-bytes")
    ap.add_argument("--listing", action="store_true")
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8", errors="surrogateescape") as f:
        src = f.read()

    payload, info = find_payload(src)

    if payload is not None:
        data = decode_hex_rle(payload)
        print(f"[i] {os.path.basename(args.input)}: VM mode ({info.get('mode')}), "
              f"{len(data)} payload bytes", file=sys.stderr)
        if args.dump_bytes:
            with open(args.dump_bytes, "wb") as f:
                f.write(data)

        if not args.listing:
            try:
                text, fn = decompile_vm(src, data)
                n_raw = len(fn["_raw"])
                print(f"[i] decompiled: {len(fn['code'])} instructions, "
                      f"{len(fn['consts'])} constants, "
                      f"{n_raw} unmapped op(s)", file=sys.stderr)
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(text)
                    print(f"[i] wrote {args.output}", file=sys.stderr)
                else:
                    sys.stdout.write(text)
                return 0
            except Exception as e:
                print(f"[!] decompile failed ({e}); falling back to listing",
                      file=sys.stderr)

        try:
            chunk = deserialize(data)
            isa, opvar, instr, regs = recover_isa(src)
            text = "\n".join(lift_chunk(chunk, isa, regs)) + "\n"
        except Exception as e:
            print(f"[!] malformed payload ({type(e).__name__}: {e})", file=sys.stderr)
            return 2
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"[i] wrote {args.output}", file=sys.stderr)
        else:
            sys.stdout.write(text)
        return 0

    out, sinfo = deobfuscate_strings(src)
    if sinfo.get("mode") is None:
        print("[!] no LuaObfuscator pattern found", file=sys.stderr)
        return 2
    print(f"[i] {os.path.basename(args.input)}: string mode, "
          f"{sinfo['count']} literals decrypted", file=sys.stderr)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"[i] wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
