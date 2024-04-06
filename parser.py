#https://docs.google.com/spreadsheets/d/17USUQ79PuanWOxXyN1eUHAXvrtet8GyQ/edit#gid=827508914
from zipfile import ZipFile
from xml.etree import ElementTree
from collections import Counter
from graphviz import Digraph

graph = Digraph()

filename = "examples/02.knwf"
metanodes = 0
multop = 0
nodes = 0
connections = 0

def parse(zf, filename):
    global multop
    global nodes
    global connections
    with zf.open(filename) as file:
        root = ElementTree.parse(file).getroot()
        outputs = Counter()
        inputs = Counter()
        for child in root:
            key = child.attrib["key"]
            if key == "nodes":
                for node in child:
                    for entry in node:
                        if entry.attrib["key"] == "node_settings_file":
                            metafile = entry.attrib["value"]
                            name = metafile.split("/")[0]
                            name = name[:name.rfind(" ")]
                            graph.node(name=node.attrib["key"].split("_")[1], label=name)
                        if entry.attrib["key"] == "node_is_meta":
                            if entry.attrib["value"]=="true":
                                print("meta", metafile)
                    nodes += 1
            if key == "connections":
                for connection in child:
                    connections += 1
                    for entry in connection:
                        if entry.attrib["key"] == "sourceID":
                            source = entry.attrib["value"]
                            outputs[source] += 1
                        if entry.attrib["key"] == "destID":
                            dest = entry.attrib["value"]
                            inputs[dest] += 1
                    graph.edge(source, dest)

        muliopSet = set()
        for node in inputs:
            if inputs[node] > 1:
                muliopSet.add(node)
        for node in outputs:
            if inputs[node] > 1:
                muliopSet.add(node)
        multop += len(muliopSet)

with ZipFile(filename) as zf:
    for filename in zf.namelist():
        if filename.endswith("workflow.knime") and filename.count("/") == 1:
            print(filename)
            parse(zf, filename)

graph.attr(rankdir='LR')
graph.render(view=True)

nodes = nodes - metanodes + 1
#connections = connections - (metanodes - 1) * 2
print("Metanodes:", metanodes)
print("Operators:", nodes)
print("Edges:", connections)
print("Operators with multIO:", multop)
