# Mini-Courier Planner

A Python capstone prototype that prioritizes parcels, selects a capacity-feasible parcel set, and plans a delivery tour using sorting, Dynamic Programming, graph algorithms, and a TSP approximation.

## Features
- Merge Sort prioritization by earliest deadline, then highest priority.
- 0/1 Knapsack Dynamic Programming to maximize parcel value under a 15 kg capacity.
- Weighted undirected customer graph.
- Dijkstra shortest paths for travel between locations.
- Nearest-Neighbour TSP approximation for a depot-returning delivery tour.
- Runtime benchmarking for sorting, knapsack, and Dijkstra.

## Requirements
- Python 3.9 or newer
- Matplotlib (only needed to regenerate runtime charts)

Install:
```bash
python -m pip install -r requirements.txt
```

## Run the application
From the project root:
```bash
python src/planner.py
```

## Run performance tests
```bash
python src/benchmark.py
```
The script writes `outputs/runtime_results.csv`. Run `python scripts/make_charts.py` to regenerate the chart (requires Matplotlib).

## Project structure
```text
mini_courier_planner/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── algorithms.py
│   ├── planner.py
│   └── benchmark.py
├── datasets/
│   ├── parcels.csv
│   └── routes.json
├── outputs/
│   └── runtime_results.csv
├── images/
│   ├── runtime_comparison.png
│   └── system_workflow.png
├── docs/
│   └── Mini_Courier_Planner_Report.pdf
└── mini_courier_planner.ipynb
```

## Assumptions and limitations
- All parcel weights and values are illustrative sample data, not operational courier data.
- The vehicle capacity is 15 kg for the demonstration.
- The road graph is a small synthetic weighted graph. Edge weights represent kilometres.
- Dijkstra requires non-negative edge weights.
- Nearest-Neighbour is a heuristic; it does not guarantee the globally shortest TSP tour.
- The route visits the locations of selected parcels and returns to `DEPOT`. When multiple selected parcels share a location, that location is visited once.

## Algorithmic complexity
Let V be graph vertices, E edges, n parcels, and W vehicle capacity.
- Merge Sort: O(n log n) time, O(n) auxiliary space.
- Insertion Sort: O(n²) worst-case time, O(1) auxiliary space.
- 0/1 Knapsack: O(nW) time and O(nW) space in this table-based implementation.
- Dijkstra with a binary heap: O((V+E) log V) time.
- Nearest-Neighbour tour: O(k) Dijkstra runs over the graph for k delivery locations; approximately O(k(V+E) log V), plus selection overhead.

