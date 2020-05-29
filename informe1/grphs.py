import matplotlib.pyplot as plt
import numpy as np; np.random.seed(1)

time = [25.8, 70.6, 2.8, 122, 46.24, 24.7, 9.25, 8.9, 9.8]
expansions = [27000, 81067, 2227,  952586, 419630, 213438, 76480, 77848, 90058]
length = [255, 241,  267,  235, 235, 239, 251, 263, 287]
names = ["ANN7", "ANN6", "ANN4", "astar 1", "astar 1.2", "astar 1.3", "astar 1.5", "astar 1.7", "astar 2"]
optimality = [i/235 for i in length]

print(len(time))
print(len(length))
print(len(names))

# fig, ax = plt.subplots()
# ax.scatter(length, time)

# for i, txt in enumerate(names):
#     ax.annotate(txt, (length[i], time[i]))

# plt.xlabel("length")
# plt.ylabel("time (s)")
# plt.show()

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
