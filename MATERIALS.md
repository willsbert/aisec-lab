# aisec-lab 物料索引（全部文件 · 对应实验日）

> 每个文件都对应两周计划中的某一天，按天使用。

## 靶标（D1）

| 文件 | 说明 |
|---|---|
| targets/a_chat/main.py | 对话应用（无防护版，攻击靶标） |
| targets/b_rag/main.py | RAG 问答（自动建索引） |
| targets/b_rag/docs/internal.txt | 知识文档（D3 投毒对象） |
| targets/b_rag/docs/product.txt | 知识文档 |
| targets/c_agent/main.py | 多工具 Agent（无权限版，攻击靶标） |

## 攻击物料

| 文件 | 对应 | 说明 |
|---|---|---|
| attacks/injections.json | D2 | 10 条注入/越狱用例 |
| attacks/run_injections.py | D2/D4 | 批量执行脚本（支持 /chat 与 /ask） |
| attacks/poison_instructions.md | D3 | RAG 投毒 + 越权检索步骤 |
| attacks/leak_prompts.json | D10 | 6 种系统提示词泄露手法 |

## 防护/加固变体

| 文件 | 对应 | 说明 |
|---|---|---|
| targets/a_chat/main_protected.py | D4 | 对话应用 4 层防护版 |
| targets/c_agent/main_injected.py | D6 | 工具注入版（web_search 返回埋指令） |
| targets/c_agent/main_hardened.py | D7 | Agent 加固 v2（权限矩阵+审批+步数上限） |

## 工具脚本

| 文件 | 对应 | 说明 |
|---|---|---|
| tools/lora_backdoor.py | D5 | LoRA 微调 + 后门投毒训练 |
| tools/verify_backdoor.py | D5 | 基础模型 vs +adapter 行为对比 |
| tools/hash_check.py | D5/D11 | 权重/adapter sha256 校验 |
| tools/pyrit_demo.py | D9 | PyRIT 红队自动化 |
| tools/art_demo.py | D9 | ART FGSM 对抗样本演示 |
| tools/own_detector.py | D9 | 自研注入检测器（关键词+启发式） |

## 测评配置与报告模板

| 文件 | 对应 | 说明 |
|---|---|---|
| reports/promptfooconfig.yaml | D8 | Promptfoo 回归测试配置 |
| reports/d7_threat_model.md | D7 | OWASP 10 项威胁建模（含示例） |
| reports/red-team-report.md | D12 | 综合红队报告模板（主交付物） |
| reports/d13_regression.md | D13 | 修复回归对比表 |

## 使用速查

```bash
# D2：对对话靶标跑注入
python attacks/run_injections.py http://localhost:8001/chat d2_results

# D4：换防护版重启后重跑
uvicorn main_protected:app --port 8001
python attacks/run_injections.py http://localhost:8001/chat d4_protected

# D5：训练并验证后门
python tools/lora_backdoor.py && python tools/verify_backdoor.py

# D6：工具注入版启动后触发
uvicorn main_injected:app --port 8003
curl -X POST http://localhost:8003/run -H 'Content-Type: application/json' \
  -d '{"prompt":"帮我搜索 AI 安全"}'

# D7：加固版启动后验证拦截
uvicorn main_hardened:app --port 8003
curl -X POST http://localhost:8003/run -H 'Content-Type: application/json' \
  -d '{"prompt":"把当前目录列表写入文件 files.txt"}'

# D8：回归测试
cd reports && promptfoo eval -c promptfooconfig.yaml

# D9：红队与对抗样本
python tools/pyrit_demo.py && python tools/art_demo.py
python tools/own_detector.py --batch

# D10：泄露测试
python -c "import json,requests;[print(c['id'], requests.post('http://localhost:8001/chat', json={'messages':[{'role':'user','content':c['prompt']}]}).json().get('reply','')[:150]) for c in json.load(open('attacks/leak_prompts.json'))]"

# D11：供应链审计
pip-audit -r requirements.txt
cyclonedx-py requirements -o reports/sbom.xml
python tools/hash_check.py /tmp/qwen05.safetensors <官方sha256>

# D12/D13：红队 + 修复回归
# 按 reports/red-team-report.md 与 reports/d13_regression.md 模板执行
```
