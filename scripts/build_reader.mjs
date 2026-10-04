// Optional build dependency: marked. Generated HTML has no runtime dependency.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const req=createRequire(import.meta.url);
let marked;
try { ({marked}=req('marked')); }
catch {
 if(!process.env.MARKED_MODULE) throw new Error('重建手册需要 marked：安装到本项目，或用 MARKED_MODULE 指定已安装模块的绝对路径。阅读已生成 HTML 无需此依赖。');
 ({marked}=req(process.env.MARKED_MODULE));
}
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const id=p=>'doc-'+p.replaceAll(/[^a-zA-Z0-9]/g,'-');
const walk=dir=>fs.existsSync(path.join(root,dir))?fs.readdirSync(path.join(root,dir),{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):e.name.endsWith('.md')?[path.join(dir,e.name)]:[]):[];
const common=['training/README.md','training/00-opening.md','training/facilitator-guide.md',...walk('docs/guides').filter(p=>!p.endsWith('README.md')),...walk('docs/case'),'demo/README.md','demo/REQUIREMENTS.md','demo/WALKTHROUGH.md','training/ai-task-cards.md','training/exercises.md',...walk('templates'),...walk('faq')];
const css=`:root{font-family:"PingFang SC","Microsoft YaHei",sans-serif;color:#183047;background:#f5f7f8;line-height:1.75}*{box-sizing:border-box}body{margin:0}header{background:#102b3f;color:white;padding:32px 5vw}header h1{font-size:32px;margin:0 0 8px}header p{margin:0;color:#c9d9e4}nav{position:sticky;top:0;background:#fff;border-bottom:1px solid #d3e0e5;padding:12px 5vw;z-index:1;display:flex;gap:24px;align-items:center;flex-wrap:wrap}a{color:#126c70;text-decoration:none}a:hover{text-decoration:underline}input{font:inherit;padding:6px 10px;border:1px solid #90a6b2;border-radius:4px;max-width:100%}main{max-width:1100px;margin:32px auto;padding:0 28px}article{padding:28px 38px;background:#fff;border:1px solid #dae2e6;margin:24px 0;scroll-margin-top:90px}h1{font-size:29px}h2{font-size:23px;border-bottom:1px solid #dce6eb;padding-bottom:8px;margin-top:30px}h3{font-size:19px;margin-top:24px}p,li{font-size:17px}table{border-collapse:collapse;width:100%;font-size:15px;display:block;overflow:auto}td,th{padding:9px 12px;border:1px solid #cddde3;text-align:left;vertical-align:top}th{background:#eef4f7}blockquote{border-left:4px solid #1b786e;background:#f4f8f8;margin:18px 0;padding:6px 20px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f4f7;padding:18px;font-size:14px}code{font-family:ui-monospace,monospace}img{max-width:100%;height:auto}.source{font-size:13px;color:#52687a}.toc{columns:2;column-gap:32px}.toc li{break-inside:avoid;font-size:15px}.hidden{display:none}@media(max-width:700px){article{padding:20px}.toc{columns:1}main{padding:0 12px}}@media print{nav,.toc-box,.source{display:none}body{background:white}header{background:white;color:#183047;padding:0}header p{color:#52687a}main{max-width:none;padding:0;margin:0}article{border:0;padding:0;break-before:page}article:first-child{break-before:auto}h1,h2,h3{break-after:avoid}table{display:table;font-size:11px}td,th{padding:5px}p,li{font-size:11pt}img{max-height:600px}pre{font-size:9pt}}`;
function make(files,title,out){
 files=[...new Set(files)].filter(p=>fs.existsSync(path.join(root,p)));
 const titles=new Map(files.map(p=>[p,fs.readFileSync(path.join(root,p),'utf8').match(/^# (.+)/m)?.[1]||p]));
 const contents=files.map(p=>{
   let html=marked.parse(fs.readFileSync(path.join(root,p),'utf8'));
   if(p==='docs/case/architecture.md'){
     let n=0;const views=['ba','aa','da','ta'];
     html=html.replace(/<pre><code class="language-mermaid">[\s\S]*?<\/code><\/pre>/g,()=>`<img src="docs/architecture-views/${views[n++]}.svg" alt="可编辑4A架构视图">`);
   }
   html=html.replace(/href="([^"]+)"/g,(match,href)=>{
     if(/^(https?:|mailto:|#)/.test(href))return match;
     const target=path.normalize(path.join(path.dirname(p),href.split('#')[0]));
     const destination=titles.has(target)?'#'+id(target):common.includes(target)?'学习手册.html#'+id(target):target==='training/answer-key.md'?'参考解析.html#'+id(target):target;
     return `href="${esc(destination)}"`;
   });
   return `<article id="${id(p)}" data-search="${esc(titles.get(p))}"><p class="source">源文件：<a href="${esc(p)}">${esc(p)}</a></p>${html}</article>`;
 }).join('\n');
 const toc=files.map(p=>`<li><a href="#${id(p)}">${esc(titles.get(p))}</a></li>`).join('');
 const html=`<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><style>${css}</style><header><h1>${title}</h1><p>软件工程 Harness 与 AI Coding · 自学版 v1.1 · 2026-10-04 · 按路径阅读，动手后对照参考解析</p></header><nav><a href="START_HERE.html">返回自学首页</a><a href="#contents">目录</a><a href="参考解析.html">参考解析与自检</a><label>查找内容 <input id="search" type="search" placeholder="输入关键词"></label><span id="count"></span></nav><main><section class="toc-box" id="contents"><h2>阅读目录</h2><ul class="toc">${toc}</ul></section>${contents}</main><script>const input=document.getElementById('search');const articles=[...document.querySelectorAll('article')];input.addEventListener('input',()=>{let n=0;for(const a of articles){let show=a.textContent.toLowerCase().includes(input.value.trim().toLowerCase());a.classList.toggle('hidden',!show);if(show)n++;}document.getElementById('count').textContent=input.value?n+' 篇匹配':'';});document.addEventListener('click',e=>{if(e.target.closest('a[href^="#doc-"]')){input.value='';for(const article of articles)article.classList.remove('hidden');document.getElementById('count').textContent='';}});</script></html>`;
 fs.writeFileSync(path.join(root,out),html);
 console.log(out+': '+files.length+' source documents');
}
make(common,'自主学习手册','学习手册.html');
make(['training/facilitator-guide.md','training/exercises.md','training/answer-key.md'],'参考解析与自检','参考解析.html');
// Preserve legacy chapter anchors while presenting only current self-study content.
make(['training/facilitator-guide.md',...common,'training/answer-key.md'],'参考解析与自检','讲师手册.html');
