"""Update source-derived coordinates for five workbench cases.

Run from the site root with Python 3 and Poppler's pdftocairo installed.
Pass a directory of cached SVGs to reproduce without downloading again.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve

DATA = Path(__file__).resolve().parents[1] / '_data/workbench_paper_data.json'
ASSET_URLS = {
    'r10': 'https://arxiv.org/html/2501.12948v2/plot_aime_with_maj.svg',
    'r11': 'https://arxiv.org/html/2501.12948v2/plot_length.svg',
    'gem0': 'https://arxiv.org/html/2403.05530v5/updated_video_haystack_final.svg',
    'llama0': 'https://arxiv.org/html/2407.21783v3/isoflops.svg',
    'vllm0': 'https://arxiv.org/html/2309.06180v1/n1-sharegpt.svg',
    'vllm1': 'https://arxiv.org/html/2309.06180v1/n1-alpaca.svg',
}

def fetch_sources(directory):
    for name, url in ASSET_URLS.items():
        urlretrieve(url, directory / (name + '.svg'))
    report = directory / 'gpt4.pdf'
    urlretrieve('https://cdn.openai.com/papers/gpt-4.pdf', report)
    run(['pdftocairo', '-svg', '-f', '3', '-l', '3', report, directory / 'gpt0.svg'], check=True)

tmp = TemporaryDirectory() if len(sys.argv) == 1 else None
ASSETS = Path(tmp.name if tmp else sys.argv[1])
if tmp:
    fetch_sources(ASSETS)
NUM = r'[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?'

def numbers(text):
    return [float(v) for v in re.findall(NUM, text)]

def load(name):
    return ET.parse(ASSETS / (name + '.svg')).getroot()

def nodes(root, clip=None):
    clip = root.get('clip-path', clip)
    yield root, clip
    for child in root:
        yield from nodes(child, clip)

def line_points(d):
    x = y = 0
    out = []
    for command, values in re.findall(r'([MLHV])([^MLHV]+)', d):
        values = numbers(values)
        if command == 'H':
            out.extend((v, y) for v in values)
            x = values[-1]
        elif command == 'V':
            out.extend((x, v) for v in values)
            y = values[-1]
        else:
            for x, y in zip(values[::2], values[1::2]):
                out.append((x, y))
    return out

def series(panel, role, style, points):
    return [[panel, role, style, round(x, 8), round(y, 8)] for x, y in points]

def ticks(lo, step, n):
    return [round(lo + step * i, 8) for i in range(n)]

def panel(title, x_label, y_label, x_range, y_range, x_ticks, y_ticks):
    return dict(title=title, xLabel=x_label, yLabel=y_label, xRange=x_range, yRange=y_range,
                xTicks=x_ticks, yTicks=y_ticks)

data = json.loads(DATA.read_text())

def store(key, title, url, citation, note, roles, colors, panels, columns, rows, grid=1):
    data[key] = dict(title=title, paper=url, original=url, source=url, citation=citation, note=note,
                     precision='原图坐标提取', roles=roles, originalColors=colors, panels=panels,
                     grid=grid, columns=columns, rows=rows)

columns = ['panel','series','geometry','x','y']
r1url = 'https://arxiv.org/html/2501.12948v2#S2.F1'
r1roles = ['Pass@1','Cons@16','Human participants','Response length']
r1rows = []
for i, color in enumerate(['#0000ff','#ff0000','#008000']):
    d = [n.get('d') for n, clip in nodes(load('r10')) if clip and n.get('stroke') == color
         and n.get('transform','').startswith('matrix(1,0,0,-1,0,') and n.get('d','').startswith('M')]
    assert len(d) == 1
    points = [(round((x - 62.664258) * 2000 / 103.52505), round(.2 + (y - 80.78544) / 496.6098, 5))
              for x,y in line_points(d[0])]
    r1rows += series(0, i, 'dashed' if i == 2 else 'line+point', points)
for n in load('r11').iter():
    if n.get('stroke') != '#0000ff':
        continue
    points = [((x - 88.90739) * 2000 / 99.46523, (y - 53.170976) * 2500 / 44.877684)
              for x,y in line_points(n.get('d'))]
    r1rows += series(1, 3, 'faint' if n.get('stroke-opacity') else 'line', points)
store('deepseek_r1','DeepSeek-R1-Zero · 训练曲线',r1url,'DeepSeek-AI，arXiv v2，Fig. 1',
      '从作者 SVG 读取两幅图的绘制坐标，经原图刻度换算。回答长度保留原图中的浅色轨迹和深色曲线。SVG 轨迹不是原始训练日志。',
      r1roles,['#0000FF','#FF0000','#008000','#0000FF'],[
      panel('AIME accuracy','Steps','Accuracy',[-290,10490],[.12,.902],ticks(0,2000,6),ticks(.2,.1,8)),
      panel('Average response length','Steps','Average length per response',[-510,10710],[-655,20960],ticks(0,2000,6),ticks(0,5000,5)),
      ],columns,r1rows,2)

gemrows = []
gem_panels = {'url(#clip_0)':(0,62.0125,492.33595,17.16923),
              'url(#clip_2)':(1,988.8387,493.4658,17.3952),
              'url(#clip_3)':(2,62.0125,231.40793,17.16923)}
for n, clip in nodes(load('gem0')):
    fill = n.get('fill')
    if fill not in ('#a8dab5','#87837e') or clip not in gem_panels: continue
    idx, x0, y0, step = gem_panels[clip]
    x,y,*_ = numbers(n.get('d'))
    gemrows.append([idx, round((x-x0)/step)+1, round((y0-y)/step)*10+5, 'success' if fill=='#a8dab5' else 'api_error'])
assert [sum(row[0]==i for row in gemrows) for i in range(3)] == [500,100,500]
assert sum(row[3]=='api_error' for row in gemrows) == 470
store('gemini_video','Gemini 1.5 · 视频长上下文检索','https://arxiv.org/html/2403.05530v5#S5.F9',
      'Gemini Team，arXiv v5，Fig. 9',
      '从作者 SVG 的 1100 个单元格读取类别。前两幅 1 小时测试每格 1.2 分钟，10 小时面板每格 1 小时；CSV 时长为分箱上界。灰格表示 API 错误。',
      ['检索成功','API 错误'],['#A8DAB5','#87837E'],
      ['Gemini 1.5 Pro: 1 minute to 1 hour','Gemini 1.5 Pro: up to 10 hours','GPT-4V: 1 minute to 1 hour'],
      ['panel','duration_bin_upper','depth_percent','result'],
      [[p,round(t*(1 if p==1 else 1.2),1),d,res] for p,t,d,res in gemrows])

llama_colors = ['#e8f3ff','#c6e7ff','#a4d8ff','#84bcf5','#48a5fa','#0082fb','#2962d9','#1d4ab2','#081d6a','#020a4d','#c42f8f']
llama_points = [[] for _ in llama_colors]
llama_rows = []
for n, clip in nodes(load('llama0')):
    color, stroke, d = n.get('fill'), n.get('stroke'), n.get('d','')
    if not clip: continue
    if stroke in llama_colors and len(d)>750 and n.get('transform','').startswith('matrix(1,0,0,-1,0,'):
        pts = [(10+(x-172.15753)/121.76594,.7+(y-68.70833)/980.997)
               for x,y in line_points(d)]
        llama_rows += series(0,llama_colors.index(stroke),'line',pts)
    if color in llama_colors:
        transform = numbers(n.get('transform',''))
        if len(transform)==6 and transform[:4]==[1,0,0,-1] and transform[4] != 0:
            x,y=transform[4:]
            llama_points[llama_colors.index(color)].append((10+(x-172.15753)/121.76594,
                                                               .7+(326.47789-y-68.70833)/980.997))
for i, points in enumerate(llama_points):
    assert points
    llama_rows += series(0,i,'diamond' if i==10 else 'point',points)
store('llama_isoflops','Llama 3 · IsoFLOPs 缩放曲线','https://arxiv.org/html/2407.21783v3#S3.F3.fig1',
      'Dubey 等，arXiv v3，Fig. 2','从作者 SVG 提取拟合线、测量点和最小值标记。横坐标 x 为训练 token 数的 log10；点坐标由刻度换算。',
      ['6e18','1e19','3e19','6e19','1e20','3e20','6e20','1e21','3e21','1e22','Fitted minimum'],
      llama_colors,[panel('IsoFLOPs profiles','Training tokens','Validation loss',[9.12,12.06],[.679,.951],
                         [[10,'10¹⁰'],[11,'10¹¹'],[12,'10¹²']],ticks(.7,.05,6))],columns,llama_rows)

vcolors = ['#808080','#ff0000','#ffa500','#008000','#0000ff']
vrows, vpanels = [], []
for group, dataset in enumerate(['ShareGPT','Alpaca']):
    root = load('vllm'+str(group))
    rects = [(78.48,373.89179),(432.97413,728.38589),(787.46829,1082.88)]
    steps = [(0.5,70.67267,5),(.2,53.71122,6),(.5,51.64538,6)] if group==0 else [(10,95.91292,4),(5,70.67267,5),(5,63.94189,5)]
    models = ['OPT-13B, 1 GPU','OPT-66B, 4 GPUs','OPT-175B, 8 GPUs']
    for idx, ((x0,x1),(dx,sx,n)) in enumerate(zip(rects,steps)):
        vpanels.append(panel('('+chr(97+group*3+idx)+') '+models[idx]+', '+dataset,
                             'Request rate (req/s)','Normalized latency (s/token)' if idx==0 else '',
                             [0,(x1-x0)*dx/sx],[0,1],ticks(0,dx,n),[0,.5,1]))
    clips = {n.get('id'):numbers(n[0].get('d'))[0] for n in root.iter() if n.tag.endswith('clipPath')}
    for n, clip in nodes(root):
        stroke = n.get('stroke')
        if not clip or stroke not in vcolors or not n.get('transform','').startswith('matrix(1,0,0,-1,0,'): continue
        x0 = clips[clip[5:-1]]
        idx = min(range(3), key=lambda i:abs(rects[i][0]-x0))
        dx,sx,_=steps[idx]
        pts = [((x-x0)*dx/sx,(y-80.81875)/83.16) for x,y in line_points(n.get('d'))]
        vrows += series(group*3+idx,vcolors.index(stroke),'line',pts)
        assert len(pts)>1
    page_height=float(root.get('viewBox').split()[-1])
    for n, clip in nodes(root):
        fill=n.get('fill')
        transform=numbers(n.get('transform',''))
        if not clip or fill not in vcolors or len(transform)!=6 or transform[:4]!=[1,0,0,-1] or transform[4]==0: continue
        x,y=transform[4:]
        idx=next((i for i, (lo,hi) in enumerate(rects) if lo <= x <= hi), None)
        if idx is None:
            continue
        x0=rects[idx][0]
        dx,sx,_=steps[idx]
        vrows += series(group*3+idx,vcolors.index(fill),'point',[((x-x0)*dx/sx,(page_height-y-80.81875)/83.16)])
assert len({(p,r) for p,r,s,_,_ in vrows if s=='line'}) == 30
store('vllm_latency','vLLM · 请求负载与时延','https://arxiv.org/html/2309.06180v1#S5.F12',
      'Kwon 等，SOSP 2023，Fig. 12','从作者 SVG 读取两行共六个面板的曲线与标记，按原图刻度近似换算。与原图一样，部分序列超出坐标范围后被裁切。',
      ['FasterTransformer','Orca (Max)','Orca (Pow2)','Orca (Oracle)','vLLM'],vcolors,vpanels,columns,vrows,3)

gptrows = []
for n,_ in nodes(load('gpt0')):
    d=n.get('d','')
    if n.get('stroke','').startswith('rgb(80.39093') and len(d)>200 and 'matrix(0.70132' in n.get('transform',''):
        pts = [( (x-439.169931)*2/77.928, 1+(258.306391-y)/43.411442 ) for x,y in line_points(d)]
        gptrows += series(0,1,'dashed',pts)
    if n.get('fill','').startswith(('rgb(45.489502','rgb(31.764221')):
        ns = numbers(d)
        x, y = ns[6], ns[1]
        role=0 if n.get('fill').startswith('rgb(45') else 2
        # Data glyphs in the first plot are between its first tick and lower baseline;
        # the two plot legends and second figure are separated by retaining only the
        # earliest glyphs in each color, then dropping the first (legend sample).
        gptrows += series(0,role,'point',[( ( (x-.599)/.70132-439.169931)*2/77.928,
                                        1+(258.306391-(y-.914874)/.70132)/43.411442 )])
gptrows=[row for row in gptrows if row[2]!='point']+[row for row in gptrows if row[1]==0][1:10]+[row for row in gptrows if row[1]==2][1:2]
assert len([r for r in gptrows if r[2]=='point'])==10
store('gpt4_scaling','GPT-4 · 算力与代码预测损失','https://cdn.openai.com/papers/gpt-4.pdf#page=3',
      'OpenAI，GPT-4 Technical Report，Fig. 1','从报告 PDF 矢量图提取小模型测量点、拟合线与 GPT-4 测量点。x 为相对 GPT-4 训练算力的 log10，损失单位 bits per word，均为图上换算。',
      ['Observed','Prediction','GPT-4'],['#747474','#CDCDCD','#51DA4C'],
      [panel('OpenAI codebase next word prediction','Relative training compute','Bits per word',[-10.61,.06],[1,6],
             [[-10,'10⁻¹⁰'],[-8,'10⁻⁸'],[-6,'10⁻⁶'],[-4,'10⁻⁴'],[-2,'10⁻²'],[0,'1']],ticks(1,1,6))],columns,gptrows)

# Keep a compact row per line, preserving manageable diffs for any dataset.
encoded = ['{']
for i, (key, case) in enumerate(data.items()):
    encoded.append('  ' + json.dumps(key) + ': {')
    for j, (field, value) in enumerate(case.items()):
        last = j == len(case) - 1
        header = '    ' + json.dumps(field) + ': '
        if field == 'rows':
            encoded.append(header + '[')
            for k, row in enumerate(value):
                encoded.append('      ' + json.dumps(row, ensure_ascii=False) + (',' if k < len(value) - 1 else ''))
            encoded.append('    ]' + ('' if last else ','))
        else:
            encoded.append(header + json.dumps(value, ensure_ascii=False) + ('' if last else ','))
    encoded.append('  }' + (',' if i < len(data) - 1 else ''))
encoded.append('}')
DATA.write_text('\n'.join(encoded) + '\n')
for key in ['deepseek_r1','gemini_video','llama_isoflops','vllm_latency','gpt4_scaling']:
    print(key,len(data[key]['rows']))
