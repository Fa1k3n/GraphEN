class NodeError(Exception):
     def __init__(self, value):
         self.error = value

     def __str__(self):
         return repr(self.error)

class Vertex(object):
    def __init__(self, label=""):
        pass

class EdgeError(Exception):
     def __init__(self, value):
         self.error = value

     def __str__(self):
         return repr(self.error)

class Edge(object):
    def __init__(self, cost, label=""):
        self._cost = cost



class GraphError(Exception):
     def __init__(self, value):
         self.error = value

     def __str__(self):
         return repr(self.error)

class Graph(object):
    def __init__(self, name=""):
        self.name = name
        self._vertex_count = 0
        self._vertices = {}

    def add_vertex(self, *vert):
        if vert not in self._vertices:
            self._vertex_count += 1
            self._vertices[vert] = []
        else:
            raise GraphError("Trying to add already existing node")

    def rem_vertex(self, vert):
        try:
            self._vertices.pop(vert)
        except:
            raise GraphError("Trying to remove none existing node")
        else:
            self._vertex_count -= 1

    """
    should take start_ and end_ vertices both as references and as named nodes
    """
    def add_edge(self, start_vert, end_vert, edge, directed=False):
        pass