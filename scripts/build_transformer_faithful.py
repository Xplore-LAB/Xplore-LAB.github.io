#!/usr/bin/env python3
"""Hand-built editable reconstruction of Attention Is All You Need, Figure 1.
All geometry is native SVG; no embedded source image or traced glyph outlines.
Run from the site's scripts directory; exports through Inkscape.
"""
from pathlib import Path
import xml.etree.ElementTree as E
import subprocess,json,base64,io
SITE=Path(__file__).resolve().parents[1]
OUT=SITE/'img/figures/transformer-faithful'
NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
def node(parent,tag,**attrs):
 return E.SubElement(parent,'{'+NS+'}'+tag,{k.replace('_','-'):str(v) for k,v in attrs.items()})
class Drawing:
 def __init__(self):
  self.root=E.Element('{'+NS+'}svg',dict(width='120mm',height=f'{120*1405/972:.6f}mm',viewBox='0 0 972 1405',role='img'))
  node(self.root,'title').text='Transformer — faithful editable reconstruction of Figure 1'
  node(self.root,'desc').text='Reconstructed from Attention Is All You Need (Vaswani et al., 2017), Figure 1, PDF page 3. Original architecture, label order, residual paths, pastel colors and layout retained. Native editable SVG geometry and text; no embedded bitmap. Roboto Light is used to approximate the original typography. Reconstruction is not pixel-identical to the original.'
  defs=node(self.root,'defs')
  # Concave, long-tip arrowhead matches the source's characteristic arrows.
  m=node(defs,'marker',id='arrowhead',viewBox='0 0 18 16',refX=17,refY=8,markerWidth=18,markerHeight=16,orient='auto',markerUnits='userSpaceOnUse')
  node(m,'path',d='M0 0 L18 8 L0 16 L4.2 8 Z',fill='#000')
  self.layer=self.root
  node(self.root,'rect',x=0,y=0,width=972,height=1405,fill='white')
 def group(self,id): self.layer=node(self.root,'g',id=id)
 def shape(self,tag,**kwargs): return node(self.layer,tag,**kwargs)
 def path(self,d,arrow=False,width=5.2,**kwargs):
  attrs=dict(d=d,fill='none',stroke='#000',stroke_width=width,stroke_linecap='butt',stroke_linejoin='round',**kwargs)
  if arrow:attrs['marker_end']='url(#arrowhead)'
  return self.shape('path',**attrs)
 def text(self,x,y,lines,size=32,anchor='middle'):
  if isinstance(lines,str):lines=[lines]
  t=self.shape('text',x=x,y=y,font_family='Roboto, Helvetica, Arial, sans-serif',font_size=size,font_weight=300,text_anchor=anchor,fill='#000')
  for i,line in enumerate(lines):node(t,'tspan',x=x,dy=0 if i==0 else size*1.2).text=line
  return t
 def box(self,id,x,y,w,h,fill,lines,size=31):
  self.group(id);self.shape('rect',x=x,y=y,width=w,height=h,rx=7,fill=fill,stroke='#000',stroke_width=5.2)
  if isinstance(lines,str):lines=[lines]
  # Match source baselines, with the visual text block centered in the box.
  self.text(x+w/2,y+h/2 + size*.34 - (len(lines)-1)*size*.6 - 2,lines,size)
 def finish(self):
  OUT.mkdir(parents=True,exist_ok=True)
  # Embed a label-only font subset so SVG image previews use the same face.
  from fontTools import subset
  from fontTools.ttLib import TTFont
  font=TTFont(OUT/'Roboto-Light.ttf');options=subset.Options();sub=subset.Subsetter(options=options)
  sub.populate(text=''.join(e.text or '' for e in self.root.iter() if e.tag.endswith(('text','tspan'))));sub.subset(font)
  font.flavor='woff2';buf=io.BytesIO();font.save(buf)
  embedded=base64.b64encode(buf.getvalue()).decode()
  node(self.root,'style').text="@font-face {font-family:'Roboto';font-style:normal;font-weight:300;src:url(data:font/woff2;base64,"+embedded+") format('woff2');}"
  E.indent(self.root);p=OUT/'transformer-faithful.svg';E.ElementTree(self.root).write(p,encoding='utf-8',xml_declaration=True)
  for ext in ['png','pdf']:
   cmd=['inkscape',str(p),f'--export-filename={p.with_suffix("."+ext)}']
   if ext=='png':cmd+=['--export-width=1944']
   subprocess.run(cmd,check=True,capture_output=True)
  print(p)
