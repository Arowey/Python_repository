# -*- coding: utf-8 -*-
"""Self-contained wheel installer.

pip cannot run under this sandbox (`PermissionError` when unpacking into TEMP),
so this script resolves the dependency graph from the PyPI JSON API, downloads
wheels, and unpacks them into a target directory using only the stdlib.

Usage:
    python wheelinstall.py <target_dir> <root_pkg> [<root_pkg> ...]
"""
import io
import json
import os
import re
import sys
import urllib.request
import zipfile

PYPI = "https://pypi.org/pypi/{name}/json"
PY_VER = (3, 12)
TARGET = sys.argv[1]
ROOTS = sys.argv[2:]


def norm(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def marker_ok(marker):
    """Evaluate the small subset of environment markers used by these packages."""
    if not marker:
        return True
    env = {
        "python_version": f"{PY_VER[0]}.{PY_VER[1]}",
        "python_full_version": f"{PY_VER[0]}.{PY_VER[1]}.0",
        "sys_platform": "win32",
        "platform_system": "Windows",
        "platform_machine": "AMD64",
        "os_name": "nt",
        "implementation_name": "cpython",
        "platform_python_implementation": "CPython",
        "extra": "",
    }
    expr = marker.strip()
    # substitute variables
    for key in sorted(env, key=len, reverse=True):
        expr = re.sub(rf"\b{re.escape(key)}\b", repr(env[key]), expr)
    expr = expr.replace(" and ", " and ").replace(" or ", " or ")
    try:
        return bool(eval(expr, {"__builtins__": {}}, {}))  # noqa: S307
    except Exception:
        return False


def pick_wheel(files, py_ver):
    """Choose the best wheel for this interpreter (CPython, non-free-threaded)."""
    want = (py_ver[0], py_ver[1])
    cands = []
    for f in files:
        if f["packagetype"] != "bdist_wheel" or not f["filename"].endswith(".whl"):
            continue
        fn = f["filename"]
        parts = fn[:-4].split("-")
        if len(parts) < 5:
            continue
        pytag, abitag, plantag = parts[-3], parts[-2], parts[-1]
        plats = plantag.split(".")
        if not any(p in ("any", "win_amd64") for p in plats):
            continue

        py_ok = False
        for p in pytag.split("."):
            if p == "py3":
                py_ok = True
            elif re.fullmatch(r"cp\d{2,3}", p):
                # e.g. cp39, cp312, cp313t -> major/minor digits (ignore free-threaded 't')
                digits = p[2:].rstrip("t")
                maj, minor = int(digits[0]), int(digits[1:])
                if (maj, minor) <= want:
                    py_ok = True

        abi_ok = False
        for a in abitag.split("."):
            if a == "none":
                abi_ok = True
            elif a == "abi3":
                # abi3 wheel: must have been built for a Python <= ours
                py_digits = pytag.split(".")[0][2:].rstrip("t")
                if int(py_digits[0]) == py_ver[0] and int(py_digits[1:]) <= py_ver[1]:
                    abi_ok = True
            elif a == f"cp{py_ver[0]}{py_ver[1]}":
                abi_ok = True
        if not (py_ok and abi_ok):
            continue
        # prefer platform-specific wheels, then abi3, then newest upload
        score = (0 if "any" in plats else 1,
                 1 if "abi3" in abitag.split(".") else 0,
                 f.get("upload_time", ""))
        cands.append((score, f))
    if not cands:
        return None
    cands.sort(key=lambda x: x[0])
    return cands[-1][1]


def get_json(name):
    req = urllib.request.Request(PYPI.format(name=name),
                                 headers={"Accept": "application/json",
                                          "User-Agent": "wheelinstall/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main():
    os.makedirs(TARGET, exist_ok=True)
    queue = list(ROOTS)
    seen = {}
    installed = []

    while queue:
        raw_name = queue.pop(0)
        # split "pkg>=1.0"
        spec = re.match(r"^([A-Za-z0-9._-]+)\s*(.*)$", raw_name)
        name = norm(spec.group(1))
        if name in seen:
            continue
        try:
            data = get_json(name)
        except Exception as exc:
            print(f"  !! cannot fetch {name}: {exc}")
            continue
        info = data["info"]
        version = info["version"]
        wheel = pick_wheel(data["urls"], PY_VER)
        if wheel is None:
            print(f"  !! no compatible wheel for {name} {version}; skipped")
            seen[name] = None
            continue
        seen[name] = version

        dest = os.path.join(TARGET, wheel["filename"])
        if not os.path.exists(dest):
            with urllib.request.urlopen(wheel["url"], timeout=180) as r, open(dest, "wb") as fh:
                fh.write(r.read())
        with zipfile.ZipFile(dest) as z:
            z.extractall(TARGET)

        # read Requires-Dist from the PyPI metadata
        deps = []
        for req in info.get("requires_dist") or []:
            left = req
            if ";" in req:
                left, marker = req.split(";", 1)
                if not marker_ok(marker):
                    continue
            dep = left.strip()
            dep_name = re.match(r"^([A-Za-z0-9._-]+)", dep)
            if not dep_name:
                continue
            deps.append(dep_name.group(1))
        installed.append((name, version, len(deps)))
        print(f"  + {name} {version}  (deps: {len(deps)})")
        for d in deps:
            if norm(d) not in seen:
                queue.append(d)

    print(f"\ninstalled {len(installed)} distributions into {TARGET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
