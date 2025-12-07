def count_timelines(lines):
    grid = [list(line.rstrip("\n")) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
                break
        else:
            continue
        break
    else:
        raise ValueError("No 'S' found")

    active = {start: 1}
    total_timelines = 0

    while active:
        next_active = {}

        for (r, c), count in active.items():
            nr = r + 1
            if nr >= rows:
                total_timelines += count
                continue

            if grid[nr][c] == '^':
                if c - 1 >= 0:
                    next_active[(nr, c - 1)] = next_active.get((nr, c - 1), 0) + count
                if c + 1 < cols:
                    next_active[(nr, c + 1)] = next_active.get((nr, c + 1), 0) + count
            else:
                next_active[(nr, c)] = next_active.get((nr, c), 0) + count

        active = next_active

    return total_timelines

with open("input.txt") as f:
    print(count_timelines(f))
