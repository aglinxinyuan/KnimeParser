import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv', sep="\t")
plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(8, 4), dpi=300)


plt.plot([80, 0], [0, 0], color='red')
plt.scatter(df["searchSpace"], df["Bottom-up Greedy - Top-down Greedy"], s=15)
plt.yscale('symlog')

plt.xlabel('Number of Non-Blocking Edges in a Workflow')
plt.ylabel('Time (ms)')
#plt.yticks([10, 100, 1000, 10000], labels=[10, 100, 1000, 10000])
plt.tight_layout()
plt.savefig('bottom-up-greedy-top-down-greedy-diff.pdf', format='pdf')
plt.show()
