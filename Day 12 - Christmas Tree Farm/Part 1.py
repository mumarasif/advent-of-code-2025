import sys
sys.setrecursionlimit(10000)

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    
    shapes, regions = {}, []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if 'x' in line and ':' in line:
            left, right = line.split(':', 1)
            if 'x' in left:
                try:
                    w, h = map(int, left.split('x'))
                    regions.append((w, h, list(map(int, right.split()))))
                    i += 1; continue
                except: pass
        if line.endswith(':') and line[:-1].isdigit():
            idx, i = int(line[:-1]), i + 1
            pattern = []
            while i < len(lines) and lines[i].strip() and not (lines[i].strip().endswith(':') and lines[i].strip()[:-1].replace(' ','').isdigit()) and not ('x' in lines[i] and ':' in lines[i]):
                pattern.append(lines[i]); i += 1
            shapes[idx] = {(r, c) for r, row in enumerate(pattern) for c, ch in enumerate(row) if ch == '#'}
        else: i += 1
    return shapes, regions

def normalize(coords):
    if not coords: return frozenset()
    min_r, min_c = min(r for r,c in coords), min(c for r,c in coords)
    return frozenset((r-min_r, c-min_c) for r,c in coords)

def get_orientations(coords):
    orients = set()
    cur = set(coords)
    for _ in range(4):
        orients.add(normalize(cur))
        orients.add(normalize({(r, -c) for r,c in cur}))
        cur = {(c, -r) for r,c in cur}
    return list(orients)

def solve_region(w, h, shape_orients, quantities):
    all_placements, shape_sizes = {}, {}
    
    for idx in range(len(quantities)):
        if quantities[idx] > 0 and idx in shape_orients and shape_orients[idx]:
            size = len(list(shape_orients[idx])[0])
            shape_sizes[idx] = size
            placements = set()
            for orient in shape_orients[idx]:
                cells = list(orient)
                if not cells: continue
                max_r, max_c = max(r for r,c in cells), max(c for r,c in cells)
                for sr in range(h - max_r):
                    for sc in range(w - max_c):
                        mask = sum(1 << ((sr+r)*w + sc+c) for r,c in cells)
                        placements.add(mask)
            all_placements[idx] = sorted(placements)
    
    shape_list = [(idx, quantities[idx]) for idx in range(len(quantities))
                  if quantities[idx] > 0 and idx in all_placements]
    
    if not shape_list: return True
    
    total = sum(shape_sizes[idx] * cnt for idx, cnt in shape_list)
    if total > w * h: return False
    
    shape_list.sort(key=lambda x: (-shape_sizes[x[0]], len(all_placements[x[0]])))
    
    def solve(sidx, count, start, grid, remaining):
        if count == 0:
            if not remaining: return True
            return solve(remaining[0][0], remaining[0][1], 0, grid, remaining[1:])
        
        placements = all_placements[sidx]
        for i in range(start, len(placements)):
            mask = placements[i]
            if grid & mask == 0:
                if solve(sidx, count-1, i+1, grid|mask, remaining):
                    return True
        return False
    
    return solve(shape_list[0][0], shape_list[0][1], 0, 0, shape_list[1:])

def main():
    shapes, regions = parse_input('input.txt')
    shape_orients = {idx: get_orientations(c) for idx, c in shapes.items()}
    print(sum(1 for w, h, qty in regions if solve_region(w, h, shape_orients, qty)))

if __name__ == '__main__':
    main()