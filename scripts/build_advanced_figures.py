#!/usr/bin/env python3
"""Build editable, original teaching diagrams. All numbers are illustrative."""
from pathlib import Path
import html, json, subprocess, zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'img/figures/advanced'; OUT.mkdir(parents=True,exist_ok=True)
COL=['#0072B2','#009E73','#D55E00','#8064A2','#B58200']
class Figure:
 def __init__(self,title,subtitle):
  self.s=['<svg xmlns="http://www.w3.org/2000/svg" width="182mm" height="100mm" viewBox="0 0 1200 660" role="img">',f'<title>{html.escape(title)}</title>', '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#526174"/></marker></defs><rect width="1200" height="660" fill="white"/>']
  self.text(36,42,title,27,True);self.text(36,73,subtitle,17)
 def text(self,x,y,t,size=20,bold=False):
  self.s.append(f'<text x="{x}" y="{y}" font-family="Liberation Sans,Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="#203044">{html.escape(t)}</text>')
 def box(self,x,y,w,h,title,lines=(),c=0):
  self.s.append(f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{COL[c]}" fill-opacity=".07" stroke="{COL[c]}" stroke-width="1.5"/>')
  self.text(x+16,y+30,title,21,True)
  for i,t in enumerate(lines):self.text(x+16,y+61+i*27,t,18)
  self.s.append('</g>')
 def arrow(self,x,y,X,Y,dashed=False):
  self.s.append(f'<path d="M{x} {y} L{X} {Y}" fill="none" stroke="#526174" stroke-width="2" {chr(32)+"stroke-dasharray='7 5'" if dashed else ""} marker-end="url(#arrow)"/>')
 def matrix(self,x,y,n=5,cell=25,causal=False):
  for i in range(n):
   for j in range(n):
    opacity=(.8 if i==j else .12) if not causal else (.6 if j<=i else .03)
    self.s.append(f'<rect x="{x+j*cell}" y="{y+i*cell}" width="{cell-2}" height="{cell-2}" fill="#0072B2" fill-opacity="{opacity}"/>')
 def save(self,slug):
  self.text(36,636,'Original educational redraw · schematic values only · SVG text and objects remain editable',15)
  p=OUT/f'{slug}.svg';p.write_text('\n'.join(self.s+['</svg>']))
  for typ in ['pdf','png']:
   cmd=['inkscape',str(p),f'--export-type={typ}',f'--export-filename={p.with_suffix("."+typ)}']
   if typ=='png':cmd+=['--export-width=1600']
   subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
items=[]
def save(f,slug,title,why,source):
 f.save(slug);items.append(dict(slug=slug,title=title,why=why,source=source))
f=Figure('Industrial agent: decisions with an explicit feedback loop','Conceptual design example; simulator validation and safety checks precede plant execution.')
f.box(35,120,220,150,'Observe context',['Sensors / alarms','Operating regime','Uncertainty / timestamps'])
f.box(325,120,250,150,'Retrieve experience',['Semantic relevance','Regime applicability','Provenance + expiry'],1)
f.box(645,120,240,150,'Plan & call tools',['Candidate actions','Simulator / knowledge','Predicted constraints'],3)
f.box(955,120,210,150,'Safety gate',['Check hard limits','Approve or reject','Human escalation'],2)
for a,b in [(255,325),(575,645),(885,955)]:f.arrow(a,195,b,195)
f.box(35,365,270,145,'Experience store',['Context → action → outcome','Revise validity conditions','Keep an auditable history'],1)
f.box(390,365,300,145,'Feedback & attribution',['Compare expected / observed','Separate tool and model errors','Update with verified outcomes'],4)
f.box(850,365,315,145,'Execute & monitor',['Approved action / operator review','Observe process response','Stop or fall back on violation'],0)
f.arrow(1060,270,1060,365);f.arrow(850,435,690,435);f.arrow(390,435,305,435)
f.arrow(170,365,170,295);f.arrow(170,295,430,295);f.arrow(430,295,430,270)
f.arrow(1060,270,1060,295,True);f.arrow(1060,295,765,295,True);f.arrow(765,295,765,270,True);f.text(820,321,'Reject → replan',17)
f.text(36,570,'Evaluation: task success + constraint violations + stale-experience reuse + tool / token cost',20)
save(f,'industrial-agent','工业智能体：有约束的闭环决策','从工况识别到经验适用性、仿真验证、安全检查与反馈更新，区分批准执行和拒绝重规划。','')
f=Figure('Transformer: encoder memory meets causal decoding','Classic post-norm architecture (Vaswani et al., 2017); arrows run bottom → top.')
for x,label,layers in [(45,'ENCODER',['Input embeddings + position','Self-attention → Add & Norm','Feed-forward → Add & Norm']),(650,'DECODER',['Shifted targets + position','Masked self-attention → Add & Norm','Cross-attention → Add & Norm','Feed-forward → Add & Norm'])]:
 f.text(x,115,label,22,True)
 for i,t in enumerate(layers):
  y=500-i*93;f.box(x,y,500,66,t,(),i%4)
  if i:f.arrow(x+250,y+93,x+250,y+66)
f.text(60,290,'Repeat encoder layer N times',17)
f.arrow(545,347,650,347);f.text(550,315,'K, V',18,True)
f.text(100,210,'Encoder outputs = memory',20,True)
f.arrow(295,314,295,230)
f.text(650,195,'Repeat decoder layer N times',17)
f.arrow(900,221,900,155);f.text(775,140,'Linear → softmax → next token',20,True)
f.text(45,595,'Decoder Q attends to encoder K,V; causal masking prevents access to future target tokens.',18)
save(f,'transformer-expanded','Transformer：编码器与因果解码器','展示正确的子层顺序、移位目标、编码器记忆及交叉注意力 K/V 路径；沿用原论文 post-norm 结构。','https://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf')
f=Figure('CLIP: align paired images and text in a shared space','Symmetric contrastive training over a minibatch of N image–text pairs (Radford et al., 2021).')
f.box(40,140,280,135,'Image encoder',['Image batch → features','Normalize: v / ||v||'],0)
f.box(40,365,280,135,'Text encoder',['Tokenized captions','Normalize: t / ||t||'],1)
f.box(410,200,300,245,'Pairwise similarities',['S[i,j] = exp(a) · v_iᵀ t_j','Learned logit scale a','Diagonal = matched pairs','Off-diagonal = negatives'],3)
f.arrow(320,205,410,260);f.arrow(320,430,410,385)
f.matrix(795,150,6,38);f.text(795,410,'Rows: images; columns: text',18)
f.arrow(710,305,785,270)
f.arrow(910,420,910,490)
f.box(420,490,730,85,'Loss = ½ [ image→text CE + text→image CE ]',['Gradients update both encoders and the logit scale.'],2)
save(f,'clip-expanded','CLIP：从双编码器到对比目标','不只画两个编码器：展开归一化、可学习温度、批内相似度矩阵与双向交叉熵。','https://proceedings.mlr.press/v139/radford21a.html')
f=Figure('Switch routing: one expert selected for each token','Top-1 routing, sparse expert computation and auxiliary load balancing (Fedus et al., 2022).')
f.box(35,130,270,130,'Token representations',['One row per token','Router scores → softmax'],0)
for row in range(5):
 for col in range(3):
  f.s.append(f'<rect x="{100+col*42}" y="{310+row*30}" width="38" height="26" fill="#0072B2" fill-opacity="{.8 if col==row%3 else .12}"/>')
f.text(95,295,'Experts 1 / 2 / 3',17)
f.text(35,495,'Rows: five illustrative tokens',17)
f.box(385,130,285,130,'Top-1 dispatch',['e(t) = argmax p(e | t)','Capacity limits per expert'],3)
f.arrow(305,195,385,195)
for i in range(3):
 y=110+i*145;f.box(800,y,350,105,f'Expert {i+1} · FFN',['Compute only assigned tokens'],i)
 f.arrow(760,y+53,800,y+53)
f.arrow(670,195,760,195)
f.s.append('<path d="M760 163 V453" fill="none" stroke="#526174" stroke-width="2"/>')
f.box(370,450,350,115,'Combine outputs',['y_t = p(e(t) | t) · E_e(t)(x_t)','Restore original token order'],1)
for y in [163,308,453]:
 f.arrow(1150,y,1175,y)
f.s.append('<path d="M1175 163 V535" fill="none" stroke="#526174" stroke-width="2"/>')
f.arrow(1175,535,720,535)
f.text(35,585,'Training: task loss + load-balancing loss. Capacity overflow handling must be specified by implementation.',18)
save(f,'switch-expanded','Switch Transformer：稀疏路由','展开 token 路由、top-1 分发、专家容量、概率加权合并及辅助负载均衡目标。','https://www.jmlr.org/papers/v23/21-0998.html')
f=Figure('Preference alignment: RLHF / PPO versus DPO','A training-path comparison; both paths begin with preference data and an initial policy.')
f.box(35,120,310,125,'Shared preference dataset',['Prompt x','Chosen y+ / rejected y−'],4)
f.arrow(345,180,410,180)
f.box(410,120,745,125,'Classical RLHF / PPO',['Fit reward model r(x,y) from preference pairs','Generate policy rollouts → reward scores → PPO updates with reference KL'],0)
f.arrow(190,245,190,330);f.arrow(190,330,410,330)
f.box(410,300,745,140,'DPO: optimize on preference pairs',['Score chosen and rejected responses under policy and frozen reference','Minimize −log σ(β [log[πθ(y+|x)/πref(y+|x)] − log[πθ(y−|x)/πref(y−|x)]])'],1)
f.box(35,485,535,100,'RLHF components',['Policy updated; reward model and reference frozen in PPO'],0)
f.box(620,485,535,100,'DPO components',['Trainable policy + frozen reference; no PPO rollout loop'],1)
save(f,'alignment-expanded','RLHF / DPO：对齐训练路径','区分奖励模型拟合、在线策略采样与离线偏好优化，并标出冻结参考模型的角色。','https://proceedings.neurips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract.html')
# Deterministic synthetic observations; interval is across independent simulated runs.
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
rng=np.random.default_rng(42);data=rng.normal(np.array([[.82,.69,.61],[.88,.81,.75],[.90,.85,.82]])[:,:,None],.035,(3,3,20))
np.savetxt(OUT/'synthetic-runs.csv',np.array([(m,c,r,data[m,c,r]) for m in range(3) for c in range(3) for r in range(20)]),delimiter=',',header='method,condition,independent_simulated_run,success_fraction',comments='')
plt.rcParams.update({'font.size':9,'svg.fonttype':'none','pdf.fonttype':42,'font.family':'DejaVu Sans'})
fig,axs=plt.subplots(2,2,figsize=(10,6.6),layout='constrained');t=np.linspace(0,100,160)
for i,col in enumerate(COL[:3]):axs[0,0].plot(t,1+(.3-.07*i)*np.exp(-np.maximum(t-25,0)/18)*np.sin(np.maximum(t-25,0)/5),c=col,label=f'Method {i+1}')
axs[0,0].axhline(1.2,color='gray',ls='--',label='Illustrative limit');axs[0,0].set(xlabel='Time (a.u.)',ylabel='Normalized output',title='(a) Constructed disturbance response');axs[0,0].legend(fontsize=7)
for m in range(3):axs[0,1].errorbar(np.arange(3)+(m-1)*.07,data[m].mean(1),yerr=data[m].std(1,ddof=1)/np.sqrt(20)*1.96,marker='o',color=COL[m],label=f'Method {m+1}')
axs[0,1].set(xticks=range(3),xticklabels=['Nominal','Shift A','Shift B'],ylabel='Success fraction',title='(b) Mean ± approximate 95% CI; n=20 / cell');axs[0,1].legend(fontsize=7)
cost=[1,2,3,4,5];score=[.72,.79,.77,.85,.83];front=[0,1,3]
axs[1,0].scatter(cost,score,color='gray');axs[1,0].plot(np.array(cost)[front],np.array(score)[front],'o--',color=COL[0]);axs[1,0].set(xlabel='Inference cost (a.u.; lower is better)',ylabel='Success fraction',title='(c) Illustrative cost–quality frontier')
im=axs[1,1].pcolormesh(np.arange(4)-.5,np.arange(4)-.5,data.mean(2),vmin=.5,vmax=1,cmap='Blues');axs[1,1].invert_yaxis();axs[1,1].set(xticks=range(3),xticklabels=['Nominal','Shift A','Shift B'],yticks=range(3),yticklabels=['Method 1','Method 2','Method 3'],title='(d) Same observations, condition breakdown')
for i in range(3):
 for j in range(3):axs[1,1].text(j,i,f'{data[i,j].mean():.2f}',ha='center',va='center')
cb=fig.colorbar(im,ax=axs[1,1],label='Mean success fraction');cb.solids.set_rasterized(False);fig.suptitle('SYNTHETIC DEMONSTRATION — no measured industrial results',fontsize=12,fontweight='bold')
for typ in ['svg','pdf','png']:fig.savefig(OUT/f'industrial-evaluation.{typ}',dpi=180)
plt.close(fig)
items.append(dict(slug='industrial-evaluation',title='工业评估：从动态响应到跨工况证据',why='四面板区分构造响应、独立模拟重复的均值与区间、成本前沿和工况分解。CSV 保留全部模拟观测；不代表实际工业效果。',source=''))
(OUT/'manifest.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
readme='''# Editable research figure examples\n\nThese are original educational diagrams, not reproductions of paper figure artwork. All matrix cells, curves and performance numbers are schematic or synthetic, never experimental findings. References are listed in manifest.json.\n\nEdit SVG text, groups and connectors in Inkscape. Regenerate with Python 3, numpy, matplotlib and Inkscape on PATH: `python scripts/build_advanced_figures.py`. PDFs are vector exports; PNGs are previews. The Transformer follows classic post-norm ordering; DPO refers to the original offline preference objective.\n\nSynthetic dataset: seed 42, 3 methods × 3 conditions × 20 independent simulated draws. Error bars: mean ± 1.96 × sample SD / sqrt(20), an approximate normal interval. Response traces and cost-quality points are separately constructed examples. Panel (d) summarizes exactly the same observations as (b), and is not independent evidence. Replace fixtures with actual, protocol-linked results before research use.\n'''
(OUT/'README.md').write_text(readme)
zip_path=ROOT/'downloads/figures-advanced/editable-figures.zip';zip_path.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.iterdir()):z.write(p,'img/figures/advanced/'+p.name)
 z.write(Path(__file__),'scripts/build_advanced_figures.py')
print(f'Built {len(items)} figures and {zip_path.name}')
