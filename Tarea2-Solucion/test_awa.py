from pancake import Pancake
from awa import Awa
import random

random.seed(0)  # semilla en 0 genera siempre los mismos problemas

show_solutions = False
total_problems = 20    # numero de instancias a ejecutar
size = 23               # tamano del panqueque
base_list = list(range(1, size+1))  # lista a desordenar
#heuristic = 'zero'
heuristic = 'gap'

print('%5s%10s%10s%10s%10s' % ('#prob','#exp', '#gen', '|sol|', 'tiempo'))

total_time = 0
total_cost = 0
for prob in range(1, total_problems+1):
    random.shuffle(base_list)
    init = Pancake(base_list)  # problema aleatorio
    s = Awa(init, heuristic, 1.5)
    for result in s.search():
        print('%5d%10d%10d%10d%10.2f' % (prob, s.expansions, len(s.generated), result.g, s.end_time-s.start_time))
        total_time += s.end_time - s.start_time
    total_cost += result.g
    if show_solutions: print(result.trace())
print('Total time: %.3f'%(total_time))
print('Total cost: %.3d'%(total_cost))
