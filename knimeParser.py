import sys
from zipfile import ZipFile
from xml.etree import ElementTree
from graphviz import Digraph
from random import randint
from collections import Counter


class Parser():
    metanodes = dict()
    nodes = 0
    edges = []
    graph = Digraph()

    def __init__(self, filename):
        with ZipFile(filename) as zf:
            for filename in zf.namelist():
                if filename.count("/") == 1 and filename.endswith("workflow.knime"):
                    self.parse(zf, filename)
        while self.metanodes.keys() & set(sum(self.edges, [])):
            for i, (source, dest) in enumerate(self.edges):
                if source in self.metanodes:
                    for meta_input in self.metanodes[source][1]:
                        self.edges[i] = [meta_input, dest]
                elif dest in self.metanodes:
                    for meta_output in self.metanodes[dest][0]:
                        self.edges[i] = [source, meta_output]

        inputs = Counter()
        outputs = Counter()

        for source, dest in self.edges:
            self.graph.edge(source, dest)
            inputs[source] += 1
            outputs[dest] += 1

        mult_op = {node for node in inputs | outputs if inputs[node] > 1 or outputs[node] > 1}

        self.graph.attr(rankdir='LR')
        #self.graph.render(filename="graph/" + str(randint(1000000, 9999999)), view=True)

        #print(self.graph.source)
        print("Operators:", self.nodes)
        print("Edges:", len(self.edges))
        print("Operators with multIO:", len(mult_op))

    def parse(self, zf, filename):
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
                                    meta_source, meta_dest = self.parse(zf,
                                                                        filename[:-14] + metafile + "/workflow.knime")
                                    if meta_source and meta_dest:
                                        self.metanodes[node_id] = [meta_source, meta_dest]
                                else:
                                    name = metafile
                                    self.graph.node(name=node_id, label=name[:name.rfind(" ")])
                                    self.nodes += 1
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
                            self.edges.append([source, dest])
        return meta_inputs, meta_outputs


if __name__ == "__main__":
    Parser("examples/02.knwf")
