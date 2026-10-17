#!/usr/bin/env python3
"""Native PDF text/geometry checks and a real editable-SVG export test."""
from pathlib import Path
import json, subprocess, tempfile, xml.etree.ElementTree as E
import pymupdf as fitz

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'img/figures/paper-grade/v3'
def spans(page):
    return [s for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
report={}
for name in ['industrial-agent-v3','experience-validity-v3']:
    source=OUT/(name+'.svg')
    doc=fitz.open(OUT/(name+'.pdf'));page=doc[0];ss=spans(page)
    overlaps=[]
    for i,a in enumerate(ss):
        for b in ss[i+1:]:
            r=fitz.Rect(a['bbox']) & fitz.Rect(b['bbox'])
            if not r.is_empty and r.width>1 and r.height>1:overlaps.append([a['text'],b['text']])
    outside=[s['text'] for s in ss if not page.rect.contains(fitz.Rect(s['bbox']))]
    tree=E.parse(source);root=tree.getroot();ns={'s':'http://www.w3.org/2000/svg'}
    texts=root.findall('.//s:text',ns)
    with tempfile.TemporaryDirectory(prefix='figure-v3-edit-') as tmp:
        edited=Path(tmp)/'edited.svg';pdf=Path(tmp)/'edited.pdf'
        target=next(t for t in texts if t.text=='E2  Expired' or t.text=='Expired rule')
        target.text='E2 edited' if name.startswith('industrial') else 'Edited rule'
        group=root.find("s:g[@id='record-E2']",ns)
        if group is None:group=root.find("s:g[@id='applicability-gate']",ns)
        group.set('transform','translate(1,0)')
        tree.write(edited,encoding='utf-8',xml_declaration=True)
        subprocess.run(['inkscape',str(edited),f'--export-filename={pdf}'],check=True,capture_output=True)
        edited_doc=fitz.open(pdf)
        edit_pass=target.text in edited_doc[0].get_text()
    audit=subprocess.run(['python3',str(Path.home()/'.codex/skills/nature-figure/scripts/audit_svg_schematic.py'),str(source),'--min-pt','8','--max-pt','13','--max-width-mm','180','--json'],capture_output=True,text=True)
    svg_audit=json.loads(audit.stdout)
    report[name]={'native_text_spans':len(ss),'raster_images':len(page.get_images()),
        'overlapping_native_spans':overlaps,'outside_canvas':outside,'actual_edit_and_pdf_export':edit_pass,
        'svg_audit':svg_audit,'visual_review':'Author self-review completed; user acceptance pending'}
    assert not overlaps and not outside and edit_pass and not page.get_images() and audit.returncode==0
report['scientific_scope']='Original conceptual fixture; not experimental results or evidence of safety.'
report['submission_scope']='180 mm provisional width; no specific venue/year compliance claimed.'
report['collision_tool_triage']={
    'raw_reports':['overview-collision.json','detail-collision.json'],
    'overview':'Five FAIL and one WARN: trace unions merge Observed trends with Limits + provenance, subtitle with column headers, and the separate question marks. Native span rectangles have no overlaps; rendered PNG checked for line/text contact. All six findings reviewed as false positives.',
    'detail':'Seven FAIL: one unioned trace bbox spans both heading and all table headers. Native spans show no overlaps. All seven findings reviewed as false positives.',
    'status':'Raw tool verdict retained; not claimed to be an automated clean pass.'}
(OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Native text bounds, no-raster checks and actual editable-SVG export tests passed for both figures.')
