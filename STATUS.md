# 当前状态

更新时间：2026-10-04。版本：培训交付包 v1.0。

## 当前阶段

全套培训材料和教学工程已完成，全量学习站已公开发布，进入试讲准备。材料完成、网站发布、工程验证、真实学习效果与客户接受分别记录。

| 工作 | 实际状态 | 证据或入口 |
|---|---|---|
| 三类开篇与分层课件 | 3 套 50 页，含逐页讲师备注与可编辑源 | [课件](training/slides/README.md) |
| 学习与授课 | 离线学员/讲师手册、6 项练习、参考答案、7 张任务卡已形成 | [课程安排](training/README.md) |
| 客户需求与架构 | 教学需求基线 A01—A08，4A 文档/图源/4 SVG 已形成 | [需求](docs/case/requirements.md)、[架构](docs/case/architecture.md) |
| 部署与 DfX | 简要对齐清单、规划/沟通/交付矩阵已形成 | [部署](templates/deployment-alignment.md)、[DfX](templates/dfx-matrix.md) |
| 答疑与项目指导 | 分层指南、导师流程、32 条 FAQ、7 份可填写模板 | [指南](docs/guides/README.md)、[FAQ](faq/README.md) |
| 进度、变更、延期 | 周报及变更模板、已填演练和对外沟通草稿已形成 | [周报](docs/case/weekly-report-example.md)、[变更](docs/case/change-example.md) |
| 教学应用 | Python 标准库 + SQLite，本地可运行；含故障演练和备份恢复 | [案例](demo/README.md) |
| 自动工程检查 | 21/21 通过；故障/备份恢复演练通过 | [工程验证](evidence/demo/VALIDATION.md) |
| 浏览器端到端检查 | 已验证创建、刷新保留、相邻允许、重叠拒绝、取消/重约、停服提示及重启持久化 | [浏览器证据](evidence/demo/BROWSER.md) |
| PPT 检查 | 50 页渲染和逐页视觉检查通过，文件结构与备注检查通过 | [课件验证](evidence/slides/QA.md) |
| 全量学习站 | 已公开发布；21 项公网 HTTPS GET 与完整文件 SHA-256 比对通过 | [在线学习站](https://baibo20260827.github.io/ai-coding-training/)、[发布证据](evidence/publishing/VALIDATION.md) |
| 真实试讲与能力考核 | 尚未实施，需要团队参与 | [考核与试点模板](templates/capability-pilot.md) |
| 真实客户确认与收益 | 尚未取得，不以教学假设代替 | [建设方案](docs/PROJECT_PLAN.md) |

在线入口：[AI Coding 学习站](https://baibo20260827.github.io/ai-coding-training/)；离线入口：[START_HERE.html](START_HERE.html)。综合验证及限制见 [验证记录](evidence/VALIDATION.md)，网站检查范围见 [发布记录](evidence/publishing/VALIDATION.md)。

## 已处理的问题

- 取消预约改为页面内二次确认，已复核保留、取消和重约。
- 午休变更练习补充测试适配原则：原合法输入因新需求失效时，保留检查目的并调整输入，记录需求依据。
- 课时统一为主管 75 分钟、工程师 150 分钟、新手 150 分钟；实际节奏待试讲。
- 架构数据字段、并发机制、课件与运行代码已交叉核对。

## 下一步：组织使用

全量学习材料已发布到 [baibo20260827/ai-coding-training](https://github.com/baibo20260827/ai-coding-training)。用户已明确授权公开全部材料；Pages 使用 `main` 分支根目录并强制 HTTPS。首次成功部署提交为 `4127fae44ac515a91f5f463729e13a636adcab0f`，GitHub 构建状态为 `built`，构建更新时间为 2026-10-04 12:12:06（上海）。21 项公网文件检查于同日 12:12:54 通过，具体范围见 [发布检查](evidence/publishing/VALIDATION.md)。本地构建输出继续保存在 `dist/github-pages/` 和 `dist/github-pages-full.zip`；更新方法见 [发布说明](docs/PUBLISH_GITHUB.md)。预约应用保留源码下载与本地运行方式，真实试讲、客户接受和收益仍待取得。

1. 用真实访谈校准三类受众的困难；确定讲师、种子导师、参加者和试讲时间。
2. 确认部门工具准入及参与者本地环境，讲师按清单先完整运行一次。
3. 按分层课程试讲，记录练习结果、疑问、实际用时和独立完成新任务的情况。
4. 选取低风险真实场景，填写客户基线、部署与 DfX 约束、验收人、资源和里程碑。
5. 用试点证据修订材料与工作约定，再决定扩大范围；保留基线和变化理由。

以上为建议执行顺序，尚未创建定时任务、安排会议或向客户发送沟通草稿。
