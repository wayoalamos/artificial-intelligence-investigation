# Una implementacion muy simplificada de DFS
import sys
import random
from node import Node
from puzzle import Puzzle

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def insert(self, item):
        self.push(item)

    def extract(self):
        return self.pop()

    def is_empty(self):
        return (self.items == [])

    def __repr__(self):
        return str(self.items) + ' (top = final de la lista) '

    def __len__(self):
        return len(self.items)


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return (self.items == [])

    def __repr__(self):
        return str(self.items) + ' (el del principio se muestra primero) '

    def __len__(self):
        return len(self.items)

    def insert(self, item):
        self.enqueue(item)

    def extract(self):
        return self.dequeue()


class GenericSearch:
    def __init__(self, initial_state, strategy, file):
        self.expansions = 0
        self.initial_state = initial_state
        self.strategy = strategy
        self.max_depth = 0
        self.file = file

    def _newopen(self):
        if self.strategy == 'bfs':
            return Queue()
        elif self.strategy == 'dfs':
            return Stack()
        else:
            print(type, 'is not supported')
            sys.exit(1)

    def write_state(self, state, depth):
        self.file.write(' '.join([str(n) for n in state.board]) + ' ' + str(depth) + '\n')

    def search(self):
        self.open = self._newopen()
        self.expansions = 0
        self.open.insert(Node(self.initial_state))
        self.generated = set()  ## generated mantiene la union entre OPEN y CLOSED
        self.generated.add(self.initial_state)
        while not self.open.is_empty():
#            print(self.open)      # muestra open list
            n = self.open.extract()   # extrae n de la open
#            print(n.state)   # muestra el estado recien expandido
            self.write_state(n.state, n.depth)
            if n.depth > self.max_depth:
                self.max_depth = n.depth
                print('at depth', n.depth)
            succ = n.state.successors()
            self.expansions += 1
            for child_state, action, _ in succ:
                if child_state in self.generated:  # en DFS este chequeo se puede hacer sobre la rama
                    continue
                child_node = Node(child_state, n, action)
                if child_state.is_goal():
                    return child_node
                self.generated.add(child_state)
                self.open.insert(child_node)
        return None


def abstract(board, pattern):
    abstract_board = []
    for x in board:
        if x in pattern or x == 0:
            abstract_board.append(x)
        else:
            abstract_board.append(-1)
    return abstract_board

# 0  1  2  3
# 4  5  6  7
# 8  9 10 11
#12 13 14 15
pattern = [2, 3, 7, 11]  ## patron a utilizar
pattern = [8, 12, 13, 14]  ## patron a utilizar
abstract_init = abstract(list(range(16)), pattern)  ## generamos estado inicial en donde se abstrae a -1 todo lo que no esta en pattern

init = Puzzle(abstract_init)
f = open('pdb2.txt', 'w')
f.write(' '.join([str(x) for x in pattern])+'\n') ## escribimos el patron
s = GenericSearch(init, 'bfs', f)
result = s.search()
print('Number of generated states=',len(s.generated))
f.close()
