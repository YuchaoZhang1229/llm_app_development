"""
mypackage —— 顶层包,演示 __init__.py 的全部知识点
=====================================================

知识点速览:
1. 包标识文件:Python 3.3+ 有命名空间包(无 __init__.py 也能导入),
   但普通包/需要初始化逻辑的包必须保留。
2. 初始化代码:第一次 import mypackage 时执行,且只执行一次。
3. __all__:控制 `from mypackage import *` 导入哪些名字。
4. 接口提升:把子模块中的常用对象提到包级别,方便使用方:
       from mypackage import greet
   而不是
       from mypackage.module_a import greet
5. 包级元数据:__version__、__author__ 等。
6. __path__:包的搜索路径,子包/子模块就是在这里面找的。
"""

import sys

# ---------- 包级元数据 ----------
__version__ = "1.0.0"
__author__ = "Tutorial"

# ---------- 演示:包初始化时执行的代码(只执行一次) ----------
print(f"[init mypackage] __name__={__name__}, __package__={__package__}, "
      f"已在sys.modules={'mypackage' in sys.modules}")

# ---------- 相对导入:从当前包中导入模块 ----------
from . import module_a               # 同包兄弟模块
from .subpackage import module_b     # 子包中的模块

# ---------- 接口提升:把常用对象提到包级别 ----------
from .module_a import greet


# ---------- __all__:仅对 `from mypackage import *` 生效 ----------
# 不写 __all__ 时,`import *` 会导入所有"不以下划线开头"的名字
__all__ = ["module_a", "module_b", "greet"]