# 部署速查 v1.7

## GitHub用途
GitHub只保存规则、模板、脚本和Skill，不保存学生真实数据。

## 一线推荐
- 一个学生一个独立对话，并绑定独立本地学生目录。
- 批改先用 `homework-grading-report`。
- 日报优先读取 `grading-data.json`。
- 周报优先读取目标周 `daily-data.json`。
- 月报优先读取目标月 `daily-data.json`；环比优先读取上月 `monthly-data.json`。
- 若对应JSON不存在，只允许读取同一日期/周期的HTML作为兼容回退，不得扩大扫描。

## v1.7 周报执行
1. 按目标周筛选 daily-data JSON；
2. `aggregate_weekly_data.py` 生成初步 `weekly-data.json`；
3. AI只补习惯总结、L3重复信号/下周重点等判断字段；
4. `validate_weekly_data.py`；
5. `render_weekly.py`；
6. `validate_visual.py`；
7. 输出最终自包含HTML。

## v1.7 月报执行
1. 按目标月筛选 L3 daily-data JSON；
2. 加入明确提供的月测、路线、上月比较数据；
3. `aggregate_monthly_data.py` 生成初步 `monthly-data.json`；
4. AI补趋势、能力地图、深度分析、干预效果、习惯、路线和下月重点；
5. `validate_monthly_data.py`；
6. `render_monthly.py`；
7. `validate_visual.py`。

## AI能力
1. 能读本地文件 + 执行脚本：推荐，完整执行v1.7。
2. 能读本地文件但不能执行脚本：可参考 schema 手工生成JSON/HTML，但稳定性和速度会下降。
3. 只能聊天：不适合机构长期标准化生产。


## v1.7 deadline field
Use daily/weekly workflow packages from v1.7 together so `tasks[].due_date` propagates correctly into weekly ongoing/carryover tracking.
