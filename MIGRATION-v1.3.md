# v1.3 GitHub 更新说明

如果仓库是从 v1.2 通过网页覆盖上传到 v1.3，上传新文件后请删除以下 6 个旧运行文件。v1.3 的周报/月报不再读取原始试卷，也不再执行裁图：

- `workflows/l2-weekly-report/references/cropping.md`
- `workflows/l2-weekly-report/scripts/safe_crop.py`
- `workflows/l3-weekly-report/references/cropping.md`
- `workflows/l3-weekly-report/scripts/safe_crop.py`
- `workflows/l3-monthly-report/references/cropping.md`
- `workflows/l3-monthly-report/scripts/safe_crop.py`

ChatGPT 的 `skill.zip` 已经完成对应删除，无需额外处理。
