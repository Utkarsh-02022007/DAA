"""Integrated Mini-Courier Planner application."""
import csv, json
from pathlib import Path
from algorithms import sort_parcels, knapsack, dijkstra, nearest_neighbour_tsp, reconstruct_path

ROOT = Path(__file__).resolve().parents[1]

def load_parcels(path=ROOT/"datasets"/"parcels.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        return [{**r, "deadline": int(r["deadline"]), "priority": int(r["priority"]),
                 "weight": int(r["weight"]), "value": int(r["value"])} for r in csv.DictReader(f)]

def load_graph(path=ROOT/"datasets"/"routes.json"):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    graph = {node: {} for node in data["nodes"]}
    for a, b, distance in data["edges"]:
        graph[a][b] = float(distance)
        graph[b][a] = float(distance)
    return graph

def run_planner(capacity=15, start="DEPOT"):
    parcels = load_parcels()
    ordered = sort_parcels(parcels, "merge")
    selected, weight, value, dp = knapsack(ordered, capacity)
    graph = load_graph()
    # The graph includes all customer locations; route through the customers
    # represented in the selected parcel list, plus the depot.
    required = {p["location"] for p in selected}
    if not required:
        return {"ordered": ordered, "selected": [], "weight": 0, "value": 0,
                "route": [start, start], "distance": 0, "shortest_paths": {}}
    # Build a complete metric closure among the depot and selected locations.
    relevant = [start] + sorted(required)
    shortest = {}
    for source in relevant:
        dist, prev = dijkstra(graph, source)
        shortest[source] = {target: (dist[target], reconstruct_path(prev, target))
                            for target in relevant}
    # Nearest-neighbour over the shortest-path distances between required stops.
    route, remaining, current, total = [start], set(required), start, 0
    while remaining:
        next_stop = min(remaining, key=lambda node: (shortest[current][node][0], node))
        distance, path = shortest[current][next_stop]
        total += distance
        route.extend(path[1:])
        remaining.remove(next_stop)
        current = next_stop
    distance, path = shortest[current][start]
    total += distance
    route.extend(path[1:])
    return {"ordered": ordered, "selected": selected, "weight": weight, "value": value,
            "route": route, "distance": total, "shortest_paths": shortest}

def main():
    result = run_planner()
    print("=" * 62)
    print("MINI-COURIER PLANNER | DEMONSTRATION RUN")
    print("=" * 62)
    print("\\n1. PRIORITIZED PARCELS (earliest deadline, then priority)")
    for p in result["ordered"]:
        print(f'{p["parcel_id"]:>4} | {p["customer"]:<14} | deadline={p["deadline"]:<2} | '
              f'priority={p["priority"]} | weight={p["weight"]} kg | value={p["value"]}')
    print("\\n2. OPTIMIZED PACKING PLAN (0/1 Knapsack)")
    for p in result["selected"]:
        print(f'  {p["parcel_id"]}: {p["customer"]} ({p["weight"]} kg, value {p["value"]})')
    print(f'Total packed weight: {result["weight"]} / 15 kg')
    print(f'Total parcel value: {result["value"]}')
    print("\\n3. DELIVERY ROUTE (Dijkstra + Nearest-Neighbour approximation)")
    print(" -> ".join(result["route"]))
    print(f'Total route distance: {result["distance"]:.1f} km')
    print("\\nNote: route is a heuristic tour, not guaranteed to be globally optimal.")

if __name__ == "__main__":
    main()
