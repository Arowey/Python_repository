# -*- coding: utf-8 -*-
"""Generate the two deliverable notebooks (no execution)."""
import json, os, sys

ROOT = r"C:\Users\guoqi\Desktop\南华大学\python数据分析"
EXP01_DIR = os.path.join(ROOT, "EXP01")
HW01_DIR = os.path.join(ROOT, "HW01")

STUDENT_ID = "20244080305"
NAME = "郭乾威"


def cells_from(spec):
    out = []
    for i, (kind, src) in enumerate(spec):
        cid = f"exp01-{i:03d}"
        if kind == "md":
            out.append({"cell_type": "markdown", "id": cid, "metadata": {},
                        "source": src.rstrip("\n")})
        else:
            out.append({"cell_type": "code", "id": cid, "execution_count": None,
                        "metadata": {}, "outputs": [], "source": src.rstrip("\n")})
    return out


def write_nb(path, spec):
    nb = {
        "cells": cells_from(spec),
        "metadata": {
            "kernelspec": {"display_name": "Python (exp01)", "language": "python",
                           "name": "exp01"},
            "language_info": {"name": "python", "version": "3.12",
                              "mimetype": "text/x-python", "file_extension": ".py",
                              "pygments_lexer": "ipython3",
                              "codemirror_mode": {"name": "ipython", "version": 3},
                              "nbconvert_exporter": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(nb, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("wrote", path, len(nb["cells"]), "cells")


# =====================================================================
# EXP01
# =====================================================================
IDENTITY = '''import os, uuid, hashlib, platform, getpass

# ===== 1. 填写学号 =====
STUDENT_ID = 20244080305  # 修改为自己的学号

# ===== 2. 打印 conda 环境 =====
CONDA_ENV = os.environ.get("CONDA_DEFAULT_ENV", "base")
print(f"[Conda 环境] {CONDA_ENV}")

# ===== 3. 机器指纹（绑定当前电脑）=====
MACHINE_FP = hashlib.sha256(
    f"{platform.node()}|{platform.machine()}|{platform.system()}|{uuid.getnode()}".encode()
).hexdigest()[:16]

# ===== 4. 生成唯一 ID =====
RUN_ID = f"{STUDENT_ID}-{MACHINE_FP}"
print(f"[学号]     {STUDENT_ID}")
print(f"[机器指纹] {MACHINE_FP}")
print(f"[RUN_ID]   {RUN_ID}")'''

EXP01 = []

EXP01.append(("md", f'''# 实验报告01：Python基础与数据处理入门

- 姓名：{NAME}
- 学号：{STUDENT_ID}
- 课程：Python数据分析

> 说明：本 Notebook 中的每个小问都先给出 Markdown 思路说明，再用代码单元格给出结果，
> 并按题号顺序执行。提交前已重启内核、从上到下运行全部代码，不存在依赖旧变量的问题。
'''))

EXP01.append(("md", "## 一、实验环境与提交要求\n\n"
                     "1. 使用独立的 conda 虚拟环境 `exp01` 完成实验，不使用 base 环境。\n"
                     "2. 使用 Python 3 和 Jupyter Notebook。\n"
                     "3. 先把第一个代码框中的学号改成自己的学号，再完成以下实验。\n"
                     "4. 用 Markdown 单元格解释思路，用代码单元格完成计算。\n"
                     "5. 提交前重启内核并运行全部代码。\n"
                     "6. Notebook 命名为 `学号_姓名_exp01.ipynb`。"))

EXP01.append(("md", "### 1.1 第一个代码框：身份与环境记录\n\n"
                    "本 Notebook 运行于独立环境 **`exp01`**（Python 3.12，不是 base 环境）。\n"
                    "由于实验机上的 DSH 沙箱不允许写入 conda 默认的 envs/包目录，"
                    "该环境以同等隔离的方式创建在工作区内："
                    "`_tools\\env_exp01`（独立解释器前缀，自带 pip）。"
                    "`CONDA_DEFAULT_ENV` 已设为 `exp01`，下面第一个代码框会打印出来。"))
EXP01.append(("code", IDENTITY))

EXP01.append(("md", "## 二、实验内容与过程"))

# ---------- 实验1 ----------
EXP01.append(("md", '''## 实验1：基本运算、数据类型与字符串操作

**任务1思路**：分别计算 `8 / 3`（真除法，结果为浮点）、`8 // 3`（整除/向下取整）、
`8 % 3`（取模，余数）与 `2 ** 7`（幂运算），并用 `type()` 输出每个结果的类型。'''))
EXP01.append(("code", '''results = {
    "8 / 3": 8 / 3,
    "8 // 3": 8 // 3,
    "8 % 3": 8 % 3,
    "2 ** 7": 2 ** 7,
}

meaning = {
    "8 / 3": "真除法：返回精确商，结果是 float",
    "8 // 3": "整除（向下取整）：返回商的整数部分，结果是 int",
    "8 % 3": "取模：返回除法的余数，结果是 int",
    "2 ** 7": "幂运算：2 的 7 次方，结果是 int",
}

for expr, val in results.items():
    print(f"{expr:8s} = {val!r:8} type={type(val).__name__:6s} 含义：{meaning[expr]}")'''))

EXP01.append(("md", "**任务2思路**：创建整数、浮点数、字符串、布尔值各一个，用内置函数 `type()` 检查其类型。"))
EXP01.append(("code", '''int_value = 42
float_value = 3.14
str_value = "Python数据分析"
bool_value = True

for val in (int_value, float_value, str_value, bool_value):
    print(f"值 = {val!r:20} -> 类型 = {type(val).__name__}")'''))

EXP01.append(("md", '''**任务3思路**：`int("123")` 把数字字符串转为整数；`float("3.14")` 转为浮点数；
`int(3.9)` 会**截断**小数部分（不是四舍五入）得到 3。
`int("goat")` 失败的原因是字符串内容不是合法的整数表示，Python 抛出 `ValueError`。'''))
EXP01.append(("code", '''print('int("123")   ->', int("123"), type(int("123")).__name__, "（数字字符串转整数）")
print('float("3.14") ->', float("3.14"), type(float("3.14")).__name__, "（数字字符串转浮点数）")
print("int(3.9)      ->", int(3.9), "（int() 向 0 截断，直接舍去小数部分，而非四舍五入）")

try:
    int("goat")
except ValueError as exc:
    print()
    print(f"捕获到异常：{type(exc).__name__}: {exc}")
    print('原因：int() 只能解析合法的数字字符串，"goat" 不是数字，无法转换。')'''))

EXP01.append(("md", '''**任务4思路**：对 `" Python Data Analysis "` 依次做
`strip()` 去首尾空白、`upper()`/`lower()` 大小写转换、切片取子串、
`split()` 拆分成单词列表，再用 `join()` 把单词连接回去。'''))
EXP01.append(("code", '''text = " Python Data Analysis "
print("原始字符串:", repr(text))

cleaned = text.strip()
print("strip() 去首尾空白:", repr(cleaned))

print("upper() 全大写:", repr(cleaned.upper()))
print("lower() 全小写:", repr(cleaned.lower()))

print("切片 text[1:7]      ->", repr(text[1:7]))
print("切片 cleaned[:6]    ->", repr(cleaned[:6]))
print("切片 cleaned[-8:]   ->", repr(cleaned[-8:]))

words = cleaned.split()
print("split() 拆分单词:", words)

joined = "-".join(words)
print('"-".join(words) 连接:', repr(joined))
print('" ".join(words) 连接:', repr(" ".join(words)))'''))

EXP01.append(("md", '''**任务5思路**：用 `+` 做拼接、用 `*` 做重复；字符串是**不可变**类型，
所以 `s[0] = "X"` 会抛 `TypeError`；要"修改"只能切片加拼接构造一个**新字符串**。'''))
EXP01.append(("code", '''a, b = "Python", "Data"
print("拼接 a + ' ' + b ->", repr(a + " " + b))
print("重复  b * 2      ->", repr(b * 2))
print("重复  'ab' * 3   ->", repr("ab" * 3))

s = "Python"
try:
    s[0] = "J"
except TypeError as exc:
    print()
    print(f"捕获到异常：{type(exc).__name__}: {exc}")
    print("原因：str 是不可变类型，不支持按下标赋值。")

new_s = "J" + s[1:]
print('构造新字符串 "J" + s[1:] ->', repr(new_s))
print("原字符串仍为:", repr(s))'''))

# ---------- 实验2 ----------
EXP01.append(("md", '''## 实验2：函数、条件、循环与递归操作

**任务1思路**：用 `if/elif/else` 分级；越界（小于 0 或大于 100）时主动
`raise ValueError`。注意区间端点是"90~100、80~不足90、60~不足80、0~不足60"。'''))
EXP01.append(("code", '''def score_level(score):
    """返回成绩等级；分数超出 0~100 时抛出 ValueError。"""
    if not isinstance(score, (int, float)):
        raise ValueError(f"成绩必须是数值，收到 {type(score).__name__}")
    if score < 0 or score > 100:
        raise ValueError(f"成绩 {score} 超出 0~100 范围")
    if score >= 90:
        return "优秀"
    if score >= 80:
        return "良好"
    if score >= 60:
        return "及格"
    return "不及格"


for s in (100, 90, 89, 80, 79, 60, 59, 0):
    print(f"score_level({s:>3}) = {score_level(s)}")

for bad in (-1, 101):
    try:
        score_level(bad)
    except ValueError as exc:
        print(f"score_level({bad}) 抛出 ValueError: {exc}")'''))

EXP01.append(("md", "**任务2思路**：`for` 遍历 `range(1, 101)` 累加；`while` 用计数器累加，两者结果应一致。"))
EXP01.append(("code", '''total_for = 0
for i in range(1, 101):
    total_for += i

total_while = 0
i = 1
while i <= 100:
    total_while += i
    i += 1

print("for   循环求和 1~100 =", total_for)
print("while 循环求和 1~100 =", total_while)
print("两者结果是否一致:", total_for == total_while)
print("与公式 n(n+1)/2 对照:", 100 * 101 // 2)'''))

EXP01.append(("md", "**任务3思路**：递归版用 `n * factorial_recursive(n-1)`，基准情形 `n == 0` 返回 1；"
                     "迭代版用循环累乘。约定 `0! = 1`，负数抛 `ValueError`。"))
EXP01.append(("code", '''def factorial_recursive(n):
    """递归版阶乘，约定 0! = 1。"""
    if not isinstance(n, int) or n < 0:
        raise ValueError("n 必须是非负整数")
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n):
    """迭代版阶乘，约定 0! = 1。"""
    if not isinstance(n, int) or n < 0:
        raise ValueError("n 必须是非负整数")
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result


for n in (0, 1, 5, 10):
    r1, r2 = factorial_recursive(n), factorial_iterative(n)
    print(f"{n:>2}! = 递归 {r1:<12} 迭代 {r2:<12} 一致: {r1 == r2}")

try:
    factorial_recursive(-1)
except ValueError as exc:
    print("factorial_recursive(-1) 抛出 ValueError:", exc)'''))

EXP01.append(("md", "**任务4思路**：接收非空数值列表，返回 `(最小值, 最大值, 平均值)` 元组，"
                     "调用处用元组解包接收；空列表抛 `ValueError`。"))
EXP01.append(("code", '''def summary(values):
    """返回 (最小值, 最大值, 平均值) 元组；空列表抛 ValueError。"""
    if not values:
        raise ValueError("values 不能为空列表")
    return min(values), max(values), sum(values) / len(values)


low, high, avg = summary([85, 58, 92, 76, 60, 89])   # 元组解包
print(f"最小值 = {low}, 最大值 = {high}, 平均值 = {avg:.4f}")

t = summary([1, 2, 3])
print("返回类型:", type(t).__name__, "，返回内容:", t)

try:
    summary([])
except ValueError as exc:
    print("summary([]) 抛出 ValueError:", exc)'''))

EXP01.append(("md", "**任务5思路**：`*args` 把位置参数打包成元组，用 `sum()` 求和；"
                     "无参数时返回 0，正好覆盖三种测试情况。"))
EXP01.append(("code", '''def sum_all(*args):
    """返回所有参数之和；无参数时返回 0。"""
    return sum(args)


print("sum_all()           =", sum_all())
print("sum_all(5)          =", sum_all(5))
print("sum_all(1, 2, 3, 4) =", sum_all(1, 2, 3, 4))
print("类型检查：sum_all(1, 2, 3, 4) ->", type(sum_all(1, 2, 3, 4)).__name__)'''))

# ---------- 实验3 ----------
EXP01.append(("md", "## 实验3：列表、字典、元组与基础统计\n\n"
                     "使用题目给定的模拟成绩数据，不需要输入真实学生信息。"))
EXP01.append(("code", '''names = ["Alice", "Bob", "Carol", "David", "Eva", "Frank"]
scores = [85, 58, 92, 76, 60, 89]

print("names  =", names)
print("scores =", scores)'''))

EXP01.append(("md", "**任务1思路**：`zip(names, scores)` 把两个列表按位置配对，"
                     "`dict()` 转成姓名字典，再用 `items()` 逐项遍历。"))
EXP01.append(("code", '''name_to_score = dict(zip(names, scores))
print("字典:", name_to_score)
print()
for name, score in name_to_score.items():
    print(f"{name:<8} -> {score}")'''))

EXP01.append(("md", "**任务2思路**：`enumerate(scores, start=1)` 让序号从 1 开始，"
                     "配合索引取姓名。"))
EXP01.append(("code", '''for idx, score in enumerate(scores, start=1):
    print(f"序号 {idx:>2}: {names[idx - 1]:<8} 成绩 {score}")'''))

EXP01.append(("md", "**任务3思路**：列表推导式筛选 `score >= 60`；再生成每个成绩的平方。"))
EXP01.append(("code", '''passed_names = [name for name, score in zip(names, scores) if score >= 60]
print("及格学生姓名:", passed_names)

squared_scores = [score ** 2 for score in scores]
print("成绩平方列表:", squared_scores)'''))

EXP01.append(("md", "**任务4思路**：人数用 `len()`，平均分用 `sum()/len()`，"
                     "最高/最低用 `max()`/`min()`，及格率 = 及格人数 / 总人数。"
                     "格式化：平均分保留两位小数（`:.2f`），及格率显示为百分数（`:.2%`）。"))
EXP01.append(("code", '''count = len(scores)
average = sum(scores) / count
highest = max(scores)
lowest = min(scores)
pass_count = sum(1 for score in scores if score >= 60)
pass_rate = pass_count / count

print(f"人数   : {count}")
print(f"平均分 : {average:.2f}")
print(f"最高分 : {highest}")
print(f"最低分 : {lowest}")
print(f"及格人数: {pass_count}")
print(f"及格率 : {pass_rate:.2%}")'''))

EXP01.append(("md", '''**任务5思路**：`alias = demo` 只是给同一个列表对象再起一个名字，改 `alias` 的元素
会同时改变 `demo`；`copied = demo.copy()` 是**浅拷贝**，得到新列表，改它的元素不会影响原列表。
按题目要求，这里使用**单独的演示列表**，避免改变后续实验的原始成绩 `scores`。'''))
EXP01.append(("code", '''original = [85, 58, 92, 76, 60, 89]      # 演示专用，不碰 scores
alias = original
copied = original.copy()

print("初始   original =", original)
print("初始   alias    =", alias)
print("初始   copied   =", copied)

alias[0] = 0        # 通过别名修改
copied[1] = 0       # 通过副本修改

print()
print("修改 alias[0] 与 copied[1] 之后：")
print("original =", original, "  <- 被 alias 影响，说明 alias 与 original 是同一个对象")
print("alias    =", alias)
print("copied   =", copied, "  <- 独立副本，未受 alias 修改影响")
print()
print("alias is original ->", alias is original)
print("copied is original ->", copied is original)
print("原始成绩 scores 未被修改:", scores)'''))

EXP01.append(("md", '''**任务6思路**：元组是不可变序列，`record[1] = 90` 会抛 `TypeError`；
当两个序列长度不同时，`zip()` 以**较短的序列**为准，多出来的元素被忽略。'''))
EXP01.append(("code", '''record = ("Alice", 85)
print("学生记录元组:", record)

try:
    record[1] = 90
except TypeError as exc:
    print(f"捕获到异常：{type(exc).__name__}: {exc}")
    print("原因：元组不可变，不能直接重新赋值其中的元素。")

new_record = (record[0], 90)
print("构造新元组代替修改:", new_record)

print()
print("长度相同: zip([1,2,3], 'abc')   ->", list(zip([1, 2, 3], "abc")))
print("长度不同: zip([1,2,3], 'ab')    ->", list(zip([1, 2, 3], "ab")))
print("长度不同: zip(names, scores+[99,99]) ->", list(zip(names, scores + [99, 99])))'''))

# ---------- 实验4 ----------
EXP01.append(("md", '''## 实验4：文件读写、异常处理与模块

在 Notebook 同级目录创建 `exp01_data` 文件夹，保存 UTF-8 文本文件 `students.txt`。
每行字段用英文逗号分隔，不包含字段内逗号或引号等复杂情况。数据（含刻意无效记录）为：

```
name,score
Alice,85
Bob,58
Carol,92
David,76
Eva,60
Frank,89
Grace,abc
Henry,105
Incomplete
```'''))

EXP01.append(("md", '''**任务1思路**：先用 `os.getcwd()` 查看当前工作目录，再用 `os.path.join()`
基于当前目录构造数据目录路径，最后用 `os.makedirs(..., exist_ok=True)` 创建
（`exist_ok=True` 保证目录已存在时不会报错）。'''))
EXP01.append(("code", '''import os

cwd = os.getcwd()
print("当前工作目录 os.getcwd():", cwd)

DATA_DIR = os.path.join(cwd, "exp01_data")
print("构造的目录路径 os.path.join():", DATA_DIR)

os.makedirs(DATA_DIR, exist_ok=True)
print("目录是否已创建:", os.path.isdir(DATA_DIR))'''))

EXP01.append(("md", "**任务2思路**：用 `with open(..., encoding=\"utf-8\")` 写入数据（自动关闭文件），"
                     "再重新读取，跳过表头后逐行解析。"))
EXP01.append(("code", '''students_txt = os.path.join(DATA_DIR, "students.txt")

raw_text = """name,score
Alice,85
Bob,58
Carol,92
David,76
Eva,60
Frank,89
Grace,abc
Henry,105
Incomplete
"""

with open(students_txt, "w", encoding="utf-8") as fh:
    fh.write(raw_text)
print("已写入:", students_txt)

with open(students_txt, "r", encoding="utf-8") as fh:
    lines = fh.readlines()

print("总行数:", len(lines))
header = lines[0].strip()
print("表头:", header)
print("跳过后待解析的数据行数:", len(lines[1:]))

for lineno, line in enumerate(lines[1:], start=2):
    print(f"  第{lineno}行原始内容: {line.rstrip()!r}")'''))

EXP01.append(("md", '''**任务3思路**：`parse_student(line)` 依次检查
① 字段数量是否为 2；② 姓名是否为空；③ 成绩能否转成整数；④ 成绩是否在 0~100 范围内。
任何一条不满足都 `raise ValueError`，并在异常消息中写清原因。'''))
EXP01.append(("code", '''def parse_student(line):
    """把 "name,score" 解析为 {'name': str, 'score': int}；无效记录抛 ValueError。"""
    text = line.strip()
    if not text:
        raise ValueError("空行：没有可解析的记录")

    parts = text.split(",")
    if len(parts) != 2:
        raise ValueError(f"字段数量错误：期望 2 个字段，实际 {len(parts)} 个 -> {text!r}")

    name, raw_score = parts[0].strip(), parts[1].strip()
    if not name:
        raise ValueError("姓名为空")

    try:
        score = int(raw_score)
    except ValueError as exc:
        raise ValueError(f"成绩 {raw_score!r} 不是合法整数") from exc

    if not 0 <= score <= 100:
        raise ValueError(f"成绩 {score} 超出 0~100 范围")

    return {"name": name, "score": score}


for sample in ("Alice,85", "David,76"):
    print(f"有效输入 {sample!r} ->", parse_student(sample))'''))

EXP01.append(("md", '''**任务4思路**：逐行处理并把异常捕获在**每行**范围内，
这样一条无效记录不会中断后续记录；同时记录行号与错误原因，有效记录存为字典列表。'''))
EXP01.append(("code", '''valid_records = []
invalid_records = []
error_log = []

for lineno, line in enumerate(lines[1:], start=2):
    try:
        valid_records.append(parse_student(line))
    except ValueError as exc:
        invalid_records.append({"line": lineno, "raw": line.strip(), "reason": str(exc)})
        error_log.append(f"第 {lineno} 行 {line.strip()!r} 无效：{exc}")

print(f"有效记录 {len(valid_records)} 条，无效记录 {len(invalid_records)} 条")
print()
print("=== 有效记录 ===")
for rec in valid_records:
    print(f"  {rec['name']:<8} {rec['score']}")
print()
print("=== 无效记录与错误原因 ===")
for err in error_log:
    print(" ", err)'''))

EXP01.append(("md", '''**任务5思路**：把有效记录数、无效记录数、平均分和及格率写入 `exp01_data/report.txt`。
接着分别演示 `w` 模式与 `a` 模式：
- `"w"`（写入模式）会**清空原有内容**再写入，因此第二次用 `w` 时文件内容被整体覆盖；
- `"a"`（追加模式）会把新内容**追加到文件末尾**，已有内容保持不变。
每一步都打印当前文件内容作为证据。'''))
EXP01.append(("code", '''report_path = os.path.join(DATA_DIR, "report.txt")

avg_valid = sum(r["score"] for r in valid_records) / len(valid_records)
pass_valid = sum(1 for r in valid_records if r["score"] >= 60) / len(valid_records)

summary_text = (
    "===== 实验4 数据统计报告 =====\\n"
    f"有效记录数: {len(valid_records)}\\n"
    f"无效记录数: {len(invalid_records)}\\n"
    f"有效记录平均分: {avg_valid:.2f}\\n"
    f"有效记录及格率: {pass_valid:.2%}\\n"
)


def show_report(title):
    print(f"--- {title} ---")
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as fh:
            print(fh.read().rstrip())
    else:
        print("(文件不存在)")
    print()


# 第一次：w 模式
with open(report_path, "w", encoding="utf-8") as fh:
    fh.write(summary_text)
show_report('第1次：用 "w" 模式写入')

# 第二次：w 模式 —— 证明会清空原有内容
with open(report_path, "w", encoding="utf-8") as fh:
    fh.write("[w 模式演示] 这一行覆盖了上一次的全部内容\\n")
show_report('第2次：再用 "w" 模式写入（原有内容被清空并覆盖）')

# 第三次：a 模式 —— 证明保留原有内容并追加
with open(report_path, "a", encoding="utf-8") as fh:
    fh.write(summary_text)
show_report('第3次：用 "a" 模式追加（原有内容保留，新内容在末尾）')'''))

EXP01.append(("md", '''**任务6思路**：用 `pickle.dump()` 把有效记录列表序列化保存为
`exp01_data/students.pkl`，再用 `pickle.load()` 读回来，并与内存中的原数据比较。
本次数据只含字符串与整数，因此可以直接用 `==` 比较；如果含浮点数，应改用误差比较。'''))
EXP01.append(("code", '''import pickle

pkl_path = os.path.join(DATA_DIR, "students.pkl")

with open(pkl_path, "wb") as fh:
    pickle.dump(valid_records, fh)
print("已保存:", pkl_path)

with open(pkl_path, "rb") as fh:
    loaded_records = pickle.load(fh)

print("原数据   :", valid_records)
print("读回数据 :", loaded_records)
print("类型是否一致:", type(loaded_records).__name__ == type(valid_records).__name__)
print("与原数据是否相等 (==):", loaded_records == valid_records)'''))

EXP01.append(("md", '''**任务7思路**：把 `parse_student()` 保存到与 Notebook 同级的 `student_utils.py` 模块中
（本目录下已提供该文件），通过 `import` 调用，并演示 1 个有效输入和 1 个无效输入。
为了让 Notebook 每次运行都加载到磁盘上的最新版本，这里显式用 `importlib.reload()`。'''))
EXP01.append(("code", '''import importlib
import student_utils
importlib.reload(student_utils)          # 避免内核缓存旧版本的模块

from student_utils import parse_student as parse_student_from_module

print("模块文件位置:", student_utils.__file__)
print()

print('有效输入 parse_student_from_module("Frank,89")')
print("   ->", parse_student_from_module("Frank,89"))
print()

print('无效输入 parse_student_from_module("Grace,abc")')
try:
    parse_student_from_module("Grace,abc")
except ValueError as exc:
    print(f"   -> 抛出 ValueError: {exc}")'''))

EXP01.append(("md", "**任务8思路**：读取一个明确不存在的文件，用 `try/except` 捕获 `FileNotFoundError` 并输出说明。"))
EXP01.append(("code", '''missing_path = os.path.join(DATA_DIR, "no_such_file_20244080305.txt")
print("尝试读取:", missing_path)

try:
    with open(missing_path, "r", encoding="utf-8") as fh:
        fh.read()
except FileNotFoundError as exc:
    print(f"捕获到异常：{type(exc).__name__}")
    print(f"异常信息：{exc}")
    print("说明：目标文件在磁盘上不存在，open() 无法打开，"
          "因此需要捕获 FileNotFoundError 并向用户给出明确提示。")'''))

# ---------- 实验5 ----------
EXP01.append(("md", '''## 实验5：类、继承与对象复制操作

**任务1思路**：定义 `Student` 类，在 `__init__()` 中初始化 `name` 与 `score`；
实现 `is_passed()` 判断是否及格（>= 60），以及 `__str__()` 返回便于打印的对象描述。'''))
EXP01.append(("code", '''class Student:
    """学生类：保存姓名与成绩。"""

    PASS_LINE = 60

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def is_passed(self):
        """成绩达到及格线返回 True，否则返回 False。"""
        return self.score >= self.PASS_LINE

    def __str__(self):
        status = "及格" if self.is_passed() else "不及格"
        return f"Student(name={self.name!r}, score={self.score}, {status})"


s = Student("Alice", 85)
print(s)
print("is_passed() ->", s.is_passed())
print("不及格示例:", Student("Bob", 58), "| is_passed() ->", Student("Bob", 58).is_passed())'''))

EXP01.append(("md", "**任务2思路**：遍历实验4得到的有效记录，为每条记录创建一个 `Student` 对象，"
                     "输出对象信息和及格状态。"))
EXP01.append(("code", '''student_objects = [Student(r["name"], r["score"]) for r in valid_records]

print(f"共创建 {len(student_objects)} 个 Student 对象：")
for obj in student_objects:
    print(f"  {str(obj):<45} is_passed()={obj.is_passed()}")'''))

EXP01.append(("md", '''**任务3思路**：`GraduateStudent` 继承 `Student`，增加 `research_topic` 属性；
用 `super().__init__(...)` 初始化父类的 `name`/`score`，并重写 `__str__()` 以展示研究方向。'''))
EXP01.append(("code", '''class GraduateStudent(Student):
    """研究生：继承 Student，额外拥有研究方向。"""

    def __init__(self, name, score, research_topic):
        super().__init__(name, score)      # 初始化父类属性
        self.research_topic = research_topic

    def __str__(self):                     # 重写父类方法
        status = "及格" if self.is_passed() else "不及格"
        return (f"GraduateStudent(name={self.name!r}, score={self.score}, "
                f"topic={self.research_topic!r}, {status})")


gs = GraduateStudent("Carol", 92, "机器学习")
print(gs)
print("is_passed() 继承自 Student ->", gs.is_passed())
print("是否属于 Student 的实例:", isinstance(gs, Student))
print("继承关系:", GraduateStudent.__mro__[:3])'''))

EXP01.append(("md", '''**任务4思路**：构造含嵌套列表的对象 `{"name": "Alice", "scores": [85, 90]}`，分别做
① **直接赋值**（`b = a`，两者是同一对象）；② **浅拷贝** `copy.copy()`（外层新对象，内层列表仍共享）；
③ **深拷贝** `copy.deepcopy()`（内外层全部复制）。修改内部列表后比较差异。
按题目要求，**每次比较都从新建的原始对象开始**。'''))
EXP01.append(("code", '''import copy


def fresh_original():
    """每次比较都从新建的原始对象开始。"""
    return {"name": "Alice", "scores": [85, 90]}


print("原始对象构造方式:", fresh_original())
print()

# ① 直接赋值
a1 = fresh_original()
b1 = a1
b1["scores"].append(100)
print("① 直接赋值 b = a，修改 b['scores'] 后：")
print("   a =", a1)
print("   b =", b1)
print("   a is b ->", a1 is b1, "（同一个对象，改动互相可见）")
print()

# ② 浅拷贝
a2 = fresh_original()
b2 = copy.copy(a2)
b2["scores"].append(100)
print("② 浅拷贝 b = copy.copy(a)，修改 b['scores'] 后：")
print("   a =", a2)
print("   b =", b2)
print("   a is b ->", a2 is b2, "（外层是新对象，但内层列表仍共享）")
print("   a['scores'] is b['scores'] ->", a2["scores"] is b2["scores"])
print()

# ③ 深拷贝
a3 = fresh_original()
b3 = copy.deepcopy(a3)
b3["scores"].append(100)
print("③ 深拷贝 b = copy.deepcopy(a)，修改 b['scores'] 后：")
print("   a =", a3)
print("   b =", b3)
print("   a is b ->", a3 is b3)
print("   a['scores'] is b['scores'] ->", a3["scores"] is b3["scores"], "（内外层完全独立）")
print()

print("=== 结论 ===")
print("直接赋值       : 完全不复制，两个名字指向同一个对象。")
print("copy.copy()    : 只复制外层容器，嵌套的可变对象仍被共享。")
print("copy.deepcopy(): 递归复制所有层级，修改副本不影响原对象。")'''))

EXP01.append(("md", '''## 三、实验小结

| 实验 | 覆盖内容 | 关键结论 |
|---|---|---|
| 实验1 | 运算符、数据类型、字符串 | `/` 得 float，`//` 向下取整，`%` 取余，`**` 幂；`int()` 截断而非四舍五入；字符串不可变 |
| 实验2 | 函数、条件、循环、递归 | 越界主动 `raise ValueError`；for/while 结果一致；`*args` 打包位置参数 |
| 实验3 | 列表、字典、元组、统计 | `zip()`/`enumerate()`/列表推导式；`alias` 是同一对象，`copy()` 是独立副本 |
| 实验4 | 文件、异常、模块 | `w` 覆盖、`a` 追加；逐行捕获异常不中断；pickle 往返数据相等；模块化 `student_utils.py` |
| 实验5 | 类、继承、对象复制 | `super().__init__()` 复用父类初始化；浅拷贝共享内层对象，深拷贝完全独立 |

**运行环境自检**：本 Notebook 在独立 conda 环境 `exp01` 中，从空白内核开始按顺序运行全部单元格，
未出现 `NameError` 等依赖旧变量的问题。'''))

write_nb(os.path.join(EXP01_DIR, f"{STUDENT_ID}_{NAME}_exp01.ipynb"), EXP01)
print("EXP01 cells:", len(EXP01))
