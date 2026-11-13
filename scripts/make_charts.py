import csv
from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader(open(ROOT/"outputs"/"runtime_results.csv",encoding="utf-8")))
fig,ax=plt.subplots(figsize=(9,5))
for alg in sorted({r["algorithm"] for r in rows}):
    subset=[r for r in rows if r["algorithm"]==alg]
    ax.plot([int(r["input_size"]) for r in subset],
            [float(r["runtime_ms"]) for r in subset],marker="o",label=alg)
ax.set_xlabel("Input size (parcel count; graph size scales with input)")
ax.set_ylabel("Execution time (milliseconds)")
ax.set_title("Mini-Courier Planner – Runtime Comparison")
ax.grid(True,alpha=.3); ax.legend()
fig.tight_layout(); fig.savefig(ROOT/"images"/"runtime_comparison.png",dpi=180)
print("Chart saved to images/runtime_comparison.png")
