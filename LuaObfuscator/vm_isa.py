import re

_RK_BIT = {"A": 1, "B": 2, "C": 4}
_FIELD = {2: "A", 3: "B", 4: "C"}


def _reg(ins, field):
    v = ins.get(field + "_raw")
    return 0 if v is None else v


def _rk(ins, field):
    raw = ins.get(field + "_raw")
    if raw is None:
        return 0
    if ins.get("mask", 0) & _RK_BIT[field]:
        return 256 + (raw - 1)
    return raw


def _is_const(ins, field):
    return bool(ins.get("mask", 0) & _RK_BIT[field])


def _pick(ins, tok, field):
    if tok is None:
        return _rk(ins, field)
    return _rk(ins, field) if tok.startswith("I[") else _reg(ins, field)


def _fold_int(m):
    try:
        v = eval(m.group(1), {"__builtins__": {}}, {})
    except Exception:
        return m.group(0)
    return str(int(v)) if isinstance(v, (int, float)) and float(v).is_integer() \
        else m.group(0)


def normalize(body, ctx):
    s = body
    for key, tok in (("code", "C"), ("instr", "I"), ("pc", "PC"),
                     ("regs", "R")):
        v = ctx.get(key)
        if v:
            s = re.sub(r"\b" + re.escape(v) + r"\b", tok, s)
    s = re.sub(r"\bv\d+\b", "V", s)
    s = re.sub(r"\s+", "", s).strip().rstrip(";")
    s = re.sub(r"\bV=nil;", "", s)
    s = re.sub(r"(?<![A-Za-z0-9_])(\d+(?:[-+*/]\d+)+)", _fold_int, s)
    s = re.sub(r"^(local[A-Za-z0-9_,]*;)+", "", s)
    s = re.sub(r"\+0(?![0-9])", "", s)
    return s


def _operand(tok, ins):
    m = re.fullmatch(r"R\[I\[(\d)\]\]", tok) or re.fullmatch(r"I\[(\d)\]", tok)
    if not m:
        return None
    f = _FIELD.get(int(m.group(1)))
    return _rk(ins, f) if f else None


def _is_fall(seg):
    return re.fullmatch(r"PC=PC\+[0-9+]+", seg) is not None


def _target_from_b(ins):
    return _reg(ins, "B")


_OPEN = ("if", "for", "while", "do", "function", "repeat")

_KEYWORDS = ("elseif", "else", "then", "end", "until", "while", "repeat",
             "function", "return", "local", "for", "do", "if", "break",
             "and", "or", "not", "in")
_IDENT_OK = {"V", "R", "I", "PC", "C", "nil", "true", "false"}


def _scan_word(s, i):
    m = re.match(r"[A-Za-z_]\w*", s[i:])
    if not m:
        return None, i, i
    w = m.group(0)
    we = i + len(w)
    if w in _IDENT_OK or w in _KEYWORDS:
        return (w if w in _KEYWORDS else None), we, we
    for k in _KEYWORDS:
        if w.startswith(k) and len(w) > len(k):
            return k, i + len(k), we
    return None, we, we


def _split_if(norm):
    if not norm.startswith("if") or not norm.endswith("end"):
        return None
    i = 2
    depth = 0
    then_pos = -1
    n = len(norm)
    while i < n:
        if norm.startswith("then", i) and depth == 0:
            then_pos = i
            break
        c = norm[i]
        if c == "(":
            depth += 1
            i += 1
            continue
        if c == ")":
            depth -= 1
            i += 1
            continue
        kw, kend, wend = _scan_word(norm, i)
        if kw in _OPEN:
            depth += 1
        elif kw in ("end", "until"):
            depth -= 1
        i = wend if wend > i else i + 1
    if then_pos < 0:
        return None
    cond = norm[2:then_pos]
    j = then_pos + 4
    depth = 0
    else_pos = -1
    while j < n:
        kw, kend, wend = _scan_word(norm, j)
        if kw in _OPEN:
            depth += 1
        elif kw in ("end", "until"):
            if depth == 0:
                break
            depth -= 1
        elif kw in ("else", "elseif") and depth == 0:
            else_pos = j
            break
        j = wend if wend > j else j + 1
    if else_pos < 0:
        return cond, norm[then_pos + 4:j].strip(";"), ""
    body_a = norm[then_pos + 4:else_pos].strip(";")
    k = else_pos + 4
    depth = 0
    while k < n:
        kw, kend, wend = _scan_word(norm, k)
        if kw in _OPEN:
            depth += 1
        elif kw in ("end", "until"):
            if depth == 0:
                break
            depth -= 1
        k = wend if wend > k else k + 1
    body_b = norm[else_pos + 4:k].strip(";")
    return cond, body_a, body_b


