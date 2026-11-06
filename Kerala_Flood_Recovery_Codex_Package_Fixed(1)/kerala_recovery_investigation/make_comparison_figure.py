import contextlib,io,runpy, numpy as np, matplotlib.pyplot as plt
from scipy.stats import rankdata
from pathlib import Path
O=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()):m=runpy.run_path(str(O/'experiment.py'))
D=m['DISTRICTS'];pub=m['pub'];B=m['burden_all'];
r=(pub-pub.min())/(pub.max()-pub.min());b=(B-B.min())/(B.max()-B.min());
rp=(rankdata(pub)-1)/13; bp=(rankdata(B)-1)/13
scores={'Published vulnerability':pub,'25% burden / continuous min-max':.75*r+.25*b,'25% burden / rank percentiles':.75*rp+.25*bp}
order=np.argsort(-pub); fig,ax=plt.subplots(figsize=(10,6.5)); y=np.arange(14)
for (name,s),mark,ofs in zip(scores.items(),['o','s','^'],[-.18,0,.18]):
 rk=rankdata(-s,method='average');ax.scatter(rk[order],y+ofs,s=40,marker=mark,label=name)
ax.set_yticks(y,[D[i] for i in order]);ax.invert_yaxis();ax.set_xlabel('Rank (1 = higher priority)');ax.set_xticks(range(1,15));ax.grid(axis='x',alpha=.2)
ax.set_title('Ranking changes depend on normalisation (illustrative, not a validated index)')
ax.legend(fontsize=9,loc='lower right');fig.tight_layout();fig.savefig(O/'figure_04_normalization_comparison.png',dpi=170);plt.close(fig)
