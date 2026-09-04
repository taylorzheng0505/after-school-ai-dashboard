# v1.6 升级说明

## 需要更新的 ChatGPT Skills
- `l2-weekly-report`
- `l3-weekly-report`
- `l3-monthly-report`

L2/L3日报与作业批改继续使用v1.5逻辑，无需本次重装。

## 主要变化
- 删除周/月旧式 `clone_template.py + LLM直接改demo HTML` 流程。
- 新增周/月 JSON schema、聚合器、数据validator和renderer。
- 周/月模板变为空壳模板，不再包含Alex、固定时长、固定成绩、示例错题图等demo。
- 下游优先读取JSON而非HTML。

## 升级方式
对已安装Skill：删除旧版对应Skill，再安装v1.6完整 `skill.zip`，避免旧脚本残留。

对GitHub本地仓库：用v1.6完整仓库覆盖本地目录，GitHub Desktop会自动识别新增/删除/修改，然后 Commit + Push。
