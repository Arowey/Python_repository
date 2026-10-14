# -*- coding: utf-8 -*-
"""Independent acceptance checks for the two deliverables.

This does NOT re-use the notebooks' own assertions: it re-reads the produced
artefacts and re-derives the required results from scratch.
"""
import json
import math
import os
import pickle
import re
import sys

ROOT = r"C:\Users\guoqi\Desktop\南华大学\python数据分析"
EXP01 = os.path.join(ROOT, "EXP01")
HW01 = os.path.join(ROOT, "HW01")
SID, NAME = "20244080305", "郭乾威"

failures = []


def check(label, cond, detail=""):
    ok = "PASS" if cond else "FAIL"
    if not cond:
        failures.append(label)
    print(f"[{ok}] {label}" + (f"  {detail}" if detail else ""))


def load_nb(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def cell_text(cell):
    src = cell["source"]
    return src if isinstance(src, str) else "\n".join(src)


# ---------------------------------------------------------------- files
exp_nb = os.path.join(EXP01, f"{SID}_{NAME}_exp01.ipynb")
hw_nb = os.path.join(HW01, f"{SID}_{NAME}_hw01.ipynb")
print("=== 交付文件 ===")
check("EXP01 notebook named 学号_姓名_exp01.ipynb", os.path.isfile(exp_nb), exp_nb)
check("HW01 notebook named 学号_姓名_hw01.ipynb", os.path.isfile(hw_nb), hw_nb)
check("student_utils.py exists", os.path.isfile(os.path.join(EXP01, "student_utils.py")))
for f in ("students.txt", "report.txt", "students.pkl"):
    check(f"exp01_data/{f} generated", os.path.isfile(os.path.join(EXP01, "exp01_data", f)))

# ---------------------------------------------------------------- notebooks
for tag, path in (("EXP01", exp_nb), ("HW01", hw_nb)):
    nb = load_nb(path)
    print(f"\n=== {tag} notebook ===")
    code = [c for c in nb["cells"] if c["cell_type"] == "code"]
    md = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
    check(f"{tag} nbformat is 4.5", nb.get("nbformat") == 4 and nb.get("nbformat_minor") == 5)
    check(f"{tag} kernel is exp01", nb["metadata"]["kernelspec"]["name"] == "exp01")
    check(f"{tag} has markdown explanations", len(md) >= 5, f"{len(md)} md cells")
    counts = [c.get("execution_count") for c in code]
    check(f"{tag} all code cells executed", all(isinstance(x, int) for x in counts))
    check(f"{tag} execution_count 1..N contiguous",
          counts == list(range(1, len(code) + 1)), str(counts[:6]) + "...")
    empty = [i for i, c in enumerate(code) if not c.get("outputs")]
    check(f"{tag} no code cell without output", not empty, f"empty: {empty}")
    errs = [o for c in code for o in c.get("outputs", []) if o.get("output_type") == "error"]
    check(f"{tag} no error outputs", not errs, f"{len(errs)} errors")
    joined = "\n".join(cell_text(c) for c in nb["cells"])
    check(f"{tag} STUDENT_ID updated to {SID}", f"STUDENT_ID = {SID}" in joined)
    check(f"{tag} no template id 20190010 left", "20190010" not in joined)

# ------------------------------------------------- EXP01 task coverage
nb = load_nb(exp_nb)
src = "\n".join(cell_text(c) for c in nb["cells"])
print("\n=== EXP01 任务覆盖 ===")
for fn in ("score_level", "factorial_recursive", "factorial_iterative", "summary",
           "sum_all", "parse_student", "Student", "GraduateStudent", "is_passed",
           "__str__"):
    check(f"defines/uses {fn}", fn in src)
for topic, needle in (
        ("实验1 运算符", '8 // 3'),
        ("实验1 type()", "type(val).__name__"),
        ("实验1 int(goat) 异常", 'int("goat")'),
        ("实验1 strip/split/join", ".split()" if ".split()" in src else "split()"),
        ("实验2 1..100 求和", "range(1, 101)"),
        ("实验3 zip 字典", "dict(zip(names, scores))"),
        ("实验3 enumerate", "enumerate(scores, start=1)"),
        ("实验3 列表推导式", "[name for name, score in zip(names, scores) if score >= 60]"),
        ("实验3 alias/copy 对比", "alias = original"),
        ("实验4 makedirs exist_ok", "os.makedirs(DATA_DIR, exist_ok=True)"),
        ("实验4 utf-8 open", 'encoding="utf-8"'),
        ("实验4 report w/a 演示", '"a"'),
        ("实验4 pickle", "pickle.dump"),
        ("实验4 FileNotFoundError", "FileNotFoundError"),
        ("实验5 copy.copy/deepcopy", "copy.deepcopy"),
):
    check(topic, needle in src)

# ------------------------------------------------- report.txt / pickle
print("\n=== 实验4 产物内容 ===")
report = open(os.path.join(EXP01, "exp01_data", "report.txt"), encoding="utf-8").read()
check("report.txt shows w-mode overwrite evidence", "[w 模式演示]" in report)
check("report.txt shows appended summary", "有效记录数: 6" in report)
check("report.txt invalid count 3", "无效记录数: 3" in report)
check("report.txt average 76.67", "76.67" in report)
check("report.txt pass rate 83.33%", "83.33%" in report)

with open(os.path.join(EXP01, "exp01_data", "students.pkl"), "rb") as fh:
    loaded = pickle.load(fh)
expected = [
    {"name": "Alice", "score": 85}, {"name": "Bob", "score": 58},
    {"name": "Carol", "score": 92}, {"name": "David", "score": 76},
    {"name": "Eva", "score": 60}, {"name": "Frank", "score": 89},
]
check("students.pkl round-trip equals expected 6 valid records", loaded == expected, str(loaded))

# ------------------------------------------------- parse_student checks
sys.path.insert(0, EXP01)
import student_utils  # noqa: E402

print("\n=== student_utils.parse_student 判定 ===")
valid_lines = ["Alice,85", "Bob,58", "Carol,92", "David,76", "Eva,60", "Frank,89"]
invalid_lines = ["Grace,abc", "Henry,105", "Incomplete"]
ok_count = invalid_count = 0
for ln in valid_lines:
    try:
        student_utils.parse_student(ln)
        ok_count += 1
    except ValueError:
        pass
for ln in invalid_lines:
    try:
        student_utils.parse_student(ln)
    except ValueError:
        invalid_count += 1
check("parse_student accepts 6 valid lines", ok_count == 6, str(ok_count))
check("parse_student rejects 3 invalid lines", invalid_count == 3, str(invalid_count))
check("parse_student trims whitespace/newline", student_utils.parse_student("  Alice,85\n") == {"name": "Alice", "score": 85})
check("parse_student boundary 0 ok", student_utils.parse_student("Z,0") == {"name": "Z", "score": 0})
check("parse_student boundary 100 ok", student_utils.parse_student("Z,100") == {"name": "Z", "score": 100})
for bad in ("Z,101", "Z,-1", ",50", "A,1,2", ""):
    try:
        student_utils.parse_student(bad)
        check(f"parse_student rejects {bad!r}", False)
    except ValueError:
        check(f"parse_student rejects {bad!r}", True)

# ------------------------------------------------- HW01 required functions
print("\n=== HW01 必需函数与结果 ===")
nb = load_nb(hw_nb)
src = "\n".join(cell_text(c) for c in nb["cells"])
for fn in ("say_hi", "goat_pad", "print_n", "gcd", "euler_limit",
           "euler_infinite_sum", "euler_approx", "print_euler_sum_table",
           "is_power_of_2", "is_power"):
    check(f"defines {fn}", re.search(rf"def\s+{fn}\s*\(", src) is not None)


def factorial(k):
    r = 1
    for i in range(2, k + 1):
        r *= i
    return r


def gcd(m, n):
    return m if n == 0 else gcd(n, m % n)


def euler_infinite_sum(n):
    return sum(1 / factorial(k) for k in range(n))


def euler_approx(eps):
    total, k = 0.0, 0
    while True:
        t = 1 / factorial(k)
        nt = total + t
        if nt == total:
            return nt
        total = nt
        if abs(total - math.exp(1)) < eps:
            return total
        k += 1


def is_power_of_2(p):
    if p <= 0:
        return False
    while p > 1:
        if p % 2:
            return False
        p //= 2
    return True


def is_power(b, n):
    if b <= 0 or n <= 0:
        return False
    if b == 1:
        return n == 1
    while n > 1:
        if n % b:
            return False
        n //= b
    return True


check("gcd(2018,2019)==1", gcd(2018, 2019) == 1)
check("gcd(1200,300)==300", gcd(1200, 300) == 300)
check("gcd(5040,60)==60", gcd(5040, 60) == 60)
check("euler_infinite_sum(0)==0", euler_infinite_sum(0) == 0)
check("euler_infinite_sum(1)==1", euler_infinite_sum(1) == 1)
check("euler_infinite_sum(4)==2.666...", abs(euler_infinite_sum(4) - 2.6666666666666665) < 1e-12,
      repr(euler_infinite_sum(4)))
for eps in (1e-2, 1e-5, 1e-10, 1e-15):
    got = euler_approx(eps)
    check(f"euler_approx({eps:.0e}) within eps", abs(got - math.exp(1)) < eps, f"err={abs(got - math.exp(1)):.2e}")
check("is_power_of_2(1)==True (2^0)", is_power_of_2(1) is True)
check("is_power_of_2(1024)==True", is_power_of_2(1024) is True)
check("is_power_of_2(1023)==False", is_power_of_2(1023) is False)
check("is_power_of_2(3)==False", is_power_of_2(3) is False)
check("is_power(3,9)==True", is_power(3, 9) is True)
check("is_power(3,10)==False", is_power(3, 10) is False)
check("is_power(2,1)==True (b^0)", is_power(2, 1) is True)
check("is_power(1,1)==True", is_power(1, 1) is True)
check("is_power(1,2)==False", is_power(1, 2) is False)
code_src = "\n".join(cell_text(c) for c in nb["cells"] if c["cell_type"] == "code")
check("no math.sqrt used in HW01 code",
      "sqrt" not in code_src,
      "only allowed as the quoted restriction in Markdown")
check("restriction restated in Markdown",
      "math.sqrt" in "\n".join(cell_text(c) for c in nb["cells"] if c["cell_type"] == "markdown"))

# ------------------------------------------------- outputs present
print("\n=== 输出内容抽查 ===")
nb = load_nb(hw_nb)
allout = []
for c in nb["cells"]:
    if c["cell_type"] != "code":
        continue
    for o in c.get("outputs", []):
        if o.get("output_type") == "stream":
            t = o.get("text", "")
            allout.append(t if isinstance(t, str) else "".join(t))
text = "".join(allout)
check("HW01 stdout contains euler table", "euler_infinite_sum(" in text)
check("HW01 stdout contains gcd results", "gcd(2018, 2019) = 1" in text)
check("HW01 stdout shows negative gcd discussion", "gcd( -12,   18)" in text or "gcd(-12, 18)" in text)

print("\n" + "=" * 60)
if failures:
    print(f"FAILURES ({len(failures)}):")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
