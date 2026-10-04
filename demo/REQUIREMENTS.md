# 会议室预约需求与验收追踪

版本：1.0，2026-10-03。性质：教学基线，非客户已批准需求。实际客户、验收人、日期与环境待真实项目确认。

教学目标：让学员能够将“预约一个会议室”变成可验证的行为，用独立证据判断实现，再处理变更和恢复。主要使用者为演示同事；讲师承担演练组织，学员承担观察和复核。

## 需求、验收与证据

| 需求 / 验收 | 场景与成功条件 | 实现位置 | 自动检查 / 人工检查 |
|---|---|---|---|
| R01 / A01 查看 | 指定有效日期时只显示该日预约，按开始时间排序；空列表有提示 | `BookingStore.list_bookings`、GET 接口、页面列表 | `test_R01_empty_and_date_filtered_order`；`test_R01_static_assets_and_health`；浏览器更换日期 |
| R02 / A02 建立预约 | 有效输入返回 ID、日期、时段、姓名、主题，并能在列表中找到 | `validate_booking`、`create_booking`、POST 接口、表单 | `test_R02_create_returns_saved_fields`；HTTP 创建读取测试 |
| R03 / A03 相邻与冲突 | 已有 10:00–11:00；11:00–12:00 允许，10:30–11:30 拒绝且不残留部分写入 | `slots` 主键、事务、409 反馈 | `test_R03_adjacent_on_both_sides_allowed`、`test_R03_overlap_variations_rejected_and_no_partial_rows`、HTTP 冲突测试；故障演练 |
| R04 / A04 取消 | 取消后列表不再出现该预约，可重新预约原时段；重复取消明确告知不存在 | 外键 `ON DELETE CASCADE`、DELETE 接口、页面确认 | `test_R04_cancel_releases_slots_and_missing_is_false`；HTTP 创建取消测试 |
| R05 / A05 持久化 | 成功预约在刷新或服务重启后仍存在；取消也持久化 | SQLite 文件与重新查询 | `test_R05_reopen_preserves_booking_and_cancel`；HTTP 重新连接；浏览器刷新与 CLI 重启步骤 |
| R06 / A06 输入边界 | 09:00–18:00，30 分钟粒度，结束晚于开始；日期有效，姓名1–30字、主题1–80字，非法请求无写入 | `validate_date`、`parse_time`、`validate_booking`、参数化SQL、页面 `textContent` | `test_R06_*`：非法输入、边界、文本作为数据；人工检查提示易懂 |
| R07 / A07 本地边界 | 仅回环地址；限制 Host/跨站写入；页面明确虚构数据、无登录、可取消全部记录 | `make_server`、Host/Origin检查、页面标识 | `test_R07_bind_loopback_origin_and_host_guards`；人工检查教学标识；不等于全面安全评估 |
| R08 / A08 同时预约一致性 | 同日同一时段并发竞争最多一条成功，其他收到冲突；相邻并发均可成功 | 独立连接、`BEGIN IMMEDIATE`、唯一时段约束 | `test_R08_simultaneous_identical_requests_exactly_one_success`、相邻并发测试、HTTP 并发测试 |

完整测试命名与逻辑见 [test_app.py](tests/test_app.py)。数据文件保护、备份恢复是案例交付支持检查，见 `test_backup_restore_new_path_and_refuse_overwrite` 与 `test_unrelated_database_is_not_adopted`。

R06 的字符数按 Python 字符串长度计数；不处理姓名真实性。默认主题只是虚构示例。R07 的本地边界不提供业务身份与授权；需要客户权限管理时属于新的需求设计。

## 数据及边界

| 数据 | 字段 | 关系与用途 |
|---|---|---|
| `bookings` | `id`、`day`、`start_minute`、`end_minute`、`name`、`purpose` | 一条业务预约；ID 为随机 UUID 十六进制串 |
| `slots` | `day`、`start_minute`、`booking_id` | 每个占用半小时一行；`(day,start_minute)` 唯一；多行属于一个预约 |

每天起止边界为 `[09:00,18:00)`，如 17:30–18:00 可预约。预约不跨日，日期不做服务器时区换算。所有环境均为本地教学，允许不同日期使用同一时间段。

## 变更练习与基线隔离

- “午休 12:00–13:00 不可预约”：用于未原样讲过的小变更考核，需要补边界用例和回归；不属于当前已实现基线。
- “增加主管审批”：用于管理者影响分析与延期沟通，不属于当前应用功能。需要重新确定业务、角色、数据状态、架构和验收条件。
- 任何范围扩展都先登记需求差异，再更新验收、设计、实现、检查和相关材料。不得仅因 AI 改写测试预期就认为基线已经变化。

## 验收记录使用方式

自动检查实际结果见 [工程验证记录](../evidence/demo/VALIDATION.md)。讲师还应填写日期、环境、操作者、步骤、观察结果和证据位置；客户接受、学员独立能力与真实业务收益分别留待相应人员确认。不要将本表存在视作所有验收已完成。
