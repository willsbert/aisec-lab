"""D5/D11 · 权重与 adapter 完整性校验（跨平台 hashlib，macOS/Linux 通用）

用法：
    python hash_check.py <文件或目录> [参考hash]
示例：
    python hash_check.py ./lora_adapter
    python hash_check.py /tmp/qwen05.safetensors <官方sha256>
说明：
    - 目录：递归计算所有文件 hash 并输出清单
    - 带参考 hash：比对并输出是否一致
"""
import hashlib
import os
import sys


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    ref = sys.argv[2] if len(sys.argv) > 2 else None

    files = []
    if os.path.isdir(path):
        for root, _, names in os.walk(path):
            for n in sorted(names):
                files.append(os.path.join(root, n))
    else:
        files = [path]

    print(f"== 校验对象：{path}（{len(files)} 个文件）==")
    for f in files:
        h = sha256(f)
        status = ""
        if ref:
            status = "一致" if h == ref.lower() else "不一致！"
        print(f"{h}  {f}  {status}")
    if not ref:
        print("\n（未提供参考 hash；如需比对，追加第二个参数：python hash_check.py <路径> <sha256>）")


if __name__ == "__main__":
    main()
