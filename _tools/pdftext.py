"""Dependency-free PDF text extractor for Type3/TTF CID PDFs exported by Word.

Fonts are reconstructed from the decompressed object streams: each number in the
footer line right before `stream` is that object's number in the file.
"""
import re, sys, zlib, os, collections

TOKEN_RE = re.compile(rb"""
    (?P<hex><(?![<])[0-9A-Fa-f\s]*>)
  | (?P<lit>\()
  | (?P<op>[A-Za-z'"*][A-Za-z0-9*'"]*)
  | (?P<num>[+-]?(?:\d+\.?\d*|\.\d+))
  | (?P<name>/[^\s/\[\]<>(){}]*)
  | (?P<arr>[\[\]])
  | (?P<dict><<|>>)
  | (?P<sp>\s+)
""", re.X | re.S)


def read_streams(path):
    """Return list of (objnum, header_bytes, decompressed_bytes)."""
    d = open(path, "rb").read()
    out = []
    i = 0
    while True:
        s = d.find(b"stream", i)
        if s < 0:
            break
        a = s + 6
        if d[a:a + 2] == b"\r\n":
            a += 2
        elif d[a:a + 1] in (b"\n", b"\r"):
            a += 1
        e = d.find(b"endstream", a)
        raw = d[a:e]
        i = e + 9
        # the object header is the text between the previous stream data and this
        # `stream` keyword; search wide enough for long /ObjStm headers
        head = d[max(0, s - 4000):s]
        nums = [int(x) for x in re.findall(rb"(\d+)\s+0\s+obj", head)]
        objnum = nums[-1] if nums else None
        try:
            dec = zlib.decompress(raw)
        except Exception:
            dec = None
        out.append((objnum, head, dec))
    return out


