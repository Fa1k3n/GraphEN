import math
import time
from Queue import PriorityQueue

from graphen.graphen import *

class Grid(Graph):

    @staticmethod
    def CellCoordLabel(x, y):
        return str(x) + "," + str(y)

    def __init__(self, x = None, y = None):
        super(Grid, self).__init__()

        self._visited_set = []
        self.size = (x, y)
        if x == None:
            x = 5
        if y == None:
            y = 5

        # Create the Grid
        for i in range(y):
            for j in range(x):
                self.add_vertex(Vertex(Grid.CellCoordLabel(j, i)))

        offs = [(+1, 0, 1), (0, +1, 1), (+1, +1, math.sqrt(2)), (-1, +1, math.sqrt(2))]

        for i in range(y):
            for j in range(x):
                center_vert = self.vertex(Grid.CellCoordLabel(j, i))
                for (off_x, off_y, cost) in offs:
                    (cx, cy) = (j+off_x, i+off_y)
                    if cx < 0 or cy < 0:
                        continue
                    if cx == x or cy == y:
                        continue
                    tmp_vert = self.vertex(Grid.CellCoordLabel(cx, cy))
                    self.add_edge(center_vert, tmp_vert, Edge(cost=cost))

    def add_cell(self, x, y):
        neigh_offs = [(-1, -1, math.sqrt(2)), (0, -1, 1), (+1, -1, math.sqrt(2)),
                      (0, -1, 1), (0, +1, 1),
                      (+1, -1, math.sqrt(2)), (+1, 0, 1), (+1, +1, math.sqrt(2))]
        vert = self.add_vertex(Vertex(Grid.CellCoordLabel(x, y)))
        for (off_x, off_y, cost) in neigh_offs:
            (cx, cy) = (x+off_x, y+off_y)
            try:
                tmp_vert = self.vertex(Grid.CellCoordLabel(cx, cy))
            except GraphError as e:
                pass
            else:
                self.add_edge(vert, tmp_vert, Edge(cost=cost))

    def del_cell(self, x, y=None):
        if y == None:
            (x, y) = x
        self.del_vertex(Grid.CellCoordLabel(x, y))

    def get_cell(self, x, y=None):
        if y == None:
            (x, y) = x
        return self.vertex(Grid.CellCoordLabel(x, y))

    def has_cell(self, x, y=None):
        if y == None:
            (x, y) = x
        try:
            self.get_cell(x, y)
        except GraphError:
            return False
        else:
            return True

    def cell_coord(self, cell):
        coord = cell.label.split(",")
        return (int(coord[0]), int(coord[1]))

    def dist(self, start, end):
        start_x, start_y = self.cell_coord(start)
        end_x, end_y = self.cell_coord(end)
        return math.sqrt((end_x -start_x)**2 + (end_y - start_y)**2)




