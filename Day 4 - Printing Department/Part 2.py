with open("input.txt", "r") as file:
    grid = [list(line.strip()) for line in file]

rows = len(grid)
cols = len(grid[0])

dirs = [
    (-1,-1), (-1,0), (-1,1),
    (0,-1),          (0,1),
    (1,-1), (1,0), (1,1)
]

total = 0

while True:
    to_remove = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '@':
                continue

            neighbors = 0
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == '@':   
                        neighbors += 1
            
            if neighbors < 4:
                to_remove.append((r, c))

    if not to_remove:
        break  

    total += len(to_remove)

    for r, c in to_remove:
        grid[r][c] = '.'

print(total)
