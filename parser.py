#https://docs.google.com/spreadsheets/d/17USUQ79PuanWOxXyN1eUHAXvrtet8GyQ/edit#gid=827508914
from zipfile import ZipFile
from xml.etree import ElementTree
from collections import Counter

filename = "examples/04.knwf"
nodes = 0
connections = 0
metanodes = 0
multop = 0
with ZipFile(filename) as zf:
    for filename in zf.namelist():
        if filename.endswith("workflow.knime"):
            metanodes += 1
            with zf.open(filename) as file:
                root = ElementTree.parse(file).getroot()
                outputs = Counter()
                inputs = Counter()
                for child in root:
                    key = child.attrib["key"]
                    if key == "nodes":
                        for node in child:
                            nodes += 1
                    if key == "connections":
                        for connection in child:
                            connections += 1
                            for entry in connection:
                                if entry.attrib["key"] == "sourceID":
                                    outputs[(entry.attrib["value"])] += 1
                                if entry.attrib["key"] == "destID":
                                    inputs[(entry.attrib["value"])] += 1
                muliopSet = set()
                for node in inputs:
                    if inputs[node] > 1:
                        muliopSet.add(node)
                for node in outputs:
                    if inputs[node] > 1:
                        muliopSet.add(node)
                multop += len(muliopSet)

nodes = nodes - metanodes + 1
#connections = connections - (metanodes - 1) * 2
print("Metanodes:", metanodes)
print("Operators:", nodes)
print("Edges:", connections)
print("Operators with multIO:", multop)
