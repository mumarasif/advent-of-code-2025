def solve(filename):
    graph = {}
    all_nodes = set()
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(':')
            device = parts[0].strip()
            all_nodes.add(device)
            
            if len(parts) > 1 and parts[1].strip():
                outputs = parts[1].strip().split()
            else:
                outputs = []
            
            for o in outputs:
                all_nodes.add(o)
            
            graph[device] = outputs
    
    for node in all_nodes:
        if node not in graph:
            graph[node] = []
    
    memo = {}
    
    def count_paths(current, mask):
        if current == 'dac':
            mask |= 1
        if current == 'fft':
            mask |= 2
        
        if current == 'out':
            return 1 if mask == 3 else 0
        
        if (current, mask) in memo:
            return memo[(current, mask)]
        
        if not graph.get(current):
            memo[(current, mask)] = 0
            return 0
        
        total_paths = 0
        for neighbor in graph[current]:
            total_paths += count_paths(neighbor, mask)
        
        memo[(current, mask)] = total_paths
        return total_paths
    
    result = count_paths('svr', 0)
    return result

if __name__ == "__main__":
    print(solve('input.txt'))