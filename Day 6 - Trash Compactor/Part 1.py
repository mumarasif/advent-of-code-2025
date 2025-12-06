with open("C:/Users/HP/Desktop/Advent of code/advent-of-code-2025/Day 6 - Trash Compactor/input.txt", "r") as file:
    rows = file.readlines()

max_width = max(len(row) for row in rows)
rows = [row.rstrip('\n').ljust(max_width) for row in rows]

height = len(rows)
width = max_width

problem_ranges = []
in_problem = False
start = 0

for col in range(width):
    column_has_data = any(rows[row][col] != ' ' for row in range(height))

    if column_has_data and not in_problem:
        in_problem = True
        start = col

    elif not column_has_data and in_problem:
        in_problem = False
        problem_ranges.append((start, col - 1))

if in_problem:
    problem_ranges.append((start, width - 1))

total = 0

for left, right in problem_ranges:
    numbers = []
    operator = None

    for row in rows:
        chunk = row[left:right + 1].strip()

        if chunk == "+" or chunk == "*":
            operator = chunk
        elif chunk.isdigit():
            numbers.append(int(chunk))

    if operator == "+":
        result = sum(numbers)
    else:
        result = 1
        for n in numbers:
            result *= n

    total += result

print(total)
