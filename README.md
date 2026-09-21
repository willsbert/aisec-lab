# aisec-lab · LLM 安全攻防实验平台

基于本地 Ollama + qwen2.5 搭建的三靶标攻防实验环境，覆盖 OWASP LLM Top 10 全链路。

## 结构
- targets/a_chat · 对话应用（基线 / 防护版）
- targets/b_rag · RAG 问答（投毒 / 越权检索）
- targets/c_agent · Agent 工具调用（注入 / 加固版）
- attacks/ · 注入与越狱用例集 + 批量执行脚本
- tools/ · LoRA 后门训练与验证、哈希校验、自动化评估
- reports/ · 威胁建模、红队报告、防御设计、供应链审计

## 快速开始
1. 安装 Ollama 并拉取 qwen2.5:7b / qwen2.5:0.5b / nomic-embed-text
2. pip install -r requirements.txt
3. uvicorn main:app --port 8001/8002/8003 启动靶标
4. python attacks/run_injections.py http://localhost:8001/chat d2_results

## 实验清单（D1-D13）
注入/越狱基线、RAG 文档投毒、越权检索、LoRA 后门、Agent 工具注入、
过度代理、记忆投毒、威胁建模、防护加固、自动化评估、供应链审计、红队报告

## 关键结论
- 关键词过滤拦直白注入 100%，高级语义绕过 0%
- 投毒文档不清理则持续泄露
- 模型对齐 ≠ 系统防御；安全与可用性需分层权衡
# aisec-lab
