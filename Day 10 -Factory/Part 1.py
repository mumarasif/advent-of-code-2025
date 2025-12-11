import re

def parse_line(line):
    indicator_match = re.search(r'\[([.#]+)\]', line)
    indicator = indicator_match.group(1)
    target = tuple(1 if c == '#' else 0 for c in indicator)
    n_lights = len(target)
    
    buttons = []
    for match in re.finditer(r'\(([^)]+)\)', line):
        content = match.group(1)
        indices = [int(x) for x in content.split(',')]
        mask = 0
        for idx in indices:
            mask |= (1 << idx)
        buttons.append(mask)
    
    target_mask = 0
    for i, bit in enumerate(target):
        if bit:
            target_mask |= (1 << i)
    
    return target_mask, buttons

def min_presses(target, buttons):
    n = len(buttons)
    
    if n == 0:
        return 0 if target == 0 else float('inf')
    
    mid = n // 2
    first_half = buttons[:mid]
    second_half = buttons[mid:]
    
    first_results = {}  
    for mask in range(1 << len(first_half)):
        xor_val = 0
        count = 0
        for i in range(len(first_half)):
            if mask & (1 << i):
                xor_val ^= first_half[i]
                count += 1
        if xor_val not in first_results or first_results[xor_val] > count:
            first_results[xor_val] = count
    
    best = float('inf')
    for mask in range(1 << len(second_half)):
        xor_val = 0
        count = 0
        for i in range(len(second_half)):
            if mask & (1 << i):
                xor_val ^= second_half[i]
                count += 1
        
        needed = target ^ xor_val
        if needed in first_results:
            total = count + first_results[needed]
            if total < best:
                best = total
    
    return best

def solve(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        target, buttons = parse_line(line)
        presses = min_presses(target, buttons)
        total += presses
    
    return total

if __name__ == "__main__":
    result = solve("input.txt")
    print(result)