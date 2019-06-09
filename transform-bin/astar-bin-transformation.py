def transform_to_bin(path, new_path):
    file = open(path, "r+")
    new_file = open(new_path, "w+")
    for line in file.readlines():
        bin_line = bin_transformation(line)
        new_file.write(bin_line + "\n")
    file.close()



def bin_transformation(line):
    solution = ""
    template = "0000000000000000 "
    line = line.split()
    for i in range(16):
        new_ans = template
        n = int(line[i])
        new_ans = template[:n] + "1" + template[n+1:]
        solution += new_ans
    for i in range(4):
        solution += line[17+i]
    return solution

path = "../moves-example-one/problem_0_.txt"
new_path = "../moves-example-one-bin/bin_problem_0_.txt"
for i in range(70):
    path = path[:29] + str(i) + "_.txt"
    new_path = new_path[:37] + str(i) + "_.txt"
    transform_to_bin(path, new_path)
