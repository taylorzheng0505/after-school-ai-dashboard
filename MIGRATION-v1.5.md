# v1.5 升级说明

本次需要更新 3 个工作流：
- `homework-grading-report`
- `l2-daily-report`
- `l3-daily-report`

L2周报、L3周报、L3月报无需重新安装。

## ChatGPT Skill 用户
删除旧版以上3个Skill，再安装 `platforms/chatgpt/<skill>/skill.zip` 的v1.5完整包。

## 本地/其他AI工作流用户
用v1.5对应的整个工作流文件夹替换旧文件夹，不建议仅覆盖单个SYSTEM_PROMPT，以免漏掉新增：
- `references/daily-data-schema.md`
- `scripts/render_daily.py`
- `scripts/validate_daily_data.py`

## 新数据链
`原始作业 → grading-data.json + crops + grading-report.html → daily-data.json → 家长日报HTML`

最终批改HTML和日报HTML都仍然可以自包含图片；变化仅发生在AI运行中间层，避免模型处理大块base64。
