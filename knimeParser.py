from collections import Counter, defaultdict
from xml.etree import ElementTree
from zipfile import ZipFile
from graphviz import Digraph
import networkx as nx


class Parser:
    def parse(self, zf, filename):
        meta_inputs = []
        meta_outputs = []
        node_hash = str(hash(filename)) + "_"
        with zf.open(filename) as file:
            root = ElementTree.parse(file).getroot()
            for child in root:
                key = child.attrib["key"]
                if key == "nodes":
                    for node in child:
                        node_id = node_hash + node.attrib["key"].split("_")[1]
                        is_meta = False
                        for entry in reversed(node):
                            if entry.attrib["key"] == "node_is_meta" and entry.attrib["value"] == "true":
                                is_meta = True
                            elif entry.attrib["key"] == "node_settings_file":
                                metafile = entry.attrib["value"].split("/")[0]
                                basepath = filename[:-14] + metafile
                                if is_meta:
                                    meta_source, meta_dest = self.parse(zf, basepath + "/workflow.knime")
                                    if meta_source or meta_dest:
                                        self.metanodes[node_id] = [meta_source, meta_dest]
                                else:
                                    name = metafile[:metafile.rfind(" ")]
                                    print(name)
                                    ports = {}
                                    base_split_len = len(basepath.split("/"))
                                    for f1 in zf.namelist():
                                        if f1.startswith(basepath + "/port_"):
                                            port = f1.split("/")[base_split_len].split("_")[-1]
                                            if f1.endswith("/data.xml"):
                                                ports[port] = ["data: ", 0, False]
                                            if f1.endswith("/object/portobject.zip"):
                                                ports[port] = ["object: ", 0, False]
                                    for f1 in zf.namelist():
                                        if f1.startswith(basepath + "/port_"):
                                            port = f1.split("/")[base_split_len].split("_")[-1]
                                            ports[port][1] += zf.getinfo(f1).file_size
                                    self.nodes[node_id] = (name, ports)
                if key == "connections":
                    for connection in child:
                        for entry in connection:
                            if entry.attrib["key"] == "sourceID":
                                source = node_hash + entry.attrib["value"]
                            if entry.attrib["key"] == "destID":
                                dest = node_hash + entry.attrib["value"]
                            if entry.attrib["key"] == "sourcePort":
                                source_port = entry.attrib["value"]
                            if entry.attrib["key"] == "destPort":
                                dest_port = entry.attrib["value"]
                        source_tuple = (source, source_port)
                        dest_tuple = (dest, dest_port)
                        if source == node_hash + "-1":
                            meta_inputs.append(dest_tuple)
                        elif dest == node_hash + "-1":
                            meta_outputs.append(source_tuple)
                        else:
                            self.edges.append((source_tuple, dest_tuple))
        return meta_inputs, meta_outputs

    def __init__(self, filename, view=False):
        #(filename)
        with open("blocking.txt") as file:
            self.blocking_op = set([line.strip() for line in file.readlines()])
        self.metanodes = dict()
        self.edges = []
        self.blocking = 0
        self.nodes = {}
        with ZipFile(filename) as zf:
            for name in zf.namelist():
                if name.count("/") == 1 and name.endswith("workflow.knime"):
                    workflow_name = name[:name.rfind("/")]
                    self.parse(zf, name)

        self.counter = 0
        while self.metanodes.keys() & set([element[0] for tup in self.edges for element in tup]):
            self.counter += 1
            for i, (source, dest) in enumerate(self.edges):
                if source[0] in self.metanodes:
                    for meta_input in self.metanodes[source[0]][1]:
                        self.edges[i] = (meta_input, dest)
                elif dest[0] in self.metanodes:
                    for meta_output in self.metanodes[dest[0]][0]:
                        self.edges[i] = (source, meta_output)
            if self.counter > 100000:
                return

        in_degree = Counter()
        out_degree = Counter()
        in_port = defaultdict(list)
        out_port = defaultdict(list)

        unique_edges = set()
        for source, dest in set(self.edges):
            unique_edges.add((source, dest))
            out_degree[source[0]] += 1
            in_degree[dest[0]] += 1
            in_port[dest[0]].append(dest[1])
            out_port[source[0]].append(source[1])
        nx_graph = nx.Graph()

        mult_in = [len(in_port[node]) for node in in_port if len(in_port[node]) > 1]
        mult_out = [len(out_port[node]) for node in out_port if len(out_port[node]) > 1]

        max_in = max(mult_in) if mult_in else 1
        max_out = max(mult_out) if mult_out else 1

        graph = Digraph()
        op_list = set([element[0] for tup in self.edges for element in tup])
        for id in op_list:
            name = self.nodes[id][0]
            output = self.nodes[id][1]

            for key, value in output.items():
                if name in self.blocking_op or value[0] == "object: ":
                    self.blocking += 1
                    self.nodes[id][1][key][2] = True
            graph.node(name=id, label=name)

        for source, dest in unique_edges:
            nx_graph.add_edge(source[0], dest[0])
            data = self.nodes[source[0]][1][source[1]]
            graph.edge(source[0], dest[0], label=data[0] + str(data[1])+"; is_blocking: "+str(data[2]))

        output = "graph/" + filename.split("/")[-1].split(".")[0]
        graph.attr(rankdir='LR')
        graph.render(filename=output + ".dot", view=view)
        try:
            cycles = nx.find_cycle(nx_graph)
        except nx.NetworkXNoCycle:
            cycles = []
        content = (f"Workflow Name: {workflow_name}\n"
                   f"Tree: {len(cycles) == 0}\n"
                   f"Operators: {len(op_list)}\n"
                   f"Edges: {len(unique_edges)}\n"
                   f"Blocking edges: {self.blocking}\n"
                   f"Operators with multiple input ports: {len(mult_in)}\n"
                   f"Operators with multiple output ports: {len(mult_out)}\n"
                   f"Maximum # of input ports in an operator: {max_in}\n"
                   f"Maximum # of output ports in an operator: {max_out}\n"
                   f"AVG indegree of operators: {sum(in_degree.values()) / len(in_degree.values())}\n"
                   f"AVG outdegree of operators: {sum(out_degree.values()) / len(in_degree.values())}\n"
                   f"MAX indegree of an operator: {max(in_degree.values())}\n"
                   f"MAX outdegree of an operator: {max(out_degree.values())}\n"
                   f"# edges in an undirected cycle: {len(cycles)}\n"
                   )
        with open(output + ".txt", "w", encoding="utf-8") as file:
            file.write(content)
        print(content)


if __name__ == "__main__":
    #Parser("workflows/1_Telve.knwf", True)

    Parser("workflows/00 Keras Simple Linear Regression.knwf", True)
    #Parser("KNIME_textanalysis_group_project_PA_final.knwf", True)
    #Parser("workflows/(test) credit score model.knwf", True)
    #Parser("workflows/フロー変数の接続によるノード実行順序の制御.knwf", False)
