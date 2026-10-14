"""student_utils.py —— 实验4第7题要求的模块。

把解析学生记录的 parse_student() 独立成模块，供 Notebook 通过 import 调用。
"""


def parse_student(line):
    """把一行 "name,score" 文本解析为 {'name': str, 'score': int} 字典。

    校验规则（任一不满足都抛出 ValueError，并在消息中说明原因）：
      1. 去掉首尾空白与行尾换行后，用英文逗号分隔必须恰好得到 2 个字段；
      2. 姓名字段不能为空；
      3. 成绩字段必须能转换成整数；
      4. 成绩必须在 0~100 范围内（含端点）。

    参数:
        line: 文件中的一行文本，例如 "Alice,85" 或 "Alice,85\\n"。

    返回:
        {'name': 'Alice', 'score': 85}
    """
    if not isinstance(line, str):
        raise ValueError(f"输入必须是字符串，实际收到 {type(line).__name__}")

    text = line.strip()
    if not text:
        raise ValueError("空行：没有可解析的记录")

    parts = text.split(",")
    if len(parts) != 2:
        raise ValueError(
            f"字段数量错误：期望 2 个字段（name,score），实际得到 {len(parts)} 个 -> {text!r}"
        )

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
