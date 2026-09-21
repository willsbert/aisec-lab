"""靶标 B：RAG 问答应用（LangChain + FAISS + Ollama，刻意不做安全防护）

启动：
    uvicorn main:app --port 8002
首次启动自动读取 docs/*.txt 构建索引；删除 index/ 目录可重建。

环境变量：
    OLLAMA_URL  Ollama 地址（默认 http://localhost:11434）
    MODEL       生成模型（默认 qwen2.5:7b）
    EMBED_MODEL 嵌入模型（默认 nomic-embed-text）
"""
import os

import requests
from fastapi import FastAPI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from pydantic import BaseModel

app = FastAPI()
OLLAMA = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "qwen2.5:7b")
EMB = OllamaEmbeddings(model=os.getenv("EMBED_MODEL", "nomic-embed-text"))
INDEX_DIR = "index"
DOC_DIR = "docs"


def build_index():
    loader = DirectoryLoader(DOC_DIR, glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30).split_documents(docs)
    db = FAISS.from_documents(chunks, EMB)
    db.save_local(INDEX_DIR)
    print(f"[build_index] 完成：{len(chunks)} 个分片 -> {INDEX_DIR}/")
    return db


if os.path.exists(INDEX_DIR):
    db = FAISS.load_local(INDEX_DIR, EMB, allow_dangerous_deserialization=True)
    print(f"[load] 已加载索引 {INDEX_DIR}/")
else:
    db = build_index()


class Req(BaseModel):
    question: str


@app.post("/ask")
def ask(req: Req):
    docs = db.similarity_search(req.question, k=3)
    ctx = "\n\n".join(d.page_content for d in docs)
    llm = ChatOllama(model=MODEL, base_url=OLLAMA)
    prompt = (
        "根据【资料】回答问题，若资料中没有相关信息则回答不知道。\n\n"
        f"【资料】\n{ctx}\n\n【问题】{req.question}\n回答："
    )
    return {
        "answer": llm.invoke(prompt).content,
        "sources": [d.page_content[:60] for d in docs],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
