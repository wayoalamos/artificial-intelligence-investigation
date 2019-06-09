import random

def random_exercise(grid):
    zero_x, zero_y = None, None
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                zero_x, zero_y = i, j

    for i in range(100): # make 50 random write_moves

        move = random.randint(0,3) # left, down, right, up
        times = random.randint(1,3) # repeat it
        for j in range(times):
            if move == 0 and zero_y > 0:
                grid[zero_x][zero_y] = grid[zero_x][zero_y - 1]
                grid[zero_x][zero_y - 1] = 0
                zero_y -= 1
            elif move == 0:
                move = 1
            elif move == 1 and zero_x < 3:
                grid[zero_x][zero_y] = grid[zero_x + 1][zero_y]
                grid[zero_x + 1][zero_y] = 0
                zero_x += 1
            elif move == 1:
                move = 2
            elif move == 2 and zero_y < 3:
                grid[zero_x][zero_y] = grid[zero_x][zero_y + 1]
                grid[zero_x][zero_y + 1] = 0
                zero_y += 1
            elif move == 2:
                move = 3
            elif move == 3 and zero_x > 0:
                grid[zero_x][zero_y] = grid[zero_x - 1][zero_y]
                grid[zero_x - 1][zero_y] = 0
                zero_x -= 1
    return grid

def to_str(grid):
    a = ""
    for i in range(4):
        for j in range(4):
            a += str(grid[i][j]) + " "
    return a

def generate_data():
    grid = [[5, 7, 11, 8], [14, 9, 13, 0], [10, 12, 3, 15], [6, 1, 4, 2]]
    for j in range(10):
        f= open("random-exercises-"+str(j)+".txt","w+")
        for i in range(500):
            grid = random_exercise(grid)
            f.write("00 " +to_str(grid) + "\n")
            print(i)
        f.close()

generate_data();
