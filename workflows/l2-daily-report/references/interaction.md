# L2 daily intake and validation

## Before intake
Read `student-context.md` and `file-access-scope.md`. Reuse stable profile fields. Read only the single latest prior daily report for unfinished long-cycle tasks; if such tasks exist and today's progress is not supplied, ask what happened today.

## First intake prompt
好的。请一次性把今天的信息发给我，文字、截图、文件路径、作业照片都可以，不需要整理成表格。

1）学生与时间：姓名/年级/路线如已在当前学生档案中明确可不重复；请确认今天日期、到校、离校、有效学习时长。
2）今日任务：今天所有任务及完成/推进情况。长期任务如果上一份日报仍未结束，我会读取上一份日报并请你确认今天推进到哪里。
3）今日原始作业/试卷：请直接上传，或告诉我今天原始作业/试卷所在的明确文件或文件夹路径。
4）本次批改结果：如果已经由你、其他AI或前序步骤批改，请直接给我文字、截图或文件；只要能明确对应今天这批原始作业即可。如果还没批改并希望我批改，也可以直接说明。
5）错题订正：请说明已确认错题是否已经答疑/订正；听写错误同理。
6）学习过程与习惯：请给1–3条今天真实看到的行为，不要只写“认真/努力”。
7）其他情况：迟到、早退、材料缺失、特殊安排等；没有写“无”。

如果原始材料是整页作业，只要批改结果确认了错题，我会逐题裁剪错题证据后再生成日报，不会把整页作业直接当成单题错题图。

## Critical/blocking
- Student identity/date cannot be reliably resolved.
- Arrival/departure/effective-study data are materially missing.
- Today's tasks/status are too vague.
- Grading result is missing and neither the supervisor nor this AI has established which questions are wrong.
- Confirmed wrong questions cannot be mapped back to the supplied/identified source page.
- Correction status is missing for reported errors.
- Habit note is absent or only vague praise.
