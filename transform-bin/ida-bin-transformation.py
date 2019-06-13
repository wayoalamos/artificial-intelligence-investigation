def transform_to_bin(path, new_path):
    file = open(path, "r+")
    new_file = open(new_path, "w+")
    line = [
    "1000000000000000",
    "0100000000000000",
    "0010000000000000",
    "0001000000000000",
    "0000100000000000",
    "0000010000000000",
    "0000001000000000",
    "0000000100000000",
    "0000000010000000",
    "0000000001000000",
    "0000000000100000",
    "0000000000010000",
    "0000000000001000",
    "0000000000000100",
    "0000000000000010",
    "0000000000000001"
    ]
    last_position = 0
    for num in file.readlines():
        num = int(num.strip())
        move = False
        if (num - last_position) == 1: # move to the left
            move = 1
        if (num - last_position) == -4: # move down
            move = 2
        if (num - last_position) == -1: # move to the right
            move = 3
        if (num - last_position) == 4: #move up
            move = 4
        temp = line[last_position]
        line[last_position] = line[num]
        line[num] = temp
        str_bin = ["0", "0", "0", "0"]
        str_bin[move-1] = "1"
        to_write = " ".join(line)+" "+ "".join(str_bin)
        last_position = num
        new_file.write(to_write + "\n")
    file.close()

path = "../moves-from-generated-data/ida_problem_0_.txt"
new_path = "../moves/bin-moves/sol_ida_problem_0_.txt"
for i in range(150):
    path = path[:41] + str(i) + "_.txt"
    new_path = new_path[:35] + str(i) + "_.txt"
    transform_to_bin(path, new_path)
