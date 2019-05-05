import matplotlib.pyplot as plt
import numpy as np; np.random.seed(1)

time = [83.98, 6.18, 3.44, 640.47, 526.92, 0.31, 0.14, 3.89, 2.33, 3.36, 11.4, 56.39]
length = [5487, 6383, 11703, 5305, 5205, 6713, 31087, 247591, 35787, 52889, 16169, 10051]
names = ["astar 1.4", "astar 2", "astar 10", "ida", "wida 1", "wida 2", "wida 10", "rta", "lrta", "rlrta", "rtaa 1000", "rtaa 10000"]
optimality = [5205/i for i in length]

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



def plot_bar_x():
    # this is for plotting purpose
    index = np.arange(len(names))
    plt.bar(index, optimality)
    plt.xlabel('Algoritmos', fontsize=5)
    plt.ylabel('Optimalidad', fontsize=5)
    plt.xticks(index, names, fontsize=15, rotation=30)
    plt.title('Optimalidad (largo/largo optimo)')
    plt.show()

plot_bar_x()
