# L2 weekly intake and validation v1.6

## First intake
请确认要生成的周报日期范围。若本地学生日报目录可读取，我会优先读取这一周对应的 `daily-data.json`，不再重复解析日报HTML；若某天没有JSON，才读取该日HTML作为兼容回退。

若某个原本应到校的日期没有任何日报资料，请说明：A 未到校/请假；B 节假日/机构不营业；C 日报缺失。除此之外无需重新总结本周数据。周报会直接继承日报任务的截止日期，并自动列出周末仍未完成、需要延续到下周或已经逾期的任务；若旧日报中某个未完成长期任务没有DDL，才会定向询问。

## Blocking gaps
- Requested week is unknown.
- Student/date mismatch.
- An expected attendance day has unknown status and no source record.
- A week-end unresolved long-cycle task has no resolvable deadline in the daily data; ask once for the DDL, then show “未明确” if genuinely unavailable.

Do not ask the supervisor to manually calculate totals that can be aggregated from daily data.
