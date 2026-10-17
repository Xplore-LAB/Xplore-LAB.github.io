#!/usr/bin/env python3
"""Check vector/editable deliverables; not a scientific validity test."""
from pathlib import Path
import xml.etree.ElementTree as E,json
from PIL import ImageFont
import pymupdf
R=Path(__file__).resolve().parents[1];D=R/'img/figures/paper-grade';S='{http://www.w3.org/2000/svg}'
report=[];proof=pymupdf.open()
for slug in ['industrial-agent-full','experience-validity-detail']:
 svg=E.parse(D/(slug+'.svg')).getroot();mx=E.parse(D/(slug+'.drawio')).getroot();cells=mx.findall('.//mxCell');ids={c.get('id') for c in cells};errors=[]
 texts={e.get('id'):''.join(e.itertext()).strip() for e in svg.iter(S+'text')}
 for c in cells:
  if c.get('value') and c.get('value')!=texts.get(c.get('id')):errors.append('SVG/draw.io label mismatch '+c.get('id'))
  if c.get('edge'):
   for k in ['source','target']:
    if c.get(k) and c.get(k) not in ids:errors.append('broken edge '+c.get('id'))
 assert not list(svg.iter(S+'image')),'SVG contains raster image'
 for e in json.loads((D/(slug+'-layout.json')).read_text()):
  fn='/usr/share/fonts/truetype/liberation/LiberationSans-'+('Bold' if e['bold'] else 'Regular')+'.ttf'
  width=ImageFont.truetype(fn,e['size']).getlength(e['text'])
  if width>e['w']+1:errors.append('text exceeds planned width: '+e['id'])
 pdf=pymupdf.open(D/(slug+'.pdf'));assert len(pdf)==1 and not pdf[0].get_images()
 spans=[s for b in pdf[0].get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']];minpt=min(s['size'] for s in spans);assert minpt>=7.2
 assert not errors,errors
 page=proof.new_page(width=595.28,height=841.89);page.insert_text((39,50),slug,fontname='hebo',fontsize=12)
 h=pdf[0].rect.height;page.show_pdf_page(pymupdf.Rect(39,80,39+pdf[0].rect.width,80+h),pdf,0)
 page.insert_text((39,80+h+28),'182 mm width / A4 reading proof / not a conference template',fontsize=9)
 report.append(dict(slug=slug,native_texts=len(texts),native_drawio_cells=len(cells),drawio_edges=sum(c.get('edge')=='1' for c in cells),pdf_raster_images=0,min_font_pt=round(minpt,2),checks='pass'))
proof.save(D/'print-proof.pdf');(D/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
