from math import prod

def solve_cephalopod_right_to_left(path: str) -> int:
    with open(path, 'r') as f:
        lines = [ln.rstrip('\n') for ln in f.readlines()]

    if not lines:
        return 0

    nrows = len(lines)
    op_row = lines[-1]

    width = max(len(ln) for ln in lines)
    grid = [ln.ljust(width) for ln in lines]

    col_has_char = [any(grid[r][c] != ' ' for r in range(nrows)) for c in range(width)]

    blocks = []
    c = 0
    while c < width:
        if col_has_char[c]:
            start = c
            while c < width and col_has_char[c]:
                c += 1
            end = c - 1
            blocks.append((start, end))
        else:
            c += 1

    grand_total = 0

    for start, end in blocks:
        op = None
        for cc in range(start, end + 1):
            ch = grid[-1][cc]
            if ch in '+*':
                op = ch
                break
        if op is None:
            continue

        numbers = []
        for cc in range(end, start - 1, -1):
            digits = []
            for rr in range(0, nrows - 1):  
                ch = grid[rr][cc]
                if ch != ' ':
                    digits.append(ch)
            if not digits:
                continue  
            num_str = ''.join(digits)
            if not num_str.isdigit():
                continue
            numbers.append(int(num_str))

        if not numbers:
            continue
        if op == '+':
            block_value = sum(numbers)
        else: 
            block_value = prod(numbers)

        grand_total += block_value

    return grand_total


if __name__ == "__main__":
    result = solve_cephalopod_right_to_left("C:/Users/HP/Desktop/Advent of code/advent-of-code-2025/Day 6 - Trash Compactor/input.txt")
    print(result)
