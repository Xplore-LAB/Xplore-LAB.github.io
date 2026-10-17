#!/usr/bin/env python3
"""A row-aligned, editable SVG redesign from the original conceptual fixture."""
from pathlib import Path
import json,xml.etree.ElementTree as E,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'img/figures/paper-grade/v2';OUT.mkdir(parents=True,exist_ok=True)
INK='#243C4C';MUTED='#657782';LIGHT='#DAE2E6';TEAL='#137D72';PALE='#E9F4F1'
svg=E.Element('svg',xmlns='http://www.w3.org/2000/svg',width='180mm',height='121.76mm',viewBox='0 0 510 345',role='img')
E.SubElement(svg,'title').text='Context-dependent experience applicability'
E.SubElement(svg,'desc').text='Three candidate experiences are checked for regime, freshness and limits. Only E1 is eligible; E2 is expired and E3 needs evidence.'
def el(tag,parent=svg,**a):return E.SubElement(parent,tag,{k.replace('_','-'):str(v) for k,v in a.items()})
def group(id):return el('g',id=id)
def text(g,x,y,t,size=8.5,color=INK,weight=400,anchor='start',italic=False):
 n=el('text',g,x=x,y=y,fill=color,font_family='Liberation Sans,Arial,sans-serif',font_size=size,font_weight=weight,text_anchor=anchor)
 if italic:n.set('font-style','italic')
 n.text=t;return n

def line(g,x,y,X,Y,color=LIGHT,width=.7,dash=None):
 n=el('line',g,x1=x,y1=y,x2=X,y2=Y,stroke=color,stroke_width=width)
 if dash:n.set('stroke-dasharray',dash)
 return n

def path(g,d,color=INK,width=.9,fill='none'):
 return el('path',g,d=d,stroke=color,stroke_width=width,fill=fill,stroke_linecap='round',stroke_linejoin='round')
def arrow(g,x,y,X,Y,color=MUTED,width=.8):
 line(g,x,y,X-3.4,y,color,width)
 el('path',g,d=f'M{X-4.4} {Y-2.2} L{X} {Y} L{X-4.4} {Y+2.2}Z',fill=color)
def check(g,x,y,status,active=False):
 fc=TEAL if active else ('#EEF1F3' if status=='yes' else 'white')
 el('circle',g,cx=x,cy=y,r=7.6,fill=fc,stroke='none' if status=='yes' else '#A2ADB5',stroke_width=.7)
 if status=='yes':path(g,f'M{x-3.2} {y} l2.1 2.2 l4.3 -4.5','white' if active else '#657782',1.05)
 elif status=='no':
  path(g,f'M{x-2.5} {y-2.5} l5 5 M{x+2.5} {y-2.5} l-5 5',INK,1)
 else:text(g,x,y+3,'?',9.1,INK,600,'middle')
def doc(g,x,y,active):
 c=TEAL if active else '#82939E'
 path(g,f'M{x} {y} h16 l6 6 v24 h-22 Z',c,.8,'white')
 path(g,f'M{x+16} {y} v6 h6',c,.7)
 for j,w in enumerate([12,10,7]):line(g,x+4,y+12+5*j,x+4+w,y+12+5*j,c,.6)

el('rect',x=0,y=0,width=510,height=345,fill='white')
f=json.loads((OUT/'experience-validity-fixture.json').read_text())
head=group('stage-labels')
for letter,label,x in [('a','Candidate memory',18),('b','Applicability gate',190),('c','Decision',395)]:
 text(head,x,23,letter,10.5,INK,700);text(head,x+14,23,label,10.5,INK,600)
# Context is an input, rather than a fourth equal-weight stage.
q=group('current-context')
el('rect',q,x=190,y=43,width=182,height=36,rx=3,fill='#F4F6F7')
text(q,200,57,'Current context c(t)',8.1,INK,600)
text(q,200,70,f['context'],7.8,MUTED)
line(q,281,79,281,94,MUTED,.75)
el('path',q,d='M278.8 91 L281 95 L283.2 91Z',fill=MUTED)
text(q,18,63,'Retrieved by relevance',8.2,MUTED)
text(q,18,77,'Checked before reuse',8.2,MUTED)
headers=group('condition-headings')
for x,t in zip([218,261,304],f['conditions']):text(headers,x,112,t,8.2,MUTED,400,'middle')
text(headers,354,112,'g',8.5,MUTED,400,'middle',True)
line(headers,190,119,372,119,LIGHT,.65)
for i,r in enumerate(f['records']):
 y=148+i*63;g=group('record-'+r['id']);passed=all(s=='yes' for s in r['checks'])
 if passed:
  el('rect',g,x=185,y=y-24,width=189,height=48,rx=4,fill=PALE)
  el('rect',g,x=185,y=y-24,width=2.2,height=48,rx=1.1,fill=TEAL)
 doc(g,18,y-15,passed)
 text(g,50,y-5,r['id'],9.2,TEAL if passed else INK,700)
 text(g,70,y-5,r['label'],8.3,INK,400)
 text(g,50,y+10,r['detail'],7.7,MUTED)
 arrow(g,161,y,181,y,TEAL if passed else '#A5B1B8',.95 if passed else .65)
 for x,s in zip([218,261,304],r['checks']):check(g,x,y,s,passed)
 line(g,328,y-13,328,y+13,'#A5CFC6' if passed else LIGHT,.65)
 text(g,354,y+4,'1' if passed else '0',11,TEAL if passed else MUTED,700,'middle')
 arrow(g,375,y,391,y,TEAL if passed else '#A5B1B8',1.2 if passed else .65)
 # Decision icons have the same visual footprint; only the admissible row is accented.
 if passed:check(g,400,y-7,'yes',True)
 elif r['decision']=='Exclude':
  el('circle',g,cx=400,cy=y-7,r=7.6,fill='white',stroke='#A2ADB5',stroke_width=.7)
  path(g,f'M397.5 {y-9.5} l5 5 M402.5 {y-9.5} l-5 5',MUTED,.9)
 else:
  el('circle',g,cx=398.8,cy=y-8.3,r=5.2,fill='white',stroke=INK,stroke_width=.9)
  path(g,f'M402.5 {y-4.6} l4 4',INK,1)
 text(g,414,y-3,r['decision'],10.3,TEAL if passed else INK,600)
 text(g,393,y+12,r['action'],7.8,MUTED)
# Separate verification annotation from the main left-to-right gate computation.
foot=group('verification-note')
line(foot,393,295,494,295,LIGHT,.65)
text(foot,393,309,'Verified evidence',7.7,INK,600)
text(foot,393,321,'New version → recheck',7.7,MUTED)
line(foot,430,311,430,314,MUTED,.6)
formula=group('gate-definition')
text(formula,190,312,'Reuse only if every required check is supported.',8.1,INK,400)
text(formula,190,326,'g(e, c) = 1  ⇔  all checks = supported',8.1,MUTED,400)
text(formula,18,326,'Conceptual example',7.5,MUTED)
E.indent(svg);p=OUT/'experience-validity-v2.svg';E.ElementTree(svg).write(p,encoding='utf-8',xml_declaration=True)
for typ in ['pdf','png']:
 cmd=['inkscape',str(p),f'--export-type={typ}',f'--export-filename={p.with_suffix("."+typ)}']
 if typ=='png':cmd+=['--export-width=2400']
 subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print('Built grouped SVG, vector PDF and PNG preview.')
