# 在自己的 GitHub 发布完整学习网站

版本：1.1；日期：2026-10-04。适用：在 Mac 上维护本项目，并将完整学习材料发布为 GitHub Pages 网站。

**当前状态：全量学习材料已按用户授权公开发布。** 账号 `baibo20260827`；[发布仓库](https://github.com/baibo20260827/ai-coding-training)；[在线学习站](https://baibo20260827.github.io/ai-coding-training/)。实际部署与检查记录见 [发布证据](../evidence/publishing/VALIDATION.md)。下文首次发布步骤保留供参考，后续维护使用第 5 节的增量更新流程。

## 1. 本次发布什么

本网站提供自学路径、自主学习手册与参考解析、完整材料的网页阅读、3 套 PPT、逐页阅读补充、6 项练习与自检、AI 任务卡、分层指南、FAQ、7 份模板、4A 图源与图片、案例源码和验证记录，并提供完整学习包下载。

本地生成位置：

- `dist/github-pages/`：静态网站，包含 `index.html`、`.nojekyll`、材料 HTML、PPT、源码和下载包；保持整个目录结构。
- `dist/github-pages-full.zip`：完整网站发布压缩包，用于分发或转移。
- `dist/harness-ai-coding-training-v1.1.zip`：可离线学习、运行 Python 示例的完整自学包。

`dist/` 是生成产物目录，会在重建时更新。**不要在 `dist/github-pages/` 中初始化 Git，也不要把它当作长期维护的发布仓库。** 使用一个独立发布目录保存 Git 历史；重建后把新产物同步进去。构建器若发现输出目录内已有 `.git`，会拒绝覆盖，应先保留并迁移该仓库。

Pages 用于托管 HTML、CSS、JavaScript 等静态文件；本项目的学习页面适合这种方式。[GitHub Pages 官方介绍](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

## 2. 先明确访问范围与仓库

本轮已确认：账号 `baibo20260827`、仓库名 `ai-coding-training`、全量培训材料允许公开。维护责任由用户所在团队落实。以下命令使用本轮目标地址；应用到其他项目时先核对自己的仓库。

**普通 Pages 发布按公开访问安排；私有代码仓库并不自动等同于内部学习网站。** 如果材料仅允许部门内部访问，先确认组织可用的访问控制和托管方式，不执行本篇的普通公开发布路径。Pages 的可用方式及访问控制还受账户、组织和套餐条件影响。[GitHub 发布来源与公开访问说明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

对于允许公开的材料，建议新建一个专门保存网站文件的空仓库。首次建仓时不要额外生成 README、许可证或 `.gitignore`，这样下面的首次推送路径不需要合并两套初始历史。已有仓库请用第 5 节的克隆与增量同步方式，保留原有历史和内容。

## 3. 从项目生成和预览网站

在终端进入本项目：

```bash
cd "/Users/baibo/Documents/ChatGPT/软件harness研究"
node scripts/build_reader.mjs
python3 scripts/package_delivery.py
node scripts/build_github_pages.mjs
```

顺序有意义：先重建阅读手册，再更新完整自学包，最后把最新下载包和全部材料纳入网站。若修改了 PPT，先按课件维护说明重建并检查。若项目已能解析 `marked` 模块，Node 命令可直接运行；若提示找不到模块，为两条 Node 命令使用实际模块路径，例如：

```bash
MARKED_MODULE="/替换为实际安装位置/marked" node scripts/build_github_pages.mjs
```

`MARKED_MODULE` 必须指向本机真实模块位置。原制作环境可通过 Codex 的 workspace dependencies 工具查到捆绑运行时；换电脑不能直接沿用他人的绝对路径。依赖只用于生成网页，访问已生成网站和运行 Python 教学程序不需要 `marked`。材料重建的其余说明见[维护说明](../scripts/README.md)。

生成成功后，可从项目根目录启动静态预览：

```bash
python3 -m http.server 8080 --bind 127.0.0.1 --directory dist/github-pages
```

打开浏览器访问 `http://127.0.0.1:8080`，检查首页、三类学习入口、完整材料目录、PPT 与学习包下载，以及多级目录之间的链接。终端保持运行，结束时按 `Ctrl+C`。这是静态材料预览，不是会议室预约后端。

## 4. 新建专用空仓库时的首次发布

下面使用独立目录 `/Users/baibo/Documents/ChatGPT/ai-coding-training-site`。可以替换为自己选定的新目录。若该目录已经存在，先确认其用途；不要对已有仓库重复执行初始化，改按下一节处理。

先复制生成的网站文件，包含 `.nojekyll`，不要只复制可见文件或单独的首页：

```bash
cd "/Users/baibo/Documents/ChatGPT/软件harness研究"
mkdir "../ai-coding-training-site"
rsync -av --exclude='.git' dist/github-pages/ ../ai-coding-training-site/
cd "../ai-coding-training-site"
pwd
```

确认 `pwd` 显示的是独立发布目录，且其中存在 `index.html` 和 `.nojekyll`，再初始化提交。以下 `git add .` 仅在这个专用网站目录执行：

```bash
git init -b main
git status --short
git add .
git diff --cached --stat
git commit -m "Publish AI coding training materials"
```

在 GitHub 创建本轮目标空仓库后，使用其 HTTPS 地址：

```bash
git remote add origin "https://github.com/baibo20260827/ai-coding-training.git"
git remote -v
git push -u origin main
```

推送使用自己的 GitHub 登录与 Git 身份配置；若认证失败，按本机已有 GitHub 登录方式处理，不把令牌写进文档、命令中的仓库 URL 或网站文件。推送成功只说明文件已经进入仓库，还需配置 Pages。

在该仓库的 **Settings → Pages → Build and deployment** 中选择：

1. **Source：Deploy from a branch**。
2. **Branch：main**。
3. **Folder：/(root)**，然后保存。

保留根目录的 `.nojekyll`，让这套预先生成的网站直接作为静态文件发布。本方案无需自行编写工作流。[发布来源配置](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

等待 GitHub 显示部署结果，再从 Pages 设置页复制实际网址。专用项目站点通常形如 `https://用户名.github.io/仓库名/`，账户主页仓库和自定义域名会不同，以实际显示结果为准。打开网站后再次检查材料目录、深层网页、图片和下载；不要把本机预览成功直接记成线上发布成功。[创建 GitHub Pages 网站](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

## 5. 已有仓库与后续更新

已有仓库先克隆到独立目录，不能在当前完整源项目里直接添加远端并推送所有文件。以下为本轮目标地址，目标目录需尚不存在：

```bash
cd "/Users/baibo/Documents/ChatGPT"
git clone "https://github.com/baibo20260827/ai-coding-training.git" ai-coding-training-site
cd ai-coding-training-site
git status --short
```

先确认当前分支、Pages 发布来源及仓库原有用途。若不是专用空白网站仓库，检查生成文件是否会与已有文件同名；有同名内容先决定整合方式，不直接覆盖。下列同步流程假定该目录已经专用于本培训网站，且当前处于实际发布分支。

每次更新先在源项目改 Markdown、PPT、代码或材料，再重建：

```bash
cd "/Users/baibo/Documents/ChatGPT/软件harness研究"
MARKED_MODULE="/替换为实际安装位置/marked" node scripts/build_reader.mjs
python3 scripts/package_delivery.py
MARKED_MODULE="/替换为实际安装位置/marked" node scripts/build_github_pages.mjs
```

如果 `marked` 已能直接解析，两条 Node 命令均可省略 `MARKED_MODULE` 设置。若更改的是本地示例行为，先按[运行说明](../demo/README.md)完成相关验证；网页重建不能替代工程检查。

然后进入独立发布仓库，确认没有未处理的本地改动，并拉取现有历史：

```bash
cd "/Users/baibo/Documents/ChatGPT/ai-coding-training-site"
git status --short
git pull --ff-only
```

若拉取提示分支分叉或有本地改动，先解决当前状态，不使用强制推送覆盖历史。状态确认后同步网站产物：

```bash
rsync -av --exclude='.git' "/Users/baibo/Documents/ChatGPT/软件harness研究/dist/github-pages/" ./
git status --short
git diff --stat
git add .
git diff --cached --stat
git commit -m "Update AI coding training materials"
git push
```

`rsync` 源目录结尾的 `/` 表示复制目录内容；`.git` 被排除，历史保留。这里不使用 `--delete`，因此旧版已停用页面可能仍在发布目录。根据本次变更逐项审查后删除确实废弃的网页或附件，再提交删除；不要把整仓清空来实现更新。如果没有文件变化，无需空提交。

推送后在 Pages 部署记录确认成功，并实际检查修改过的页面及下载包。维护记录可写入[改进日志](IMPROVEMENTS.md)，明确源材料版本、发布提交与线上验证结果。

## 6. Python 预约程序为什么不能直接在 Pages 运行

本项目包含两种不同用途的内容：

| 内容 | Pages 上能做什么 | 运行方式 |
|---|---|---|
| 学习网页、架构图、练习、FAQ | 在线阅读、查看图表 | 浏览器打开网站 |
| PPT、模板和完整学习包 | 下载与离线使用 | 下载后用对应工具打开 |
| Python、SQLite 预约程序 | 查看或下载源码；不在 Pages 上启动 Python 服务 | 下载完整包或克隆本发布仓库后，在自己的电脑运行 |

案例启动命令保持为：

```bash
python3 demo/app.py --port 8765
```

下载包解压后或 GitHub 仓库克隆完成后，在其根目录执行上述命令；完整运行、验证和恢复步骤见[案例运行说明](../demo/README.md)。发布构建保持 `demo/static/index.html` 原始应用源码不变，以便克隆后仍能运行同一个案例。网站的全量材料目录提供本地运行说明与独立的 `demo/SOURCE.html` 源码预览入口。

`http://127.0.0.1:8765` 指向**当前读者自己的电脑**；只有该读者已启动程序时才可用，它不是 GitHub 上的在线预约服务。程序仅监听本机，并通过本地 HTTP 接口读写 SQLite；这些后端功能不会随上传 HTML 自动出现。

也不要把 `demo/static/index.html` 单独设为网站首页：它引用 `/assets/` 并请求 `/api/`，需要案例 Python 服务提供路径和处理逻辑。在项目 Pages 子路径下这些地址没有相应服务，页面不能完成预约。

若将来希望不同员工在线共享预约数据，那是新增应用托管任务，需要另行确定身份、权限、后端运行环境与业务交付范围。当前发布交付的是完整学习网站和可下载的本地案例，不应将它标成已上线的共享预约系统。[静态托管边界](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

## 7. 发布完成记录

- 仓库：[baibo20260827/ai-coding-training](https://github.com/baibo20260827/ai-coding-training)。
- 访问范围：用户于 2026-10-04 明确授权公开全部学习材料。
- 实际站点：[AI Coding 全量学习站](https://baibo20260827.github.io/ai-coding-training/)。
- 发布来源：`main` 分支、仓库根目录；GitHub Pages API 模式为 `legacy`，`https_enforced=true`。
- 首次成功部署提交：`4127fae44ac515a91f5f463729e13a636adcab0f`；GitHub 构建状态 `built`，更新时间为 2026-10-04T04:12:06Z（上海 12:12:06）。
- 公网检查：2026-10-04T04:12:54.821492+00:00，21 项 HTTPS GET、内容类型与完整文件 SHA-256 比对通过；详见[发布记录](../evidence/publishing/VALIDATION.md)及[机器检查结果](../evidence/publishing/online-check.json)。

后续更新保留材料版本、发布提交和检查时间的对应关系。本节记录首次已核实部署；补充状态文档后的后续构建与部署应另行检查。网站上线不表示 Python 后端已在 Pages 运行，也不代表已完成网站浏览器视觉/交互验证、真实客户验收或培训成效验证。

## 自学版 v1.1 的入口兼容

主要入口为 `学习手册.html` 与 `参考解析.html`，材料按独立阅读、操作和自检组织。原 `讲师手册.html` 保留当前自学内容、参考解析及原章节锚点，`training/facilitator-guide.html` 保留地址并改为自学实践指南。完整包使用 v1.1 文件名；原 v1.0 ZIP 下载地址保留为当前包的兼容副本，避免已分享链接失效。旧发布记录中的哈希只证明对应历史版本，不能用于核对更新后的文件。
