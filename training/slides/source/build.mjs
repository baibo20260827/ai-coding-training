import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile, FileBlob } from '@oai/artifact-tool';

// Copy this source into evidence/slides/build, whose node_modules symlink points
// to the bundled runtime. Then run with the bundled Node.js executable.
const workspaceDir=process.env.WORKSPACE_DIR ?? process.cwd();
const SKILL_DIR=process.env.PRESENTATIONS_SKILL_DIR ?? '/Users/baibo/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations';
const RUNTIME_PYTHON=process.env.RUNTIME_PYTHON ?? '/Users/baibo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
process.env.RUNTIME_NODE_MODULES ??= '/Users/baibo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
process.env.RUNTIME_NODE ??= process.execPath;
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL_DIR,'container_tools/artifact_tool_utils.mjs')).href);
const content=JSON.parse(await fs.readFile(path.join(workspaceDir,'training/slides/source/content.json'),'utf8'));
const FONT='Arial Unicode MS';
const C={paper:'#FAF8F3',ink:'#17333C',muted:'#5D6B70',line:'#C8D2D0',white:'#FFFFFF'};
const revision=process.env.SLIDE_REVISION ?? 'v1';
const evidenceDir=path.join(workspaceDir,'evidence/slides');
await fs.mkdir(path.join(evidenceDir,'build'),{recursive:true});

