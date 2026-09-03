# 课后托管 AI 看板工作流

> L2 / L3 家长看板统一规则、固定 HTML 模板、跨 AI 工作流与 ChatGPT Skills 的内部版本库。

## 这个仓库存什么

- `core/`：机构统一规则。产品规则变更时先改这里。
- `workflows/`：6 个平台无关工作流，每个目录含 `SYSTEM_PROMPT.md`、规则、锁定 HTML 模板和必要脚本。
- `platforms/chatgpt/`：可直接安装到 ChatGPT 的 6 个 `skill.zip`（当前运行版 v1.5；周/月未改动部分沿用v1.3逻辑）。
- `student-folder-template/`：本地学生资料目录结构示例，仅用于复制到本地，不存真实学生数据。

## 六个工作流

1. `homework-grading-report` — 跨学科作业批改与标准批改报告
2. `l2-daily-report` — L2 日看板
3. `l2-weekly-report` — L2 周看板
4. `l3-daily-report` — L3 日看板
5. `l3-weekly-report` — L3 周看板
6. `l3-monthly-report` — L3 月看板

## 给不同 AI 产品部署

### A. ChatGPT
进入 `platforms/chatgpt/<工作流>/`，安装对应 `skill.zip`。

### B. 支持 System Prompt / Agent / Project Instructions 的其他 AI
将对应 `workflows/<工作流>/SYSTEM_PROMPT.md` 作为系统指令，并让 AI 访问该工作流目录中明确引用的 `references/`、`assets/` 和必要 `scripts/`。

### C. 支持读取本地文件的 AI
建议“一个学生 = 一个独立对话 + 一个本地学生文件夹”。必须遵守 `core/file-access-scope.md`，不要让AI扫描整个学生工作区。

## v1.5 关键运行逻辑

- `homework-grading-report` 固定输出 `grading-data.json + crops/ + grading-report.html`。
- `grading-report.html` 仍是完整自包含的人看报告；`grading-data.json` 才是日报机器接口。
- L2/L3日报优先读取轻量 `grading-data.json`，只引用其中明确列出的错题裁图路径，不再正常解析带base64图片的重型批改HTML。
- L2/L3日报先生成小型 `daily-data.json`，最终由 `render_daily.py` 读取图片文件并嵌入家长HTML；模型不再手动搬运base64。
- 日报固定HTML模板已去除示例base64图片，从约260KB降至约8KB，视觉CSS/两题一行布局保持不变。
- 没有标准批改包的听写、临时小测等仍保留日报自主裁图能力。
- 日报继续读取最近一份日报中的未完成长期任务，其他当日事实保持 Fresh-State。
- 周报/月报仍按 v1.3 白名单读取日报，不扫描原始试卷或独立错题库。

## 数据安全

**禁止把任何真实学生资料提交到本仓库。** 包括姓名、成绩、日报、错题图片、家长信息、学校材料等。本仓库只保存规则、模板、脚本和空目录规范。

## 更新顺序

`core/source-of-truth` → 运行/交互规则 → workflow → 平台适配包 → 测试 → 发布新版本

## 当前版本

- 工作流/ChatGPT Skills：v1.5
- Source of Truth：v1.0
- 文件读取范围：v1.5
