import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(8, 4), dpi=300)

df = pd.read_csv('data.csv', sep="\t")
import numpy as np
# set height of bar
a = df["Cost of Optimal Schedule"]
b = df["Cost of Greedy Schedule"]
r = (b-a)/b

IT = r

# Set position of bar on X axis
br1 = np.arange(len(IT))
# Make the plot
plt.bar(br1, IT, color="black")

plt.xticks([r for r in range(len(IT))],
           [''] * len(IT))

plt.xlabel('Workflow')
plt.ylabel('Cost Reduction (%)')
plt.tight_layout()
plt.savefig('cost-reduction.pdf', format='pdf')
plt.show()