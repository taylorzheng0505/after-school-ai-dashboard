# 课后托管 AI 看板工作流

> L2 / L3 家长看板、跨学科作业批改、固定HTML模板与跨AI工作流的统一版本库。

## 仓库结构
- `core/`：机构统一产品、数据接口、文件读取和视觉规则。
- `workflows/`：6个跨平台工作流。
- `platforms/chatgpt/`：6个可安装 ChatGPT `skill.zip`。
- `student-folder-template/`：本地学生资料目录示例，不存真实学生数据。

## 六个工作流
1. `homework-grading-report` — 跨学科作业批改与标准批改报告
2. `l2-daily-report` — L2 日看板
3. `l2-weekly-report` — L2 周看板
4. `l3-daily-report` — L3 日看板
5. `l3-weekly-report` — L3 周看板
6. `l3-monthly-report` — L3 月看板

## v1.7 核心架构
- 作业批改：`grading-data.json + crops/ + grading-report.html`
- 日报：`daily-data.json → validate → render_daily.py → HTML`
- 周报：`daily-data.json → aggregate_weekly_data.py → weekly-data.json → validate → render_weekly.py → HTML`
- 月报：`daily-data.json + 月测/路线/上月数据 → aggregate_monthly_data.py → monthly-data.json → validate → render_monthly.py → HTML`
- 周/月模板已彻底清除模拟学生和示例base64图片；模型不再在成品demo HTML上逐格替换。
- HTML只作为最终展示；JSON作为工作流之间的首选机器接口。详见 `core/data-pipeline-v1.7.md`。

## 部署
### ChatGPT
进入 `platforms/chatgpt/<工作流>/` 安装对应 `skill.zip`。

### 其他支持 System Prompt / Agent 的 AI
使用 `workflows/<工作流>/SYSTEM_PROMPT.md`，并让AI读取同目录的 `references/`、`assets/` 和 `scripts/`。

### 本地文件
推荐“一个学生 = 一个独立对话 + 一个本地学生文件夹”。严格遵守 `core/file-access-scope.md`。

## 数据安全
**禁止把任何真实学生资料提交到本仓库。** 姓名、成绩、日报、错题图片、家长信息、学校材料均只应存在受控本地/机构存储。

## 当前版本
- 工作流 / ChatGPT Skills：v1.7
- Source of Truth：v1.0
- 数据流水线：v1.7


### v1.7 任务截止日期
日报每个任务记录DDL；周报从日报JSON继承DDL并显示跨周待办/逾期状态。
