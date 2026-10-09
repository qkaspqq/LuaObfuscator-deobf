import struct

OPNAMES = [
    "MOVE", "LOADK", "LOADBOOL", "LOADNIL", "GETUPVAL", "GETGLOBAL", "GETTABLE",
    "SETGLOBAL", "SETUPVAL", "SETTABLE", "NEWTABLE", "SELF", "ADD", "SUB",
    "MUL", "DIV", "MOD", "POW", "UNM", "NOT", "LEN", "CONCAT", "JMP", "EQ",
    "LT", "LE", "TEST", "TESTSET", "CALL", "TAILCALL", "RETURN", "FORLOOP",
    "FORPREP", "TFORLOOP", "SETLIST", "CLOSE", "CLOSURE", "VARARG",
]
OP = {n: i for i, n in enumerate(OPNAMES)}

IABC = "iABC"
IABX = "iABx"
IASBX = "iAsBx"
OPMODE = {n: IABC for n in OPNAMES}
for n in ("LOADK", "GETGLOBAL", "SETGLOBAL", "CLOSURE"):
    OPMODE[n] = IABX
for n in ("JMP", "FORLOOP", "FORPREP"):
    OPMODE[n] = IASBX

SIZE_Bx = 262144
MAXARG_Bx = SIZE_Bx - 1
OFFSET_sBx = MAXARG_Bx >> 1


def iABC(op, a, b=0, c=0):
    return (op & 0x3F) | ((a & 0xFF) << 6) | ((c & 0x1FF) << 14) | ((b & 0x1FF) << 23)


def iABx(op, a, bx):
    return (op & 0x3F) | ((a & 0xFF) << 6) | ((bx & 0x3FFFF) << 14)


def iAsBx(op, a, sbx):
    return iABx(op, a, sbx + OFFSET_sBx)


def make_ins(name, a, b=0, c=0):
    op = OP[name]
    mode = OPMODE[name]
    if mode == IABC:
        return iABC(op, a, b, c)
    if mode == IABX:
        return iABx(op, a, b)
    return iAsBx(op, a, b)


def _size_t(n):
    return struct.pack("<I", n)


def _string(s):
    if s is None:
        return _size_t(0)
    b = s.encode("latin-1", "replace") if isinstance(s, str) else s
    return _size_t(len(b) + 1) + b + b"\x00"


def _constant(k):
    if k is None:
        return b"\x00"
    if isinstance(k, bool):
        return b"\x01" + (b"\x01" if k else b"\x00")
    if isinstance(k, (int, float)):
        return b"\x03" + struct.pack("<d", float(k))
    if isinstance(k, (str, bytes)):
        return b"\x04" + _string(k)
    raise ValueError(f"unsupported constant {k!r}")


def write_function(fn, out):
    out.append(_string(fn.get("source")))
    out.append(struct.pack("<i", fn.get("linedefined", 0)))
    out.append(struct.pack("<i", fn.get("lastlinedefined", 0)))
    out.append(bytes([fn.get("nups", 0) & 0xFF]))
    out.append(bytes([fn.get("numparams", 0) & 0xFF]))
    out.append(bytes([fn.get("is_vararg", 2) & 0xFF]))
    out.append(bytes([fn.get("maxstacksize", 2) & 0xFF]))

    code = fn["code"]
    out.append(_size_t(len(code)))
    out.append(b"".join(struct.pack("<I", w) for w in code))

    consts = fn.get("consts", [])
    out.append(_size_t(len(consts)))
    for k in consts:
        out.append(_constant(k))

    protos = fn.get("protos", [])
    out.append(_size_t(len(protos)))
    for p in protos:
        write_function(p, out)

    lines = fn.get("lines", [])
    out.append(_size_t(len(lines)))
    out.append(b"".join(struct.pack("<I", ln) for ln in lines))
    locals_ = fn.get("locals", [])
    out.append(_size_t(len(locals_)))
    for name, startpc, endpc, _register in locals_:
        out.append(_string(name))
        out.append(struct.pack("<i", startpc))
        out.append(struct.pack("<i", endpc))
    out.append(_size_t(0))


def build_chunk(fn):
    hdr = b"\x1bLua" + bytes([0x51, 0x00, 0x01, 0x04, 0x04, 0x04, 0x08, 0x00])
    out = [hdr]
    write_function(fn, out)
    return b"".join(out)