def build():
 family=subprocess.run(['fc-match','-f','%{family}','Roboto:weight=light'],check=True,capture_output=True,text=True).stdout
 if 'Roboto' not in family:raise RuntimeError('Install the bundled Roboto-Light.ttf before PDF/PNG export; font substitution would change the reconstruction.')
 f=Drawing()
 # Structural backgrounds. Encoding and decoding stacks contain one repeated block.
 f.group('encoder-stack');f.shape('rect',x=131.5,y=545.5,width=323,height=469,rx=28,fill='#f3f3f4',stroke='#000',stroke_width=5.2)
 f.group('decoder-stack');f.shape('rect',x=512,y=326.5,width=316,height=688,rx=30,fill='#f3f3f4',stroke='#000',stroke_width=5.2)
 # Inter-module vertical paths, positioned below nodes in painter order.
 f.group('encoder-main-stream')
 for y0,y1 in [(1285,1222),(1131,1099),(1060,934),(841,832),(788,712),(620,611)]:f.path(f'M321 {y0} V{y1}',abs(y0-y1)>20)
 f.group('decoder-main-stream')
 for y0,y1 in [(1285,1222),(1131,1103),(1066,932),(806,798),(753,678),(588,576),(533,492),(401,390),(345,297),(251,213),(168,128)]:f.path(f'M645 {y0} V{y1}',abs(y0-y1)>20)
 # Encoder residual paths: input to self-attention Add&Norm; FFN input to upper Add&Norm.
 f.group('encoder-self-attention-residual');f.path('M321 992 H176 Q155 992 155 971 V835 Q155 811 179 811 H210',True)
 f.group('encoder-feed-forward-residual');f.path('M321 750 H177 Q155 750 155 728 V613 Q155 589 178 589 H210',True)
 # Three Q/K/V arrows into encoder self-attention.
 f.group('encoder-self-attention-qkv');f.path('M321 964 H262 Q241 964 241 943 V934',True);f.path('M321 964 H379 Q400 964 400 943 V934',True)
 # Decoder input Q/K/V fan-out and the three independent residual returns.
 f.group('decoder-masked-attention-qkv');f.path('M645 964 H586 Q565 964 565 944 V934',True);f.path('M645 964 H705 Q725 964 725 944 V934',True)
 f.group('decoder-masked-attention-residual');f.path('M645 993 H783 Q806 993 806 970 V800 Q806 776 782 776 H756',True)
 f.group('decoder-cross-attention-residual');f.path('M645 736 H782 Q805 736 805 713 V579 Q805 555 782 555 H756',True)
 f.group('decoder-feed-forward-residual');f.path('M645 521 H782 Q805 521 805 497 V390 Q805 365 782 365 H756',True)
 # Encoder output supplies K and V; masked-decoder output supplies Q.
 # Original routes intentionally enter at left/center/right rather than semantic QKV labels.
 f.group('encoder-output-to-decoder-kv')
 f.path('M321 568 V541 Q321 518 344 518 H461 Q485 518 485 542 V689 Q485 713 509 713 H542 Q565 713 565 689 V678',True)
 f.path('M509 713 H623 Q645 713 645 690 V678',True)
 f.group('decoder-query-to-cross-attention');f.path('M645 753 V735 Q645 712 668 712 H703 Q725 712 725 690 V678',True)
 # Nodes from the source, retaining exact labels and all five Add&Norm stages.
 for id,x,y,w,h,color,label in [
  ('input-embedding',212.5,1133,217,87,'#fce0e1',['Input','Embedding']),
  ('output-embedding',537,1133,216,87,'#fce0e1',['Output','Embedding']),
  ('encoder-self-attention',212.5,843,217,87,'#ffe2bb',['Multi-Head','Attention']),
  ('encoder-self-attention-add-norm',212.5,790,217,42,'#f2f4c1','Add & Norm'),
  ('encoder-feed-forward',212.5,622,217,87,'#c2e8f7',['Feed','Forward']),
  ('encoder-feed-forward-add-norm',212.5,569,217,41,'#f2f4c1','Add & Norm'),
  ('decoder-masked-self-attention',537,807,216,123,'#ffe2bb',['Masked','Multi-Head','Attention']),
  ('decoder-masked-self-attention-add-norm',537,754,216,42,'#f2f4c1','Add & Norm'),
  ('decoder-cross-attention',537,589,216,87,'#ffe2bb',['Multi-Head','Attention']),
  ('decoder-cross-attention-add-norm',537,534,216,41,'#f2f4c1','Add & Norm'),
  ('decoder-feed-forward',537,401,216,87,'#c2e8f7',['Feed','Forward']),
  ('decoder-feed-forward-add-norm',537,346,216,41,'#f2f4c1','Add & Norm'),
  ('linear-projection',537,253,216,40,'#dbdfef','Linear'),
  ('softmax',537,169,216,40,'#cce7cf','Softmax')]:f.box(id,x,y,w,h,color,label)
 # Position addition and sinusoidal positional encoding icons.
 for side,cx,cy,ix in [('input',321,1078,236),('output',645,1083,730)]:
  f.group(side+'-position-addition');f.shape('circle',cx=cx,cy=cy,r=16,fill='white',stroke='black',stroke_width=3)
  f.path(f'M{cx-11} {cy} H{cx+11} M{cx} {cy-11} V{cy+11}',width=2.7)
  f.group(side+'-positional-encoding');f.shape('circle',cx=ix,cy=cy,r=35,fill='white',stroke='black',stroke_width=3)
  if side=='input':
   f.path('M202 1078 C207 1054 237 1055 237 1079 C237 1101 263 1101 270 1078',width=3)
   f.path('M271 1078 H304',width=4.8)
  else:
   f.path('M695 1083 C701 1060 730 1060 730 1084 C730 1107 757 1106 764 1083',width=3)
   f.path('M662 1083 H695',width=4.8)
 f.group('stack-multiplicity');f.text(76,809,'N×',36);f.text(882,696,'N×',36)
 f.group('input-output-labels');f.text(321,1332,'Inputs',36);f.text(645,1332,['Outputs','(shifted right)'],36);f.text(645,74,['Output','Probabilities'],36)
 f.group('positional-encoding-labels');f.text(26,1066,['Positional','Encoding'],36,'start');f.text(786,1072,['Positional','Encoding'],36,'start')
 f.finish()
if __name__=='__main__':build()
