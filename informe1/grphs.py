import matplotlib.pyplot as plt
import numpy as np; np.random.seed(1)

time = [2.8, 102, 42, 54, 122, 46.24, 24.7, 9.25, 8.9, 9.8, 4.13]
expansions = [2227, 111950, 49069, 56807, 952586, 419630, 213438, 76480, 77848, 90058, 35766]
length = [267,  259, 279, 261, 235, 235, 239, 251, 263, 287, 335]
names = ["ANN4", "ANN3", "ANN2", "ANN1", "astar 1", "astar 1.2", "astar 1.3", "astar 1.5", "astar 1.7", "astar 2", "astar 3"]
optimality = [i/235 for i in length]

print(len(time))
print(len(length))
print(len(names))

fig, ax = plt.subplots()
ax.scatter(length, time)

for i, txt in enumerate(names):
    ax.annotate(txt, (length[i], time[i]))

plt.xlabel("length")
plt.ylabel("time (s)")
plt.show()

fig, ax = plt.subplots()
ax.scatter(length, expansions)

for i, txt in enumerate(names):
    ax.annotate(txt, (length[i], expansions[i]))

plt.xlabel("length")
plt.ylabel("expansions")
plt.show()





def plot_bar_x():
    # this is for plotting purpose
    index = np.arange(len(names))
    plt.bar(index, optimality)
    plt.xlabel('Algoritmos', fontsize=5)
    plt.ylabel('Optimalidad', fontsize=5)
    plt.xticks(index, names, fontsize=15, rotation=30)
    plt.title('Optimalidad (largo/largo optimo)')
    plt.show()

# plot_bar_x()
