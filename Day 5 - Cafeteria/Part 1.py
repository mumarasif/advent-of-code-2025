ranges = []
available = []
reading_ranges = True
fresh = 0

with open("input.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line == "":
            reading_ranges = False
            continue

        if reading_ranges:
            a, b = map(int, line.split('-'))
            ranges.append((a, b))
        else:
            available.append(int(line))

for id in available:
    for a, b in ranges:
        if a <= id <= b:
            fresh += 1
            break
    
print(fresh)