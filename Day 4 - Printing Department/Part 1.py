with open("input.txt", "r") as file:
    grid = [line.strip() for line in file]

total = 0
rows = len(grid)
cols = len(grid[0])

# for i in range(rows):
#     for j in range(cols):
#         roll = 0
#         if grid[i][j] == '@':
#             if (i-1 >= 0 and j-1 >= 0) and grid[i-1][j-1] == '@':
#                 roll += 1

#             if (i-1 >= 0) and grid[i-1][j] == '@':
#                 roll += 1
            
#             if (i-1 >= 0 and j+1 < cols) and grid[i-1][j+1] == '@':
#                 roll += 1

#             if (j-1 >= 0) and grid[i][j-1] == '@':
#                 roll += 1

#             if (j+1 < cols) and grid[i][j+1] == '@':
#                 roll += 1
            
#             if (i+1 < rows and j-1 >= 0) and grid[i+1][j-1] == '@':
#                 roll += 1
            
#             if (i+1 < rows) and grid[i+1][j] == '@':
#                 roll += 1

#             if (i+1 < rows and j+1 < cols) and grid[i+1][j+1] == '@':
#                 roll += 1

#             if roll < 4: total +=1 


# 8 directions (row, col)
dirs = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1), (1, 0), (1, 1)
]

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
            total += 1

print(total)