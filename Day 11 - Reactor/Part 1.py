def solve(filename):
    graph = {}
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(':')
            device = parts[0].strip()
            
            if len(parts) > 1 and parts[1].strip():
                outputs = parts[1].strip().split()
            else:
                outputs = []
            
            graph[device] = outputs
    
    if 'out' not in graph:
        graph['out'] = []
    
    def count_paths(current, visited):
        if current == 'out':
            return 1
        
        if current not in graph:
            return 0
        
        total_paths = 0
        
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                total_paths += count_paths(neighbor, visited)
                visited.remove(neighbor)
        
        return total_paths
    
    visited = {'you'}
    result = count_paths('you', visited)
    
    return result  

if __name__ == "__main__":
    print(solve('input.txt'))