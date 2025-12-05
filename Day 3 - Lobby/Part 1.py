total = 0

with open("input.txt", "r") as f:
    for line in f:
        digits = line.strip()

        best = 0

        for i in range(len(digits)):
            for j in range(i + 1, len(digits)):
                num = int(digits[i] + digits[j])
                if num > best:
                    best = num

        total += best

print(total)
