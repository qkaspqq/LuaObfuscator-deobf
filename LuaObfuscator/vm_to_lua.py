import os

import lua51_chunk as L
import luaobf_deobf as D
import vm_isa


def _steps(body, instr, ctx):
    split = D.split_op_steps(body, instr)
    if "while true do" in body:
        blocks = vm_isa.unflatten_blocks(body, ctx)
        if blocks and len(blocks) == len(split):
            return blocks
    return split


def _expand(chunk, isa, instr, regs, ctx=None):
    atoms, vm2a = [], {}
    code = chunk["code"]
    pc = 0
    while pc < len(code):
        ins = code[pc]
        if ins is None:
            pc += 1
            continue
        body = D.fold_constants(isa.get(ins["op"], ""))
        steps = _steps(body, instr, ctx or {}) or [""]
        vm2a[pc] = len(atoms)
        for j, st in enumerate(steps):
            sub = code[pc + j] if (pc + j) < len(code) and code[pc + j] else ins
            atoms.append({"sem": D.classify_op(st, regs), "text": st,
                          "ins": sub, "vm_pc": pc + j})
        advance = len(steps)
        if D.classify_op(body, regs) == "CLOSURE":
            nup = ins.get("C")
            if isinstance(nup, int) and nup > 0:
                advance += nup
        pc += advance
    return atoms, vm2a


_RK = 256


def _decode(w):
    op = w & 0x3F
    name = L.OPNAMES[op]
    a = (w >> 6) & 0xFF
    mode = L.OPMODE[name]
    if mode == L.IABX:
        return (name, a, (w >> 14) & 0x3FFFF, 0)
    if mode == L.IASBX:
        return (name, a, (w >> 14) - 131071, 0)
    return (name, a, (w >> 23) & 0x1FF, (w >> 14) & 0x1FF)


def _touched_regs(op):
    name = op[0]
    a = op[1] if op[1] is not None else 0
    b = op[2] if len(op) > 2 and op[2] is not None else 0
    c = op[3] if len(op) > 3 and op[3] is not None else 0
    if name in ("JMP",):
        return ()
    if name in ("LOADK", "GETGLOBAL", "SETGLOBAL", "GETUPVAL", "SETUPVAL",
                "CLOSURE", "LOADBOOL", "NEWTABLE", "CLOSE"):
        return (a,)
    if name in ("UNM", "NOT", "LEN"):
        return (a, b)
    if name == "VARARG":
        return tuple(range(a, a + max(b, 1)))
    if name == "CONCAT":
        return tuple(r for r in range(min(b, c), max(b, c) + 1))
    if name == "SETLIST":
        return tuple(range(a, a + max(b, 1) + 1))
    if name == "LOADNIL":
        return tuple(range(min(a, b), max(a, b) + 1))
    if name == "MOVE":
        return (a, b)
    if name in ("GETTABLE", "ADD", "SUB", "MUL", "DIV", "MOD", "POW"):
        out = [a]
        if b < _RK:
            out.append(b)
        if c < _RK:
            out.append(c)
        return tuple(out)
    if name == "SETTABLE":
        out = [a]
        if b < _RK:
            out.append(b)
        if c < _RK:
            out.append(c)
        return tuple(out)
    if name in ("EQ", "LT", "LE"):
        out = []
        if b < _RK:
            out.append(b)
        if c < _RK:
            out.append(c)
        return tuple(out)
    if name == "TEST":
        return (a,)
    if name == "TESTSET":
        return (a, b)
    if name == "SELF":
        out = [a, a + 1, b]
        if c < _RK:
            out.append(c)
        return tuple(out)
    if name in ("CALL", "TAILCALL"):
        out = [a]
        if b >= 1:
            out.extend(range(a, a + b))
        if c >= 2:
            out.extend(range(a, a + c - 1))
        return tuple(out)
    if name == "RETURN":
        if b >= 2:
            return tuple(range(a, a + b - 1))
        return (a,)
    if name in ("FORPREP", "FORLOOP"):
        return (a, a + 1, a + 2)
    if name == "TFORLOOP":
        return (a, a + 1, a + 2, a + 3)
    return (a,)


