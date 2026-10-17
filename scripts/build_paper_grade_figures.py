#!/usr/bin/env python3
"""Original editable teaching diagrams. Geometry shared by SVG and draw.io.
Read docs/figures-paper-grade/design-contract.md first.
No measured results or novelty claims are represented here.
"""
from pathlib import Path
import xml.etree.ElementTree as E
import html, math, subprocess, json, zipfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'img/figures/paper-grade';OUT.mkdir(parents=True,exist_ok=True)
C={'ink':'#23364A','muted':'#65758A','blue':'#2775A5','green':'#26836E','orange':'#B36A26','gray':'#A8B3BF','light':'#F4F7FA','pale':'#EEF6FB','mint':'#EEF7F2','sand':'#FBF5EA'}
class Figure:
 def __init__(self,slug,title,h):
  self.slug=slug;self.h=h;self.k=0;self.nodes={};self.parents={'1':(0,0)};self.records=[]
  self.svg=E.Element('svg',xmlns='http://www.w3.org/2000/svg',width='182mm',height=f'{182*h/1420:.2f}mm',viewBox=f'0 0 1420 {h}')
  E.SubElement(self.svg,'title').text=title
  defs=E.SubElement(self.svg,'defs')
  for color in ['ink','blue','green','orange']:
   m=E.SubElement(defs,'marker',id='arr-'+color,viewBox='0 0 10 10',refX='9',refY='5',markerWidth='7',markerHeight='7',orient='auto-start-reverse')
   E.SubElement(m,'path',d='M0 0L10 5L0 10Z',fill=C[color])
  E.SubElement(self.svg,'rect',width='1420',height=str(h),fill='white')
  self.mx=E.Element('mxfile',host='app.diagrams.net',version='24.7.17',type='device');d=E.SubElement(self.mx,'diagram',id=slug,name=title)
  model=E.SubElement(d,'mxGraphModel',dx='1420',dy=str(h),grid='1',gridSize='10',page='1',pageScale='1',pageWidth='1420',pageHeight=str(h),background='#ffffff',math='0',shadow='0');self.root=E.SubElement(model,'root');E.SubElement(self.root,'mxCell',id='0');E.SubElement(self.root,'mxCell',id='1',parent='0')
  self.text('title',20,20,1380,38,title,30,True)
  self.text('sub',20,62,1380,28,'CONCEPTUAL DESIGN EXAMPLE  /  illustrative records and signals  /  no experimental results',20,color='muted')
 def cell(self,id,x,y,w,h,value='',style='',parent='1'):
  px,py=self.parents[parent];cell=E.SubElement(self.root,'mxCell',id=id,value=value,vertex='1',parent=parent,style=style)
  E.SubElement(cell,'mxGeometry',x=str(x-px),y=str(y-py),width=str(w),height=str(h),attrib={'as':'geometry'})
  self.nodes[id]=(x,y,w,h);return cell
 def text(self,id,x,y,w,h,t,size=21,bold=False,color='ink',parent='1',align='left'):
  self.cell(id,x,y,w,h,t,f'text;html=0;strokeColor=none;fillColor=none;fontFamily=Arial;fontSize={size};fontColor={C[color]};fontStyle={1 if bold else 0};align={align};verticalAlign=middle;whiteSpace=wrap;overflow=visible;',parent)
  te=E.SubElement(self.svg,'text',id=id,x=str(x if align=='left' else x+w/2),y=str(y+h/2+size*.34),fill=C[color],attrib={'font-family':'Liberation Sans,Arial,sans-serif','font-size':str(size),'font-weight':'700' if bold else '400','text-anchor':'start' if align=='left' else 'middle'})
  for i,line in enumerate(t.split('\n')):
   if i==0:te.text=line
   else:E.SubElement(te,'tspan',x=te.get('x'),dy=str(size*1.2)).text=line
  self.records.append(dict(id=id,x=x,y=y,w=w,h=h,text=t,size=size,bold=bold))
 def rect(self,id,x,y,w,h,fill='white',stroke='gray',parent='1',radius=10,dash=False):
  fc=C.get(fill,fill);sc=C.get(stroke,stroke)
  self.cell(id,x,y,w,h,'',f'rounded={1 if radius else 0};arcSize=8;whiteSpace=wrap;html=0;fillColor={fc};strokeColor={sc};strokeWidth=1.4;dashed={1 if dash else 0};',parent)
  E.SubElement(self.svg,'rect',id=id,x=str(x),y=str(y),width=str(w),height=str(h),rx=str(radius),fill=fc,stroke=sc,attrib={'stroke-width':'1.4',**({'stroke-dasharray':'7 5'} if dash else {})})
 def panel(self,id,x,y,w,h,title,hero=False):
  self.rect(id,x,y,w,h,'pale' if hero else 'light','blue' if hero else 'gray');self.parents[id]=(x,y)
  self.text(id+'-heading',x+18,y+16,w-36,32,title,25,True,parent=id)
 def box(self,id,x,y,w,h,title,lines=(),fill='white',stroke='blue',parent='1'):
  self.rect(id,x,y,w,h,fill,stroke,parent);self.parents[id]=(x,y)
  self.text(id+'-title',x+13,y+10,w-26,27,title,22,True,parent=id)
  for i,t in enumerate(lines):self.text(id+f'-line{i}',x+13,y+40+25*i,w-26,25,t,21,parent=id)
 def edge(self,id,points,color='ink',dash=False,source=None,target=None):
  style=f'edgeStyle=none;rounded=0;html=0;endArrow=block;endFill=1;strokeColor={C[color]};strokeWidth=1.8;dashed={1 if dash else 0};'
  attr=dict(id=id,edge='1',parent='1',style=style)
  if source:attr['source']=source
  if target:attr['target']=target
  cell=E.SubElement(self.root,'mxCell',**attr);g=E.SubElement(cell,'mxGeometry',relative='1',attrib={'as':'geometry'})
  for key,p in [('sourcePoint',points[0]),('targetPoint',points[-1])]:E.SubElement(g,'mxPoint',x=str(p[0]),y=str(p[1]),attrib={'as':key})
  if len(points)>2:
   a=E.SubElement(g,'Array',attrib={'as':'points'})
   for p in points[1:-1]:E.SubElement(a,'mxPoint',x=str(p[0]),y=str(p[1]))
  # Explicit anchors prevent draw.io from selecting a different side on import.
  for node,p,pre in [(source,points[0],'exit'),(target,points[-1],'entry')]:
   if node:
    x,y,w,h=self.nodes[node];style+=f'{pre}X={(p[0]-x)/w};{pre}Y={(p[1]-y)/h};{pre}Dx=0;{pre}Dy=0;{pre}Perimeter=0;'
  cell.set('style',style)
  E.SubElement(self.svg,'path',id=id,d='M'+' L'.join(f'{x} {y}' for x,y in points),fill='none',stroke=C[color],attrib={'stroke-width':'1.8','marker-end':f'url(#arr-{color})',**({'stroke-dasharray':'7 5'} if dash else {})})
 def line(self,id,points,color='gray',dash=False):
  self.edge(id,points,color='ink' if color=='gray' else color,dash=dash);self.svg[-1].attrib.pop('marker-end',None);self.root[-1].set('style',self.root[-1].get('style').replace('endArrow=block','endArrow=none'))
 def tag(self,id,x,y,w,t,color='green',parent='1'):
  self.rect(id,x,y,w,34,'mint' if color=='green' else 'sand',color,parent,radius=6)
  self.text(id+'-text',x,y,w,34,t,20,True,color,parent,align='center')
 def save(self):
  E.indent(self.mx);E.ElementTree(self.mx).write(OUT/(self.slug+'.drawio'),encoding='utf-8',xml_declaration=True)
  # Mirror draw.io semantic groups so a module's rectangle and full labels move together.
  original=list(self.svg);byid={e.get('id'):e for e in original if e.get('id')}
  parents={c.get('id'):c.get('parent') for c in self.root if c.get('id') in byid}
  children={}
  for id,parent in parents.items():children.setdefault(parent,[]).append(id)
  def grouped(id):
   if id not in children:return byid[id]
   g=E.Element('g',id=id+'-group',attrib={'data-module':id});g.append(byid[id])
   for child in children[id]:g.append(grouped(child))
   return g
  self.svg[:]=[grouped(e.get('id')) if e.get('id') in byid else e for e in original if parents.get(e.get('id'),'1')=='1']
  E.indent(self.svg);E.ElementTree(self.svg).write(OUT/(self.slug+'.svg'),encoding='utf-8',xml_declaration=True)
  (OUT/(self.slug+'-layout.json')).write_text(json.dumps(self.records,indent=2))
  for typ in ['pdf','png']:
   cmd=['inkscape',str(OUT/(self.slug+'.svg')),f'--export-type={typ}',f'--export-filename={OUT/(self.slug+"."+typ)}']
   if typ=='png':cmd+=['--export-width=2200']
   subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)

