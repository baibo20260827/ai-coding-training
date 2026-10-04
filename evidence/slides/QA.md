# 自学版课件检查记录

日期：2026-10-04。对象为 `training/slides/` 三套自学版 v1.1 PPTX。当前最终修订分别为主管 r1、工程师 r2、新手 r4。

## 交付与检查范围

| 文件 | 页数 | 原生表格所在页 | 原生 4A 图所在页 | 结果 |
|---|---:|---|---|---|
| [manager.pptx](../../training/slides/manager.pptx) | 14 | 7、9、10、13 | 8 | 通过 |
| [engineer.pptx](../../training/slides/engineer.pptx) | 18 | 6、11、16 | 7 | 通过 |
| [beginner.pptx](../../training/slides/beginner.pptx) | 18 | 7、16 | 8 | 通过 |

共 50 页。正文、表格和 4A 图均为原生可编辑对象。每页备注提供直接解释、操作任务及自检或完成标准；三份逐页阅读补充与 PPTX 同源生成。

## 本轮修订

- 重写所有页备注，移除模拟现场讲解、互动指令和固定学习分钟数，补充独立阅读顺序及完成证明。
- 保留三种虚构失败情境，并在画面与备注明确标注。读者先独立判断，再对照解释。
- 新手第 14 页标为进阶练习；可先完成需求与验收，实现需按 L4 在独立副本和隔离空库中操作。未改代码时实现仍为未完成。封面、第 18 页及课件索引保持相同边界。
- 保持客户场景、验收、4A、阶段报告、变更影响、合理延期、工具与人才、持续改进的主题覆盖。部署与 DfX 仅作基础说明。
- 审批与午休限制仍是新增练习，未写成基线已实现功能。测试适配需要需求依据，并保护原检查目的。

## 实际执行与结果

1. 通过 `@oai/artifact-tool` JavaScript ES modules 重新生成三套 PPTX，16:9、1280 × 720 像素；保留 [build.mjs](../../training/slides/source/build.mjs) 与 [content.json](../../training/slides/source/content.json)。
2. presentations 技能 finalizer 校验包结构、尺寸、页数、标题几何、字体、原生表格及最终文件导入。三份当前报告均为 **0 findings、0 warnings**，Artifact Tool 导入均通过。
3. 回读已定稿 PPTX，渲染全部 50 页。逐页以完整尺寸查看文字、换行、表格、页码、4A 连接线及边界，未发现遮挡或溢出。新手第 14、18 页的最后修改已重新查看。
4. 工程师最后一次修订仅改第 18 页备注；忽略自动生成的 `creationId` 后，18 页可见内容 XML 与已逐页查看版本完全一致。新手最后修订除第 14、18 页外，其余 16 页可见内容 XML 也与首轮自学版一致。
5. 运行 [inspect_submission.py](inspect_submission.py)：3 套、50 页通过。检查包括自学措辞、备注与内容源一致、各页独立自检标准、可编辑对象、原生表格、4A 标签与连接线、字号及渲染文件存在。
6. 核对交付文件 SHA-256 与最终检查版本逐字节一致，结果保存在 [selfstudy-review.json](selfstudy-review.json)。

当前报告：

- [manager-selfstudy-v1.1-r1.validation.json](manager-selfstudy-v1.1-r1.validation.json)
- [engineer-selfstudy-v1.1-r2.validation.json](engineer-selfstudy-v1.1-r2.validation.json)
- [beginner-selfstudy-v1.1-r4.validation.json](beginner-selfstudy-v1.1-r4.validation.json)
- [submission-check.json](submission-check.json)

逐页 PNG 与布局数据位于 `renders/manager/`、`renders/engineer/`、`renders/beginner/`，文件名为 `slide-01.png`、`slide-01.layout.json` 等。`finalized/` 保存检查版本；旧修订属于历史证据，当前交付以本页所列报告为准。

## 验证边界

此次完成文件结构、内容一致性和 Artifact Tool 渲染检查，没有在 Microsoft PowerPoint 或 Google Slides 中实际打开、编辑、播放和保存。未使用桌面或捆绑 LibreOffice。

本轮没有新增外部技术主张；官方链接和技术说明保留 2026-10-03 的核对记录。没有声称真实自学效果已验证、客户已接受或示例已满足生产部署要求。应用测试与学习任务完成证据应分别保存。
