"""子包。知识点：子包结构、接口提升。"""
print(f"[init subpackage] __name__={__name__}, __package__={__package__}")

from . import module_b
__all__ = ["module_b"]