def overview():
 f=Figure('industrial-agent-full','Industrial agent with context-dependent experience reuse',960)
 f.panel('context',20,110,300,590,'(a) Process context')
 f.box('state',40,175,260,90,'Operating context',['Regime A · limits · time t'],parent='context')
 # Process mini diagram: explicitly illustrative, not an engineering P&ID.
 f.text('plant-label',40,285,260,28,'Process sketch',20,parent='context')
 f.box('compress',45,335,110,70,'Feed',[],stroke='gray',parent='context');f.box('column',190,335,105,70,'Unit',[],stroke='gray',parent='context')
 f.edge('feed-column',[(155,370),(190,370)],'blue',source='compress',target='column')
 f.text('signals-label',40,430,260,28,'Observed trends (schematic)',20,parent='context')
 f.line('signal-x',[(50,565),(290,565)]);f.line('signal-y',[(50,475),(50,565)])
 for k,col in enumerate(['blue','green']):
  points=[(52+i*3,520+k*24+13*math.sin(i*.13+k)+(.0 if i<40 else -18)) for i in range(78)]
  f.line('trace-'+str(k),points,col)
 f.text('window-label',45,580,250,26,'Window → state estimate',20,parent='context')
 f.tag('constraints',40,635,260,'Constraints + provenance','orange','context')
 f.panel('memory',355,110,680,590,'(b) Applicability-aware memory',True)
 f.box('query',375,175,640,75,'Task-conditioned query',['q(t) = task + c(t) + available tools'],parent='memory')
 f.box('retrieve',375,290,205,95,'1  Retrieve',['Candidate set C(t)','Semantic similarity'],parent='memory')
 f.box('validate',625,290,390,95,'2  Check applicability',['Match regime ∧ fresh ∧ within limits','Unknown → request evidence'],fill='mint',stroke='green',parent='memory')
 f.edge('ctx-query',[(300,212),(375,212)],'blue',source='state',target='query')
 f.edge('query-retrieve',[(478,250),(478,290)],'blue',source='query',target='retrieve')
 f.edge('retrieve-check',[(580,337),(625,337)],'blue',source='retrieve',target='validate')
 f.text('table-heading',375,411,630,27,'3  Filter first; rank the admissible candidates',22,True,parent='memory')
 for j,(name,x,w) in enumerate([('Experience',375,190),('Relevance',565,155),('Validity',720,145),('Decision',865,150)]):
  f.rect(f'th{j}',x,455,w,42,'pale','gray','memory',0);f.text(f'thl{j}',x+10,460,w-20,28,name,20,True,parent='memory')
 for i,row in enumerate([('E1 · regime A','High','Pass','KEEP'),('E2 · old rule','High','Expired','BLOCK'),('E3 · incomplete','Moderate','Unknown','VERIFY')]):
  y=497+i*42
  for j,(x,w) in enumerate([(375,190),(565,155),(720,145),(865,150)]):
   f.rect(f'tc{i}{j}',x,y,w,42,'mint' if i==0 else 'sand','gray','memory',0);f.text(f'txt{i}{j}',x+10,y+5,w-20,28,row[j],20,parent='memory')
 f.edge('table-selected',[(695,623),(695,645)],'green')
 f.box('selected',375,645,640,40,'Selected E1 → bounded planning context',[],fill='white',stroke='green',parent='memory')
 f.edge('check-table',[(825,385),(825,404)],'green',source='validate')
 f.panel('execution',1070,110,330,590,'(c) Tools & constraints')
 f.box('planner',1090,175,285,90,'LLM planner',['Task + selected experience'],parent='execution')
 f.box('inspect',1090,310,130,70,'Inspect',[],parent='execution');f.box('simulator',1245,310,130,70,'Simulate',[],parent='execution')
 f.edge('planner-tool-a',[(1160,265),(1160,310)],'blue',source='planner',target='inspect')
 f.edge('planner-tool-b',[(1310,265),(1310,310)],'blue',source='planner',target='simulator')
 f.box('safety',1090,435,260,100,'Constraint evaluation',['Check tool predictions','Approve / reject / review'],fill='sand',stroke='orange',parent='execution')
 f.edge('tool-check-a',[(1160,380),(1160,435)],'blue',source='inspect',target='safety')
 f.edge('tool-check-b',[(1310,380),(1310,435)],'blue',source='simulator',target='safety')
 f.box('execute',1245,600,130,70,'Execute',[],fill='mint',stroke='green',parent='execution')
 f.box('review',1090,600,130,70,'Review',[],fill='sand',stroke='orange',parent='execution')
 f.edge('safety-review',[(1150,535),(1150,600)],'orange',source='safety',target='review')
 f.edge('safety-execute',[(1300,535),(1300,600)],'green',source='safety',target='execute')
 f.edge('safety-replan',[(1350,485),(1384,485),(1384,285),(1335,285),(1335,265)],'orange',True,source='safety',target='planner')
 
 f.edge('selected-planner',[(1015,665),(1052,665),(1052,215),(1090,215)],'green',source='selected',target='planner')
 f.panel('feedback',20,760,1380,140,'(d) Outcome verification and versioned feedback')
 for id,x,w,title,lines in [('outcome',1070,305,'Observe outcome',['Actual response + tool trace']),('attribute',620,380,'Verify & attribute',['Check evidence; attribute errors']),('update',40,510,'Revise experience record',['Update conditions / version / evidence link'])]:
  f.box(id,x,810,w,75,title,lines,parent='feedback')
 f.edge('outcome-attribute',[(1070,848),(1000,848)],'blue',True,source='outcome',target='attribute')
 f.edge('attribute-update',[(620,848),(550,848)],'green',True,source='attribute',target='update')
 f.edge('action-outcome',[(1310,670),(1310,810)],'blue',True,source='execute',target='outcome')
 f.edge('update-memory',[(40,848),(8,848),(8,720),(700,720),(700,700)],'green',True,source='update',target='memory')
 f.text('legend',20,920,1380,25,'Solid: task / tool flow  |  Dashed: blue = observations; green = verified updates; orange = rejected plan',20,color='muted')
 f.save()

