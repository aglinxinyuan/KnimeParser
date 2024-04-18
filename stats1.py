from collections import Counter
import matplotlib.pyplot as plt
from os import listdir, path


op = []
edge = []
blocking = []
cycle = []

plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(8, 4), dpi=300)

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

#plt.plot(*count(blocking),  label='# Blocking Edges',               linestyle='dotted', marker='1')
#plt.plot(*count(cycle),     label='# Edges In An Undirected Cycle', linestyle='dotted', marker='2')
plt.hist(op,bins=range(10, 150, 5))
plt.xlabel('Number of Operators')
plt.ylabel('Number of Workflows')
plt.tight_layout()
plt.savefig('op_edge.pdf', format='pdf')
plt.show()