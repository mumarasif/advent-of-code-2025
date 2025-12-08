def read_points(path):
    pts = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                pts.append(tuple(map(int, line.strip().split(','))))
    return pts

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n
        self.components = n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        self.sz[ra] += self.sz[rb]
        self.components -= 1
        return True

def squared_dist(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return dx*dx + dy*dy + dz*dz

def main():
    path = "input.txt"

    points = read_points(path)
    n = len(points)

    dsu = DSU(n)

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            d = squared_dist(points[i], points[j])
            edges.append((d, i, j))

    edges.sort()

    for _, i, j in edges:
        if dsu.union(i, j):
            if dsu.components == 1:
                print(points[i][0] * points[j][0])
                return

if __name__ == "__main__":
    main()