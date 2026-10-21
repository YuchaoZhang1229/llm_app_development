"""子包内模块"""
print(f"[load module_b] __name__={__name__}, __package__={__package__}")

__all__ = ["add"]


def add(a, b):
    return a + b

if __name__ == "__main__":
    print(add(1,2))
