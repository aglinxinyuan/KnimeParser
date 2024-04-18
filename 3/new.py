from itertools import pairwise

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv', sep="\t")
plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(9, 5), dpi=300)

ratio = df["# blocking edges"] / df["# edges"] * 100
pos = df["Bottom-up - Top-down"] >= 5
neg = df["Bottom-up - Top-down"] < -5

dic = {}
for i in range(len(ratio)):
    dic[ratio[i]] = (pos[i],neg[i])
import numpy as np

bin_tree = sorted(dic.items())
print(bin_tree)
res1 = []
res2 = []

bin = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
for pair in pairwise(bin):
    total = 0
    pos_count = 0
    neg_count = 0
    for i in bin_tree:
        if pair[0] <= i[0] < pair[1] :
            total += 1
            if i[1][0] == True:
                pos_count += 1
            if i[1][1] == True:
                neg_count -= 1

    if pos_count != 0:
        res1.append(pos_count/total*100)
    else:
        res1.append(0)
    if neg_count != 0:
        res2.append(neg_count/total*100)
    else:
        res2.append(0)
    #print("Range:", pair[0], "-", pair[1], ", OP:", total, ", Number:", res[-1])
x = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
plt.bar(x, res1, label='Top-Down Search Was More Efficient', width=4)
plt.bar(x, res2, label='Bottom-Up Search Was More Efficient', width=4)
#plt.plot([80, 0], [0, 0], color='red')
# Add value labels on top of each bar
#for bar in bars:
#    yval = bar.get_height()
#    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 1), ha='center', va='bottom')

plt.xticks(x, labels=["0-9","10-19","20-29","30-39","40-49", "50-59", "60-69", "70-79", "80-89", "90-100"],rotation=45)
plt.tight_layout(pad=1.4)
plt.yticks(range(-20,61,10), labels=[20,10,0,10,20,30,40,50,60])
plt.xlabel('Ratio of Blocking Edges (%)')
plt.ylabel('Ratio of Workflows (%)')
plt.legend()
plt.savefig('bottom-up-to-down-diff.pdf', format='pdf')
plt.show()
