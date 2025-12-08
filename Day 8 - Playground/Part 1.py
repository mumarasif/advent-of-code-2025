import heapq
from collections import Counter

def read_points(path):
    pts = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            parts = s.split(',')
            if len(parts) != 3:
                raise ValueError(f"Bad line (expected 3 comma-separated ints): {line!r}")
            x, y, z = map(int, parts)
            pts.append((x, y, z))
    return pts

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1]*n
    def find(self, a):
        p = self.p
        while p[a] != a:
            p[a] = p[p[a]]
            a = p[a]
        return a
    def union(self, a, b):
        pa = self.find(a)
        pb = self.find(b)
        if pa == pb:
            return False
        if self.sz[pa] < self.sz[pb]:
            pa, pb = pb, pa
        self.p[pb] = pa
        self.sz[pa] += self.sz[pb]
        return True

def squared_dist(a, b):
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    dz = a[2]-b[2]
    return dx*dx + dy*dy + dz*dz

def k_smallest_pairs(points, k=1000):
    n = len(points)
    if n < 2:
        return []
    heap = []
    push = heapq.heappush
    pop = heapq.heappop
    for i in range(n):
        pi = points[i]
        for j in range(i+1, n):
            d = squared_dist(pi, points[j])
            if len(heap) < k:
                push(heap, (-d, i, j))
            else:
                if d < -heap[0][0]:
                    pop(heap)
                    push(heap, (-d, i, j))
    result = [(-negd, i, j) for (negd, i, j) in heap]
    result.sort(key=lambda x: x[0])
    return result

def main():
    path = 'input.txt'
    points = read_points(path)
    n = len(points)
    if n == 0:
        return

    k = 1000
    max_pairs = n*(n-1)//2
    if max_pairs < k:
        k = max_pairs

    edges = k_smallest_pairs(points, k=k)

    dsu = DSU(n)
    for dist, i, j in edges:
        dsu.union(i, j)

    roots = [dsu.find(i) for i in range(n)]
    cnt = Counter(roots)
    sizes = sorted(cnt.values(), reverse=True)

    top3 = sizes[:3] + [1]*max(0, 3 - len(sizes))
    prod = 1
    for s in top3:
        prod *= s
    print(prod)

if __name__ == "__main__":
    main()