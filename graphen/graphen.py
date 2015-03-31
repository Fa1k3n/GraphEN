import warnings
import logging
import collections


class GraphError(Exception):
     def __init__(self, value):
         self.error = value

     def __str__(self):
         return repr(self.error)

class Vertex(object):
    def __init__(self, label=""):
        if not isinstance(label, str):
            warnings.warn("Trying to add a non string label")
        self.label = label


class Edge(object):
    def __init__(self, label="", cost=1, directed=False):
        self.cost = cost
        self.label = label
        self.directed = directed

class Graph(object):
    _GraphItem = collections.namedtuple('_GraphItem', ['vertex', 'edge'])
    def __init__(self, name=""):
        self.name = name
        self.label_generator = {
            "undirected edge": lambda v1, v2: str(v1.label) + "<->" + str(v2.label),
            "directed edge": lambda v1, v2: str(v1.label) + "-->" + str(v2.label),
            "new vertex": lambda self: str(self._vertex_count)
        }
        self._vertex_count = 0
        self._edge_count = 0
        self._vertices = {}

    def add_vertex(self, *vert_args):
        vert_list = list(vert_args)
        new_vert = None

        if len(vert_list) == 0:
            new_vert = Vertex(self.label_generator["new vertex"](self))
            vert_list.append(new_vert)

        for vert in vert_list:
            if isinstance(vert, str):
                try:
                    vert = self.vertex(vert)
                except:
                    vert = Vertex(vert)

            if vert not in self._vertices:
                self._vertex_count += 1
                self._vertices[vert] = []
            else:
                raise GraphError("Trying to add already existing vertex: " + str(vert))

        return new_vert

    def del_vertex(self, *vert_args):
        vert_list = list(vert_args)
        for vert in vert_list:
            if isinstance(vert, str):
                vert = self.vertex(vert)
            try:
                self._vertices.pop(vert)
            except:
                raise GraphError("Trying to remove none existing node")
            else:
                pass
                ## Iterate over all nodes and their edges


                for v in self._vertices:
                    items_to_pop = []
                    for idx, graph_item in enumerate(self.neighbours(v)):
                        if graph_item.vertex == vert:
                            items_to_pop.append(idx)
                    self._vertices[v] = [gi for i,gi in enumerate(self.neighbours(v)) if i not in items_to_pop]


    def add_edge(self, start_vert, end_vert, edge=None, directed=False):
        self._edge_count += 1
        try:
            start_vert = self.vertex(start_vert)
        except GraphError:
            logging.info(str(start_vert) + " created")
            start_vert = Vertex(start_vert)
            self.add_vertex(start_vert)
        try:
            end_vert = self.vertex(end_vert)
        except GraphError:
            logging.info(str(end_vert) + " created")
            end_vert = Vertex(end_vert)
            self.add_vertex(end_vert)

        if edge == None: # or edge.label == "":
            type = "undirected edge"
            if directed:
                type = "directed edge"
            lbl = self.label_generator[type](start_vert, end_vert)
            edge = Edge(lbl, directed=directed)

        if end_vert not in list(self.neighbours(start_vert)):
            self._vertices[start_vert].append(Graph._GraphItem(end_vert, edge))
        if not directed and start_vert not in self.neighbours(end_vert):
            self._vertices[end_vert].append(Graph._GraphItem(start_vert, edge))

    def edge(self, label, vert_2=None):
        if isinstance(label, str) and vert_2 == None:
            return self._get_labeled_edge(label)
        else:
            vert_1 = self.vertex(label)
            vert_2 = self.vertex(vert_2)
            for graph_item in self._vertices[vert_1]:
                if graph_item.vertex == vert_2:
                    return graph_item.edge
        raise GraphError("Edge not found")

    def edges(self, vert):
        for graph_item in self._vertices[vert]:
            yield graph_item.edge

    def vertices(self):
        for vert in self._vertices:
            yield vert

    def neighbours(self, vert):
        for graph_item in self._vertices[vert]:
            yield graph_item

    def _get_labeled_edge(self, label):
        for vert_key in self._vertices:
            for graph_item in self._vertices[vert_key]:
                if graph_item.edge.label == label:
                    return graph_item.edge
        raise GraphError("Label not found: " + str(label))

    def vertex(self, vert):
        if isinstance(vert, str):
            return self._get_labeled_vertex(vert)
        elif isinstance(vert, Vertex):
            if vert in self._vertices.keys():
                return vert
        raise GraphError("Vertex not found")

    def _get_labeled_vertex(self, label):
        for vert in self._vertices:
            if vert.label == label:
                return vert
        raise GraphError("Label not found:" + str(label))

    def __contains__(self, item):
        if isinstance(item, str):
            try:
                self._get_labeled_vertex(item)
            except:
                pass
            else:
                return True
        elif isinstance(item, Vertex):
            return item in self._vertices
        elif isinstance(item, tuple):
            (start, end) = item
            try:
                e = self.edge(start, end)
                if not e.directed:
                    self.edge(end, start)
            except:
                return False
            else:
                return True

        return False
