# Migration to v1.7

Update these four workflows together:
- `l2-daily-report`
- `l3-daily-report`
- `l2-weekly-report`
- `l3-weekly-report`

No change is required for `homework-grading-report` or `l3-monthly-report`.

## Data change
- Daily `tasks[]` adds `due_date` (`YYYY-MM-DD` or `null`).
- Weekly `ongoing_tasks[]` adds `due_date`, `status`, `deadline_state`, and `carryover_to_next_week`.
- L3 weekly adds the same ongoing/deadline section already used by the L2 base.

For older daily JSON without `due_date`, weekly aggregation remains readable but displays an unresolved DDL as `未明确`; supervisors should supply the DDL for still-active long-cycle tasks when available.