def _clean_cond(cond):
    c = cond
    for _ in range(6):
        prev = c
        c = re.sub(r"\([0-9+\-*/%<>=.\s]+\)and", "", c)
        c = re.sub(r"and\([0-9+\-*/%<>=.\s]+\)", "", c)
        c = re.sub(r"\([0-9+\-*/%<>=.\s]+\)or", "", c)
        c = re.sub(r"or\([0-9+\-*/%<>=.\s]+\)", "", c)
        if c == prev:
            break
    while c.startswith("(") and c.endswith(")"):
        depth = 0
        ok = True
        for i, ch in enumerate(c):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and i != len(c) - 1:
                    ok = False
                    break
        if not ok:
            break
        c = c[1:-1]
    return c


def _cond_ops(cond, a, b, ins):
    if _is_fall(a) and b == "PC=I[3]":
        tgt, jump_when_true = _target_from_b(ins), False
    elif _is_fall(b) and a == "PC=I[3]":
        tgt, jump_when_true = _target_from_b(ins), True
    else:
        return None

    cond = _clean_cond(cond)
    neg = False
    if cond.startswith("not"):
        neg = True
        cond = _clean_cond(cond[3:])
    want = jump_when_true ^ neg

    lhs = _operand(cond, ins)
    if lhs is not None:
        return [("TEST", lhs, 0, 1 if want else 0), ("JMP", 0, tgt, None)]

    m = re.fullmatch(r"\(?(R\[I\[2\]\]|I\[2\])(==|~=|<|<=|>|>=)"
                     r"(R\[I\[4\]\]|I\[4\])\)?", cond)
    if not m:
        return None
    lo = _operand(m.group(1), ins)
    ro = _operand(m.group(3), ins)
    op = m.group(2)
    if lo is None or ro is None:
        return None
    if op in (">", ">="):
        lo, ro = ro, lo
        op = "<" if op == ">" else "<="
    lua = {"==": "EQ", "~=": "EQ", "<": "LT", "<=": "LE"}[op]
    exp = 1 if want else 0
    if op == "~=":
        exp = 1 - exp
    return [(lua, exp, lo, ro), ("JMP", 0, tgt, None)]


def _testset_ops(norm, ins):
    m = re.fullmatch(r"(?:local)?V=R\[I\[4\]\];if(not)?Vthen(.*?);"
                     r"elseR\[I\[2\]\]=V;PC=I\[3\];end", norm)
    if not m:
        return None
    neg = m.group(1) is not None
    a = m.group(2)
    if not _is_fall(a):
        return None
    want = True ^ neg
    dst = _reg(ins, "A")
    src = _reg(ins, "C")
    return [("TESTSET", dst, src, 1 if want else 0),
            ("JMP", 0, _target_from_b(ins), None)]


def _call_ops(m, ins, kind):
    a = _reg(ins, "A")
    last = m.group(1)
    b = 0 if last == "V" else max(1, _reg(ins, "B") - a + 1)
    return [("CALL", a, b, {"none": 1, "one": 2, "many": 0}[kind])]


