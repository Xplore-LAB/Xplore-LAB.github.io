#!/usr/bin/env python3
"""Editable conceptual schematics; no measured data or external artwork."""
from pathlib import Path
import xml.etree.ElementTree as E
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'img/figures/paper-grade/v3'
INK, GRAY, LINE = '#223442', '#526672', '#D6DFE3'
TEAL, PALE, BG = '#087F78', '#EAF5F2', '#F4F6F7'

class Figure:
    def __init__(self, name, height, title):
        self.name = name
        self.root = E.Element('svg', xmlns='http://www.w3.org/2000/svg',
            width='180mm', height=f'{height/5}mm', viewBox=f'0 0 900 {height}', role='img')
        E.SubElement(self.root, 'title').text = title
        E.SubElement(self.root, 'desc').text = 'Conceptual example; not experimental evidence. Live text and grouped vector geometry.'
        self.g = self.root
        self.box(0, 0, 900, height, 'white', stroke='none', radius=0)
    def el(self, tag, **a):
        return E.SubElement(self.g, tag, {k.replace('_','-'):str(v) for k,v in a.items()})
    def group(self, id):
        self.g = E.SubElement(self.root, 'g', id=id)
    def text(self,x,y,s,size=16,color=INK,weight=400,anchor='start'):
        self.el('text',x=x,y=y,font_family='Liberation Sans, Arial, sans-serif',font_size=size,
                font_weight=weight,fill=color,text_anchor=anchor).text=s
    def box(self,x,y,w,h,fill=BG,stroke='none',radius=6):
        self.el('rect',x=x,y=y,width=w,height=h,rx=radius,fill=fill,stroke=stroke,stroke_width=1)
    def path(self,d,c=GRAY,w=1.5,dash=None):
        a=dict(d=d,fill='none',stroke=c,stroke_width=w,stroke_linecap='round',stroke_linejoin='round')
        if dash:a['stroke_dasharray']=dash
        self.el('path',**a)
    def arrow(self,x,y,X,Y,c=GRAY,w=1.7):
        self.path(f'M{x} {y} L{X} {Y}',c,w)
        if Y==y:
            k=1 if X>x else -1
            self.el('path',d=f'M{X-7*k} {Y-3.5} L{X} {Y} L{X-7*k} {Y+3.5} Z',fill=c)
        else:
            k=1 if Y>y else -1
            self.el('path',d=f'M{X-3.5} {Y-7*k} L{X} {Y} L{X+3.5} {Y-7*k} Z',fill=c)
    def check(self,x,y,state,accent=False):
        self.el('circle',cx=x,cy=y,r=9,fill=TEAL if accent else 'white',stroke=TEAL if accent else LINE,stroke_width=1.2)
        c='white' if accent else GRAY
        if state==1:self.path(f'M{x-4} {y} l3 3 l5 -6',c,1.8)
        elif state==0:self.path(f'M{x-3} {y-3} l6 6 m0 -6 l-6 6',c,1.6)
        else:self.text(x,y+5,'?',16,GRAY,600,'middle')
    def finish(self):
        OUT.mkdir(parents=True,exist_ok=True)
        E.indent(self.root)
        p=OUT/(self.name+'.svg')
        E.ElementTree(self.root).write(p,encoding='utf-8',xml_declaration=True)
        for ext in ['pdf','png']:
            cmd=['inkscape',str(p),f'--export-filename={p.with_suffix("."+ext)}']
            if ext=='png':cmd+=['--export-width=2400']
            subprocess.run(cmd,check=True,capture_output=True)