function txt(s,text,x,y,w,h,size=28,color=C.ink,bold=false,align='left',name='text'){
 const t=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 t.text=text;t.text.style={typeface:FONT,fontSize:size,bold,color,alignment:align,verticalAlignment:'top',autoFit:'none',wrap:'square',insets:{top:0,right:0,bottom:0,left:0}};
 return t;
}
function bottom(s,text,accent){if(text)txt(s,text,64,619,1152,50,24,accent,false,'left','takeaway');}
function base(s,d,i,n,item){
 s.background.fill=C.paper;
 txt(s,item.title,64,45,1152,70,44,C.ink,true,'left','slide-title');
 if(item.lead)txt(s,item.lead,64,137,1152,62,26,C.muted,false,'left','slide-lead');
 txt(s,d.name,64,683,580,25,16,C.muted,false,'left','footer-audience');
 txt(s,`${String(i+1).padStart(2,'0')} / ${n}`,1080,683,136,25,16,C.muted,false,'right','footer-page');
}
function makeTable(s,item,accent){
 const values=[item.headers,...item.rows];const height=Math.min(396,values.length*76);
 const table=s.tables.add({rows:values.length,columns:item.headers.length,left:64,top:210,width:1152,height,columnWidths:item.widths,values});
 table.cells.block({row:0,column:0,rowCount:values.length,columnCount:item.headers.length}).assign({textStyle:{typeface:FONT,fontSize:24,color:C.ink},margins:{top:11,bottom:11,left:16,right:16},anchor:'center'});
 table.borders.assign({style:'solid',fill:C.line,width:0.8});
 for(let c=0;c<item.headers.length;c++){const cell=table.getCell(0,c);cell.fill=accent;cell.text.style={typeface:FONT,fontSize:24,bold:true,color:C.white};}
 for(let r=1;r<values.length;r++){for(let c=0;c<item.headers.length;c++)table.getCell(r,c).fill=r%2?C.white:C.paper;}
 return table;
}
function node(s,text,x,y,w,h,accent,name){
 const sh=s.shapes.add({geometry:'rect',name,position:{left:x,top:y,width:w,height:h},fill:C.white,line:{fill:accent,width:1.3}});
 sh.text=text;sh.text.style={typeface:FONT,fontSize:26,color:C.ink,alignment:'center',verticalAlignment:'middle',autoFit:'none',insets:{top:7,bottom:7,left:9,right:9}};return sh;
}
function architecture(s,accent){
 const labels=[['BA','业务架构'],['AA','应用架构'],['DA','数据架构'],['TA','技术架构']];
 const ns=[['查看空闲','提交预约 / 取消','结果提示'],['原生页面','HTTP 接口与校验','预约数据存取'],['预约记录','1 对多占用格','同日每格唯一'],['本机浏览器','Python 3 服务','SQLite 文件']];
 for(let r=0;r<4;r++){
  const y=210+r*94;txt(s,labels[r][0],64,y+7,84,35,30,accent,true);txt(s,labels[r][1],64,y+45,150,35,24,C.muted);
  const shapes=ns[r].map((value,c)=>node(s,value,250+c*320,y,285,76,accent,`4A-${labels[r][0]}-${c}`));
  for(let c=0;c<2;c++)s.shapes.connect(shapes[c],shapes[c+1],{kind:'straight',fromSide:'right',toSide:'left',line:{fill:accent,width:1.5},tail:{type:r===2?'none':'triangle',width:'sm',length:'sm'}});
 }
}
function renderItem(s,d,item){
 const a=d.accent;
 if(item.kind==='cover'){
  s.background.fill=C.ink;
  txt(s,item.subtitle,64,82,1120,50,28,'#A8CCCA');
  txt(s,item.title,64,213,1140,186,66,C.white,true);
  txt(s,item.focus,64,472,1140,60,32,'#D4E4E2');
  txt(s,'软件工程 Harness 能力建设',64,638,850,34,23,'#A8CCCA');
  txt(s,'2026.10',1025,638,190,34,23,'#A8CCCA',false,'right');
  return;
 }
 if(item.kind==='story'){
  txt(s,item.role,64,161,500,50,28,a,true);
  txt(s,item.quote,64,232,530,205,42,C.ink,true);
  item.rows.forEach((row,j)=>{txt(s,row[0],640,211+j*109,82,42,25,a,true);txt(s,row[1],749,211+j*109,467,88,26);});
  txt(s,item.takeaway,64,573,1152,64,28,a);
  txt(s,'虚构教学情境',64,646,850,30,23,C.muted);
 }else if(item.kind==='columns'){
  item.columns.forEach((col,j)=>{const x=64+j*600;txt(s,col.heading,x,215,550,52,31,a,true);col.items.forEach((v,k)=>txt(s,v,x,284+k*72,550,65,26));});
  bottom(s,item.bottom,a);
 }else if(item.kind==='rows'){
  item.rows.forEach((row,j)=>{const y=219+j*86;txt(s,row[0],64,y,258,65,27,a,true);txt(s,row[1],350,y,866,68,28);});bottom(s,item.bottom,a);
 }else if(item.kind==='table'){
  makeTable(s,item,a);bottom(s,item.bottom,a);
 }else if(item.kind==='architecture'){
  txt(s,'同一需求映射到流程、职责、数据和运行环境',64,137,1152,50,26,C.muted);architecture(s,a);bottom(s,item.bottom,a);
 }else if(item.kind==='comparison'){
  txt(s,item.leftTitle,64,208,540,58,32,a,true);txt(s,item.leftText,64,320,548,185,40);
  txt(s,item.rightTitle,664,208,540,58,32,'#A24E36',true);txt(s,item.rightText,664,320,548,185,40);bottom(s,item.bottom,a);
 }else if(item.kind==='commands'){
  item.commands.forEach((cmd,j)=>{txt(s,cmd.label,64,207+j*177,1152,47,27,a,true);txt(s,cmd.code,64,269+j*177,1152,78,33,C.ink);});bottom(s,item.bottom,a);
 }else if(item.kind==='steps'){
  item.steps.forEach((st,j)=>{const y=219+j*88;txt(s,st[0],64,y,85,65,33,a,true);txt(s,st[1],172,y,328,67,28,C.ink,true);txt(s,st[2],526,y,690,68,27);});bottom(s,item.bottom,a);
 }else if(item.kind==='prompt'){
  item.prompt.split('\n').forEach((line,j)=>txt(s,line,64,215+j*85,1152,70,30));bottom(s,item.bottom,a);
 }else throw new Error(`Unknown slide kind ${item.kind}`);
}

