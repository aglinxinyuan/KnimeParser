from collections import Counter
from xml.etree import ElementTree
from zipfile import ZipFile
from graphviz import Digraph
import networkx as nx


class Parser:
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
                                    if meta_source or meta_dest:
                                        self.metanodes[node_id] = [meta_source, meta_dest]
                                else:
                                    name = metafile[:metafile.rfind(" ")]
                                    if name in self.blocking_op:
                                        self.blocking += 1
                                    self.graph.node(name=node_id, label=name)
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
                            self.edges.append((source, dest))
        return meta_inputs, meta_outputs

    def __init__(self, filename, view=False):
        with open("blocking.txt") as file:
            self.blocking_op = set([line.strip() for line in file.readlines()])
        self.metanodes = dict()
        self.nodes = 0
        self.edges = []
        self.graph = Digraph()
        self.blocking = 0
        with ZipFile(filename) as zf:
            for name in zf.namelist():
                if name.count("/") == 1 and name.endswith("workflow.knime"):
                    self.workflow_name = name[:name.rfind("/")]
                    self.parse(zf, name)

        self.counter = 0

        print(self.metanodes.keys())
        while self.metanodes.keys() & set(sum(self.edges, [])):
            self.counter += 1
            for i, (source, dest) in enumerate(self.edges):
                if source in self.metanodes:
                    for meta_input in self.metanodes[source][1]:
                        self.edges[i] = [meta_input, dest]
                elif dest in self.metanodes:
                    for meta_output in self.metanodes[dest][0]:
                        self.edges[i] = [source, meta_output]
            if self.counter > 100000:
                return

        inputs = Counter()
        outputs = Counter()

        for source, dest in self.edges:
            self.graph.edge(source, dest)
            inputs[source] += 1
            outputs[dest] += 1
        mult_out = {node for node in inputs if inputs[node] > 1}
        mult_in = {node for node in outputs if outputs[node] > 1}

        output = "graph/" + filename.split("/")[-1].split(".")[0]
        self.graph.attr(rankdir='LR')
        self.graph.render(filename=output + ".dot", cleanup=True, view=view)
        content = (f"Workflow Name: {self.workflow_name}\n"
                   f"Operators: {self.nodes}\n"
                   f"Edges: {len(self.edges)}\n"
                   f"Blocking edges: {self.blocking}\n"
                   f"Operators with multiple input ports: {len(mult_in)}\n"
                   f"Operators with multiple output ports: {len(mult_out)}\n"
                   f"Maximum # of input ports in an operator: {2}\n"
                   f"Maximum # of output ports in an operator: {2}\n"
                   f"# edges in an undirected cycle: {0}\n"
                   f"Tree: Yes")
        print(content)
        with open(output + ".txt", "w") as file:
            file.write(content)


if __name__ == "__main__":
    Parser("workflows/KNIME_textanalysis_group_project_PA_final.knwf", True)
list_of_tuples = [(1, 2), (3, 4)]
flattened_list = [element for tup in list_of_tuples for element in tup]
print(flattened_list)