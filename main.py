from zipfile import ZipFile
import xml.etree.ElementTree as ET

nodes = 0
connections = 0
metanodes = 0
with ZipFile('2.knwf') as zf:
    for filename in zf.namelist():
        if filename.endswith("workflow.knime"):
            metanodes += 1
            with zf.open(filename) as file:
                tree = ET.parse(file)
                root = tree.getroot()
                for child in root:
                    key = child.attrib["key"]
                    if key == "nodes":
                        for node in child:
                            nodes += 1
                    if key == "connections":
                        for connection in child:
                            connections +=1
nodes = nodes-metanodes+1
print("Nodes:", nodes)
print("Connections:", connections)
print("Metanodes:", metanodes)
