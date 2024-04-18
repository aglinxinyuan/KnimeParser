import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(9, 5), dpi=300)

seconds = 1
cutoff = seconds * 1000  #ms
# Load the CSV data into a DataFrame
df = pd.read_csv('data.csv', sep="\t")
dic = {}
# Load the CSV data into a DataFrame
df = pd.read_csv('data.csv', sep="\t")
for index, row in df.iterrows():
    key = row["searchSpace"]
    value1 = row["00000-searchTime"]
    value2 = row["00100-searchTime"]
    value3 = row["00001-searchTime"]
    value4 = row["00010-searchTime"]
    value5 = row["00111-searchTime"]

    x1 = row["00000-searchFinished"]
    x2 = row["00100-searchFinished"]
    x3 = row["00001-searchFinished"]
    x4 = row["00010-searchFinished"]
    x5 = row["00111-searchFinished"]
    if key in dic:
        if value1 < cutoff:
            dic[key][0] += 1
        if value2 < cutoff:
            dic[key][1] += 1
        if value3 < cutoff:
            dic[key][2] += 1
        if value4 < cutoff:
            dic[key][3] += 1
        if value5 < cutoff:
            dic[key][4] += 1
        dic[key][5] += 1
    else:
        dic[key] = [
            0,
            0,
            0,
            0,
            0,
            1]
r1 = []
r2 = []
r3 = []
r4 = []
r5 = []
c = []
rx1 = []
rx2 = []
rx3 = []
rx4 = []
rx5 = []
ry1 = []
ry2 = []
ry3 = []
ry4 = []
ry5 = []
k = []
for key, value in sorted(dic.items()):
    k.append(key)
    v1 = value[0] / value[5] * 100
    v2 = value[1] / value[5] * 100
    v3 = value[2] / value[5] * 100
    v4 = value[3] / value[5] * 100
    v5 = value[4] / value[5] * 100
    r1.append(v1)
    r2.append(v2)
    r3.append(v3)
    r4.append(v4)
    r5.append(v5)
    c.append(value[5])

for i, key in enumerate(k):
    print(i, key)
k = [k[9], k[19], k[28], k[37]]
r1 = [r1[9], r1[19], r1[28], r1[37]]
r2 = [r2[9], r2[19], r2[28], r2[37]]
r3 = [r3[9], r3[19], r3[28], r3[37]]
r4 = [r4[9], r4[19], r4[28], r4[37]]
r5 = [r5[9], r5[19], r5[28], r5[37]]

barWidth = 0.15
# Set position of bar on X axis
br2 = np.arange(len(r1))
br1 = [k - barWidth for k in br2]
br3 = [k + barWidth for k in br2]
br4 = [k + barWidth for k in br3]
br5 = [k + barWidth for k in br4]

# Make the plot
plt.bar(br1, r1, width=barWidth, label='No Optimization')
plt.bar(br2, r3, width=barWidth, label='Optimization (Early Stopping)')
plt.bar(br3, r4, width=barWidth, label='Optimization (Clean Edges)')
plt.bar(br4, r2, width=barWidth, label='Optimization (Chains)')
plt.bar(br5, r5, width=barWidth, label='All Optimizations')

plt.xticks([r + barWidth for r in range(len(r1))], labels=["10", "20", "30", "40"])

plt.xlabel('Number of Non-Blocking Edges in a Workflow')
plt.ylabel('Ratio of Workflows (%)')
plt.legend(loc='upper right', prop={'size': 13})
plt.tight_layout()
plt.savefig('ablation-chain-time.pdf', format='pdf')
plt.show()
