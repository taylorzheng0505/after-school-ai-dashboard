# L3 monthly intake and validation

## Source scope
Read `student-context.md` and `file-access-scope.md`. Determine the target month, filter the daily-report folder by date/file name, and read only matching L3 daily reports. Do not scan raw worksheets or the standalone wrong-question library.

## First intake prompt
好的。请确认要生成的月份。若本地日报文件夹可读取，我会只读取该月份的L3日报。另请提供或明确告诉我以下资料所在路径：

1）本月模拟测试/月测结果；
2）本月路线进度；
3）如需环比，上个月L3月报；首次月报可写“首月”；
4）本月特殊事项（长假、考试周、长期请假、课程调整等），没有写“无”。

其余月度数据我会从当月日报自动汇总，不需要重新总结，也不会扫描原始试卷或独立错题库。

## Critical/blocking
- Target-month daily source data are insufficient to reconstruct the month.
- Mock assessment status is unknown.
- Latest route/transition status is unknown; “本月无更新” is valid.

## Evidence-strength rules
- One isolated error: occurrence, not stable weakness.
- Repeated across multiple days/weeks: may enter the ability problem map.
- Intervention effect requires before/after evidence.
- Missing mock assessment: never infer a score from homework performance.
