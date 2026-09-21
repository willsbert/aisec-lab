# -*- coding: utf-8 -*-
"""D6 实验3：带持久记忆的 Agent（演示记忆层投毒）"""
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage

MODEL = "qwen2.5:7b"
app = FastAPI()
llm = ChatOllama(model=MODEL)
memory = []  # 模拟持久记忆：[(role, content)]

class Req(BaseModel):
    prompt: str

@app.post("/run")
def run(req: Req):
    memory.append(("user", req.prompt))
    msgs = [HumanMessage(content=c) if r == "user" else AIMessage(content=c) for r, c in memory]
    reply = llm.invoke(msgs).content
    memory.append(("assistant", reply))
    return {"reply": reply, "memory_len": len(memory)}
