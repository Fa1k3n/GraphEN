from node import *
import sys
import math
import time

class GridError(Exception):
     def __init__(self, value):
         self.error = value

     def __str__(self):
         return repr(self.error)

class AlgObj(object):

    def __init__(self, graph):
        self._graph = graph
        self._came_from = {}
        self.closedset = []
        self.openset = []

    def shortest_path(self, start, goal): pass

    def visited(self):
        return self.closedset

    def fringe(self):
        return self.openset

    def effort(self, n): pass

    def reconstruct_path(self, start, goal):
        curr = goal
        shortest_path = []

        while curr != start:
            shortest_path.append(self._graph.cell_coord(curr))
            curr = self._came_from[curr]

        shortest_path.append(self._graph.cell_coord(start))
        return list(reversed(shortest_path))


class Djikstra(AlgObj):
    def __init__(self, graph):
        super(Djikstra, self).__init__(graph)
        self._tentative_weight = {}
        self.g_score = {}
        self.dist = lambda x,y : 0

    def shortest_path(self, start, goal):
        t1 = time.clock()
        r = self._shortest_path(start, goal)
        dt = time.clock() - t1
        print "Delta t: ", dt

    def _shortest_path(self, start, goal):
        self.openset.append(start)
        f_score = {}
        self.g_score[start] = 0
        f_score[start] = self.g_score[start] + self.dist(start, goal)

        while len(self.openset) > 0:
            # Find lowest f_score value, this can use a
            # sort of the f_score dict instead
            next_node = self.openset[0]
            for node in self.openset:
                if f_score[node] < f_score[next_node]:
                    next_node = node

            current = next_node
            self.openset.pop(self.openset.index(current))

            if current == goal:
                # Found path
                self.path = self.reconstruct_path(start, goal)
                return True

            self.closedset.append(current)

            for edge in current.edges():
                if edge.end_node in self.closedset:
                    continue
                tentative_g_score = self.g_score[current] + edge.cost

                if edge.end_node not in self.openset or tentative_g_score < self.g_score[edge.end_node]:
                    edge.end_node._parent_cell = current
                    self._came_from[edge.end_node] = current
                    self.g_score[edge.end_node] = tentative_g_score
                    f_score[edge.end_node] = self.g_score[edge.end_node] + self.dist(edge.end_node, goal)
                    if edge.end_node not in self.openset:
                        self.openset.append(edge.end_node)
        return False

    def effort(self, node):
        return self._g_score[node]

# AStar is a Djikstra with a distance function
class AStar(Djikstra):
    def __init__(self, graph, dist):
        super(AStar, self).__init__(graph)
        self.dist = self.cached_dist
        #self.dist = self._graph.dist
        self.dist_cache = {}

    """
    A very simple distance caching mechanism so that each node only need to
    do an expencive sqrt calculation onece

    Early measurements:
        0.0561 - vert, not cached
        0.0787 - hori, not cached
        0.7050 - diag, not cached

        0.0606 - vert, cached
        0.0745 - hori, cached
        0.4604 - diag, cached
    """
    def cached_dist(self, start, end):
        if start not in self.dist_cache:
            self.dist_cache[start] = self._graph.dist(start, end)
        return self.dist_cache[start]


class Grid():
    NEIGHBOUR_OFFSETS = [
        ((-1, -1), math.sqrt(2)), (( 0, -1), 1), ((+1, -1), math.sqrt(2)),
        ((-1,  0), 1),                ((+1,  0), 1),
        ((-1, +1), math.sqrt(2)), (( 0, +1), 1), ((+1, +1), math.sqrt(2))
        ]

    def __init__(self, x = None, y = None):
        self.cells = None
        self._visited_set = []
        self.size = (x, y)
        if x != None and y != None:
            for i in range(y):
                for j in range(x):
                    self.add_cell(j, i, Node())

    def get_cell(self, x, y):
        if self.cells == None:
            return None
        try:
            if self.cells[y][x] == None:
                raise GridError("Cell does not exists")
        except IndexError:
            raise GridError("Trying to get cell outside Grid")
        else:
            return self.cells[y][x]

    def _check_and_add_neighbour(self, c, x, y, cost):
        if x < 0 or y < 0:
            return
        try:
            n = self.get_cell(x, y)
        except Exception:
            pass
        else:
            c.add_neighbour(n, cost)
            n.add_neighbour(c, cost)

    def _check_and_remove_neighbour(self, c, x, y):
        try:
            n = self.get_cell(x, y)
            c.remove_neighbour(n)
            n.remove_neighbour(c)
        except Exception:
            pass

    def add_cell(self, x, y, c, cost=1):
        # Check if the lists has been created, if not create it
        if self.cells == None:
            self.cells = [[None]]

        # Check if the coordinates are outside the current dimension of the 
        # list, if so extend it
        if len(self.cells) <= y:
            self.cells.extend([[None]]*(y - len(self.cells) + 1))

        if len(self.cells[y]) <= x:
            self.cells[y].extend([None]*(x - len(self.cells[y]) + 1))

        # Add the cell
        self.cells[y][x] = c

        [self._check_and_add_neighbour(c, x + offset_x, y + offset_y, cost*cost_scale) for (offset_x, offset_y), cost_scale in Grid.NEIGHBOUR_OFFSETS]


    def remove_cell(self, x, y):
        try:
            c = self.cells[y][x]
        except Exception:
            raise GridError("Cell does not exists")
        [self._check_and_remove_neighbour(c, x + offset_x, y + offset_y) for (offset_x, offset_y), cost_scale in Grid.NEIGHBOUR_OFFSETS]
        self.cells[y][x] = None

        
    def cell_neighbours(self, c):
        ret_list = []
        for n in c.neighbours():
            for i in range(len(self.cells)):
                try:
                    pos = self.cells[i].index(n)
                    ret_list.append((pos, i))
                except ValueError:
                    pass
        return ret_list

    def cell_coord(self, c):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j] == c:
                    return (j, i)
        raise GridError("Cell not found")

    def dist(self, start, end):
        start_x, start_y = self.cell_coord(start)
        end_x, end_y = self.cell_coord(end)
        return math.sqrt((end_x -start_x)**2 + (end_y - start_y)**2)




