import matplotlib.pyplot as plt
from os import listdir, path
import numpy as np
from itertools import pairwise

plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(9, 5), dpi=300)


tree = []
dag = []

for filename in listdir("graph"):
    if filename.endswith(".txt"):
        with open(path.join("graph", filename), "r") as f:
            f.readline()
            t = f.readline().split()[-1]
            o = int(f.readline().split()[-1])
            if o >= 10:
                f.readline()
                f.readline()
                if t == "True":
                    tree.append(o)
                else:
                    dag.append(o)

bin_tree = np.bincount(np.array(tree))
bin_dag = np.bincount(np.array(dag))
res = []

bin = [0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 380]
for pair in pairwise(bin):
    total_tree = 0
    total_dag = 0
    for j in range(pair[0], pair[1]):
        total_tree += bin_tree[j]
        if j >= len(bin_dag):
            total_dag += 0
        else:
            total_dag += bin_dag[j]
    total = total_tree + total_dag
    if total != 0:
        r = total_dag / total * 100
        res.append(r)
    else:
        res.append(0)
    print("Range:", pair[0], "-", pair[1], ", Tree:", total_tree, ", DAG:", total_dag, ", Ratio:", res[-1])
x = [10, 15, 20, 25,30, 35,40, 45,50]
bars = plt.bar(x, res[1:], color="black", label='True', width=4)
plt.xlabel('Workflow Size (Operator Number)')
plt.ylabel('Non-Tree Workflows (%)')
# Add value labels on top of each bar
#for bar in bars:
#    yval = bar.get_height()
#    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 1), ha='center', va='bottom')


plt.xticks(x, labels=["10-14", "15-19", "20-24","25-30", "30-34", "35-39", "40-44","45-49", "50+"])
plt.tight_layout()
plt.savefig('dag.pdf', format='pdf')
plt.show()
