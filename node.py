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
        if isinstance(label, str):
            self.label = label
        else:
            warnings.warn("Trying to add a non string label")

class Edge(object):
    def __init__(self, label="", cost=1):
        self.cost = cost
        self.label = label

class Graph(object):
    _GraphItem = collections.namedtuple('_GraphItem', ['vertex', 'edge'])
    def __init__(self, name=""):
        self.name = name
        self._vertex_count = 0
        self._edge_count = 0
        self._vertices = {}

    def add_vertex(self, *vert_args):
        vert_list = list(vert_args)
        new_vert = None
        if len(vert_list) == 0:
            new_vert = Vertex()
            vert_list.append(new_vert)

        for vert in vert_list:
            if vert not in self._vertices:
                self._vertex_count += 1
                self._vertices[vert] = []
            else:
                raise GraphError("Trying to add already existing node")

        return new_vert

    def del_vertex(self, vert):
        if isinstance(vert, str):
            vert = self.vertex(vert)
        try:
            self._vertices.pop(vert)
        except:
            raise GraphError("Trying to remove none existing node")
        else:
            self._vertex_count -= 1

    """
    should take start_ and end_ vertices both as references and as named nodes
    if one of the vertices does not exists it should create it
    """
    def add_edge(self, start_vert, end_vert, edge=None, directed=False):
        self._edge_count += 1
        try:
            start_vert = self.vertex(start_vert)
        except GraphError:
            logging.info("str(start_vert)" + " created")
            start_vert = Vertex(start_vert)
            self.add_vertex(start_vert)
        try:
            end_vert = self.vertex(end_vert)
        except GraphError:
            logging.info(str(end_vert) + " created")
            end_vert = Vertex(end_vert)
            self.add_vertex(end_vert)

        if edge == None:
            edge = Edge()

        self._vertices[start_vert].append(Graph._GraphItem(end_vert, edge))
        if not directed:
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
        return GraphError("Vertex not found")

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
                self.edge(start, end)
                self.edge(end, start)
            except:
                return False
            else:
                return True

        return False
