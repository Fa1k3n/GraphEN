class NodeError(Exception):
     def __init__(self, value):
         self.error = value

     def __str__(self):
         return repr(self.error)

class Node(object):
    def __init__(self, cost = 1):
        self.cost = cost
        self.neighbour_list = []
        self._tentative_weight = 0
        self._parent_cell = None

    def get_cost(self):
        return self.cost

    def set_cost(self, cost):
        self.cost = cost

    def add_neighbour(self, node):
        self.neighbour_list.append(node)

    def get_neighbours(self):
        return self.neighbour_list

    def neighbours(self):
        for i in range(len(self.neighbour_list)):
            yield self.neighbour_list[i]

    def remove_neighbour(self, node):
        if node not in self.neighbour_list:
            raise NodeError("Trying to remove a non existing neigbour")
        self.neighbour_list.pop(self.neighbour_list.index(node))


class EdgeError(Exception):
     def __init__(self, value):
         self.error = value

     def __str__(self):
         return repr(self.error)

class Edge(object):
    def __init__(self, cost, start_node, end_node, bi_directional=False):
        self._cost = cost

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, new_cost):
        if new_cost < 0:
            raise EdgeError("Only positive edge costs are supported")
        self._cost = new_cost
