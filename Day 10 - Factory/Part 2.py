import re
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def parse_line(line):
    buttons = []
    for match in re.finditer(r'\(([^)]+)\)', line):
        content = match.group(1)
        indices = [int(x) for x in content.split(',')]
        buttons.append(indices)
    
    joltage_match = re.search(r'\{([^}]+)\}', line)
    joltages = [int(x) for x in joltage_match.group(1).split(',')]
    
    return buttons, joltages

def min_presses_joltage(buttons, targets):
    n_counters = len(targets)
    n_buttons = len(buttons)
    
    if n_buttons == 0:
        return 0 if all(t == 0 for t in targets) else float('inf')
    
    A = np.zeros((n_counters, n_buttons), dtype=float)
    for i, button in enumerate(buttons):
        for j in button:
            if j < n_counters:
                A[j][i] = 1
    
    b = np.array(targets, dtype=float)
    c = np.ones(n_buttons)
    constraints = LinearConstraint(A, b, b)
    
    upper = max(targets) + 1 if targets else 1
    bounds = Bounds(lb=0, ub=upper * n_buttons)
    
    integrality = np.ones(n_buttons)
    
    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)
    
    if result.success:
        return int(round(result.fun))
    else:
        bounds = Bounds(lb=0, ub=sum(targets) + 1)
        result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)
        if result.success:
            return int(round(result.fun))
        return float('inf')

def solve(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        buttons, targets = parse_line(line)
        presses = min_presses_joltage(buttons, targets)
        total += presses
    
    return total

if __name__ == "__main__":
    result = solve("input.txt")
    print(result)