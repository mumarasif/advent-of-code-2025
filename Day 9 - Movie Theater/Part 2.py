def read_points(path):
    pts = []
    with open(path) as f:
        for line in f:
            if line.strip():
                x, y = map(int, line.split(','))
                pts.append((x, y))
    return pts

def get_line_points_compressed(p1, p2, x_to_idx, y_to_idx, idx_to_x, idx_to_y):
    """Get all compressed points on a straight line between p1 and p2 (inclusive)"""
    x1, y1 = p1
    x2, y2 = p2
    points = set()
    
    if x1 == x2:  
        min_y, max_y = min(y1, y2), max(y1, y2)
        for iy in range(len(idx_to_y)):
            real_y = idx_to_y[iy]
            if min_y <= real_y <= max_y:
                points.add((x_to_idx[x1], iy))
    elif y1 == y2:  
        min_x, max_x = min(x1, x2), max(x1, x2)
        for ix in range(len(idx_to_x)):
            real_x = idx_to_x[ix]
            if min_x <= real_x <= max_x:
                points.add((ix, y_to_idx[y1]))
    
    return points

def build_valid_tiles(red_points, x_to_idx, y_to_idx, idx_to_x, idx_to_y):
    """Build set of valid tiles using coordinate compression"""
    n = len(red_points)
    
    boundary = set()
    for i in range(n):
        p1 = red_points[i]
        p2 = red_points[(i + 1) % n]
        boundary.update(get_line_points_compressed(p1, p2, x_to_idx, y_to_idx, idx_to_x, idx_to_y))
    
    nx = len(idx_to_x)
    ny = len(idx_to_y)
    
    valid = set(boundary)
    
    for iy in range(ny):
        inside = False
        prev_on_boundary = False
        
        for ix in range(nx):
            on_boundary = (ix, iy) in boundary
            
            if on_boundary:
                has_above = (ix, iy + 1) in boundary if iy + 1 < ny else False
                has_below = (ix, iy - 1) in boundary if iy > 0 else False
                
                if has_above and has_below:
                    inside = not inside
                elif has_above or has_below:
                    if not prev_on_boundary:
                        inside = not inside
                
                valid.add((ix, iy))
                prev_on_boundary = True
            else:
                if inside:
                    valid.add((ix, iy))
                prev_on_boundary = False
    
    return valid

def build_valid_tiles_v2(red_points, x_to_idx, y_to_idx, idx_to_x, idx_to_y):
    """Build valid tiles using flood fill from outside"""
    n = len(red_points)
    nx = len(idx_to_x)
    ny = len(idx_to_y)
    
    boundary = set()
    for i in range(n):
        p1 = red_points[i]
        p2 = red_points[(i + 1) % n]
        boundary.update(get_line_points_compressed(p1, p2, x_to_idx, y_to_idx, idx_to_x, idx_to_y))
    
    exterior = set()
    stack = [(-1, -1)]
    visited = set()
    
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        
        if cx < -1 or cx > nx or cy < -1 or cy > ny:
            continue
        
        if (cx, cy) in boundary:
            continue
        
        exterior.add((cx, cy))
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ncx, ncy = cx + dx, cy + dy
            if (ncx, ncy) not in visited:
                stack.append((ncx, ncy))
    
    valid = set()
    for ix in range(nx):
        for iy in range(ny):
            if (ix, iy) not in exterior:
                valid.add((ix, iy))
    
    return valid

def max_area(path):
    red_points = read_points(path)
    if len(red_points) < 2:
        return 0
    
    all_x = sorted(set(p[0] for p in red_points))
    all_y = sorted(set(p[1] for p in red_points))
    
    x_to_idx = {x: i for i, x in enumerate(all_x)}
    y_to_idx = {y: i for i, y in enumerate(all_y)}
    idx_to_x = all_x
    idx_to_y = all_y
    
    valid = build_valid_tiles_v2(red_points, x_to_idx, y_to_idx, idx_to_x, idx_to_y)
    
    nx = len(all_x)
    ny = len(all_y)
    
    valid_grid = [[1 if (ix, iy) in valid else 0 for iy in range(ny)] for ix in range(nx)]
    
    prefix = [[0] * (ny + 1) for _ in range(nx + 1)]
    for ix in range(nx):
        for iy in range(ny):
            prefix[ix + 1][iy + 1] = (valid_grid[ix][iy] 
                                       + prefix[ix][iy + 1] 
                                       + prefix[ix + 1][iy] 
                                       - prefix[ix][iy])
    
    def count_valid(ix1, iy1, ix2, iy2):
        """Count valid cells in rectangle from (ix1,iy1) to (ix2,iy2) inclusive"""
        return (prefix[ix2 + 1][iy2 + 1] 
                - prefix[ix1][iy2 + 1] 
                - prefix[ix2 + 1][iy1] 
                + prefix[ix1][iy1])
    
    def rect_size(ix1, iy1, ix2, iy2):
        """Number of cells in compressed rectangle"""
        return (ix2 - ix1 + 1) * (iy2 - iy1 + 1)
    
    def real_area(ix1, iy1, ix2, iy2):
        """Actual area using real coordinates"""
        x1, x2 = idx_to_x[ix1], idx_to_x[ix2]
        y1, y2 = idx_to_y[iy1], idx_to_y[iy2]
        return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
    
    red_compressed = set()
    for x, y in red_points:
        red_compressed.add((x_to_idx[x], y_to_idx[y]))
    
    red_list = list(red_compressed)
    best = 0
    
    for i in range(len(red_list)):
        ix1, iy1 = red_list[i]
        for j in range(i + 1, len(red_list)):
            ix2, iy2 = red_list[j]
            
            if ix1 == ix2 or iy1 == iy2:
                continue
            
            min_ix, max_ix = min(ix1, ix2), max(ix1, ix2)
            min_iy, max_iy = min(iy1, iy2), max(iy1, iy2)
            
            total_cells = rect_size(min_ix, min_iy, max_ix, max_iy)
            valid_cells = count_valid(min_ix, min_iy, max_ix, max_iy)
            
            if valid_cells == total_cells:
                area = real_area(min_ix, min_iy, max_ix, max_iy)
                if area > best:
                    best = area
    
    return best

if __name__ == "__main__":
    path = "input.txt"
    print(max_area(path))