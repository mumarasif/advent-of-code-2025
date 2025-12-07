def count_splits(lines):
    grid = [list(line.rstrip("\n")) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    start = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
                break
        if start:
            break
    if start is None:
        raise ValueError("No start 'S' found in grid")

    active = { start }   
    splits = 0

    while active:
        next_active = set()
        for r, c in active:
            nr = r + 1
            if nr >= rows:
                continue
            below = grid[nr][c]
            if below == '^':
                splits += 1
                left_c = c - 1
                right_c = c + 1
                if 0 <= left_c < cols:
                    next_active.add((nr, left_c))
                if 0 <= right_c < cols:
                    next_active.add((nr, right_c))
            else:
                next_active.add((nr, c))
        active = next_active

    return splits

with open("input.txt") as f:
    print(count_splits(f))