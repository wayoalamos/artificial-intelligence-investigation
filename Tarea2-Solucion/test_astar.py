from puzzle import Puzzle
from astar import Astar
import random

random.seed(0)  # semilla en 0 genera siempre los mismos problemas

show_solutions = False
total_problems = 20    # numero de instancias a ejecutar
size = 23               # tamano del panqueque
heuristic = Puzzle.zero_heuristic
heuristic = Puzzle.manhattan
heuristic = Puzzle.pdb_1
Puzzle.initialize_pdb(1)


print('%5s%10s%10s%10s%10s' % ('#prob','#exp', '#gen', '|sol|', 'tiempo'))

problems = []
problems.append(Puzzle([0, 1, 9, 7, 11, 13, 5, 3, 14, 12, 4, 2, 8, 6, 10, 15]))
problems.append(Puzzle([14, 1, 9, 6, 4, 8, 12, 5, 7, 2, 3, 0, 10, 11, 13, 15]))
problems.append(Puzzle([4, 5, 7, 2, 9, 14, 12, 13, 0, 3, 6, 11, 8, 1, 15, 10]))
problems.append(Puzzle([13, 8, 14, 3, 9, 1, 0, 7, 15, 5, 4, 10, 12, 2, 6, 11]))
problems.append(Puzzle([9, 14, 5, 7, 8, 15, 1, 2, 10, 4, 13, 6, 12, 0, 11, 3]))
problems.append(Puzzle([7, 11, 8, 3, 14, 0, 6, 15, 1, 4, 13, 9, 5, 12, 2, 10]))
problems.append(Puzzle([5, 7, 11, 8, 0, 14, 9, 13, 10, 12, 3, 15, 6, 1, 4, 2]))
problems.append(Puzzle([6, 10, 1, 14, 15, 8, 3, 5, 13, 0, 2, 7, 4, 9, 11, 12]))
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