def _written_regs(op):
    name = op[0]
    a = op[1] or 0
    b = op[2] or 0
    c = op[3] or 0
    if name == "LOADNIL":
        return tuple(range(min(a, b), max(a, b) + 1))
    if name == "VARARG":
        return tuple(range(a, a + max(b, 1)))
    if name in ("MOVE", "LOADK", "LOADBOOL", "GETUPVAL", "GETGLOBAL", "GETTABLE",
                "NEWTABLE", "ADD", "SUB", "MUL", "DIV", "MOD", "POW", "UNM",
                "NOT", "LEN", "CONCAT", "CLOSURE", "TESTSET"):
        return (a,)
    if name == "SELF":
        return (a, a + 1)
    if name in ("CALL", "TAILCALL"):
        return tuple(range(a, a + c - 1)) if c >= 2 else ()
    return ()


def _fb2int(x):
    e = (x >> 3) & 0x1F
    return x if e == 0 else ((x & 7) + 8) << (e - 1)


def _fb_encode(n):
    if n <= 0:
        return 0
    for x in range(1, 232):
        if _fb2int(x) >= n:
            return x
    return 231


def _max_register(ops):
    m = 0
    for op in ops:
        for r in _touched_regs(op):
            if r > m:
                m = r
    return m


def _read_counts(ops, nreg):
    rc = [0] * nreg
    for op in ops:
        for r in _touched_regs(op):
            if 0 <= r < nreg:
                rc[r] += 1
    return rc


def _valid_ops(ops, nconst, nproto):
    for op in ops:
        name = op[0]
        if name == "JMP":
            continue
        a, b, c = op[1], op[2], op[3]
        if name in ("LOADK", "GETGLOBAL", "SETGLOBAL"):
            if not (0 <= b < nconst):
                return False
        elif name == "CLOSURE":
            if not (0 <= b < nproto or 0 <= b - 1 < nproto):
                return False
        for v in (a, b, c):
            if isinstance(v, int) and v < 0:
                return False
            if isinstance(v, int) and v >= 256 and not (256 <= v < 256 + nconst):
                return False
        mode = L.OPMODE.get(name)
        if mode == L.IABC:
            for v in (b, c):
                if isinstance(v, int) and v >= 512:
                    return False
        elif mode == L.IABX and isinstance(b, int) and not 0 <= b < (1 << 18):
            return False
        for r in _touched_regs(op):
            if r >= 200:
                return False
    return True


def _consts_ok(ops, consts):
    for op in ops:
        if op[0] in ("GETGLOBAL", "SETGLOBAL"):
            b = op[2]
            if not (isinstance(b, int) and 0 <= b < len(consts)
                    and isinstance(consts[b], str)):
                return False
    return True


