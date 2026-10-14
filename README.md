# 交付说明

本仓库为《Python数据分析》课程作业交付，由两份任务书 PDF 中的要求逐条完成。

| 目录 | 内容 |
|---|---|
| `EXP01/` | 实验报告01：Python基础与数据处理入门 |
| `HW01/` | 作业1：Data Types, Functions and Conditionals |

## EXP01 实验报告01

| 文件 | 说明 |
|---|---|
| `20244080305_郭乾威_exp01.ipynb` | 实验1~5 全部 33 个操作任务，已执行、带输出 |
| `student_utils.py` | 实验4第7题要求的模块（`parse_student`） |
| `exp01_data/students.txt` | 实验4第2题的数据文件（含刻意无效记录） |
| `exp01_data/report.txt` | 实验4第5题输出，含 `w` 覆盖与 `a` 追加的对比证据 |
| `exp01_data/students.pkl` | 实验4第6题 pickle 往返验证产物 |

模拟成绩数据（题目给定）：

```python
names = ["Alice", "Bob", "Carol", "David", "Eva", "Frank"]
scores = [85, 58, 92, 76, 60, 89]
```

关键结果：有效记录 6 条、无效记录 3 条（`Grace,abc` 非整数、`Henry,105` 越界、`Incomplete` 字段不足），
有效记录平均分 76.67、及格率 83.33%。

## HW01 作业1

| 文件 | 说明 |
|---|---|
| `20244080305_郭乾威_hw01.ipynb` | 4 部分共 16 小题，已执行、带输出 |

涵盖：热身在函数（`say_hi` / `goat_pad` / `print_n`）、欧几里得算法（`gcd`）、
近似欧拉数 e（`euler_limit` / `euler_infinite_sum` / `euler_approx` / `print_euler_sum_table`）、
测试整数属性（`is_power_of_2` / `is_power`）。

关键结果：`gcd(2018,2019)=1`、`gcd(1200,300)=300`、`gcd(5040,60)=60`；
`euler_infinite_sum(0)=0`、`(1)=1`、`(4)≈2.667`。

## 运行环境

两个 Notebook 均在独立的 Python 3.12 环境中执行（非 base 环境），
按顺序从空白内核运行全部代码，无报错、无依赖旧变量的问题。

## 说明

- 学号 20244080305，姓名 郭乾威；`STUDENT_ID` 已按要求替换。
- 两份原始任务书 PDF（`EXP01.pdf`、`HW01.pdf`）保留在各自目录中，未作修改。
- `_tools/` 为完成过程中的辅助脚本（PDF 取字工具、Notebook 生成/执行/校验脚本），
  不影响作业内容，可按需忽略或删除。
