# v1.4 升级说明

本次升级新增作业批改工作流，并更新 L2/L3 日报。

## ChatGPT 用户
- 删除旧版 `l2-daily-report` 后安装 v1.4 完整 `skill.zip`。
- 删除旧版 `l3-daily-report` 后安装 v1.4 完整 `skill.zip`。
- 新安装 `homework-grading-report/skill.zip`。
- L2/L3 周报和 L3 月报保持 v1.3，无需重装。

## 其他AI / 本地工作流
用 v1.4 仓库中的以下目录整体替换对应旧目录：
- `workflows/l2-daily-report/`
- `workflows/l3-daily-report/`

并新增：
- `workflows/homework-grading-report/`

不要只覆盖单个 `SYSTEM_PROMPT.md`，因为本次同时更新了模板、规则和脚本。
