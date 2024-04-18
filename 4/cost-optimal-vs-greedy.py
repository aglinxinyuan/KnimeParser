import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(8, 4), dpi=300)


df = pd.read_csv('data.csv', sep="\t")




#plt.yticks([10, 100, 1000, 10000], labels=[10, 100, 1000, 10000])


import numpy as np
# set height of bar
IT = df["Cost of Optimal Schedule"]
ECE = df["Cost of Greedy Schedule"]

barWidth = 0.25
# Set position of bar on X axis
br1 = np.arange(len(IT))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]


# Make the plot
plt.bar(br1, IT, width=barWidth, label='Exhaustive Search')
plt.bar(br2, ECE, width=barWidth, label='Greedy Search')

plt.xticks([r + barWidth for r in range(len(IT))],
           [''] * len(IT))

plt.xlabel('Workflow')
plt.ylabel('Materialization Cost (Bytes)')
plt.legend()
plt.tight_layout()
plt.yscale('log')
plt.savefig('cost-optimal-vs-greedy.pdf', format='pdf')
plt.show()