def build_function(chunk, isa, instr, regs, ctx=None, depth=0):
    ctx = dict(ctx or {})
    ctx.setdefault("regs", regs)
    ctx.setdefault("instr", instr)

    atoms, vm2a = _expand(chunk, isa, instr, regs, ctx)

    consts = list(chunk["consts"])

    nconst = len(consts)
    nproto = len(chunk["protos"])

    lua_ops = []
    atom_of = []
    for i, a in enumerate(atoms):
        ops = vm_isa.emit(a["text"], a["ins"], ctx)
        if ops and _valid_ops(ops, nconst, nproto) and _consts_ok(ops, consts):
            for o in ops:
                lua_ops.append(o)
                atom_of.append(i)
        else:
            lua_ops.append(("__RAW__", a["sem"], a["text"], i))
            atom_of.append(i)

    dedup, datom = [], []
    for op, ai in zip(lua_ops, atom_of):
        if (op[0] == "JMP" and dedup and dedup[-1][0] == "JMP"
                and dedup[-1][2] == op[2]):
            continue
        dedup.append(op)
        datom.append(ai)
    lua_ops, atom_of = dedup, datom

    atom2lua = {}
    out_idx = 0
    for ai, op in zip(atom_of, lua_ops):
        if op[0] != "__RAW__":
            atom2lua.setdefault(ai, out_idx)
            out_idx += 1
    total_out = out_idx

    def _resolve(tgt_vm):
        tgt_atom = vm2a.get(tgt_vm)
        if tgt_atom is None:
            cands = sorted(v for k, v in vm2a.items() if k >= tgt_vm)
            tgt_atom = cands[0] if cands else None
        if tgt_atom is None:
            return None
        if tgt_atom in atom2lua:
            return atom2lua[tgt_atom]
        for a2 in sorted(atom2lua):
            if a2 >= tgt_atom:
                return atom2lua[a2]
        return total_out

    out_code = []
    for op in lua_ops:
        name = op[0]
        if name == "__RAW__":
            continue
        if name == "JMP":
            tgt_lua = _resolve(op[2])
            if tgt_lua is None:
                tgt_lua = total_out
            tgt_lua = min(max(tgt_lua, 0), total_out)
            sbx = tgt_lua - (len(out_code) + 1)
            out_code.append(L.make_ins("JMP", 0, sbx))
        elif name == "CLOSURE":
            a, bx = op[1], op[2]
            if not (0 <= bx < nproto) and 0 <= bx - 1 < nproto:
                bx -= 1
            out_code.append(L.make_ins("CLOSURE", a, bx))
        else:
            out_code.append(L.make_ins(name, op[1],
                                       op[2] if op[2] is not None else 0,
                                       op[3] if op[3] is not None else 0))

    if not out_code or (out_code[-1] & 0x3F) not in (
            L.OP["RETURN"], L.OP["TAILCALL"]):
        out_code.append(L.make_ins("RETURN", 0, 1))

    for i, w in enumerate(out_code):
        if (w & 0x3F) != L.OP["JMP"]:
            continue
        sbx = ((w >> 14) & 0x3FFFF) - L.OFFSET_sBx
        target = i + 1 + sbx
        target = min(max(target, 0), len(out_code) - 1)
        out_code[i] = L.make_ins("JMP", (w >> 6) & 0xFF, target - (i + 1))

    decoded = [_decode(w) for w in out_code]

    active, cap = {}, {}
    for idx, op in enumerate(decoded):
        name, a = op[0], op[1] or 0
        if name == "NEWTABLE":
            active[a] = idx
            cap[idx] = 0
        elif name == "SETLIST":
            if a in active:
                cap[active[a]] += max(1, op[2] or 0)
        elif name == "SETTABLE":
            if a in active:
                cap[active[a]] += 1
        else:
            for r in _written_regs(op):
                active.pop(r, None)
    for idx, n in cap.items():
        if n > 0:
            out_code[idx] = L.make_ins("NEWTABLE", decoded[idx][1] or 0,
                                       _fb_encode(n), 0)

    maxreg = _max_register(decoded)
    numparams = chunk["numparams"]
    maxstack = min(250, max(8, numparams + 4, maxreg + 5))

    mode = os.environ.get("VM_LOCALS", "all")
    locals_ = []
    if maxreg > 0:
        rc = _read_counts(decoded, maxstack)
        for r in range(maxstack):
            if mode == "smart" and rc[r] == 1:
                continue
            locals_.append((f"R{r}", 0 if mode == "all" else r,
                            max(0, len(decoded) - 1), r))

    protos = [build_function(p, isa, instr, regs, ctx, depth + 1)
              for p in chunk["protos"]]

    return dict(
        source=chunk.get("source") or None,
        linedefined=0, lastlinedefined=0,
        nups=0,
        numparams=chunk["numparams"],
        is_vararg=2 if depth == 0 else 0,
        maxstacksize=maxstack,
        code=out_code,
        consts=consts,
        protos=protos,
        lines=[],
        locals=locals_,
        _raw=[o for o in lua_ops if o[0] == "__RAW__"],
    )


def vm_to_lua_chunk(src: str, payload: bytes):
    chunk = D.deserialize(payload)
    isa, opvar, instr, regs = D.recover_isa(src)
    if not isa or not instr:
        raise ValueError("could not recover the interpreter dispatch")
    ctx = {"regs": regs, "instr": instr}
    blk, _opvar = D._find_dispatch(src)
    if blk:
        pcv, cv = D._pc_and_code(blk, instr)
        if pcv:
            ctx["pc"], ctx["code"] = pcv, cv
    fn = build_function(chunk, isa, instr, regs, ctx)
    return L.build_chunk(fn), fn
