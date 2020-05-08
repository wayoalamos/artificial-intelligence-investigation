from puzzle import Puzzle
from multi_astar import MultiAstar
import random

random.seed(0)  # semilla en 0 genera siempre los mismos problemas

show_solutions = False
total_problems = 20    # numero de instancias a ejecutar
size = 23               # tamano del panqueque
heuristics = [Puzzle.pdb_1, Puzzle.pdb_2]
#heuristics = [Puzzle.pdb_max12]
Puzzle.initialize_pdb(1)
Puzzle.initialize_pdb(2)

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
problems.append(Puzzle([13, 9, 14, 6, 12, 8, 1, 2, 3, 4, 0, 7, 5, 10, 11, 15]))
problems.append(Puzzle([3, 14, 9, 11, 5, 4, 8, 2, 13, 12, 6, 7, 10, 1, 15, 0]))
problems.append(Puzzle([14, 13, 4, 11, 15, 8, 6, 9, 0, 7, 3, 1, 2, 10, 12, 5]))
problems.append(Puzzle([8, 11, 4, 6, 7, 3, 10, 9, 2, 12, 15, 13, 0, 1, 5, 14]))
problems.append(Puzzle([12, 15, 2, 6, 1, 14, 4, 8, 5, 3, 7, 0, 10, 13, 9, 11]))
problems.append(Puzzle([6, 0, 5, 10, 11, 12, 9, 2, 1, 7, 4, 3, 14, 8, 13, 15]))
problems.append(Puzzle([12, 8, 15, 13, 1, 0, 5, 4, 6, 3, 2, 11, 9, 7, 14, 10]))
problems.append(Puzzle([4, 7, 13, 10, 1, 2, 9, 6, 12, 8, 14, 5, 3, 0, 11, 15]))
problems.append(Puzzle([6, 14, 10, 5, 15, 8, 7, 1, 3, 4, 2, 0, 12, 9, 11, 13]))
problems.append(Puzzle([13, 14, 6, 12, 4, 5, 1, 0, 9, 3, 10, 2, 15, 11, 8, 7]))
problems.append(Puzzle([3, 14, 9, 7, 12, 15, 0, 4, 1, 8, 5, 6, 11, 10, 2, 13]))
total_time = 0
total_cost = 0
total_problems = len(problems) # cambiar si quieres menos problemas
for prob in range(0, total_problems):
    init = problems[prob]  # problema aleatorio
    s = MultiAstar(init, heuristics, 50)
    result = s.search()
    print('%5d%10d%10d%10d%10.2f' % (prob+1,s.expansions, len(s.generated), result.g, s.end_time-s.start_time))
    total_time += s.end_time - s.start_time
    total_cost += result.g
    if show_solutions: print(result.trace())
print('Total time: %.3f'%(total_time))
print('Total cost: %.3d'%(total_cost))
