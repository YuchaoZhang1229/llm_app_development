"""
module_a —— 包内子模块,演示:
- __name__ / __package__ / __file__ 等模块属性
- 绝对导入 vs 相对导入
- 模块级 __all__
- if __name__ == "__main__": 支持 python -m 直接运行
"""

print(f"[load module_a] __name__={__name__}, __package__={__package__}")

# ---------- 绝对导入(推荐,可读性好,包内包外都能用) ----------
import os

# ---------- 相对导入语法(此处仅注释,避免循环导入) ----------
# 只能在包内使用:
#   from .      import xxx      # 当前包
#   from ..     import xxx      # 上一级包(父包)
#   from ..sub  import xxx      # 兄弟子包
#
# 直接用 `python module_a.py` 运行时,__package__ 为空,
# 相对导入会抛 ImportError: attempted relative import with no known parent package

__all__ = ["greet"]

def greet(name: str = "World") -> str:
    """普通函数,会被 __init__.py 提升到包级别"""
    return f"Hello, {name}! (来自 mypackage.module_a)"

# ---------- 作为脚本直接运行 ----------
# 方式一:python -m mypackage.module_a   ✅ 推荐, __package__ 正常
# 方式二:python mypackage/module_a.py   ⚠️ __package__ 为空, 相对导入会报错
if __name__ == "__main__":
    print(greet("module_a 以脚本方式运行(__name__ == '__main__')"))
