import os
import csv
results = []
for filename in os.listdir("graph"):
    if filename.endswith(".txt"):
        name = filename.split(".")[0]
        print(name)
        with open(os.path.join("graph", filename), "r") as f:
            operators = f.readline().split()[-1]
            edges = f.readline().split()[-1]
            multIO = f.readline().split()[-1]
            results.append([name, operators, edges, multIO])


with open('results.csv', 'w', newline='') as file:

    writer = csv.writer(file)
    writer.writerow(["Workflow", "Operators", "Edges", "multIO"])
    for result in results:
        writer.writerow(result)
