# L3 monthly intake and validation v1.6

## First intake
请确认要生成的月份。若本地学生日报目录可读取，我会优先读取该月份的 L3 `daily-data.json`，不重复解析已有日报HTML；只有某日JSON缺失时才读取该日HTML作为兼容回退。

另外请提供或明确以下资料：
1）本月模拟测试/月测结果；
2）本月路线进度（无变化可写“无更新”）；
3）如需环比，优先提供上月 `monthly-data.json`，没有时可提供上月月报HTML；首次月报直接说明“首月”；
4）本月特殊事项。

其余执行、错题、听写、专项辅导和习惯原始数据从当月日报JSON自动聚合。

## Blocking gaps
- Target month is unknown.
- Mock assessment status is unknown.
- Latest route status/update is unknown.
- Source data are insufficient to reconstruct the target month.
