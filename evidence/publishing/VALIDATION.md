# 全量学习站本地发布检查

日期：2026-10-04。用户要求：将网页及全量学习材料发布到自己的 GitHub。当前阶段：发布文件准备完成，未进行外部发布。

## 已完成

- 使用 [构建器](../../scripts/build_github_pages.mjs) 生成静态首页、全量材料目录、学员/讲师手册和全部 Markdown 的 HTML 阅读页。
- 保留三套可编辑 PPT、逐页讲稿、练习/答案、FAQ、模板、4A 图源/图片、案例源码和验证记录；首页提供完整离线培训包下载。
- 保留原始 Markdown 下载入口；在线导航改指向 HTML，使用相对路径以支持项目站点子目录。
- 添加根目录 `index.html` 和 `.nojekyll`。源码页面说明 Python 应用须本地运行，不把静态页面当成共享预约系统。
- 运行交付检查：本地链接目标、SVG XML、三套 PPTX 页数和全部备注检查通过。网站构建结果在 `dist/github-pages/evidence/delivery-check.json`。
- 本轮完整培训包重新生成并通过清单哈希及解压检查；发布 ZIP 为 `dist/github-pages-full.zip`，首页位于 ZIP 根目录。

## 发布前仍需完成

用户已确认 GitHub 账号 `baibo20260827`、目标仓库 `ai-coding-training` 及全量公开范围。已读取账号公开仓库列表，尚无对应培训仓库。本机未找到可用 GitHub Git 凭据；正在准备登录。当前未执行仓库创建、推送、开启 Pages 或线上访问检查。

HTML 发布适配采用静态链接/结构检查，没有将这些结果声称为浏览器视觉检查、GitHub 部署成功或真实学习效果。上线后还需检查实际站点首页、深层页面、PPT 和完整包下载。具体步骤见 [发布说明](../../docs/PUBLISH_GITHUB.md)。
