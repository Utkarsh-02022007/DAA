"""Core algorithms for the Mini-Courier Planner."""
import heapq
import time

def sort_parcels(parcels, method="merge"):
    """Return parcels ordered by earliest deadline, then highest priority.

    Supported methods: merge (merge sort), insertion (insertion sort),
    and builtin (Python's Timsort).
    """
    items = [dict(p) for p in parcels]
    key = lambda p: (p["deadline"], -p["priority"])
    if method == "builtin":
        return sorted(items, key=key)
    if method == "insertion":
        for i in range(1, len(items)):
            current = items[i]
            j = i - 1
            while j >= 0 and key(items[j]) > key(current):
                items[j + 1] = items[j]
                j -= 1
            items[j + 1] = current
        return items
    if method != "merge":
        raise ValueError("method must be 'merge', 'insertion', or 'builtin'")

    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
        result, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:]); result.extend(right[j:])
        return result
    return merge_sort(items)

def knapsack(parcels, capacity):
    """0/1 knapsack maximizing parcel value under weight capacity.

    Returns selected parcel dictionaries, total weight, and total value.
    """
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight, value = int(parcels[i-1]["weight"]), int(parcels[i-1]["value"])
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i-1][cap]
            if weight <= cap:
                dp[i][cap] = max(dp[i][cap], value + dp[i-1][cap-weight])
    selected, cap = [], capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i-1][cap]:
            selected.append(dict(parcels[i-1]))
            cap -= int(parcels[i-1]["weight"])
    selected.reverse()
    return selected, sum(int(p["weight"]) for p in selected), sum(int(p["value"]) for p in selected), dp

def dijkstra(graph, start):
    """Single-source shortest paths for a non-negative weighted graph."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    heap = [(0, start)]
    while heap:
        distance, node = heapq.heappop(heap)
        if distance != distances[node]:
            continue
        for neighbour, weight in graph[node].items():
            candidate = distance + weight
            if candidate < distances[neighbour]:
                distances[neighbour] = candidate
                previous[neighbour] = node
                heapq.heappush(heap, (candidate, neighbour))
    return distances, previous

def reconstruct_path(previous, target):
    path = []
    while target is not None:
        path.append(target)
        target = previous[target]
    return list(reversed(path))

def nearest_neighbour_tsp(graph, start):
    """Approximate a round trip through every graph node using shortest paths."""
    nodes = list(graph)
    if start not in graph:
        raise ValueError("Starting node is not in graph")
    current, unvisited = start, set(nodes) - {start}
    route, total = [start], 0
    # Dijkstra distances allow travel between non-adjacent customer points.
    while unvisited:
        distances, _ = dijkstra(graph, current)
        reachable = [(distances[node], node) for node in unvisited if distances[node] < float("inf")]
        if not reachable:
            raise ValueError("Graph is disconnected; not all locations are reachable")
        distance, next_node = min(reachable)
        total += distance
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node
    distances, _ = dijkstra(graph, current)
    if distances[start] == float("inf"):
        raise ValueError("Cannot return to the starting depot")
    total += distances[start]
    route.append(start)
    return route, total