def parse_cmap(txt):
    """Parse a ToUnicode CMap into (code_width, {code: text})."""
    width = 1
    cs = re.search(rb"begincodespacerange(.*?)endcodespacerange", txt, re.S)
    if cs:
        first = re.search(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", cs.group(1))
        if first:
            width = max(1, (len(first.group(1)) + 1) // 2)
    m = {}
    for blk in re.findall(rb"beginbfchar(.*?)endbfchar", txt, re.S):
        for a, b in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            try:
                m[int(a, 16)] = bytes.fromhex(b.decode()).decode("utf-16-be", "replace")
            except Exception:
                pass
    for blk in re.findall(rb"beginbfrange(.*?)endbfrange", txt, re.S):
        for lo, hi, dst in re.findall(
                rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            lo_i, hi_i, base = int(lo, 16), int(hi, 16), int(dst, 16)
            for k in range(lo_i, min(hi_i, lo_i + 65535) + 1):
                m[k] = chr(base + (k - lo_i))
    return width, m


def parse_objstm(dec, head=b""):
    """Yield (objnum, start, end) for objects packed in an /ObjStm stream.

    `/N` and `/First` live in the object's dictionary (in `head`); the
    decompressed body starts with the N (objnum, offset) pairs.
    """
    # `head` may contain the dictionaries of earlier objects, so take the LAST
    # /N ... /First ... pair, which belongs to this stream's own dictionary.
    m = re.findall(rb"/N\s+(\d+)\s*/First\s+(\d+)", head)
    if m:
        n, first = int(m[-1][0]), int(m[-1][1])
    else:
        m = re.findall(rb"/First\s+(\d+)\s*/N\s+(\d+)", head)
        if not m:
            return
        first, n = int(m[-1][0]), int(m[-1][1])
    header = dec[:first]
    nums = [int(x) for x in re.findall(rb"(\d+)", header)]
    pairs = [(nums[k], nums[k + 1]) for k in range(0, len(nums) - 1, 2)][:n]
    for k, (num, off) in enumerate(pairs):
        start = first + off
        end = first + pairs[k + 1][1] if k + 1 < len(pairs) else len(dec)
        yield num, start, end


def consensus_cmap(fmap):
    """Build a fallback code->text map only from codes whose meaning is
    identical across every per-font CMap that defines them. Word's per-font
    ToUnicode tables overlap on unrelated codes, so a naive union is wrong."""
    votes = {}
    for _, m in fmap.values():
        for code, txt in m.items():
            votes.setdefault(code, set()).add(txt)
    return {c: next(iter(v)) for c, v in votes.items() if len(v) == 1}


def build_index(path):
    streams = read_streams(path)
    byobj = {}
    unpacked = []
    for num, head, dec in streams:
        if num is not None and dec is not None:
            byobj.setdefault(num, dec)
        if head and b"/ObjStm" in head and dec is not None:
            for onum, st, en in parse_objstm(dec, head):
                body = dec[st:en]
                byobj.setdefault(onum, body)
                unpacked.append(body)
    allb = b"\n".join([dec for _, _, dec in streams if dec] + unpacked)
    rawg = parse_cmap(allb)[1]
    # font object -> (code width, cmap), via its /ToUnicode reference
    fmap = {}
    for num, dec in byobj.items():
        if b"/ToUnicode" not in dec:
            continue
        if b"/Font" not in dec:
            continue
        m = re.search(rb"/ToUnicode\s+(\d+)\s+0\s+R", dec)
        if m:
            tu = byobj.get(int(m.group(1)))
            if tu:
                fmap[num] = parse_cmap(tu)
    gmap = consensus_cmap(fmap)
    if not gmap:
        gmap = rawg
    # resource names such as /F5 are local to a page's /Font dictionary, so map
    # every page's name -> font object -> ToUnicode CMap.
    name_maps = {}
    for dec in list(byobj.values()) + [d for _, _, d in streams if d]:
        if b"/Font" not in dec:
            continue
        res = re.search(rb"/Font\s*<<(.*?)>>", dec, re.S)
        if not res:
            continue
        for name, ref in re.findall(rb"/(\w+)\s+(\d+)\s+0\s+R", res.group(1)):
            nm = name.decode("latin-1")
            if nm.startswith("F") and nm[1:].isdigit() and int(nm[1:]) in fmap:
                name_maps.setdefault(nm, fmap[int(nm[1:])])
    return streams, byobj, gmap, fmap, name_maps


ESC = {b"n": b"\n", b"r": b"\r", b"t": b"\t", b"b": b"\b", b"f": b"\f",
       b"(": b"(", b")": b")", b"\\": b"\\"}


def unescape(s):
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i:i + 1]
        if c != b"\\":
            out += c
            i += 1
            continue
        n = s[i + 1:i + 2]
        if n in ESC:
            out += ESC[n]
            i += 2
        elif n.isdigit():
            j = i + 1
            o = b""
            while j < len(s) and len(o) < 3 and 48 <= s[j] <= 55:
                o += s[j:j + 1]
                j += 1
            out.append(int(o, 8) & 0xFF)
            i = j
        elif n in (b"\n", b"\r"):
            i += 2
        else:
            out += n
            i += 2
    return bytes(out)


def tokenize(buf):
    """Yield (kind, value, offset) with literal strings consumed whole."""
    pos = 0
    n = len(buf)
    while pos < n:
        m = TOKEN_RE.match(buf, pos)
        if not m:
            pos += 1
            continue
        pos = m.end()
        if m.group("sp"):
            continue
        if m.group("lit"):
            # find matching close paren respecting escapes and nesting
            start = m.start()
            depth = 0
            j = m.start()
            while j < n:
                ch = buf[j:j + 1]
                if ch == b"\\":
                    j += 2
                    continue
                if ch == b"(":
                    depth += 1
                elif ch == b")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            yield ("str", buf[start:j + 1], start)
            pos = j + 1
            continue
        kind = ("hex" if m.group("hex") else "op" if m.group("op") else
                "num" if m.group("num") else "name" if m.group("name") else
                "arr" if m.group("arr") else "dict")
        yield (kind, m.group(0), m.start())


def decode_str(raw, ishex, cmap, gmap, width=1):
    """Decode a PDF text string using a ToUnicode CMap of the given code width."""
    if ishex:
        h = re.sub(rb"\s", b"", raw[1:-1])
        if len(h) % 2:
            h += b"0"
        try:
            data = bytes.fromhex(h.decode())
        except Exception:
            data = b""
    else:
        data = unescape(raw[1:-1])
    out = []
    i = 0
    if width == 2:
        while i < len(data):
            code = data[i] << 8 | (data[i + 1] if i + 1 < len(data) else 0)
            i += 2
            if code in cmap:
                out.append(cmap[code])
            elif code in gmap:
                out.append(gmap[code])
            else:
                out.append("\ufffd")
    else:
        for b in data:
            if b in cmap:
                out.append(cmap[b])
            elif b in gmap:
                out.append(gmap[b])
            else:
                out.append("\ufffd")
    return "".join(out)


def extract_stream(buf, fmap, gmap):
    """Return list of (x, y, text) text runs in content order."""
    runs = []
    stack = []
    font = None
    tm = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
    tlm = tm
    leading = 0.0

    def cmap_for(fn):
        m = dict(gmap)
        width = 1
        ent = fmap.get(fn)
        if ent:
            width, c = ent
            m.update(c)
        return width, m

    def show(v):
        width, m = cmap_for(font)
        s = decode_str(v, v.startswith(b"<"), m, {}, width)
        if s:
            runs.append((round(tm[4], 2), round(-tm[5], 2), s))

    for kind, val, off in tokenize(buf):
        kind = kind.decode("latin-1") if isinstance(kind, bytes) else kind
        if kind == "op":
            op = val.decode("latin-1")
            if op == "Tf":
                if len(stack) >= 2:
                    nm = stack[-2]
                    if isinstance(nm, bytes):
                        nm = nm.decode("latin-1")
                    if isinstance(nm, str) and nm.startswith("/"):
                        d = nm[1:]
                        m = re.fullmatch(r"F(\d+)", d)
                        if m:
                            font = "F" + m.group(1)
                        elif d.isdigit():
                            font = d
            elif op == "BT":
                tm = tlm = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
            elif op in ("Td", "TD"):
                if len(stack) >= 2:
                    try:
                        tx, ty = float(stack[-2]), float(stack[-1])
                    except (ValueError, TypeError):
                        tx = ty = 0.0
                    tlm = (tlm[0], tlm[1], tlm[2], tlm[3], tlm[4] + tx, tlm[5] + ty)
                    tm = tlm
                    if op == "TD":
                        leading = -ty
            elif op == "Tm":
                if len(stack) >= 6:
                    try:
                        tm = tlm = tuple(float(v) for v in stack[-6:])
                    except (ValueError, TypeError):
                        pass
            elif op == "TL":
                if stack:
                    try:
                        leading = float(stack[-1])
                    except (ValueError, TypeError):
                        pass
            elif op == "T*":
                tlm = (tlm[0], tlm[1], tlm[2], tlm[3], tlm[4], tlm[5] - leading)
                tm = tlm
            elif op == "'":
                tlm = (tlm[0], tlm[1], tlm[2], tlm[3], tlm[4], tlm[5] - leading)
                tm = tlm
                if stack and isinstance(stack[-1], bytes):
                    show(stack[-1])
            elif op in ("Tj", '"'):
                if stack and isinstance(stack[-1], bytes):
                    v = stack[-1]
                    if v.startswith(b"<") or v.startswith(b"("):
                        show(v)
            stack = []
            continue
        stack.append(val)
        if len(stack) > 24:
            del stack[:-24]
    return runs


def page_runs(path):
    streams, byobj, gmap, fmap, name_maps = build_index(path)
    # keyed by resource name: /F5 -> object 5's CMap, plus the identity fallback
    fonts = {f"F{n}": m for n, m in fmap.items()}
    fonts.update(name_maps)
    seen = set()
    pages = []
    for num, head, dec in streams:
        if dec is None or num is None or num in seen:
            continue
        if b"BT" not in dec or b"Tj" not in dec:
            continue
        if b"begincmap" in dec or b"beginbfchar" in dec:
            continue
        seen.add(num)
        pages.append((num, extract_stream(dec, fonts, gmap)))
    return pages, fonts, gmap


def main():
    path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "raw"
    pages, fonts, gmap = page_runs(path)
    print(f"pages={len(pages)} fonts={len(fonts)}", file=sys.stderr)
    for num, runs in pages:
        txt = "".join(t for _, _, t in runs)
        print(f"\n########## PAGE {num} (missing={txt.count(chr(0xFFFD))}) ##########")
        if mode == "lines":
            byline = collections.OrderedDict()
            for x, y, t in runs:
                byline.setdefault(y, []).append((x, t))
            for y in sorted(byline):
                line = "".join(t for _, t in sorted(byline[y]))
                if line.strip():
                    print(line)
        else:
            print(txt)


if __name__ == "__main__":
    main()
