def read_points(path):
    pts = []
    with open(path) as f:
        for line in f:
            if line.strip():
                x, y = map(int, line.split(','))
                pts.append((x, y))
    return pts

def max_area(path):
    points = list(dict.fromkeys(read_points(path)))  
    n = len(points)
    if n < 2:
        return 0

    best = 0
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            if x1 == x2 or y1 == y2:
                continue 
            width  = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height
            if area > best:
                best = area
    return best

if __name__ == "__main__":
    path = "input.txt"
    print(max_area(path))
