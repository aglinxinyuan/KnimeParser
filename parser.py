#https://docs.google.com/spreadsheets/d/17USUQ79PuanWOxXyN1eUHAXvrtet8GyQ/edit#gid=827508914
from zipfile import ZipFile
from xml.etree import ElementTree
from graphviz import Digraph
from random import randint
from collections import Counter

graph = Digraph()

filename = "examples/02.knwf"
metanodes = dict()
nodes = 0
edges = []

def parse(zf, filename):
    global nodes
    meta_inputs = []
    meta_outputs = []
    with zf.open(filename) as file:
        root = ElementTree.parse(file).getroot()
        for child in root:
            key = child.attrib["key"]
            if key == "nodes":
                for node in child:
                    node_id = node.attrib["key"].split("_")[1]
                    is_meta = False
                    for entry in reversed(node):
                        if entry.attrib["key"] == "node_is_meta" and entry.attrib["value"] == "true":
                            is_meta = True
                        elif entry.attrib["key"] == "node_settings_file":
                            metafile = entry.attrib["value"].split("/")[0]
                            if is_meta:
                                meta_source, meta_dest = parse(zf, filename[:-14] + metafile + "/workflow.knime")
                                if meta_source and meta_dest:
                                    metanodes[node_id] = [meta_source, meta_dest]
                            else:
                                name = metafile
                                graph.node(name=node_id, label=name[:name.rfind(" ")])
                                nodes += 1
            if key == "connections":
                for connection in child:
                    for entry in connection:
                        if entry.attrib["key"] == "sourceID":
                            source = entry.attrib["value"]
                        if entry.attrib["key"] == "destID":
                            dest = entry.attrib["value"]
                    if source == "-1":
                        meta_inputs.append(dest)
                    elif dest == "-1":
                        meta_outputs.append(source)
                    else:
                        edges.append([source, dest])
    return meta_inputs, meta_outputs


with ZipFile(filename) as zf:
    for filename in zf.namelist():
        if filename.count("/") == 1 and filename.endswith("workflow.knime"):
            parse(zf, filename)
while metanodes.keys() & set(sum(edges, [])):
    for i, (source, dest) in enumerate(edges):
        if source in metanodes:
            for meta_input in metanodes[source][1]:
                edges[i] = [meta_input, dest]
        elif dest in metanodes:
            for meta_output in metanodes[dest][0]:
                edges[i] = [source, meta_output]

inputs = Counter()
outputs = Counter()

for source, dest in edges:
    graph.edge(source, dest)
    inputs[source] += 1
    outputs[dest] += 1

mult_op = {node for node in inputs | outputs if inputs[node] > 1 or outputs[node] > 1}

graph.attr(rankdir='LR')
graph.render(filename="graph/" + str(randint(1000000, 9999999)), view=True)

print("Operators:", nodes)
print("Edges:", len(edges))
print("Operators with multIO:", len(mult_op))
