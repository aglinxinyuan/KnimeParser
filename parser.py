#https://docs.google.com/spreadsheets/d/17USUQ79PuanWOxXyN1eUHAXvrtet8GyQ/edit#gid=827508914
from zipfile import ZipFile
from xml.etree import ElementTree

filename = "14"
nodes = 0
connections = 0
metanodes = 0
with ZipFile(filename+".knwf") as zf:
    for filename in zf.namelist():
        if filename.endswith("workflow.knime"):
            metanodes += 1
            with zf.open(filename) as file:
                tree = ElementTree.parse(file)
                root = tree.getroot()
                for child in root:
                    key = child.attrib["key"]
                    if key == "nodes":
                        for node in child:
                            nodes += 1
                    if key == "connections":
                        for connection in child:
                            connections +=1
nodes = nodes - metanodes + 1
#connections = connections - (metanodes - 1) * 2
print("Metanodes:", metanodes)
print("Operators:", nodes)
print("Edges:", connections)
