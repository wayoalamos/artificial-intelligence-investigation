GOAL = {
    1: (0, 0), 2: (0,1), 3: (0, 2), 4: (0,3),
    5: (1, 0), 6: (1,1), 7: (1, 2), 8: (1,3),
    9: (2, 0), 10: (2,1), 11: (2, 2), 12: (2,3),
    13: (3, 0), 14: (3,1), 15: (3, 2), 0: (3,3),
}

class State:
    def __init__(self, values=[], goal=GOAL):
        self.goal = goal
        self.values = values
        self.matrix = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        self.set_matrix()
        self.next = None
        self.heuristic = self.calculate_heuristic()

    def set_matrix(self):
        if not self.values: return
        for i in range(4):
            for j in range(4):
                self.matrix[i][j] = self.values[4*i + j]
    
    def calculate_heuristic(self):
        total = 0
        for i in range(4):
            for j in range(4):
                manhattan_distance = self.get_manhattan_distance(i, j)
                print(i,j,manhattan_distance)
                total += manhattan_distance
        return total
    
    def get_manhattan_distance(self, i, j):
        value = self.values[4*i + j]
        last = self.goal[value] # (i, j)
        diff_i = abs(i-last[0])
        diff_j = abs(j-last[1])
        return diff_i + diff_j 
    
    def print_state(self, state):
        print("STATE: ")
        for i in range(4):
            line = ""
            for j in range(4):
                val = state[i][j]
                line += str(val) + "  "
                if val < 10: line +=" "
            print(line)
    
    def get_positions(self):
        # {value: (i, j)}
        positions = {}
        for i in range(4):
            for j in range(4):
                positions[self.matrix[i][j]] = (i, j)
        return positions
        


class ManageFile:
    def __init__(self):
        pass

    def convert_line(self, line):
        line = line.split(" ")
        line = line[1:]
        line = [int(i) for i in line]
        return line


class LRTA:
    def __init__(self, initial_state):
        self.acutal_state = initial_state
        # self.heuristics.print_state(self.heuristics.values)
    
    def get_state_copy(self, state):
        new_state = State(state.values)
        return new_state

    def is_goal(self, state):
        return self.goal.values == state.values
    
    def find_next_state(self, state):
        # return State
        pass

    def run(self):
        while not self.is_goal(self.acutal_state):
            next_state = self.find_next_state(self.acutal_state) # [State, ]
            #self.heuristics.values[]
            



mf = ManageFile()

problem = "00 0 1 9 7 11 13 5 3 14 12 4 2 8 6 10 15"
problem = mf.convert_line(problem)
s = State(problem)
# l = LRTA(s)













