import pandas as pd
import matplotlib.pyplot as plt
# Load the CSV data into a DataFrame
plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(9, 5), dpi=300)
df = pd.read_csv('bottom-up.csv', sep="\t")
dic = {}
for index, row in df.iterrows():
    key = row["searchSpace"]
    value1 = row["exhausitive-searchTime"]
    value2 = row["greedy-searchTime"]
    if key in dic:
        dic[key][0] += value1
        dic[key][1] += value2
        dic[key][2] += 1
    else:
        dic[key] = [value1, value2, 1]
r1 = []
r2 = []
r3 = []
x = []
for key, value in sorted(dic.items()):
    x.append(key)
    r1.append(value[0]/value[2])
    r2.append(value[1]/value[2])
    r3.append(value[2])

import numpy as np
barWidth = 0.40
# Set position of bar on X axis
br1 = np.arange(len(r1))
br2 = [x + barWidth for x in br1]


# Make the plot
plt.bar(br1, r1, width=barWidth, label='Exhaustive Search')
plt.bar(br2, r2, width=barWidth, label='Greedy Search')
a = range(-2,51,6)

plt.xticks(a, labels=[0, 10, 20, 30, 40, 50, 60, 70, 80])

plt.yscale('log')

plt.xlabel('Number of Non-Blocking Edges in A Workflow')
plt.ylabel('Search Time (ms)')
#plt.yticks([10, 100, 1000, 10000], labels=[10, 100, 1000, 10000])
plt.tight_layout()
plt.legend()
plt.savefig('bottom-up-search-efficiency-runtime.pdf', format='pdf')
plt.show()