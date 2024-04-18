import pandas as pd
import matplotlib.pyplot as plt
import csv

dic = {}
plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(8, 4), dpi=300)
with open("data.csv", mode='r', encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=',')
    for row in csv_reader:
        key = int(row[0])
        value1 = float(row[1])
        if key in dic:
            dic[key][0] += value1
            dic[key][1] += 1
        else:
            dic[key] = [value1, 1]
r0 = []
r1 = []
r2 = []
for key, value in sorted(dic.items()):
    r0.append(key)
    r1.append((1.0 - (value[0] / value[1])) * 100)
    r2.append(value[1])
plt.bar(r0, r1, color="black")
#plt.scatter(r0, r1, s=r2)
#plt.yscale('linear')
#plt.yticks([10, 100, 1000, 10000], labels=[10, 100, 1000, 10000])

plt.xlabel('Number of Non-Blocking Edges in a Workflow')
plt.ylabel('Relative Cost (%)')
plt.tight_layout()
plt.savefig('mat-size-diff.pdf', format='pdf')
plt.show()
