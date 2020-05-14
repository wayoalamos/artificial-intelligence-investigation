from puzzle import Puzzle
from astar import Astar

show_solutions = False
heuristic = Puzzle.manhattan


def load_problems(problems):  ## carga los problemas en memoria
    f = open('problems.txt')
    while f:
        line = f.readline()
        line = line.rstrip()
        numlist = line.split(' ')
        if len(numlist) < 15:
            return
        problems.append(Puzzle([int(x) for x in numlist[1:]]))

print('%5s%10s%10s%10s%10s' % ('#prob','#exp', '#gen', '|sol|', 'tiempo'))

problems = []
load_problems(problems)
 
total_time = 0
total_cost = 0
total_problems = len(problems) # cambiar si quieres menos problemas
for prob in range(0, total_problems):
    init = problems[prob]  # problema aleatorio
    s = Astar(init, heuristic, 1)
    result = s.search()
    print('%5d%10d%10d%10d%10.2f' % (prob+1,s.expansions, len(s.generated), result.g, s.end_time-s.start_time))
    total_time += s.end_time - s.start_time
    total_cost += result.g
    if show_solutions: print(result.trace())
print('Total time: %.3f'%(total_time))
print('Total cost: %.3d'%(total_cost))
