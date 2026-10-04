# 课件检查记录

日期：2026-10-03。检查对象为 `training/slides/` 下三套 PPTX，当前检查版本为 v4。

## 交付与检查范围

| 文件 | 页数 | 原生表格所在页 | 原生 4A 图所在页 | 检查结果 |
|---|---:|---|---|---|
| [manager.pptx](../../training/slides/manager.pptx) | 14 | 7、9、10、13 | 8 | 结构、布局、字体、导入与逐页视觉检查通过 |
| [engineer.pptx](../../training/slides/engineer.pptx) | 18 | 6、11、16 | 7 | 结构、布局、字体、导入与逐页视觉检查通过 |
| [beginner.pptx](../../training/slides/beginner.pptx) | 18 | 7、16 | 8 | 结构、布局、字体、导入与逐页视觉检查通过 |

共 50 页。每页均有嵌入讲师备注，三份 Markdown 备注与内容 JSON 同源生成。全部文字、表格和图形为原生可编辑对象，没有将整页或 4A 图压成截图。

## 实际执行

1. 使用 `@oai/artifact-tool` JavaScript ES modules 生成 PPTX，16:9 画布，1280 × 720 像素。
2. presentations 技能的 finalizer 检查文件结构、尺寸、页数、标题几何、字体、原生表格及 Artifact Tool 导入，三个当前报告均为 0 findings、0 warnings。
3. 将已检查的最终 PPTX 重新导入 Artifact Tool，渲染全部 50 页为 PNG，逐页以完整尺寸检查中文、换行、边界、表格、页码及连接线。
4. 修正首轮 4A 连接箭头方向，复核三张图。将虚构情境说明调整到 17.25 pt，并复查共同开篇九页。对工程师部署页和新手启动页的标点修订重新检查。
5. 数据视图及并发说明已对齐实际实现：`bookings` 对应多条半小时 `slots`，`(day,start_minute)` 唯一占用，`BEGIN IMMEDIATE` 内整笔写入，冲突回滚，取消级联释放占用。
6. 运行 [inspect_submission.py](inspect_submission.py)，检查 3 套、50 页的备注完整性、原生对象、可见正文字号、4A 标签与连接线数量、渲染文件存在，结果为 pass。
7. 与培训总索引统一整课时长为主管 75 分钟、工程师 150 分钟、新手 150 分钟，同步封面备注、内容源和课件索引。v4 重新校验并渲染全部页面，排除自动生成的 Office creationId 后，50 页可见内容的 XML 与已逐页检查的 v3 完全一致，结果见 [duration-revision-check.json](duration-revision-check.json)。

当前检查报告：

- [manager-v4.validation.json](manager-v4.validation.json)
- [engineer-v4.validation.json](engineer-v4.validation.json)
- [beginner-v4.validation.json](beginner-v4.validation.json)
- [submission-check.json](submission-check.json)

逐页图像与布局数据分别在 `renders/manager/`、`renders/engineer/`、`renders/beginner/`。文件名按 `slide-01.png` 和 `slide-01.layout.json` 排列。`finalized/` 保存与交付文件字节一致的当前已检查版本，哈希见 JSON 报告。

## 内容核对

- 三类共同开篇均明确标注虚构教学情境。
- 主管版覆盖客户场景、验收、4A、阶段报告、变更影响、合理延期、工具依赖、人才及持续改进。
- 工程师版覆盖任务边界、需求编号、审查、独立验收、并发与持久化、命令、恢复、变更评估及导师责任。
- 新手版覆盖软件基础、场景表达、逐步操作、验收、问题报告、小变更、求助和能力证明。
- 部署与 DfX 保持概要，没有展开产品选型。
- 固定命令与案例范围已核对。审批与午休禁约明确属于新增练习，未声称基线应用已实现。
- 官方资料链接置于相关页备注，2026-10-03 已访问核对。用户场景与流程建议来自本项目材料，没有虚构外部统计或成效数字。

## 验证边界

此次为文件结构和 Artifact Tool 渲染检查，没有在 Microsoft PowerPoint 或 Google Slides 中打开、编辑、播放和保存这些文件。没有调用用户桌面 LibreOffice，也没有使用捆绑 LibreOffice；当前渲染不依赖它。

视觉检查及材料完整性不证明真实培训有效、真实部署适用或客户已经接受。应用实际测试、客户验收和试讲结果应分别查看对应工程证据与后续试讲记录。
