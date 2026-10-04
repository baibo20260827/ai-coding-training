#!/usr/bin/env python3
"""Build editable SVG engineering views using only Python's standard library."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'architecture-views'
OUT.mkdir(parents=True, exist_ok=True)

def text(x, y, value, size=24, color='#193047', weight='400'):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>'

def box(x, y, w, h, title, lines=(), fill='#f1f6f8'):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="#90a6b2"/>'
    s+=text(x+22,y+40,title,26,weight='600')
    for i,line in enumerate(lines): s+=text(x+22,y+78+i*34,line,21)
    return s

def arrow(x1,y1,x2,y2,label=None):
    s=f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#1b786e" stroke-width="3" marker-end="url(#arrow)"/>'
    if label:s+=text(min(x1,x2)+12,min(y1,y2)-12,label,19,'#1b786e')
    return s

def save(name,title,subtitle,body,footer):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="800" viewBox="0 0 1400 800" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title><desc>{escape(subtitle)}</desc>
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#1b786e"/></marker></defs>
<g font-family="PingFang SC,Microsoft YaHei,Noto Sans CJK SC,sans-serif"><rect width="1400" height="800" fill="#ffffff"/>
{text(60,72,title,38,weight='700')}{text(60,116,subtitle,22,'#52687a')}
{body}
{text(60,742,footer,21,'#52687a')}{text(60,775,'CASE-ROOM-01 · 教学架构 v1.0 · 图源可编辑 · 真实客户环境待对齐',17,'#52687a')}
</g></svg>'''
    (OUT/name).write_text(svg,encoding='utf-8')

b=''
b+=box(60,190,300,150,'使用者选择日期',['查看预约 R01','选择空闲时段 R02'])
b+=box(460,190,430,150,'核对业务规则 R03 / R06',['09:00—18:00，半小时刻度','相邻允许；重叠拒绝'])
b+=box(990,190,350,150,'形成有效预约',['写入后持久可见 R05','失败时说明原因'])
b+=arrow(360,265,460,265)+arrow(890,265,990,265)
b+=box(460,455,430,150,'取消预约 R04',['取消指定记录','释放全部占用格'])
b+=arrow(1165,340,1165,530)+arrow(1165,530,890,530)
b+=box(60,455,300,150,'时段重新可用',['再次查询或建立预约','验收责任由人承担'])
b+=arrow(460,530,360,530)
save('ba.svg','BA 业务架构','用户场景、规则和业务结果',b,'范围：本地单会议室，无登录、审批或真实客户承诺')

b=box(60,195,300,170,'浏览器页面',['采集虚构预约信息','显示列表与可理解错误','HTML / CSS / JavaScript'])
b+=box(460,195,430,170,'Python 请求与业务处理',['校验 date / start / end','校验 name / purpose','建立、查询与取消'])
b+=box(990,195,350,170,'SQLite 数据访问',['原子事务','占用格唯一约束','持久化存储'])
b+=arrow(360,265,460,265)+arrow(890,265,990,265)
b+=arrow(990,335,890,335)+arrow(460,335,360,335)
b+=box(460,480,430,130,'独立验证',['unittest + 故障演练','需求导出的正常例子与反例'])
b+=arrow(675,480,675,365)
save('aa.svg','AA 应用架构','职责与接口关系；模块是逻辑职责，可在同一源文件实现',b,'API：GET /api/bookings · POST /api/bookings · DELETE /api/bookings/{id}')

b=box(100,190,510,350,'bookings 预约记录',['id：TEXT，预约编号','day：所选日期','start_minute / end_minute','name：虚构姓名','purpose：预约主题'])
b+=box(790,190,510,350,'slots 半小时占用格',['day：所选日期','start_minute：格开始分钟','booking_id：外键 → bookings.id','主键：(day, start_minute)','删除预约时级联释放占用格'])
b+=arrow(610,335,790,335,'1 → 多')
b+=text(100,600,'10:00—11:00 → 占用 10:00 和 10:30 两格',26)
b+=text(100,650,'同一日期每格唯一；全部写入成功才提交，冲突时整体回滚',26)
save('da.svg','DA 数据架构','实际表字段与关键约束；同一日期内的半开区间 [开始,结束)',b,'单会议室省略 room_id；多会议室或审批需求需重新评估数据与验收')

b='<rect x="60" y="170" width="1280" height="510" rx="8" fill="#f7fafb" stroke="#90a6b2" stroke-dasharray="10 6"/>'
b+=text(85,210,'同一台教学电脑',24,weight='600')
b+=box(110,280,320,160,'浏览器',['本机页面','虚构姓名与预约主题'])
b+=box(550,280,660,160,'Python 3 标准库 HTTP 服务',['127.0.0.1:8765','app.py → 业务校验 → SQLite 事务'])
b+=arrow(430,360,550,360,'HTTP')
b+=box(550,530,350,105,'SQLite 文件',['demo/data/bookings.sqlite3'])
b+=arrow(725,440,725,530)
b+=box(960,530,300,105,'隔离验证',['临时测试库与故障脚本'])
save('ta.svg','TA 技术架构','本机运行与数据边界；无需调用模型即可运行已有应用',b,'生产环境、账号权限、资源容量和运维责任需另行与客户确认')
print('Generated 4 editable SVG architecture views.')