def overview():
    f=Figure('industrial-agent-v3',480,'Industrial agent: check experience before planning')
    f.group('headings')
    for x,n,t in [(24,'a','Observe'),(246,'b','Check before reuse'),(660,'c','Plan & validate')]:
        f.text(x,32,n,20,TEAL,700);f.text(x+25,32,t,20,INK,600)
    # Process stays subordinate; no invented numerical measurements.
    f.group('process-context')
    f.text(24,77,'Operating context',17,INK,600)
    f.text(24,103,'Regime A · time t',16,GRAY)
    f.box(24,125,78,45,'white',LINE);f.text(63,153,'Feed',16,INK,400,'middle')
    f.box(130,125,78,45,'white',LINE);f.text(169,153,'Unit',16,INK,400,'middle')
    f.arrow(102,147,130,147)
    f.path('M30 211 H198 M30 211 V184',LINE,1)
    f.path('M31 199 C55 181 72 211 94 197 S130 179 149 194 S180 204 198 187',GRAY,1.8)
    f.text(24,242,'Observed trends',16,GRAY)
    f.text(24,269,'Limits + provenance',16,GRAY)
    f.text(24,306,'Task + context',16,INK,600)
    f.text(24,329,'Query for retrieval',16,GRAY)
    f.path('M205 313 H232 V92 H246',TEAL,1.7)
    f.arrow(232,92,246,92,TEAL,1.7)
    # Hero region: the decisive distinction is suitability, not a larger box graph.
    f.group('applicability-gate')
    f.box(246,53,382,282,PALE,radius=8)
    f.text(264,81,'Retrieve candidates',17,INK,600)
    f.text(264,107,'Check regime, freshness and limits',16,GRAY)
    f.text(264,144,'Experience',16,GRAY)
    f.text(447,144,'Relevant',16,GRAY,400,'middle')
    f.text(566,144,'Applicable',16,TEAL,600,'middle')
    f.path('M264 154 H610', '#C4DDD7',1)
    for y,label,status,gate in [(181,'E1  Compatible',1,'YES'),(222,'E2  Expired',0,'NO'),(263,'E3  Unresolved',None,'?')]:
        f.text(264,y+5,label,16,INK,600 if status==1 else 400)
        f.text(447,y+5,'High' if status is not None else 'Moderate',16,GRAY,400,'middle')
        f.check(529,y,status,status==1)
        f.text(570,y+5,gate,16,TEAL if status==1 else GRAY,600,'middle')
    f.box(264,286,346,33,TEAL,radius=4)
    f.text(437,308,'Rank only admissible experiences',16,'white',600,'middle')
    f.group('planner-and-tools')
    f.path('M610 303 H644 V87 H660',TEAL,2)
    f.arrow(644,87,660,87,TEAL,2)
    f.box(660,60,216,54,'white',LINE)
    f.text(768,83,'LLM planner',17,INK,600,'middle')
    f.text(768,104,'Task + selected E1',16,GRAY,400,'middle')
    f.path('M768 114 V122 H709 M768 122 H824',GRAY,1.3)
    f.arrow(709,122,709,132)
    f.arrow(824,122,824,132)
    f.box(660,132,99,40,BG);f.text(709,157,'Inspect',16,INK,400,'middle')
    f.box(773,132,103,40,BG);f.text(824,157,'Simulate',16,INK,400,'middle')
    # Main candidate-context connection enters the planner, not the execution branch.
    f.path('M709 172 V190 H824 V172',GRAY,1.3)
    f.arrow(768,190,768,207)
    f.box(660,208,216,44,'white',LINE)
    f.text(768,235,'Constraint check',17,INK,600,'middle')
    f.path('M768 252 V264 H711 M768 264 H825',GRAY,1.3)
    f.arrow(711,264,711,280,GRAY,1.3)
    f.arrow(825,264,825,280,TEAL,1.6)
    f.box(660,280,102,52,BG);f.text(711,301,'Review',16,INK,400,'middle')
    f.box(774,280,102,52,TEAL);f.text(825,301,'Execute',16,'white',600,'middle')
    f.text(711,320,'uncertain',14.2,GRAY,400,'middle')
    f.text(825,320,'approved',14.2,'white',400,'middle')
    f.path('M876 230 H888 V87 H877',GRAY,1.2)
    f.arrow(888,87,877,87,GRAY,1.2)
    f.text(660,349,'Reject → replan',14.2,GRAY)
    # Outcome verification is separate from observations and preserves version history.
    f.group('verified-feedback')
    f.path('M825 332 V383',GRAY,1.3,'5 4')
    f.arrow(825,376,825,387,GRAY,1.3)
    f.path('M24 358 H772',LINE,1)
    f.text(24,386,'d',20,TEAL,700)
    f.text(49,386,'Verified feedback',18,INK,600)
    f.text(876,406,'Observe outcome',16,INK,600,'end')
    f.arrow(729,400,619,400)
    f.text(504,406,'Verify & attribute',16,INK,600,'middle')
    f.arrow(390,400,355,400)
    f.text(281,406,'Version record',16,INK,600,'middle')
    f.path('M281 387 V350 H437',TEAL,1.4,'5 4')
    f.arrow(437,350,437,335,TEAL,1.4)
    f.text(24,458,'Conceptual design · illustrative context and records · no experimental results',14.2,GRAY)
    f.finish()

def detail():
    f=Figure('experience-validity-v3',310,'Applicability gate: relevance alone does not justify reuse')
    f.group('context')
    f.text(24,31,'Applicability gate',21,INK,600)
    f.text(876,31,'Current context: regime A · time t · limits',16,GRAY,400,'end')
    f.group('column-labels')
    for x,label,anchor in [(24,'Candidate experience','start'),(419,'Regime','middle'),(512,'Fresh','middle'),(605,'Limits','middle'),(682,'g','middle'),(736,'Decision','start')]:
        f.text(x,77,label,16,GRAY,400,anchor)
    f.path('M24 88 H876',LINE,1)
    rows=[('E1','Compatible case','Current; supported',(1,1,1),'Reuse',True),
          ('E2','Expired rule','Similar; superseded',(1,0,1),'Exclude',False),
          ('E3','Missing evidence','Regime unknown',(None,1,1),'Verify',False)]
    for i,(id,label,sub,checks,result,active) in enumerate(rows):
        y=119+i*57
        f.group('record-'+id)
        if active:f.box(16,y-23,868,51,PALE,radius=5)
        f.text(28,y+2,id,17,TEAL if active else INK,700)
        f.text(68,y+2,label,17,INK,600 if active else 400)
        f.text(68,y+22,sub,14.2,GRAY)
        for x,s in zip([419,512,605],checks):f.check(x,y,s,active)
        f.text(682,y+6,'1' if active else '0',18,TEAL if active else GRAY,600,'middle')
        f.arrow(707,y,726,y,TEAL if active else GRAY,1.6)
        f.text(740,y+6,result,18,TEAL if active else INK,600)
    f.group('gate-definition')
    f.path('M24 263 H876',LINE,1)
    f.text(24,285,'Reuse iff all checks are supported; otherwise exclude or request evidence.',16,INK)
    f.text(24,306,'Conceptual example · verified evidence creates a new version and triggers rechecking.',14.2,GRAY)
    f.finish()

if __name__=='__main__':
    overview()
    detail()
    print(OUT)
