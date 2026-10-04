# 软件工程 Harness 与 AI Coding 自学指南

自学版 v1.1 · 2026-10-04。面向部门主管、资深开发者与无编码经验者，用阅读、动手练习和自检建立软件交付能力。按自己的问题选择路径，随时查阅 FAQ 和工作模板。

**[打开在线自学网站](https://baibo20260827.github.io/ai-coding-training/)** · [下载完整自学包](https://baibo20260827.github.io/ai-coding-training/downloads/harness-ai-coding-training-v1.1.zip) · [GitHub 仓库](https://github.com/baibo20260827/ai-coding-training)。离线解压后打开 [START_HERE.html](START_HERE.html)，保持目录结构。

## 从哪里开始

先读 [三个小失败](training/00-opening.md)，再选择路径。PPT 提供概览，指南解释具体做法，练习用来检验能否实际完成。

| 你的起点 | 阅读与实践顺序 | 完成后应留下的结果 |
|---|---|---|
| 部门主管 | [主管指南](docs/guides/manager.md) → 客户场景与验收 → 阶段进度 → 变更与资源；[主管 PPT](training/slides/manager.pptx) | 一份需求基线、阶段报告与有依据的变更方案；完成 L1/L5/L6 |
| 资深开发者 | [工程师指南](docs/guides/engineer.md) → 运行案例 → 独立验收 → 差异审查与小变更；[工程师 PPT](training/slides/engineer.pptx) | 任务边界、检查结果、审查与恢复记录；完成 L2/L3/L4 |
| 无编码经验者 | [新手指南](docs/guides/beginner.md) → 输入与结果 → 验收例子 → 操作案例 → 尝试小变更；[新手 PPT](training/slides/beginner.pptx) | 一个可执行的小需求、操作结果和清楚的问题描述；完成 L1/L2，进阶 L4 可先做需求与验收 |

准备条件、分步路线和完成标准见 [自学入口](training/README.md)。需要帮助时，先按 [问题排查与协作求助](docs/guides/mentoring.md)整理预期、实际结果和已做检查。

## 随时可查的材料

| 用途 | 入口 |
|---|---|
| 连续阅读 | [自主学习手册](学习手册.html)、[自学实践指南](training/facilitator-guide.md) |
| 动手与自检 | [6 项练习](training/exercises.md)、[参考解析与自检](参考解析.html)、[7 张 AI 任务卡](training/ai-task-cards.md) |
| 端到端案例 | [运行说明](demo/README.md)、[分步实践](demo/WALKTHROUGH.md)、[需求与验收](docs/case/requirements.md)、[故障练习](demo/labs/failure_lab.py) |
| 架构与运行约束 | [4A 架构及图源](docs/case/architecture.md)、[部署对齐表](templates/deployment-alignment.md)、[DfX 矩阵](templates/dfx-matrix.md) |
| 日常答疑 | [32 条 FAQ](faq/README.md)、[分层指南](docs/guides/README.md) |
| 客户、进度与变更 | [场景基线](templates/scenario-baseline.md)、[阶段报告模板](templates/weekly-milestone.md)、[已填报告](docs/case/weekly-report-example.md)、[变更模板](templates/change-control.md)、[变更与延期实例](docs/case/change-example.md) |
| 独立实践与复盘 | [任务与评审](templates/task-review.md)、[能力自评与实践记录](templates/capability-pilot.md) |

三套 PPT 共 50 页，附逐页阅读补充；7 份工作模板、Markdown、JSON、SVG 和案例代码保留可编辑源。先独立尝试练习，再对照参考解析；能处理一个没有原样练过的问题，才有进一步判断掌握程度的依据。

## 运行案例

下载并解压材料，或克隆仓库。在项目根目录打开终端，使用部门准入且仍受维护的 Python 3：

```bash
python3 demo/app.py --port 8765
```

浏览器访问 `http://127.0.0.1:8765`。案例只依赖 Python 标准库，使用 SQLite 保存预约，支持查看、建立、冲突处理和取消。按 [分步实践](demo/WALKTHROUGH.md)检查刷新保留、相邻允许、重叠拒绝和取消后重约。

```bash
python3 -m unittest discover -s demo/tests -v
python3 demo/labs/failure_lab.py
python3 demo/backup.py exercise
```

Windows 启动、停止、备份与恢复方法见 [运行说明](demo/README.md)。没有 AI 工具也可以运行案例和检查。GitHub Pages 提供静态阅读与下载，预约后端需要在本机启动。

## 维护与持续改进

- [AGENTS.md](AGENTS.md)：长期工作原则，默认直接面向自学者写作。
- [建设方案](docs/PROJECT_PLAN.md)：能力目标、材料范围和实践建议。
- [STATUS.md](STATUS.md)：实际状态、证据和后续实践。
- [改进日志](docs/IMPROVEMENTS.md)：反馈、修改与验证。
- [材料重建](scripts/README.md)、[GitHub 发布说明](docs/PUBLISH_GITHUB.md)：维护方法。
- [验证记录](evidence/VALIDATION.md)：工程、文件和阅读检查的范围与限制。

记录哪里看不懂、哪一步做不出、哪个检查发现问题，保留实际结果后修订材料。材料制作完成不等于已经取得人员能力提升或业务收益。

## 使用边界

案例、估算和角色均为虚构学习素材。真实项目仍需确认客户场景、工具准入、部署约束、验收权限和日期；学习者的自检不能替代业务验收与技术评审。预约案例没有身份认证、审批或生产交付承诺。

## 参考资料

- [OpenAI：AGENTS.md 项目指导](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [OpenAI：沙箱与访问边界](https://learn.chatgpt.com/docs/sandboxing)
- [The Open Group：业务、应用、数据、技术架构及关联](https://help.opengroup.org/hc/en-us/articles/32115987894930-How-the-ArchiMate-Language-and-the-TOGAF-Standard-Complement-Each-Other)
- [Python：HTTP 服务库及使用边界](https://docs.python.org/3/library/http.server.html)
- [Python：SQLite 接口](https://docs.python.org/3/library/sqlite3.html)
- [SQLite：事务](https://www.sqlite.org/lang_transaction.html)
