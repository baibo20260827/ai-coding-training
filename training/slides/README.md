# 分层培训课件

版本 1.0，2026-10-03。用于培训赋能、案例演示与讨论。授课时长为建议，真实试讲与学习效果尚待验证。

| 受众 | 课件 | 逐页讲师备注 | 建议安排 |
|---|---|---|---|
| 部门主管 | [manager.pptx](manager.pptx)，14 页 | [manager-notes.md](manager-notes.md) | 整课 75 分钟 |
| 资深开发者 | [engineer.pptx](engineer.pptx)，18 页 | [engineer-notes.md](engineer-notes.md) | 整课 150 分钟 |
| 无编码经验者 | [beginner.pptx](beginner.pptx)，18 页 | [beginner-notes.md](beginner-notes.md) | 整课 150 分钟 |

整课包含环境准备、共同开篇、讲解操作、练习及反馈，具体安排以 [培训总索引](../README.md) 为准。备注中的逐页时间是讲师节奏参考，不代替整课排期。

每套第 2—4 页为共同开篇的三个虚构小失败。完整开篇材料见 [00-opening.md](../00-opening.md)。讲师备注同时嵌入 PPTX，包含用时建议、讲解要点、提问、演示节点、边界及适用的官方资料链接。原生文本、表格与 4A 图可继续编辑。

先按案例运行说明准备本地环境，在授课时运行真实命令并展示真实结果。课件没有预填任何客户接受、真实培训反馈或生产成效数字。审批与午休禁约都是新增变更练习，基线应用尚未实现。

## 内容维护

[source/content.json](source/content.json) 保存三套课件文字、备注、来源及共同开篇。[source/build.mjs](source/build.mjs) 使用 `@oai/artifact-tool` JavaScript ES modules 构建可编辑 PPTX。

修改内容后，检查需求编号、案例规则、4A、代码、命令和讲师手册是否一致。`decks[].expectedCount` 是总页数，包含封面和共同开篇。受众色分别为青绿、蓝色与棕色。正文采用 Arial Unicode MS，主要标题 33 pt，封面标题 49.5 pt，表格正文 18 pt，其余正文至少 17.25 pt，页码为辅助字号。

## 重建

在项目根目录执行。使用当前 Codex 提供的捆绑运行时，不安装替代依赖。以下路径对应本次制作环境。若换环境，先通过 `load_workspace_dependencies` 重新定位 Node.js、Python 与 Node packages，并相应设置 `RUNTIME_NODE_MODULES`、`RUNTIME_PYTHON`、`PRESENTATIONS_SKILL_DIR`。

```bash
mkdir -p evidence/slides/build
ln -s /Users/baibo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules evidence/slides/build/node_modules
cp training/slides/source/build.mjs evidence/slides/build/build.mjs
SLIDE_REVISION=v5 /Users/baibo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node evidence/slides/build/build.mjs
```

若已有 `node_modules` 链接，确认其目标正确后跳过 `ln -s`。每次重建使用新的 `SLIDE_REVISION`，避免覆盖留存的已检查文件。构建器在 `evidence/slides/finalized/` 生成已校验版本，再将相同字节复制到本目录三个固定文件名，并同步讲师备注。设置 `DECK_ID=manager`、`engineer` 或 `beginner` 可只构建其中一套。

每次以 AI 创建或编辑课件时，仍应遵循当前 presentations 技能的操作标记与验证要求。脚本本身不代替逐页视觉检查。

```bash
/Users/baibo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 evidence/slides/inspect_submission.py
```

渲染、检查结果与适用边界见 [视觉检查记录](../../evidence/slides/QA.md)。当前使用 Artifact Tool 对最终 PPTX 重新导入并渲染，未在 PowerPoint 或 Google Slides 中进行应用级操作检查。
