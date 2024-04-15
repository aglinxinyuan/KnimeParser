from os import listdir, path

result = {}
for filename in listdir("graph"):
    if filename.endswith(".txt"):
        with open(path.join("graph", filename), "r", encoding="utf-8") as file:
            name = file.readline().split(":")[-1].strip()
            b = file.readline().split()[-1]
            c = int(file.readline().split()[-1])
            d = int(file.readline().split()[-1])
            e = int(file.readline().split()[-1])
            f = int(file.readline().split()[-1])
            g = int(file.readline().split()[-1])
            h = int(file.readline().split()[-1])
            i = int(file.readline().split()[-1])
            j = float(file.readline().split()[-1])
            k = float(file.readline().split()[-1])
            l = int(file.readline().split()[-1])
            m = int(file.readline().split()[-1])
            n = int(file.readline().split()[-1])
            result[filename] = f"{name}\t{b}\t{c}\t{d}\t{e}\t{f}\t{g}\t{h}\t{i}\t{j}\t{k}\t{l}\t{m}\t{n}"


su = {}
with open("schedulability_results.csv", mode ='r', encoding="utf-8") as file:
  lines = file.readlines()
  for line in lines[1:]:
      line = line.strip()
      line = line.split(".dot    ")
      su[line[0]] = line[1]



with open("result.txt", "w", encoding="utf-8") as file:
    for filename in result:
        key = filename[:-4]
        if key in su:
            s = su[key]
        else:
            s = ""
        print(s)
        file.writelines(result[filename] + f"\t{s}\n")
