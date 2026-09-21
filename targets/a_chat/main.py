"""靶标 A：纯对话应用（刻意不做安全防护，作为攻击靶标）

启动：
    uvicorn main:app --port 8001
环境变量：
    OLLAMA_URL  Ollama 地址（默认 http://localhost:11434）
    MODEL       模型名（默认 qwen2.5:7b，内存紧张可切 qwen2.5:3b）
"""
import os

import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
OLLAMA = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "qwen2.5:7b")


class Req(BaseModel):
    messages: list


@app.post("/chat")
def chat(req: Req):
    r = requests.post(
        f"{OLLAMA}/api/chat",
        json={"model": MODEL, "messages": req.messages, "stream": False},
        timeout=180,
    )
    return {"reply": r.json()["message"]["content"]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