SIMPLE = [
    (r"^R\[I\[2\]\]=R\[I\[3\]\]$", lambda i, m: [("MOVE", _reg(i, "A"), _reg(i, "B"), None)]),
    (r"^PC=I\[3\]$", lambda i, m: [("JMP", 0, _reg(i, "B"), None)]),
    (r"^R\[I\[2\]\]=R\[I\[3\]\]\[(I\[4\]|R\[I\[4\]\])\]$",
     lambda i, m: [("GETTABLE", _reg(i, "A"), _reg(i, "B"),
                    _pick(i, m.group(1), "C"))]),
    (r"^R\[I\[2\]\]\[(I\[3\]|R\[I\[3\]\])\]=(I\[4\]|R\[I\[4\]\])$",
     lambda i, m: [("SETTABLE", _reg(i, "A"), _pick(i, m.group(1), "B"),
                    _pick(i, m.group(2), "C"))]),
    (r"^R\[I\[2\]\]=I\[3\]$",
     lambda i, m: [("LOADK", _reg(i, "A"), _reg(i, "B") - 1, None)]),
    (r"^R\[I\[2\]\]=I\[3\]~=0$",
     lambda i, m: [("LOADBOOL", _reg(i, "A"), 1 if _reg(i, "B") else 0, _reg(i, "C"))]),
    (r"^R\[I\[2\]\]=\{\}$",
     lambda i, m: [("NEWTABLE", _reg(i, "A"), 0, 0)]),
    (r"^forV=I\[2\],I\[3\]doR\[V\]=nil;end$",
     lambda i, m: [("LOADNIL", _reg(i, "A"), _reg(i, "B"), None)]),
    (r"^V\[I\[3\]\]=R\[I\[2\]\]$",
     lambda i, m: ([("SETGLOBAL", _reg(i, "A"), _reg(i, "B") - 1, None)]
                   if _is_const(i, "B") else
                   [("SETUPVAL", _reg(i, "A"), _reg(i, "B"), None)])),
    (r"^R\[I\[2\]\]=V\[I\[3\]\]$",
     lambda i, m: ([("GETGLOBAL", _reg(i, "A"), _reg(i, "B") - 1, None)]
                   if _is_const(i, "B") else
                   [("GETUPVAL", _reg(i, "A"), _reg(i, "B"), None)])),
    (r"^doreturn;end$", lambda i, m: [("RETURN", 0, 1, None)]),
    (r"^doreturnR\[I\[2\]\];end$", lambda i, m: [("RETURN", _reg(i, "A"), 2, None)]),
    (r"^R\[I\[2\]\]=notR\[I\[3\]\]$", lambda i, m: [("NOT", _reg(i, "A"), _reg(i, "B"), None)]),
    (r"^R\[I\[2\]\]=-R\[I\[3\]\]$", lambda i, m: [("UNM", _reg(i, "A"), _reg(i, "B"), None)]),
    (r"^R\[I\[2\]\]=#R\[I\[3\]\]$", lambda i, m: [("LEN", _reg(i, "A"), _reg(i, "B"), None)]),
    (r"^R\[I\[2\]\]=(R\[I\[3\]\]|I\[3\])([+\-*/%^])(R\[I\[4\]\]|I\[4\])$",
     lambda i, m: [({"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV",
                     "%": "MOD", "^": "POW"}[m.group(2)],
                    _reg(i, "A"), _pick(i, m.group(1), "B"),
                    _pick(i, m.group(3), "C"))]),
    (r"^(?:local)?V=I\[2\];(?:local)?V=R\[I\[3\]\];R\[V\+1\]=V;"
     r"R\[V\]=V\[(I\[4\]|R\[I\[4\]\])\]$",
     lambda i, m: [("SELF", _reg(i, "A"), _reg(i, "B"),
                    _pick(i, m.group(1), "C"))]),
    (r"^(?:local)?V=I\[2\];(?:local)?V=R\[V\];forV=1,I\[3\]doV\[V\]=R\[V\+V\];end$",
     lambda i, m: [("SETLIST", _reg(i, "A"), _reg(i, "B"), 1)]),
    (r"^(?:local)?V=I\[2\];(?:local)?V=R\[V\];(?:local)?V=I\[3\];"
     r"forV=1,VdoV\[V\]=R\[V\+V\];end$",
     lambda i, m: [("SETLIST", _reg(i, "A"), _reg(i, "B"), 1)]),
    (r"^(?:local)?V=I\[2\];(?:local)?V=R\[V\];(?:local)?V=I\[3\];"
     r"forV=1,VdoV\[V\]=R\[V\+V\];end(?:V\(\);)?$",
     lambda i, m: [("SETLIST", _reg(i, "A"), _reg(i, "B"), 1)]),
    (r"^(?:local)?V=I\[2\];(?:local)?V=R\[V\];forV=V\+1,VdoV\(V,R\[V\]\);end$",
     lambda i, m: [("SETLIST", _reg(i, "A"), _reg(i, "B"), 1)]),
    (r"^(?:local)?V=I\[3\];(?:local)?V=R\[V\];forV=V\+1,I\[4\]doV=V\.\.R\[V\];endR\[I\[2\]\]=V$",
     lambda i, m: [("CONCAT", _reg(i, "A"), _reg(i, "B"), _reg(i, "C"))]),
    (r"^R\[I\[2\]\]\(\)$", lambda i, m: [("CALL", _reg(i, "A"), 1, 1)]),
    (r"^(?:local)?V=I\[2\];(?:local)?V,V=V\(R\[V\]\(\)\);"
     r"(?:V|PC)=\(V\+V\)-1;(?:local)?V=0;"
     r"forV=V,(?:V|PC)doV=V\+1;R\[V\]=V\[V\];end$",
     lambda i, m: [("CALL", _reg(i, "A"), 1, 0)]),
    (r"^(?:local)?V=I\[2\];R\[V\]\(R\[V\+1\]\)$",
     lambda i, m: [("CALL", _reg(i, "A"), 2, 1)]),
    (r"^(?:local)?V=I\[2\];R\[V\]=R\[V\]\(R\[V\+1\]\)$",
     lambda i, m: [("CALL", _reg(i, "A"), 2, 2)]),
    (r"^(?:local)?V=I\[2\];R\[V\]=R\[V\]\(\)$",
     lambda i, m: [("CALL", _reg(i, "A"), 1, 2)]),
    (r"^(?:local)?V=I\[2\];R\[V\]=R\[V\]\(V\(R,V\+1,(I\[3\]|V)\)\)$",
     lambda i, m: _call_ops(m, i, "one")),
    (r"^(?:local)?V=I\[2\];R\[V\]\(V\(R,V\+1,(I\[3\]|V)\)\)$",
     lambda i, m: _call_ops(m, i, "none")),
    (r"^(?:local)?V=I\[2\];(?:local)?V=\{R\[V\]\(R\[V\+1\]\)\};",
     lambda i, m: [("CALL", _reg(i, "A"), 2, 0)]),
    (r"^(?:local)?V=I\[2\];(?:local)?V,V=V\(R\[V\]\(R\[V\+1\]\)\);",
     lambda i, m: [("CALL", _reg(i, "A"), 2, 0)]),
    (r"^(?:local)?V=I\[2\];(?:local)?V,V=V\(R\[V\]\(V\(R,V\+1,(I\[3\]|V)\)\)\);",
     lambda i, m: _call_ops(m, i, "many")),
    (r"^(?:local)?V=I\[2\];(?:local)?V=\{R\[V\]\(V\(R,V\+1,(I\[3\]|V)\)\)\};",
     lambda i, m: _call_ops(m, i, "many")),
    (r"^(?:local)?V=I\[2\];doreturnV\(R,V,V\);end$",
     lambda i, m: [("RETURN", _reg(i, "A"), 0, None)]),
    (r"^doreturnR\[I\[2\]\]\(\);end$",
     lambda i, m: [("TAILCALL", _reg(i, "A"), 0, 0)]),
    (r"^(?:local)?V=I\[2\];doreturnR\[V\]\(",
     lambda i, m: [("TAILCALL", _reg(i, "A"), _reg(i, "B"), 0)]),
    (r"^R\[I\[2\]\]=V\(V\[I\[3\]\],",
     lambda i, m: [("CLOSURE", _reg(i, "A"), _reg(i, "B"), 0)]),
]

