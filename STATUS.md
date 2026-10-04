# 当前状态

更新时间：2026-10-04。材料版本：自学版 v1.1。

## 当前使用方式

以自主阅读、动手实践和对照自检为主。首页先呈现三类读者的困难与小失败，再给出学习路径和分步任务。按自己需要选择一条路径，保存实际结果，遇到问题查解析、FAQ 或整理信息求助。

在线入口：[AI Coding 自学网站](https://baibo20260827.github.io/ai-coding-training/)；源材料：[GitHub 仓库](https://github.com/baibo20260827/ai-coding-training)。离线解压后打开 [START_HERE.html](START_HERE.html)。

| 内容 | 状态与用途 | 入口 |
|---|---|---|
| 三类路径与开篇 | 主管、资深开发者、新手；保留虚构小失败，提供阅读顺序、产出、自检和排查入口 | [自学路线](training/README.md) |
| 文档与实践 | 自主学习手册、参考解析、6 项练习、7 张任务卡 | [学习手册](学习手册.html)、[参考解析](参考解析.html) |
| PPT | 三套 14/18/18 页，可编辑，附逐页阅读补充 | [PPT 说明](training/slides/README.md) |
| 客户、进度与变更 | 需求基线、阶段报告、系统变更与延期分析、可复用工作模板 | [需求](docs/case/requirements.md)、[变更](docs/case/change-example.md) |
| 4A、部署与 DfX | 四类架构文档及可编辑图源、4 SVG；部署和 DfX 保持简要 | [架构](docs/case/architecture.md)、[模板](templates/dfx-matrix.md) |
| 查阅与协作 | 32 条 FAQ、三类指南、问题排查与协作求助 | [FAQ](faq/README.md)、[求助](docs/guides/mentoring.md) |
| 本地案例 | Python 标准库 + SQLite，提供运行、验收、故障练习和备份恢复说明 | [运行说明](demo/README.md)、[分步实践](demo/WALKTHROUGH.md) |
| 自学版修订检查 | 记录本轮文字、生成文件、页面与发布检查 | [本轮检查](evidence/SELF_STUDY.md) |
| 既有工程证据 | v1.0 保留故障/恢复和应用浏览器证据；本轮仅调整一条错误提示，现有 21 项测试再次通过 | [工程验证](evidence/demo/VALIDATION.md) |
| 真实学习与业务效果 | 尚无本部门真实独立实践、客户接受或收益数据 | [实践记录](templates/capability-pilot.md) |

## 本次反馈的落实

去除讲师台词、课堂组织、举手互动和固定授课时长。直接说明操作、预期结果与完成标准；PPT 备注用于补充解释。原讲师手册地址继续提供参考解析，旧下载链接保留兼容，便于已分享的材料继续访问。

长期写作规则已写入 [AGENTS.md](AGENTS.md)，改进来源和范围见 [I-012](docs/IMPROVEMENTS.md)。客户确认、技术把关与变更审批仍由相应责任人完成，自学自检不替代实际项目职责。

## 发布与维护

Pages 使用 `main` 分支根目录并强制 HTTPS。首次发布和历次检查分别记录在 [发布证据](evidence/publishing/VALIDATION.md)及 [自学版检查](evidence/SELF_STUDY.md)。源材料修改后依次重建手册、完整学习包和网站；如改动 PPT，需同步重建课件。方法见 [材料维护](scripts/README.md)与 [发布说明](docs/PUBLISH_GITHUB.md)。

## 后续实践

1. 选择一条学习路径，按准备条件运行或阅读案例。
2. 保存练习结果，对照解析标明独立完成、协助完成和尚未完成的部分。
3. 尝试一个没有原样练过的小任务，记录卡点与检查证据。
4. 在真实项目中确认客户、环境、验收责任人与当前基线，再使用工作模板。
5. 根据实践问题修订材料与工作约定，观察是否减少重复卡点。

上述行动按个人与团队实际情况安排，没有自动建立日程或对外承诺。
