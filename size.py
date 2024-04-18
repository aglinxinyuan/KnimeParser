import os

map = {}
map1 = {}
for filename in os.listdir('graph'):
    if filename.endswith('.txt'):
        with open(os.path.join("graph", filename), "r") as f:
            name = f.readline().split(": ")[-1].strip()
            map[name] = filename.split(".")[0]
            map1[filename.split(".")[0]] = name

import csv
import graphviz
with open("id.csv", mode ='r', encoding="utf-8") as file:
  csv_reader = csv.reader(file, delimiter='\t')
  for row in csv_reader:
      map[row[1]] = row[0]
res = []
for filename in os.listdir('graph'):
    if filename.endswith('.dot'):
        id = map[map1[filename.split('.')[0]]]
        with open(os.path.join("graph", filename), "r") as f:
            size = 0
            for line in f:
                if "->" in line:
                    data = line.strip().split('"')[-2].split(";")
                    datasize = int(data[0].split(": ")[-1])
                    if (data[1].split(": ")[-1]=="False"):
                        size += datasize
        res.append([id, size])

with open("mat.csv", mode ='w', encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=',')
    for row in res:
        writer.writerow(row)