for(const d of content.decks){
 if(process.env.DECK_ID && process.env.DECK_ID!==d.id)continue;
 const all=[d.cover,...content.opening,...d.slides];
 if(all.length!==d.expectedCount)throw new Error(`${d.id}: wrong slide count ${all.length}`);
 const p=Presentation.create({slideSize:{width:1280,height:720}});
 const notes=[];const tableSlides=[];const diagramSlides=[];
 for(let i=0;i<all.length;i++){
  const item=all[i];const s=p.slides.add();
  if(item.kind!=='cover')base(s,d,i,all.length,item);
  renderItem(s,d,item);
  if(item.kind==='table')tableSlides.push(i+1);
  if(item.kind==='architecture')diagramSlides.push(i+1);
  const refs=(item.sources??[]).map(k=>`${k}: ${content.sources[k]}`).join('\n');
  const note=`第 ${i+1} 页：${item.title.replaceAll('\n',' ')}\n\n${item.notes}\n\n材料来源：本项目 AGENTS.md、docs/PROJECT_PLAN.md、training/00-opening.md。\n${refs ? '官方资料（2026-10-03 核对）：\n'+refs : '本页为教学设计与示例，无外部统计数据。'}`;
  s.speakerNotes.textFrame.setText(note);notes.push(`## ${i+1}. ${item.title.replaceAll('\n',' ')}\n\n${note}`);
 }
 const candidate=path.join(evidenceDir,'build',`${d.id}-${revision}-candidate.pptx`);
 await(await PresentationFile.exportPptx(p)).save(candidate);
 const deliveredPath=path.join(workspaceDir,'training/slides',`${d.id}.pptx`);
 const finalPath=path.join(evidenceDir,'finalized',`${d.id}-${revision}.pptx`);
 await fs.mkdir(path.dirname(finalPath),{recursive:true});
 const result=await finalizePresentation({workspaceDir,candidatePath:candidate,finalPath,pythonExecutable:RUNTIME_PYTHON,
  integrityValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...tableSlides.flatMap(n=>['--require-native-table-slide',String(n)])],
  explicitTotalSlideCount:all.length,requiredNativeTableOwnerSlides:tableSlides,
  fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,
  receiptPath:path.join(evidenceDir,`${d.id}-${revision}.validation.json`)});
 await fs.copyFile(finalPath,deliveredPath);
 await fs.writeFile(path.join(workspaceDir,'training/slides',`${d.id}-notes.md`),`# ${d.name}逐页讲师备注\n\n版本 ${content.version}，${content.date}。${content.status}。\n\n`+notes.join('\n\n'),'utf8');
 // Render the finalized file, not only the authored in-memory presentation.
 const imported=await PresentationFile.importPptx(await FileBlob.load(finalPath));
 const renderDir=path.join(evidenceDir,'renders',d.id);await fs.mkdir(renderDir,{recursive:true});
 for(let i=0;i<imported.slides.items.length;i++){
  const slide=imported.slides.items[i];
  const png=await imported.export({slide,format:'png',scale:1});
  await fs.writeFile(path.join(renderDir,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
  const layout=await slide.export({format:'layout'});await fs.writeFile(path.join(renderDir,`slide-${String(i+1).padStart(2,'0')}.layout.json`),await layout.text());
 }
 await fs.writeFile(path.join(evidenceDir,`${d.id}-inventory.json`),JSON.stringify({deck:d.id,slides:all.length,tableSlides,diagramSlides,font:FONT,finalPath,deliveredPath,renderDir,renderedFromFinalFile:true},null,2));
 console.log(JSON.stringify({deck:d.id,slides:all.length,finalPath,renderDir,validation:result}));
}
