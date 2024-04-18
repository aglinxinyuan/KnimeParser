import matplotlib.pyplot as plt
from os import listdir, path
import numpy as np
from itertools import pairwise

plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(8, 4), dpi=300)

op = []
edge = []
blocking = []
cycle = []


for filename in listdir("graph"):
    if filename.endswith(".txt"):
        with open(path.join("graph", filename), "r") as f:
            f.readline()
            f.readline()
            o = int(f.readline().split()[-1])
            if o >= 10:

                e = int(f.readline().split()[-1])
                if e >= 10:
                    op.append(o)
                    edge.append(e)
                    blocking.append(int(f.readline().split()[-1]))

                    f.readline()
                    f.readline()
                    f.readline()
                    f.readline()
                    f.readline()
                    f.readline()
                    f.readline()
                    f.readline()

                    cycle.append(int(f.readline().split()[-1]))


bin_tree = np.bincount(np.array(op))
res = []

bin = [0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 380]
for pair in pairwise(bin):
    total_tree = 0
    total_dag = 0
    for j in range(pair[0], pair[1]):
        total_tree += bin_tree[j]

    if total_tree != 0:
        res.append(total_tree)
    else:
        res.append(0)
    print("Range:", pair[0], "-", pair[1], ", OP:", total_tree, ", Number:", res[-1])
x = [10, 15, 20, 25,30, 35,40, 45,50]
bars = plt.bar(x, res[1:], label='True', width=4, color="black")

# Add value labels on top of each bar
#for bar in bars:
#    yval = bar.get_height()
#    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 1), ha='center', va='bottom')

plt.xticks(x, labels=["10-14", "15-19", "20-24","25-30", "30-34", "35-39", "40-44","45-49", "50+"])
plt.tight_layout(pad=1.3)
plt.xlabel('Workflow Size (Operator Number)')
plt.ylabel('Number of Workflows')
plt.savefig('op-bar.pdf', format='pdf')
plt.show()
