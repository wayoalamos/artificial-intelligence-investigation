INITITAL_FILE = 0
PROBLEMS = 24177
# states from 0 to 23177: 1133410
# states from 23178 to 24177: 52075
# total states: 1185485

counter = 0
load_all_data = []

for i in range(INITITAL_FILE, PROBLEMS + 1):
    fo = open('../moves/bin-moves/sol_ida_problem_'+str(i)+'_.txt')
    #counter += len(fo.readlines())
    for l in fo.readlines():
        load_all_data.append(l)
    fo.close()
print(counter)
print(len(load_all_data))
