# 课后托管 AI 看板工作流

> L2 / L3 家长看板统一规则、固定 HTML 模板、跨 AI 工作流与 ChatGPT Skills 的内部版本库。

## 这个仓库存什么

- `core/`：机构统一规则。产品规则变更时先改这里。
- `workflows/`：5 个平台无关工作流，每个目录含 `SYSTEM_PROMPT.md`、规则、锁定 HTML 模板和必要脚本。
- `platforms/chatgpt/`：可直接安装到 ChatGPT 的 5 个 `skill.zip`（当前 v1.3）。
- `student-folder-template/`：本地学生资料目录结构示例，仅用于复制到本地，不存真实学生数据。

## 五个工作流

1. `l2-daily-report` — L2 日看板
2. `l2-weekly-report` — L2 周看板
3. `l3-daily-report` — L3 日看板
4. `l3-weekly-report` — L3 周看板
5. `l3-monthly-report` — L3 月看板

## 给不同 AI 产品部署

### A. ChatGPT
进入 `platforms/chatgpt/<工作流>/`，安装对应 `skill.zip`。

### B. 支持 System Prompt / Agent / Project Instructions 的其他 AI
将对应 `workflows/<工作流>/SYSTEM_PROMPT.md` 作为系统指令，并让 AI 访问该工作流目录中明确引用的 `references/`、`assets/` 和必要 `scripts/`。

### C. 支持读取本地文件的 AI
建议“一个学生 = 一个独立对话 + 一个本地学生文件夹”。必须遵守 `core/file-access-scope.md`，不要让AI扫描整个学生工作区。

## v1.3 关键运行逻辑

- 日报：稳定档案 + 最近一份日报中的长期任务 + 督导明确指定的今日原始作业/试卷 + 督导提供的本次批改结果 + 今日执行信息。
- 批改结果来源不限；已存在且能对应今日材料时不重复批改。
- 日报整页原始作业中一旦确认错题，**必须逐题裁剪**；整页嵌入只能作为裁剪技术失败的异常兜底。
- 周报：只读取指定周内日报，不扫描原始试卷/独立错题库，不重新裁图。
- 月报：只读取指定月内日报 + 月测/路线资料 + 必要时上月月报，不扫描原始试卷/独立错题库，不重新裁图。
- 页面视觉必须以固定 HTML 模板为底稿，禁止重新设计。
- L2 不做错因和能力诊断。
- L3 周专项辅导：Math 2×30min + English 2×30min，当周完成，不结转。
- 不得把跨对话记忆作为学生报告事实来源。

## 数据安全

**禁止把任何真实学生资料提交到本仓库。** 包括姓名、成绩、日报、错题图片、家长信息、学校材料等。本仓库只保存规则、模板、脚本和空目录规范。

## 更新顺序

`core/source-of-truth` → 运行/交互规则 → workflow → 平台适配包 → 测试 → 发布新版本

## 当前版本

- 工作流/ChatGPT Skills：v1.3
- Source of Truth：v1.0
- 文件读取范围：v1.3
