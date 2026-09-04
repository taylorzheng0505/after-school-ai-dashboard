# 数据驱动看板流水线 v1.6

从 v1.6 起，所有高频看板工作流采用“结构化数据 → 校验 → 固定渲染器 → HTML”的统一架构。

```text
原始作业
  ↓
homework-grading-report
  ├─ grading-data.json   # 机器接口
  ├─ crops/              # 错题证据
  └─ grading-report.html # 人看
        ↓
L2/L3 daily
  ├─ daily-data.json
  └─ daily-report.html
        ↓
L2/L3 weekly
  ├─ weekly-data.json
  └─ weekly-report.html
        ↓
L3 monthly
  ├─ monthly-data.json
  └─ monthly-report.html
```

## 原则
1. HTML 是展示件，不是首选机器接口。
2. 下游优先读取上游 JSON；只有JSON缺失时才解析对应HTML。
3. 模型负责事实理解与需要判断的摘要；确定性统计、HTML拼装、图片base64嵌入交给脚本。
4. 模板只保留 CSS / JS / 占位符，不存任何学生 demo。
5. 生成前先校验 JSON，生成后再校验视觉结构。
6. 周/月不回到原始试卷或独立错题库重新分析。

## Deadline propagation v1.7
`daily-data.json.tasks[]` now carries `due_date` for every task. Weekly aggregation inherits the DDL and creates `ongoing_tasks[]` with `deadline_state` and `carryover_to_next_week`.

This creates the machine-readable chain:

`task due_date (daily) -> weekly ongoing_tasks deadline -> next-week continuation / overdue visibility`

Do not infer or rewrite long-cycle deadlines at the weekly layer.
