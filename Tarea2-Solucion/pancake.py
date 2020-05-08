import sys
import random
import copy


class Pancake:
    goal = None
    size = 0

    def __init__(self, stack):
        self.stack = list(stack)
        if Pancake.size == 0:
            Pancake.set_size(len(stack))

    def set_size(size):
        Pancake.size = size
        Pancake.goal = list(range(1, Pancake.size + 1))

    def set_heuristic(self, heur='gap'):
        if heur == 'gap':
            Pancake.heuristic = Pancake.gap_heuristic
        elif heur == 'lgap':
            Pancake.heuristic = Pancake.lgap_heuristic
        elif heur == 'zero':
            Pancake.heuristic = Pancake.zero_heuristic
        else:
            print('Unsupported heuristic')
            sys.exit(1)

    def __hash__(self):
        return hash(tuple(self.stack))

    def __eq__(self, other):
        return self.stack == other.stack

    def __repr__(self):
        return self.stack.__repr__()

    def zero_heuristic(self):
        return 0

    def gap_heuristic(self):
        '''
            retorna el valor de la heurística gap_heuristic
        '''
        h = 0
        for i in range(0, Pancake.size-1):
            diff = self.stack[i] - self.stack[i+1]
            if diff != 1 and diff != -1:
                h += 1
        return h

    def lgap_heuristic(self):
        '''
            retorna el valor de la heurística gap_heuristic
        '''
        h = 0
        decrease = False
        for i in range(0, Pancake.size-1):
            diff = self.stack[i] - self.stack[i+1]
            if diff != 1 and diff != -1:
                h += 1
                diff2 = self.stack[0] - self.stack[i+1]
                if (diff2 == 1 or diff2 == -1) and i != 0:
                    decrease = True
        if not decrease:
            h += 1
            print(self)
        return h

    def successors(self):
        '''
            Crea una lista de tuplas de la forma (estado, accion, costo)
            donde estado es el estado sucesor de self que se genera al ejecutar
            accion (un string) y costo (un numero real) es el costo de accion
        '''
        def create_child(flip):
            child = Pancake(self.stack)
            i = 0
            j = flip - 1
            while i < j:
                child.stack[i], child.stack[j] = child.stack[j], child.stack[i]
                i += 1
                j -= 1
            return child

        succ = []
        for f in range(2, Pancake.size + 1):
            succ.append((create_child(f), 'flip('+str(f)+')', 1))
        return succ

    def is_goal(self):
        return self.stack == self.goal