_CLOSURE_ENV = re.compile(r"__index=function")


def _balanced(t):
    if not (t.startswith("(") and t.endswith(")")):
        return False
    d = 0
    for i, ch in enumerate(t):
        if ch == "(":
            d += 1
        elif ch == ")":
            d -= 1
            if d == 0 and i != len(t) - 1:
                return False
    return d == 0


def _split_top(s, kw):
    out, d, last, i = [], 0, 0, 0
    while i < len(s):
        c = s[i]
        if c == "(":
            d += 1
        elif c == ")":
            d -= 1
        elif d == 0 and s.startswith(kw, i) \
                and (i == 0 or not (s[i - 1].isalnum() or s[i - 1] == "_")) \
                and (i + len(kw) >= len(s)
                     or not (s[i + len(kw)].isalnum() or s[i + len(kw)] == "_")):
            out.append(s[last:i])
            i += len(kw)
            last = i
            continue
        i += 1
    out.append(s[last:])
    return out


def _const_int(expr):
    e = re.sub(r"\s+", "", expr or "")
    if not e or not re.fullmatch(r"[0-9+\-*/()]+", e):
        return None
    try:
        v = eval(e, {"__builtins__": {}}, {})
    except Exception:
        return None
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return int(v) if float(v).is_integer() else None


