# 分层自学课件

自学版 v1.1，2026-10-04。三套课件可以独立阅读，配有逐页解释、操作任务与自检标准。按自己的节奏完成，不设固定学习时长。

| 受众 | 可编辑课件 | 逐页阅读补充 | 完成证明 |
|---|---|---|---|
| 部门主管 | [manager.pptx](manager.pptx)，14 页 | [manager-notes.md](manager-notes.md) | 一份有证据和前提的交付决策 |
| 资深开发者 | [engineer.pptx](engineer.pptx)，18 页 | [engineer-notes.md](engineer-notes.md) | 一次有边界的修改、故障定位及实际验证 |
| 无编码经验者 | [beginner.pptx](beginner.pptx)，18 页 | [beginner-notes.md](beginner-notes.md) | 场景卡与正常/异常验收记录；小变更为进阶 |

## 怎样自学

1. 阅读每套第 2—4 页的三个虚构小失败，先自行判断缺少哪些依据，再查看对应阅读补充。
2. 主管继续学习场景、验收、4A、报告与变更决策。工程师在理解任务边界后运行故障、测试与恢复实验。新手先认识软件组成，再启动应用并逐项验收。
3. 每页先看主要概念，再打开同页阅读补充，其中说明原理、具体操作与自检依据。相同内容也保存在 PPTX 的备注区。
4. 完成独立练习，记录真实结果，再对照参考解析。遇到不确定的业务或技术影响，保留具体问题并请求对应负责人复核。

完整学习路径、练习与参考资料见 [学习总索引](../README.md)。共同案例说明见 [三个小失败](../00-opening.md)。应用准备和命令以 [案例运行说明](../../demo/README.md) 为准。

课件没有预填客户接受、真实学习反馈或生产成效数字。审批与午休禁约属于新增练习，基线应用尚未实现。材料可阅读、能够完成独立任务、真实客户接受，是需要分别验证的结果。

## 内容维护

[source/content.json](source/content.json) 保存正文、逐页阅读补充、官方资料链接及共同案例。[source/build.mjs](source/build.mjs) 使用 `@oai/artifact-tool` JavaScript ES modules 构建可编辑 PPTX。原生文本、表格和 4A 图均可继续编辑。

修改后核对需求编号、案例规则、架构、实现、命令与阅读材料的一致性。`decks[].expectedCount` 包含封面和共同案例。正文采用 Arial Unicode MS，主要标题 33 pt，封面标题 49.5 pt，表格正文 18 pt，其余正文至少 17.25 pt，页码使用辅助字号。

## 重建

在项目根目录执行，使用当前 Codex 提供的捆绑运行时。换环境时先通过 `load_workspace_dependencies` 定位 Node.js、Python 和 Node packages，再设置 `RUNTIME_NODE_MODULES`、`RUNTIME_PYTHON`、`PRESENTATIONS_SKILL_DIR`。

```bash
mkdir -p evidence/slides/build
ln -s /Users/baibo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules evidence/slides/build/node_modules
cp training/slides/source/build.mjs evidence/slides/build/build.mjs
SLIDE_REVISION=selfstudy-v1.1-r5 /Users/baibo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node evidence/slides/build/build.mjs
```

若链接已存在，确认目标正确后跳过 `ln -s`。每次重建使用新的 `SLIDE_REVISION`。构建器先在 `evidence/slides/finalized/` 生成已校验版本，再将相同字节复制到三个固定交付文件名，并同步阅读补充。`DECK_ID=manager`、`engineer` 或 `beginner` 可只构建一套。

使用 AI 编辑时，仍应遵循当前 presentations 技能的操作标记和验证要求。构建脚本不代替逐页视觉检查。

```bash
/Users/baibo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 evidence/slides/inspect_submission.py
```

检查范围见 [课件验证记录](../../evidence/slides/QA.md)。当前使用 Artifact Tool 对最终 PPTX 重新导入并渲染，未在 PowerPoint 或 Google Slides 中进行应用级操作检查。
