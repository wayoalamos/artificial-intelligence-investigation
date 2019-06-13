file = open("solutions_e.txt", "w+")
for i in range(70):
    path = "../moves-example-one-bin-astar/bin_problem_" + str(i) + "_.txt"
    f = open(path, "r")
    lines = f.readlines()
    for line in lines:
        file.write(line)
    f.close()
file.close()
