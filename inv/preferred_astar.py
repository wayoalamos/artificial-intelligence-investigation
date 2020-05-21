from multi_binary_heap import MultiBinaryHeap
from multi_node import MultiNode
import time
import sys


class PrefAstar:
    def __init__(self, initial_state, heuristic, weight=1):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.weight = weight
        self.heuristic = heuristic


    def estimate_suboptimality(self):
        fmin = 100000000
        if self.solution is not None:
            if self.open.is_empty() and self.preferred.is_empty():
                return 1
            for node in self.open:
                if fmin > node.g + node.h:
                    fmin = node.g + node.h
            for node in self.preferred:
                if fmin > node.g + node.h:
                    fmin = node.g + node.h
            return self.solution.g/fmin


    def fvalue(self, g, h):
        return 10000*(g + self.weight*h) - g

    def search(self):
        self.start_time = time.process_time()
        self.open = MultiBinaryHeap(0)
        self.preferred = MultiBinaryHeap(0)
        self.expansions = 0
        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]
        initial_node.key[0] = self.fvalue(initial_node.g,initial_node.h[0])  # asignamos el valor f
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])
        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        current = 0
        while not self.open.is_empty() or not self.preferred.is_empty():
            if current == 1 and not self.preferred.is_empty():
                queue = self.preferred
            elif current == 0 and not self.open.is_empty():
                queue = self.open
            else:
                print("error in loop")
                continue
            n = queue.extract()   # extrae n de la open
#            if queue == self.preferred:
#                print('{}/'.format(n.h),end='')
#                sys.stdout.flush()
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n
            succ = n.state.successors()
            self.expansions += 1

            for child_state, action, cost in succ:
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new: # creamos el nodo de child_state
                        child_node = MultiNode(child_state, n)
                        child_node.h[0] = self.heuristic(child_state)
                        child_node.h[1] = child_node.h[0]
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    for i in range(2):
                        child_node.key[i] = self.fvalue(child_node.g,child_node.h[i]) # actualizamos el f de child_node
                    if child_node.state.preferred > 0.5 and current == 1:
                        self.preferred.insert(child_node) # inserta child_node a la open si no esta en la open, inserta en open preferida
                    elif child_node.state.preferred > 0.1:
                        self.open.insert(child_node) # inserta en open no preferidaa

        print("Error esto no deberia pasar!!!!!!!!!!!!!!")
        self.end_time = time.process_time() # en caso contrario, modifica la posicion de child_node en open
        return None