def mechanism():
 f=Figure('experience-validity-detail','Experience applicability: a gate before relevance ranking',850)
 f.panel('records',20,110,385,600,'(a) Candidate records')
 f.box('current',40,175,345,85,'Current query',['Task k; regime A; time t'],parent='records')
 for i,(title,lines,col) in enumerate([('E1  Compatible case',['Regime A; current; checked','Relevance: high'],'green'),('E2  Similar but expired',['Regime A; superseded rule','Relevance: high'],'orange'),('E3  Missing evidence',['Regime unknown; current','Relevance: moderate'],'orange')]):
  f.box('experience-'+str(i),40,295+i*125,345,105,title,lines,fill='white',stroke=col,parent='records')
 f.text('record-schema',40,678,340,25,'Record = context + action + evidence',20,parent='records')
 f.panel('gate',440,110,520,600,'(b) Three-valued condition gate',True)
 f.text('predicate-label',460,175,480,28,'All required checks must be supported',22,True,parent='gate')
 headers=['Regime','Fresh','Limits'];values=[['YES','YES','YES'],['YES','NO','YES'],['?','YES','YES']]
 for j,title in enumerate(headers):f.text(f'col-{j}',535+j*120,235,125,28,title,21,True,parent='gate',align='center')
 for i in range(3):
  f.text('row-'+str(i),460,292+i*74,65,45,'E'+str(i+1),22,True,parent='gate')
  for j in range(3):
   t=values[i][j];fc='mint' if t=='YES' else ('sand' if t=='?' else 'light');sc='green' if t=='YES' else ('orange' if t=='?' else 'gray')
   f.rect(f'matrix-{i}-{j}',535+j*120,287+i*74,105,60,fc,sc,'gate',6);f.text(f'matrix-label-{i}-{j}',535+j*120,287+i*74,105,60,t,22,True,parent='gate',align='center')
 f.text('gate-output-label',912,235,36,28,'g',21,True,parent='gate',align='center')
 for i,v in enumerate(['1','0','0']):
  y=297+i*74
  f.rect('gate-output-'+str(i),912,y,36,40,'mint' if i==0 else 'sand','green' if i==0 else 'orange','gate',4)
  f.text('gate-output-text-'+str(i),912,y,36,40,v,21,True,parent='gate',align='center')
  f.edge('row-g-'+str(i),[(880,y+20),(912,y+20)],'green' if i==0 else 'orange')
 f.box('predicate',460,545,480,90,'Admissibility predicate',['g(e,c) = 1 iff every check = YES','NO or ? → do not automatically reuse'],fill='white',stroke='green',parent='gate')
 f.text('rank',460,658,480,28,'Rank by relevance only within {e : g(e,c)=1}',20,True,parent='gate')
 for i,y in enumerate([347,472,597]):
  f.edge('candidate-bus-'+str(i),[(385,y),(423,y)],'blue',source='experience-'+str(i))
 f.line('candidate-spine',[(423,347),(423,597)],'blue')
 f.edge('candidates-gate',[(423,475),(440,475)],'blue',target='gate')
 f.edge('current-conditions',[(385,217),(440,217)],'blue',source='current',target='gate')
 f.panel('decision',995,110,405,600,'(c) Decisions & updates')
 f.box('reuse',1015,175,365,95,'E1  Eligible for planning',['Reuse with provenance','Then apply execution constraints'],fill='mint',stroke='green',parent='decision')
 f.box('exclude',1015,310,365,75,'E2  Exclude expired version',['Keep history for audit'],fill='white',stroke='gray',parent='decision')
 f.box('verify',1015,425,365,95,'E3  Request missing evidence',['Tool / operator verification','Unknown → hold until verified'],fill='sand',stroke='orange',parent='decision')
 f.box('version',1015,585,365,95,'Verified update → new version',['YES: reevaluate; NO: restrict scope','Unverified feedback cannot upgrade'],fill='white',stroke='blue',parent='decision')
 f.edge('yes-reuse',[(948,317),(974,317),(974,220),(1015,220)],'green',target='reuse')
 f.edge('no-exclude',[(948,391),(984,391),(984,348),(1015,348)],'ink',target='exclude')
 f.edge('unknown-verify',[(948,465),(1015,465)],'orange',target='verify')
 f.edge('verify-update',[(1200,520),(1200,585)],'orange',True,source='verify',target='version')
 f.edge('version-gate',[(1110,680),(1110,733),(700,733),(700,710)],'blue',True,source='version',target='gate')
 f.text('fixture-note',20,770,1380,28,'Illustrative gate: E1 passes; E2 is stale; E3 is unresolved. This example does not establish method novelty or effectiveness.',21,color='muted')
 f.text('legend',20,810,1380,25,'YES = supported;  NO = contradicted;  ? = missing evidence.  Verify feedback before changing validity.',20,color='muted')
 f.save()

if __name__=='__main__':
 overview();mechanism();print('Generated two editable SVG / draw.io figures and PDF / PNG exports.')
