file_path = "input.txt"
with open(file_path, 'r') as f:
    line = f.read().strip()

ranges = line.split(",")

total = 0

def is_invalid_id(n: int) -> bool:
    s = str(n)
    
    # length must be even (otherwise cannot be X+X)
    if len(s) % 2 == 1:
        return False
    
    half = len(s) // 2
    left = s[:half]
    right = s[half:]
    
    return left == right


for r in ranges:
    start, end = map(int, r.split("-"))
    
    for n in range(start, end + 1):
        if is_invalid_id(n):
            total += n

print(total)
