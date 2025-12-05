def max_k_from_digits(s: str, k: int) -> str:
    n = len(s)
    if k >= n:
        return s  
    drop = n - k
    stack = []
    for ch in s:
        while drop and stack and stack[-1] < ch:
            stack.pop()
            drop -= 1
        stack.append(ch)
    if drop:
        stack = stack[:-drop]
    return ''.join(stack[:k])


def total_joltage_for_file(path: str, k: int = 12) -> int:
    total = 0
    with open(path, 'r') as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            chosen = max_k_from_digits(s, k)
            total += int(chosen)
    return total


if __name__ == "__main__":
    result = total_joltage_for_file("input.txt", k=12)
    print(result)
