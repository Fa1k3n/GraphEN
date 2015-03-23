class NodeError(Exception):
     def __init__(self, value):
         self.error = value

     def __str__(self):
         return repr(self.error)

class Node(object):
    def __init__(self):
        self.edge_list = []
        self._tentative_weight = 0

    def add_neighbour(self, end_node, cost=1, bi_directional=False):
        self.edge_list.append(Edge(self, end_node, cost, bi_directional))

    def neighbours(self):
        for edge in self.edge_list:
            yield edge.end_node

    def edges(self):
        return self.edge_list

    def change_edge_costs(self, cost):
        for edge in self.edge_list:
            edge.cost = cost

    def remove_neighbour(self, node):
        (end_node, idx) = (None, None)
        for idx, edge in enumerate(self.edge_list):
            if edge.end_node == node:
                (end_node, idx) = (edge.end_node, idx)
                break
        if end_node is None:
            raise NodeError("Trying to remove a non existing neigbour")
        self.edge_list.pop(idx)

class EdgeError(Exception):
     def __init__(self, value):
         self.error = value

     def __str__(self):
         return repr(self.error)

class Edge(object):
    def __init__(self, start_node, end_node, cost, bi_directional=False):
        self._cost = cost
        self.start_node = start_node
        self.end_node = end_node
        self.bi_directional = bi_directional

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, new_cost):
        if new_cost < 0:
            raise EdgeError("Only positive edge costs are supported")
        self._cost = new_cost
