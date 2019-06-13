f = open("../../shuffle-data/solutions.txt", "a")
for i in range (150):
    path = "sol_ida_problem_" + str(i) +"_.txt"
    file = open(path, "r")
    for line in file.readlines():
        f.write(line)
    file.close()
f.close()

## 37.253