def _const_bool(expr):
    e = re.sub(r"\s+", "", expr or "")
    if not e or not re.fullmatch(r"[0-9+\-*/()<>=~.]+", e):
        return None
    try:
        return bool(eval(e, {"__builtins__": {}}, {}))
    except Exception:
        return None


def _guard_states(cond, state):
    c = re.sub(r"\s+", "", cond)
    while _balanced(c):
        c = c[1:-1]
    acc = set()
    for part in _split_top(c, "or"):
        s = _guard_term(part, state)
        if s is None:
            return None
        if s == "ALL":
            return "ALL"
        acc |= s
    return acc


def _guard_term(t, state):
    t = t.strip()
    while _balanced(t):
        t = t[1:-1]
    subs = _split_top(t, "and")
    if len(subs) > 1:
        acc = "ALL"
        for s in subs:
            st = _guard_term(s, state)
            if st is None:
                return None
            if st == "ALL":
                continue
            acc = set(st) if acc == "ALL" else (acc & st)
        return acc
    t = t.strip()
    pat = (r"\(?(?:\(?(\d+)\)?==\b" + re.escape(state) + r"\b)\)?"
           r"|\(?\b" + re.escape(state) + r"\b==\(?(\d+)\)?\)?")
    m = re.fullmatch(pat, t)
    if m:
        return {int(m.group(1) or m.group(2))}
    b = _const_bool(t)
    if b is not None:
        return "ALL" if b else set()
    return None


def _next_state(payload, state):
    assigns = re.findall(r"\b" + re.escape(state) + r"\s*=\s*([^;]+);", payload)
    if not assigns:
        return None
    return _const_int(assigns[-1])


_BLOCK_TOK = re.compile(r"\b(if|elseif|else|then|end|while|for|do|function|"
                        r"repeat|until)\b")


def _find_block_end(s, start):
    depth = 0
    pending_do = 0
    for t in _BLOCK_TOK.finditer(s, start):
        w = t.group(1)
        if w in ("for", "while"):
            depth += 1
            pending_do += 1
        elif w == "do":
            if pending_do:
                pending_do -= 1
            else:
                depth += 1
        elif w in ("if", "function", "repeat"):
            depth += 1
        elif w in ("end", "until"):
            if depth == 0:
                return t.start()
            depth -= 1
    return -1


def _payloads(body, state):
    out = []
    for im in re.finditer(r"\bif\b", body):
        j = im.end()
        while j < len(body) and body[j] in " \t\r\n":
            j += 1
        if j >= len(body) or body[j] != "(":
            continue
        depth, k = 0, j
        while k < len(body):
            if body[k] == "(":
                depth += 1
            elif body[k] == ")":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        cond = body[j + 1:k]
        if not re.search(r"\b" + re.escape(state) + r"\b", cond):
            continue
        rest = body[k + 1:]
        tm = re.match(r"\s*then\b", rest)
        if not tm:
            continue
        bstart = k + 1 + tm.end()
        end_pos = _find_block_end(body, bstart)
        if end_pos < 0:
            continue
        g = _guard_states(cond, state)
        if g is None:
            continue
        out.append((g, body[bstart:end_pos]))
    return out


def _clean_payloads(payloads, state):
    cleaned = []
    for st in payloads:
        st = re.sub(r"\b" + re.escape(state) + r"\s*=\s*[^;]+;", ";", st)
        st = re.sub(r"\bbreak\s*;", ";", st)
        st = st.strip().strip(";").strip()
        if st:
            cleaned.append(st)
    return ";".join(cleaned) if cleaned else None


def _state_var(body):
    votes = {}
    for m in re.finditer(r"\b(\w+)\s*==\s*\(?\d+", body):
        v = m.group(1)
        votes[v] = votes.get(v, 0) + 1
    if not votes:
        return None
    return max(votes, key=votes.get)


def _fragment(body):
    state = _state_var(body)
    if not state:
        return None
    stmts = []
    pat = re.compile(r"\bif\s*\(([^()]*\b" + re.escape(state) + r"\b[^()]*)\)\s*then\b")
    for m in pat.finditer(body):
        if _guard_states(m.group(1), state) is None:
            continue
        rest = body[m.end():]
        end = _find_block_end(rest, 0)
        if end < 0:
            nxt = pat.search(rest)
            end = nxt.start() if nxt else len(rest)
        stmts.append(rest[:end])
    if not stmts:
        return None
    return _clean_payloads(stmts, state)


