# 材料维护与重建

现成 HTML、SVG 和 PPTX 可直接使用。运行教学应用仅需要 Python 标准库，不需要以下材料构建依赖。

## Markdown → 离线手册

修改相关 Markdown 后，在项目根目录运行：

```bash
node scripts/build_reader.mjs
```

构建脚本需要已安装的 `marked` Node 模块；也可设置 `MARKED_MODULE` 为模块所在的绝对路径。Codex 环境可先通过 `load_workspace_dependencies` 获取捆绑 Node.js 与模块目录。生成的 HTML 不联网、不依赖该模块。主入口是 `学习手册.html` 和 `参考解析.html`；旧 `讲师手册.html` 地址包含当前自学内容与参考解析，并保留原章节锚点，供已有链接继续访问。

## 4A SVG

```bash
python3 scripts/build_architecture.py
```

图源在脚本，业务说明及 Mermaid 源在 `docs/case/architecture.md`。两者与代码、课件架构需要同步审查。

## PPTX

可直接编辑 PPTX；使用内容源重建时见 [课件维护说明](../training/slides/README.md)。依赖 Codex presentations 技能与 Artifact Tool，不属于案例应用依赖。

## 交付检查与打包

```bash
python3 scripts/check_delivery.py
python3 scripts/package_delivery.py
```

先修复检查失败再打包。打包包括文档、HTML、PPTX、图源、代码与验证记录，排除运行数据库、缓存、依赖目录和临时构建目录。`MANIFEST.json` 记录包内文件 SHA-256，压缩包 `harness-ai-coding-training-v1.1.zip` 写入 `dist/`。解压后保持目录结构，从 `START_HERE.html` 开始。

材料改动还需人工复核教学一致性；链接检查不能证明内容正确，代码测试不能证明真实学习有效。

## GitHub Pages 全量学习站

先重建完整培训包，再运行：

```bash
node scripts/build_github_pages.mjs
```

该脚本同样需要 `marked`，可使用 `MARKED_MODULE` 指定模块路径。输出 `dist/github-pages/` 与 `dist/github-pages-full.zip`，将 Markdown 转为带导航的 HTML，保留 PPT/图源/源码和完整下载包，添加 `index.html` 与 `.nojekyll`，检查相对链接。脚本只做本地构建，不上传。

发布目录使用独立 Git 工作副本，不要在生成目录中初始化 Git；生成器检测到 `.git` 会拒绝覆盖。发布步骤、更新方式与 Pages 适用边界见 [发布说明](../docs/PUBLISH_GITHUB.md)。

自学版 v1.1 发布时保留旧 v1.0 ZIP 下载地址，内容为当前完整包的兼容副本。更新需要同时重建手册、三套 PPT（如有课件修改）、完整包与静态站；不能只改首页文字。
