#!/usr/bin/env python3
"""Reproduce reviewed crops of P1–P10 from supplied source PDFs (no downloads).
Usage: python3 scripts/extract_reference_originals.py --pdf-dir /path/to/pdfs
Requires PyMuPDF. Bounds are PDF points, top-left origin; page numbers are 1-based.
"""
import argparse,hashlib,json,re,zipfile
from pathlib import Path
import fitz
SITE=Path(__file__).resolve().parents[1]
OUT=SITE/'img/figures/originals'
# Deliberately reviewed rectangles rather than automatic 'first image' extraction:
# PDF figures commonly mix vectors, text and multiple embedded bitmap objects.
FIGURES=[
('instructgpt','InstructGPT','2203.02155','2',3,[106,63,506,300],'https://arxiv.org/pdf/2203.02155','原图三阶段横排，包含标注员、模型训练和采样；重绘仅保留阶段骨架。'),
('bert','BERT','1810.04805','1',3,[72,66,526,250],'https://aclanthology.org/N19-1423.pdf','原图含预训练任务头和多个微调任务；重绘只保留双阶段关系。'),
('transformer','Transformer','1706.03762','1',3,[190,62,423,399],'https://arxiv.org/pdf/1706.03762','原图保留完整编解码子层、残差与归一化；重绘压缩了这些结构。'),
('clip','CLIP','2103.00020','1',2,[53,64,545,245],'https://proceedings.mlr.press/v139/radford21a/radford21a.pdf','原图还含文本构造分类器和零样本预测两步；重绘主要展示对比训练。'),
('ddpm','DDPM','2006.11239','2',2,[158,68,455,122],'https://arxiv.org/pdf/2006.11239','原图 xT 在左、x0 在右；生成方向向右、加噪方向向左。重绘改变了状态排列，不能照搬其方向说明。'),
('vit','Vision Transformer','2010.11929','1',3,[130,75,480,256],'https://arxiv.org/pdf/2010.11929','原图同时展开 Transformer Encoder 内部与分类头；重绘强调 patch 转 token。'),
('gpt3','GPT-3','2005.14165','3.8',20,[71,65,543,290],'https://arxiv.org/pdf/2005.14165','选用 Figure 3.8：左图是模型规模，右图是上下文示例数。原图是两个面板；重绘多任务曲线并非逐点复现，示意数值不可当作原论文结果。'),
('dpo','DPO','2305.18290','1',2,[106,69,507,154],'https://arxiv.org/pdf/2305.18290','原图 RLHF 与 DPO 左右并排；重绘改为上下两行。原图包含采样与奖励计算回路。'),
('switch','Switch Transformer','2101.03961','2',4,[90,86,523,297],'https://www.jmlr.org/papers/volume23/21-0998/21-0998.pdf','原图左侧是编码器模块定位，右侧展开稀疏 FFN；左侧不是密集 FFN 对照。每个 token 选一个专家，两个 token 可选择不同专家。'),
('cot','Chain-of-Thought','2201.11903','1',1,[115,450,501,642],'https://arxiv.org/pdf/2201.11903','原图包含网球示例和食堂测试题两组输入输出；重绘只保留提示对照。原图最终答案为 27 与 9。')]
def build(pdf_dir):
 OUT.mkdir(parents=True,exist_ok=True)
 html=(SITE/'figures.html').read_text()
 manifest=[]
 for i,(slug,title,aid,num,pno,bounds,url,note) in enumerate(FIGURES,1):
  source=pdf_dir/(slug+'.pdf'); doc=fitz.open(source);page=doc[pno-1];clip=fitz.Rect(bounds)
  captions=[b[4].strip() for b in page.get_text('blocks') if re.match(r'^Figure\s+'+re.escape(num)+r'\s*[:.]',b[4].strip())]
  assert captions, (slug,'caption not found')
  png=OUT/(slug+'.png');page.get_pixmap(clip=clip,dpi=300,alpha=False).save(png)
  cropped=fitz.open();outpage=cropped.new_page(width=clip.width,height=clip.height)
  outpage.show_pdf_page(outpage.rect,doc,pno-1,clip=clip)
  cropped.set_metadata({'title':title+' — Figure '+num,'subject':'Unmodified figure region extracted from source PDF','author':'Original paper authors','keywords':aid})
  cropped.save(OUT/(slug+'.pdf'),garbage=4,deflate=True)
  card=re.search(r'<details id="c-p'+str(i)+r'".*?(?=<details id="c-p|<section|<h2)',html,re.S)
  assert card,slug
  svg=re.search(r'<svg\b.*?</svg>',card.group(),re.S).group()
  (OUT/(slug+'-redraw.svg')).write_text(svg)
  pix=fitz.Pixmap(png)
  manifest.append(dict(case='P'+str(i),slug=slug,title=title,arxiv_id=aid,figure=num,pdf_page=pno,source_url=url,source_pdf_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),crop_pdf_points=bounds,dpi=300,width=pix.width,height=pix.height,caption=captions[0],comparison_note=note,png=slug+'.png',pdf=slug+'.pdf',redraw=slug+'-redraw.svg',method='PDF region rendering; original text, vectors and images retained; no redrawing',rights='Original figure copyright belongs to the paper rights holders; site code license does not apply.'))
 (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 return manifest
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--pdf-dir',type=Path,required=True);args=ap.parse_args();m=build(args.pdf_dir);print('Extracted',len(m),'reviewed figure regions at 300 dpi')
