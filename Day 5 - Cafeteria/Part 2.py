ranges = []

with open("input.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line == "":
            break
        a, b = map(int, line.split('-'))
        ranges.append((a, b))

ranges.sort()

merged = []

curr_start, curr_end = ranges[0]

for start, end in ranges[1:]:
    if start <= curr_end + 1:
        curr_end = max(curr_end, end)
    else:
        merged.append((curr_start, curr_end))
        curr_start, curr_end = start, end

merged.append((curr_start, curr_end))

fresh = 0
for a, b in merged:
    fresh += (b - a +1)

print(fresh)