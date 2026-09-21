"""批量执行注入/越狱用例，结果写入 reports/<name>.json

用法：
    python run_injections.py [靶标地址] [输出文件名]
示例：
    python run_injections.py http://localhost:8001/chat d2_results
    python run_injections.py http://localhost:8002/ask   # RAG 靶标（字段为 question，见下方适配）
"""
import json
import sys

import requests

CASES = json.load(open("attacks/injections.json", encoding="utf-8"))


def send(target: str, prompt: str) -> dict:
    """默认按靶标 A（/chat, messages 字段）发送；RAG 靶标需改字段。"""
    if target.endswith("/ask"):
        r = requests.post(target, json={"question": prompt}, timeout=180)
        return {"reply": r.json().get("answer", "")}
    r = requests.post(target, json={"messages": [{"role": "user", "content": prompt}]}, timeout=180)
    return {"reply": r.json().get("reply", "")}


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8001/chat"
    name = sys.argv[2] if len(sys.argv) > 2 else "d2_results"
    results = []
    for c in CASES:
        try:
            out = send(target, c["prompt"])
            reply = out.get("reply", "")
            print(f"[{c['id']}] {c['label']} -> 响应长度 {len(reply)}")
            results.append({"id": c["id"], "label": c["label"], "prompt": c["prompt"], "reply": reply[:300]})
        except Exception as e:
            print(f"[{c['id']}] {c['label']} -> 出错 {e}")
            results.append({"id": c["id"], "label": c["label"], "prompt": c["prompt"], "error": str(e)})
    path = f"reports/{name}.json"
    json.dump(results, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"已写入 {path}")


if __name__ == "__main__":
    main()
