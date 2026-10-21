"""
mymodule.py —— 单个模块示例

要点：
1. 一个 .py 文件就是一个模块（module）
2. 模块里可以放：变量、函数、类
3. __name__ == "__main__" 保护"只在直接运行时才执行的代码"
"""

# ---------- 1. 模块级变量 ----------
VERSION = "1.0.0"
PI = 3.14159

# 用 __all__ 控制 `from calculator import *` 会导出哪些名字
__all__ = ["add", "divide", "Calculator", "PI"]


# ---------- 2. 函数 ----------
def add(a, b):
    """返回两数之和"""
    return a + b


def divide(a, b):
    """返回两数之商，除数为 0 时抛异常"""
    if b == 0:
        raise ValueError("除数不能为 0")
    return a / b


# ---------- 3. 类 ----------
class Calculator:
    """一个带历史记录的简单计算器"""

    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def show_history(self):
        return "\n".join(self.history) or "(空)"


# ---------- 4. 模块级测试代码 ----------
# 只有 `python mymodule.py` 直接运行时，这段才执行；
# 被 import 时不会执行，避免污染调用方。
if __name__ == "__main__":
    print("我是作为脚本直接运行的，__name__ =", __name__)
    print("add(1, 2) =", add(1, 2))
    print("divide(10, 4) =", divide(10, 4))

    c = Calculator()
    c.add(3, 5)
    print("历史记录：", c.show_history())