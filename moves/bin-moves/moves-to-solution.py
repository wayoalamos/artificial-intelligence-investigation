f = open("../../shuffle-data/solutions.txt", "w")
for i in range (65):
    path = "sol_ida_problem_" + str(i) +"_.txt"
    file = open(path, "r")
    for line in file.readlines():
        f.write(line)
    file.close()
f.close()

## 33818 + 3300 = 36.700
