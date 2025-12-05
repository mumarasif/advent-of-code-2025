file_path = "input.txt"
dial = 50
password = 0
with open(file_path, 'r') as file:
    for rotation in file:
        dir = rotation[0]
        dist = int(rotation[1:])

        if dir == 'L':
            dial -= dist

        else:
            dial += dist

        dial = dial % 100
        
        if dial == 0:
            password += 1

print(password)