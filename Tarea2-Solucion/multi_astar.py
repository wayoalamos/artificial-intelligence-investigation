from multi_binary_heap import MultiBinaryHeap
from multi_node import MultiNode
import time


class MultiAstar:
    def __init__(self, initial_state, heuristics, weight=1):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.weight = weight
        self.nopen = len(heuristics)
        self.heuristics = heuristics

    def search(self):
        def all_empty():
            for i in range(self.nopen):
                if not self.open[i].is_empty():
                    return False
            return True

        self.start_time = time.process_time()
        self.open = [None] * self.nopen
        for i in range(self.nopen):
            self.open[i] = MultiBinaryHeap(i)
        self.expansions = 0
        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        for i in range(self.nopen):
            initial_node.h[i] = self.heuristics[i](self.initial_state)
            initial_node.key[i] = 10000*self.weight*initial_node.h[i]  # asignamos el valor f
            self.open[i].insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        current = 0
        while not all_empty():
            if self.open[current].is_empty():
                current = (current + 1) % self.nopen
                continue
            n = self.open[current].extract()   # extrae n de la open
            if n.state.is_goal():
                self.end_time = time.process_time()
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
                    if is_new:  # creamos el nodo de child_state
                        child_node = MultiNode(child_state, n)
                        for i in range(self.nopen):
                            child_node.h[i] = self.heuristics[i](child_state)
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    for i in range(self.nopen):
                        child_node.key[i] = 10000*(child_node.g + self.weight*child_node.h[i]) - child_node.g # actualizamos el f de child_node
                        self.open[i].insert(child_node) # inserta child_node a la open si no esta en la open
            current = (current + 1) % self.nopen
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None
