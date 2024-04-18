from collections import Counter
import matplotlib.pyplot as plt
from os import listdir, path

plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(8, 4), dpi=300)


def count(item):
    x = []
    y = []
    current = 0
    for c in sorted(Counter(item).items()):
        current += c[1] / len(item) * 100
        x.append(c[0])
        y.append(current)
    return x, y

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

plt.figure(figsize=(10, 4))
plt.plot(*count(op),        label='# Operators',                    linestyle='solid', marker='+')
plt.plot(*count(edge),      label='# Edges',                        linestyle='dashdot', marker='x')
#plt.plot(*count(blocking),  label='# Blocking Edges',               linestyle='dotted', marker='1')
#plt.plot(*count(cycle),     label='# Edges In An Undirected Cycle', linestyle='dotted', marker='2')
plt.xscale('log')
plt.xticks([10, 30, 100, 380], labels=['10', '30', '100','380'])
plt.xlabel('Workflow Size')
plt.ylabel('Ratio (%)')
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('op_edge.pdf', format='pdf')
plt.show()