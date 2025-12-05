file_path = "input.txt"
dial = 50
num = dial
password = 0

with open(file_path, "r") as file:
    for rotation in file:
        direction = rotation[0]
        dist = int(rotation[1:])

        step = -1 if direction == 'L' else 1

        for _ in range(dist):
            dial = (dial + step) % 100
            if dial == 0:
                password += 1

print(password)