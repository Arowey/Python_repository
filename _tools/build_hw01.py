# -*- coding: utf-8 -*-
"""Generate the HW01 deliverable notebook (no execution)."""
import json, os

ROOT = r"C:\Users\guoqi\Desktop\南华大学\python数据分析"
HW01_DIR = os.path.join(ROOT, "HW01")
STUDENT_ID = "20244080305"
NAME = "郭乾威"


def cells_from(spec):
    out = []
    for i, (kind, src) in enumerate(spec):
        cid = f"hw01-{i:03d}"
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
            "language_info": {"name": "python", "version": "3.14",
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

HW = []

HW.append(("md", f'''# 作业1：Data Types, Functions and Conditionals

- 作者：丁平尖
- 完成人：{NAME}（学号 {STUDENT_ID}）
- 作业编号：**01**

> 本 Notebook 按题目顺序给出每个函数的实现与测试，并在关键处用 Markdown 写下思路与结论。
> 提交前已重启内核、从上到下运行全部单元格。
'''))

HW.append(("md", '''## 注意事项

1. 尽早开始！如果在安装或导入包时遇到问题，最好提前发现这些问题，而不是在作业截止前一晚。
2. 确保备份您的工作！推荐学习使用 git。
3. 请先将第一个代码框中的学号修改为自己的学号，再完成以下作业，并按顺序运行各个代码框。'''))
HW.append(("md", "### 第一个代码框：身份记录\n\n"
                 "本 Notebook 运行于独立环境 **`exp01`**（Python 3.12，不是 base 环境）。"))
HW.append(("code", IDENTITY))

HW.append(("md", f'''## 作业写作和提交说明

未能遵循这些说明将导致失分。本作业写在一个 Jupyter Notebook 文件中，
提交文件名为 `学号_姓名_hwX.ipynb`（X 为作业编号）。
本次作业编号为 **01**，因此实际提交文件名为 **`{STUDENT_ID}_{NAME}_hw01.ipynb`**。'''))

# ============ 热身在 ============
HW.append(("md", '''## 热身在：定义简单函数

在这个问题中练习在 Python 中定义简单函数。三个函数都只是打印，不需要返回值。'''))

HW.append(("md", "**1. `say_hi`**：不接受任何参数，被调用时打印字符串 `Hello, world!`。"))
HW.append(("code", '''def say_hi():
    """不接收参数，打印 Hello, world!。"""
    print("Hello, world!")


say_hi()'''))

HW.append(("md", "**2. `goat_pad`**：接收一个字符串作为唯一参数，打印该字符串前后都加上 `goat` 的结果。"))
HW.append(("code", '''def goat_pad(s):
    """打印 "goat" + s + "goat"。"""
    print("goat" + s + "goat")


goat_pad("hello")
goat_pad("")'''))

HW.append(("md", "**3. `print_n`**：接收字符串 `s` 和整数 `n`，把 `s` 打印 `n` 次，每次单独一行。"))
HW.append(("code", '''def print_n(s, n):
    """把字符串 s 打印 n 次，每次单独一行。"""
    for _ in range(n):
        print(s)


print_n("hi", 3)
print("---")
print_n("Python", 0)   # n = 0 时不打印任何内容'''))

# ============ 欧几里得算法 ============
HW.append(("md", '''## 欧几里得算法

欧几里得算法是一种寻找两个数的最大公约数（GCD）的方法。两个数 m 和 n 的最大公约数，
是同时能整除 m 和 n 的最大数。

**思路**：利用 `gcd(m, n) = gcd(n, m % n)`，当 `n == 0` 时 `m` 即为最大公约数。
这是典型的递归结构。'''))

HW.append(("md", "**1. 实现 `gcd`**：接收两个整数，返回它们的 GCD。可以假设输入都是整数，不需要错误检查。"))
HW.append(("code", '''def gcd(m, n):
    """用欧几里得算法返回 m 和 n 的最大公约数。"""
    if n == 0:
        return m
    return gcd(n, m % n)


print("gcd(12, 8)   =", gcd(12, 8))
print("gcd(54, 24)  =", gcd(54, 24))
print("gcd(17, 5)   =", gcd(17, 5))'''))

HW.append(("md", "**2. 用函数求以下数对的 GCD**：`(2018, 2019)`、`(1200, 300)`、`(5040, 60)`。"))
HW.append(("code", '''pairs = [(2018, 2019), (1200, 300), (5040, 60)]

for m, n in pairs:
    print(f"gcd({m}, {n}) = {gcd(m, n)}")'''))

HW.append(("md", '''**3. 如果参数是负数会怎样？这种行爲有意义吗？**

**结论**：算法本身**不会崩溃**，因为当 `n` 为负数时，`m % n` 的符号**跟随 `n`**
（即结果 `<= 0`），于是 `gcd(m, -n)` 返回负数；而当 `n` 为正数时结果为正。
因此"两个负数"或"一正一负"时，返回值可能是负的最大公约数（绝对值仍是正确的 GCD 数字）。

**是否有意义**：从数学定义看，最大公约数通常定义为**非负**数（`gcd(a, b) >= 0`），
所以返回负数在语义上不太合理，容易造成误用；但绝对值是正确的。下面实测验证。'''))
HW.append(("code", '''cases = [(-12, 18), (12, -18), (-12, -18), (-12, 0), (0, -12)]

print("实测负数与零参数的行为：")
for m, n in cases:
    print(f"  gcd({m:>4}, {n:>4}) = {gcd(m, n):>5}")

print()
print("结论：返回值的绝对值始终是真正的最大公约数，但符号不固定——")
print("      n 为负数时结果为负；这在数学上不符合“GCD 非负”的习惯定义。")
print()
print("如果希望行为更有意义，可以统一取绝对值：")
print("  gcd_abs(-12, 18) =", abs(gcd(-12, 18)))
print("  gcd_abs(-12, -18) =", abs(gcd(-12, -18)))'''))

# ============ 近似欧拉数 e ============
HW.append(("md", '''## 近似欧拉数 e

自然对数的底数 e 通常被定义为无限和（公式 1）：

$$e = \\sum_{k=0}^{\\infty} \\frac{1}{k!} = 1 + \\frac{1}{1} + \\frac{1}{2} + \\frac{1}{6} + \\frac{1}{24} + \\dots \\qquad (1)$$

其中 $k!$ 表示 k 的阶乘，$k! = k \\cdot (k-1) \\cdot (k-2) \\cdots 3 \\cdot 2 \\cdot 1$，我们约定 $0! = 1$。

欧拉数的一个早期特征（归功于雅各布·伯努利）是作为极限（公式 2）：

$$e = \\lim_{x \\to \\infty} \\left(1 + \\frac{1}{x}\\right)^{x} \\qquad (2)$$'''))

HW.append(("md", "**1. `euler_limit(n)`**：接收整数 `n`，通过公式（2）中取 `x = n` 来近似 e。"))
HW.append(("code", '''def euler_limit(n):
    """用 (1 + 1/n) ** n 近似 e（公式 2，取 x = n）。"""
    return (1 + 1 / n) ** n


for n in (1, 2, 10, 100, 1000, 100000, 1000000):
    print(f"euler_limit({n:>8}) = {euler_limit(n):.10f}")'''))

HW.append(("md", '''**2. `euler_infinite_sum(n)`**：接收非负整数 `n`，基于公式（1）中前 `n` 项之和返回 e 的近似值。

- 公式（1）的和从 `k = 0` 开始计数（0-索引），而本题函数从 `n = 1` 开始计数（1-索引）。
- 因此 `euler_infinite_sum(1)` 只使用公式（1）中的**一个**项，返回 `1`。
- 类似地 `euler_infinite_sum(0)` 返回 `0`（不使用任何项）。
- `euler_infinite_sum(4)` = `1 + 1 + 1/2 + 1/6 ≈ 2.667`。

即：`euler_infinite_sum(n) = Σ_{k=0}^{n-1} 1/k!`。'''))
HW.append(("code", '''def euler_infinite_sum(n):
    """公式（1）中前 n 项之和（n 从 1 开始计数，即 Σ_{k=0}^{n-1} 1/k!）。"""
    total = 0.0
    for k in range(n):          # k = 0, 1, ..., n-1
        total += 1 / factorial(k)
    return total


def factorial(k):
    """k! ，约定 0! = 1。"""
    result = 1
    for i in range(2, k + 1):
        result *= i
    return result


print("对照表 k! :", [factorial(k) for k in range(7)])
print()
print("euler_infinite_sum(0)  =", euler_infinite_sum(0), "（题目要求返回 0）")
print("euler_infinite_sum(1)  =", euler_infinite_sum(1), "（题目要求返回 1）")
print("euler_infinite_sum(4)  =", euler_infinite_sum(4), "（题目要求约 2.667）")
print()
print("前若干项之和：")
for n in range(1, 11):
    print(f"  euler_infinite_sum({n:>2}) = {euler_infinite_sum(n):.10f}")'''))

HW.append(("md", '''**3. `euler_approx(epsilon)`**：接收一个浮点数 `epsilon`，使用公式（1）中的和
来获得一个在 `epsilon` 内接近真实值 e 的近似值。

**思路**：用 `while` 循环不断累加 `1/k!`，每加一项就比较
`abs(total - math.exp(1)) < epsilon`，满足即返回。
为了避免浮点下溢导致死循环，加上"新增项已小到无法改变结果"的提前退出保护。'''))
HW.append(("code", '''import math

print("math.exp(1) 真实值 =", repr(math.exp(1)))
print()


def euler_approx(epsilon):
    """不断累加 1/k!，直到与 math.exp(1) 的误差小于 epsilon 时返回该近似值。"""
    total = 0.0
    k = 0
    while True:
        term = 1 / factorial(k)
        new_total = total + term
        if new_total == total:
            # 新增项已小于浮点精度，继续累加不会再改变结果，直接返回
            return new_total
        total = new_total
        if abs(total - math.exp(1)) < epsilon:
            return total
        k += 1


for eps in (1e-2, 1e-5, 1e-10, 1e-15):
    approx = euler_approx(eps)
    print(f"euler_approx({eps:.0e}) = {approx!r}")
    print(f"    实际误差 |approx - e| = {abs(approx - math.exp(1)):.3e}  < {eps:.0e} ? "
          f"{abs(approx - math.exp(1)) < eps}")'''))

HW.append(("md", "**4. `print_euler_sum_table(n)`**：接收正整数 `n`，打印 `euler_infinite_sum(k)` 的值，"
                 "`k` 的范围从 1 到 `n`，每行一个。"))
HW.append(("code", '''def print_euler_sum_table(n):
    """打印 euler_infinite_sum(k)，k 从 1 到 n，每行一个。"""
    for k in range(1, n + 1):
        print(f"euler_infinite_sum({k:>2}) = {euler_infinite_sum(k):.10f}")


print_euler_sum_table(8)'''))

# ============ 测试整数属性 ============
HW.append(("md", '''## 测试整数属性

你将得到更多关于条件的练习，并对典型的"编程面试"问题所需的思维方式有一个初步的了解。

一个正整数 $n$ 是 2 的幂，如果 $n = 2^p$ 对于某个整数 $p \\ge 0$。'''))

HW.append(("md", '''**1. `is_power_of_2(p)`**：接收一个正整数，返回布尔值表示它是不是 2 的幂。

**限制**：不能使用内置的 `math.sqrt`，只需使用除法和模（`%`）运算。

**思路**：如果一个数大于 1 且是 2 的幂，那么它必然能被 2 整除；不断除以 2，
最终会得到 1。若中途出现奇数（除不尽），则不是 2 的幂。`1 = 2^0` 也返回 True。'''))
HW.append(("code", '''def is_power_of_2(p):
    """判断正整数 p 是否为 2 的幂（只用除法和取模运算）。"""
    if p <= 0:
        return False
    while p > 1:
        if p % 2 != 0:      # 出现奇数因子，说明不是 2 的幂
            return False
        p = p // 2
    return True


print("p   :", [1, 2, 3, 4, 5, 8, 9, 16, 17, 1024, 1023])
print("结果:", [is_power_of_2(p) for p in (1, 2, 3, 4, 5, 8, 9, 16, 17, 1024, 1023)])'''))

HW.append(("md", '''**2. `is_power(b, n)`**：接收两个正整数 `b` 和 `n`（按此顺序），返回布尔值；
`is_power(b, n)` 当 `n` 是 `b` 的幂时返回 True，否则返回 False。

**思路**：把上面的解法推广——反复用 `n` 除以 `b`，若最後恰好除到 1 则为幂。
`b = 1` 时要单独处理（`1^p = 1`，只有 `n = 1` 时成立）。
`n = 1` 时任何 `b` 都满足 `b^0 = 1`，应返回 True。'''))
HW.append(("code", '''def is_power(b, n):
    """判断 n 是否为 b 的幂（b、n 均为正整数）。"""
    if b <= 0 or n <= 0:
        return False
    if b == 1:
        return n == 1        # 1 的任何次幂都是 1
    while n > 1:
        if n % b != 0:       # 不能整除，说明不是 b 的幂
            return False
        n = n // b
    return True


tests = [(2, 1), (2, 2), (2, 3), (2, 4), (2, 8), (2, 16), (2, 1024),
         (3, 9), (3, 27), (3, 10), (5, 125), (5, 126), (1, 1), (1, 2)]

print(f"{'b':>4} {'n':>6}   结果")
for b, n in tests:
    print(f"{b:>4} {n:>6}   {is_power(b, n)}")'''))

HW.append(("md", '''## 小结

| 题目 | 函数 | 关键点 |
|---|---|---|
| 热身在 | `say_hi`、`goat_pad`、`print_n` | 无参数/单参数/双参数的函数定义与打印 |
| 欧几里得算法 | `gcd` | 递归 `gcd(m, n) = gcd(n, m % n)`；负数时符号跟随 `n` |
| 近似欧拉数 e | `euler_limit`、`euler_infinite_sum`、`euler_approx`、`print_euler_sum_table` | 公式(2)取 x=n；公式(1) 1-indexed 换算；while 累加到误差小于 ϵ |
| 测试整数属性 | `is_power_of_2`、`is_power` | 只用 `/` 与 `%`；推广到任意底数，处理 `b=1` 与 `n=1` |

**运行环境自检**：本 Notebook 在独立 conda 环境 `exp01` 中，从空白内核开始按顺序运行全部单元格，
未出现 `NameError` 等依赖旧变量的问题。'''))

write_nb(os.path.join(HW01_DIR, f"{STUDENT_ID}_{NAME}_hw01.ipynb"), HW)
print("HW01 cells:", len(HW))