def _strip_runtime(payload, ctx):
    instr, pc, code = ctx.get("instr"), ctx.get("pc"), ctx.get("code")
    if instr and pc and code:
        payload = re.sub(r"\b" + re.escape(instr) + r"\s*=\s*" + re.escape(code)
                         + r"\s*\[" + re.escape(pc) + r"\]\s*;", ";", payload)
        payload = re.sub(r"\b" + re.escape(pc) + r"\s*=\s*" + re.escape(pc)
                         + r"\s*\+\s*[^;]+;", ";", payload)
    return payload


def unflatten_blocks(body, ctx):
    m = re.search(r"local\s+(\w+)\s*=\s*([^;]+);"
                  r"(?:\s*local\s+\w+\s*;)*\s*while true do", body)
    if not m:
        return None
    state = m.group(1)
    blocks = _payloads(body, state)
    init = _const_int(m.group(2))
    if not blocks or init is None:
        return None

    order, used, cur = [], set(), init
    for _ in range(len(blocks) + 4):
        pick = None
        for idx, (g, _p) in enumerate(blocks):
            if idx not in used and g != "ALL" and cur in g:
                pick = idx
                break
        if pick is None:
            for idx, (g, _p) in enumerate(blocks):
                if idx not in used and g == "ALL":
                    pick = idx
                    break
        if pick is None:
            break
        used.add(pick)
        payload = blocks[pick][1]
        order.append(payload)
        if re.search(r"\bbreak\b", payload):
            break
        nxt = _next_state(payload, state)
        if nxt is None:
            break
        cur = nxt

    if not order:
        return None
    out = []
    for p in order:
        p = _strip_runtime(p, ctx)
        p = re.sub(r"\b" + re.escape(state) + r"\s*=\s*[^;]+;", ";", p)
        p = re.sub(r"\bbreak\s*;", ";", p)
        p = p.strip().strip(";").strip()
        if p:
            out.append(p)
    return out or None


def _unflatten_seq(body, state):
    return _clean_payloads([p for _g, p in _payloads(body, state)], state)


def _unflatten(body, ctx):
    if "while true do" not in body:
        return None
    m = re.search(r"local\s+(\w+)\s*=\s*([^;]+);"
                  r"(?:\s*local\s+\w+\s*;)*\s*while true do", body)
    if not m:
        return None
    state = m.group(1)

    blocks = _payloads(body, state)
    if not blocks:
        return None

    init = _const_int(m.group(2))
    if init is None:
        return _unflatten_seq(body, state)

    order, used, cur = [], set(), init
    for _ in range(len(blocks) + 4):
        pick = None
        for idx, (g, _p) in enumerate(blocks):
            if idx not in used and g != "ALL" and cur in g:
                pick = idx
                break
        if pick is None:
            for idx, (g, _p) in enumerate(blocks):
                if idx not in used and g == "ALL":
                    pick = idx
                    break
        if pick is None:
            break
        used.add(pick)
        payload = blocks[pick][1]
        order.append(payload)
        if re.search(r"\bbreak\b", payload):
            break
        nxt = _next_state(payload, state)
        if nxt is None:
            break
        cur = nxt

    if not order:
        return _unflatten_seq(body, state)
    return _clean_payloads(order, state)


def _match(norm, ins):
    if norm.startswith("if") and norm.endswith("end"):
        parts = _split_if(norm)
        if parts:
            ops = _cond_ops(parts[0], parts[1], parts[2], ins)
            if ops:
                return ops
    if re.match(r"^(?:local)?V=R\[I\[4\]\];if", norm):
        ops = _testset_ops(norm, ins)
        if ops:
            return ops

    if _CLOSURE_ENV.search(norm):
        return [("CLOSURE", _reg(ins, "A"), _reg(ins, "B"), _reg(ins, "C"))]

    for pat, fn in SIMPLE:
        m = re.match(pat, norm)
        if not m:
            continue
        try:
            ops = fn(ins, m)
        except Exception:
            return None
        if ops:
            return ops
    return None


def emit(body, ins, ctx):
    ops = _match(normalize(body, ctx), ins)
    if ops:
        return ops
    un = _unflatten(body, ctx)
    if un:
        ops = _match(normalize(un, ctx), ins)
        if ops:
            return ops
    frag = _fragment(body)
    if frag:
        return _match(normalize(frag, ctx), ins)
    return None
