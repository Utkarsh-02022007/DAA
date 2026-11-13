"""Benchmark sorting, knapsack and Dijkstra with reproducible synthetic inputs."""
import csv, random, time, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from algorithms import sort_parcels, knapsack, dijkstra

ROOT = Path(__file__).resolve().parents[1]
random.seed(42)
rows=[]
for n in [50, 100, 200, 400]:
    parcels=[{"parcel_id":f"P{i}","deadline":random.randint(1,30),
              "priority":random.randint(1,5),"weight":random.randint(1,10),
              "value":random.randint(5,50)} for i in range(n)]
    graph={str(i):{} for i in range(max(10,n//4))}
    for i in graph:
        for j in graph:
            if int(i)<int(j) and random.random()<0.18:
                wt=random.randint(1,20); graph[i][j]=wt; graph[j][i]=wt
    for label, fn in [
        ("Merge sort", lambda: sort_parcels(parcels,"merge")),
        ("Insertion sort", lambda: sort_parcels(parcels,"insertion")),
        ("Python Timsort", lambda: sort_parcels(parcels,"builtin")),
        ("0/1 Knapsack", lambda: knapsack(parcels, 60)),
        ("Dijkstra", lambda: dijkstra(graph,"0"))
    ]:
        start=time.perf_counter()
        fn()
        elapsed=(time.perf_counter()-start)*1000
        rows.append([n,label,round(elapsed,4)])
out=ROOT/"outputs"/"runtime_results.csv"
with open(out,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["input_size","algorithm","runtime_ms"]); w.writerows(rows)
print(f"Saved benchmark results to {out}")
for row in rows: print(row)
