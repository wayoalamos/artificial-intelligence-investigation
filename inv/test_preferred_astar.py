from puzzle_nn import Puzzle
from preferred_astar import PrefAstar

def load_problems(problems):  ## carga los problemas en memoria
    f = open('problems.txt')
    while f:
        line = f.readline()
        line = line.rstrip()
        numlist = line.split(' ')
        if len(numlist) < 15:
            return
        problems.append(Puzzle([int(x) for x in numlist[1:]]))


show_solutions = False        # mostramos las soluciones?
total_problems = 20           # numero de instancias a ejecutar
size = 23                     # tamano del panqueque

heuristic = Puzzle.zero_heuristic  # h = 0 -- búsqueda ciega
heuristic = Puzzle.manhattan       # heuristica basda en distancia manhattan
#heuristic = Puzzle.pdb_max12          # una heurística basada en pattern databases que usted debe implementar
#Puzzle.initialize_pdb(1)          # inicialización de la heurística basada en PDBs
#Puzzle.initialize_pdb(2)

print('%5s%10s%10s%10s%10s%10s' % ('#prob','#exp', '#gen', '|sol|', 'tiempo','maxsubopt'))
problems = []
load_problems(problems)
#problems = [Puzzle([1,2,3,4,0,5,6,7,8,9,10,11,12,13,14,15])]
total_time = 0
total_cost = 0
total_expansions = 0
#num_problems = len(problems) # cambiar si quieres ejecutar sobre todos los problemas
num_problems = 10             # solo ejecutamos los primeros 10 problemas
for prob in range(0, num_problems):
    init = problems[prob]
    s = PrefAstar(init, heuristic, 1) # agregar un tercer parámetro una vez que lo hayas transformado en Weighted A*
    result = s.search()
    print('%5d%10d%10d%10d%10.2f%10.2f' % (prob+1, s.expansions, len(s.generated), result.g, s.end_time-s.start_time, s.estimate_suboptimality()))
    total_time += s.end_time - s.start_time
    total_cost += result.g
    total_expansions += s.expansions
    if show_solutions:
        print(result.trace())
print('Tiempo total:        %.2f'%(total_time))
print('Expansiones totales: %d'%(total_expansions))
print('Costo total:         %d'%(total_cost))
