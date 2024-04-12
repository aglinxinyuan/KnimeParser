from collections import Counter
import matplotlib.pyplot as plt
from os import listdir, path


def count(item):
    x = []
    y = []
    current = 0
    for c in sorted(Counter(item).items()):
        current += c[1] / len(item)
        x.append(c[0])
        y.append(current)
    return x, y

op = []
edge = []
multi_in = []
multi_out = []
op_list = []

for filename in listdir("graph"):
    if filename.endswith(".txt"):
        with open(path.join("graph", filename), "r") as f:
            operators = int(f.readline().split()[-1])
            edges = int(f.readline().split()[-1])
            if operators <= 1000 and edges <= 1000:
                op.append(operators)
                edge.append(edges)
                multi_in.append(int(f.readline().split()[-1]))
                multi_out.append(int(f.readline().split()[-1]))
            else:
                print(filename)
    if filename.endswith(".op"):
        with open(path.join("graph", filename), "r") as f:
            for line in f.readlines():
                op_list.append(line.rstrip())


plt.figure(figsize=(10, 4))
plt.plot(*count(op),        label='# Operators',                            linestyle='solid', marker='+')
plt.plot(*count(edge),      label='# Edges',                                linestyle='dashdot', marker='x')
plt.plot(*count(multi_in),  label='# Operators with multiple input ports',  linestyle='dotted', marker='1')
plt.plot(*count(multi_out), label='# Operators with multiple output ports', linestyle='dotted', marker='2')
plt.xscale('symlog')
plt.legend(loc='lower right')
plt.tight_layout()
plt.show()
