# 软件工程 Harness 与 AI Coding 能力建设

培训交付包 v1.0 · 2026-10-03。面向部门主管、资深开发者与无编码经验者，支撑培训赋能、日常答疑、项目指导和持续改进。

**开始使用：打开 [培训包入口 START_HERE.html](START_HERE.html)。** 可离线阅读；完整目录应保持在一起。正式试讲前按讲师手册检查演示环境。

## 已交付材料

| 用途 | 入口与产物 |
|---|---|
| 分层赋能 | [培训安排](training/README.md)；[主管 PPT：14 页](training/slides/manager.pptx)、[工程师 PPT：18 页](training/slides/engineer.pptx)、[新手 PPT：18 页](training/slides/beginner.pptx)；每页嵌入讲师备注 |
| 备课与学习 | [讲师手册与答案](讲师手册.html)、[学员手册](学习手册.html)；[三个小失败开篇](training/00-opening.md)、[6 项练习](training/exercises.md)、[7 张 AI 任务卡](training/ai-task-cards.md) |
| 端到端实践 | [案例运行说明](demo/README.md)、[源码](demo/app.py)、[需求与验收](docs/case/requirements.md)、[现场演示步骤](demo/WALKTHROUGH.md)、[故障演练](demo/labs/failure_lab.py) |
| 架构与运行约束 | [4A 架构及图源](docs/case/architecture.md)，另附 4 个 SVG；[部署对齐表](templates/deployment-alignment.md)、[DfX 矩阵](templates/dfx-matrix.md) |
| 答疑与项目指导 | [32 条 FAQ](faq/README.md)、[分层指南](docs/guides/README.md)、[导师流程](docs/guides/mentoring.md) |
| 客户、汇报与变更 | [客户场景基线](templates/scenario-baseline.md)、[周报/里程碑模板](templates/weekly-milestone.md)、[已填周报](docs/case/weekly-report-example.md)、[变更确认模板](templates/change-control.md)、[延期分析与沟通演练](docs/case/change-example.md) |
| 能力与成效 | [委派与评审](templates/task-review.md)、[能力考核与试点复盘](templates/capability-pilot.md) |
| 验证证据 | [总验证记录](evidence/VALIDATION.md)、[工程验证](evidence/demo/VALIDATION.md)、[浏览器演示](evidence/demo/BROWSER.md)、[课件检查](evidence/slides/QA.md) |

可填写模板共 7 份，均在 `templates/`。PPT、Markdown、JSON、SVG 与代码保留可编辑源；HTML 手册可查找与打印。

## 运行案例

在本项目根目录打开终端。使用部门准入且仍受维护的 Python 3；案例仅依赖标准库。Windows 入口见案例说明。

```bash
python3 demo/app.py --port 8765
```

浏览器访问 `http://127.0.0.1:8765`。示例为单会议室预约，含查看、建立、冲突处理、取消和 SQLite 持久化。只使用虚构信息；没有身份认证、审批或生产交付承诺。

```bash
python3 -m unittest discover -s demo/tests -v
python3 demo/labs/failure_lab.py
python3 demo/backup.py exercise
```

启动、停止、备份和恢复的完整说明见 [案例 README](demo/README.md)。不使用 AI 工具也能运行案例与工程检查。

## 项目维护

全量材料发布到 GitHub 的步骤见 [GitHub Pages 发布说明](docs/PUBLISH_GITHUB.md)。本地发布构建器会补齐网站首页、文档阅读页、全量目录和完整培训包下载；用户已确认账号 `baibo20260827`、仓库名 `ai-coding-training` 并允许全量公开，实际部署状态见 STATUS。

- [AGENTS.md](AGENTS.md)：长期工作约定与 AI 阅读入口。
- [建设方案](docs/PROJECT_PLAN.md)：目标、方法、交付台账和组织实施建议。
- [STATUS.md](STATUS.md)：实际状态、验证及下一步。
- [改进日志](docs/IMPROVEMENTS.md)：反馈、修改和效果验证。
- [材料维护与重建](scripts/README.md)：HTML、架构图、交付检查和压缩包的生成方式。

AGENTS.md 保存稳定原则。具体课程、案例、进度和反馈分别维护，修改时同步相关证据，避免把材料完成当作能力建设已经见效。

## 使用边界

本包已完成材料制作与本地工程验证，可进入试讲。真实客户场景、部门工具准入、人员投入、验收权限和实际日期仍需组织对齐；客户确认、真实试讲、能力提升和业务收益尚未取得。教学案例、估算和角色对话均有标注。

## 参考资料

- [OpenAI：AGENTS.md 项目指导](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [OpenAI：沙箱与访问边界](https://learn.chatgpt.com/docs/sandboxing)
- [The Open Group：业务、应用、数据、技术架构及关联](https://help.opengroup.org/hc/en-us/articles/32115987894930-How-the-ArchiMate-Language-and-the-TOGAF-Standard-Complement-Each-Other)
- [Python：HTTP 服务库及使用边界](https://docs.python.org/3/library/http.server.html)
- [Python：SQLite 接口](https://docs.python.org/3/library/sqlite3.html)
- [SQLite：事务](https://www.sqlite.org/lang_transaction.html)

资料支持机制与术语说明；组织流程、课程和演练由本项目针对当前需求设计。
