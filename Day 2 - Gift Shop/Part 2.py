file_path = "input.txt"

with open(file_path) as f:
    line = f.read().strip()

ranges = line.split(",")

total = 0

def is_invalid_id(n: int) -> bool:
    s = str(n)
    L = len(s)

    for block_size in range(1, L // 2 + 1):
        if L % block_size != 0:
            continue
        
        block = s[:block_size]
        repeat_count = L // block_size
      
        if repeat_count >= 2 and block * repeat_count == s:
            return True

    return False


for r in ranges:
    start, end = map(int, r.split("-"))
    
    for n in range(start, end + 1):
        if is_invalid_id(n):
            total += n

print(total)
