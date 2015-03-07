class CellError(Exception):
     def __init__(self, value):
         self.error = value

     def __str__(self):
         return repr(self.error)

class Cell:
    def __init__(self, cost = 1):
        self.cost = cost
        self.neighbours = []
        self._tentative_weight = 10000
        self._parent_cell = None
        self._status = "NOT VISITED"

    def get_cost(self):
        return self.cost

    def set_cost(self, cost):
        self.cost = cost

    def add_neighbour(self, cell):
        self.neighbours.append(cell)

    def get_neighbours(self):
        return self.neighbours
    
    def remove_neighbour(self, cell):
        if cell not in self.neighbours:
            raise CellError("Trying to remove a non existing neigbour")
        self.neighbours.pop(self.neighbours.index(cell))
