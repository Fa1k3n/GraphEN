from node import *
import sys
import math

class GridError(Exception):
     def __init__(self, value):
         self.error = value

     def __str__(self):
         return repr(self.error)

class AlgObj(object):

    def __init__(self, graph):
        self.graph = graph

    def shortest_path(self, start, goal): pass

    def visited(self): pass

    def effort(self, n): pass

    def reconstruct_path(self, start, goal):
        curr = goal
        shortest_path = []

        while curr != start:
            shortest_path.append(self.graph.cell_coord(curr))
            curr = curr._parent_cell

        shortest_path.append(self.graph.cell_coord(start))
        return list(reversed(shortest_path))



class AStar(AlgObj):
    def __init__(self, graph):
        self.g_score = {}
        self.closedset = {}
        self.graph = graph

    def shortest_path(self, start, goal):
        current = start
        openset = [start]
        self.closedset = []
        self.g_score = {}
        f_score = {}
        heuristic_fun = self.dist

        self.g_score[start] = 0
        f_score[start] = self.g_score[start] + heuristic_fun(start, goal)

        while len(openset) > 0:
            # Find lowest f_score value, this can use a
            # sort of the f_score dict instead
            next_node = openset[0]
            for node in openset:
                if f_score[node] < f_score[next_node]:
                    next_node = node

            current = next_node
            openset.pop(openset.index(current))


            if current == goal:
                # Found path
                self.path = self.reconstruct_path(start, goal)
                return True

            self.closedset.append(current)

            for edge in current.edges():
                if edge.end_node in self.closedset:
                    continue
                tentative_g_score = self.g_score[current] + edge.cost

                if edge.end_node not in openset or tentative_g_score < self.g_score[edge.end_node]:
                    edge.end_node._parent_cell = current
                    self.g_score[edge.end_node] = tentative_g_score
                    f_score[edge.end_node] = self.g_score[edge.end_node] + heuristic_fun(edge.end_node, goal)
                    if edge.end_node not in openset:
                        openset.append(edge.end_node)
        return False

    def visited(self):
        return self.closedset

    def effort(self, node):
        return self.g_score[node]

    def dist(self, start, end):
        #return 0
        start_x, start_y = self.graph.cell_coord(start)
        end_x, end_y = self.graph.cell_coord(end)
        return math.sqrt((end_x -start_x)**2 + (end_y - start_y)**2)

class Djikstra(AlgObj):
     # Djikstras shortest path algorithm
    # Refactor this!

    def shortest_path(self, start, goal):
        self._prepare_cells()
        curr = start
        curr._tentative_weight = 0
        tentative_weight = 0
        pending_exploration = [(start, tentative_weight)]
        self._visited_set = []
        self._tentative_weight = {}
        self._tentative_weight[start] = 0

        while curr != goal:
            try:
                curr, tentative_weight = pending_exploration.pop(0)
            except IndexError:  # pending_exploration is empty, no path found
                raise GridError("No path found")

            for edge in curr.edges():
                if edge in self._visited_set:
                    next
                possible_cost = tentative_weight + edge.cost
                if edge.end_node._tentative_weight > possible_cost:
                    edge.end_node._tentative_weight = possible_cost
                    edge.end_node._parent_cell = curr
                    if edge not in pending_exploration:
                        pending_exploration.append((edge.end_node, possible_cost))
            pending_exploration = sorted(pending_exploration, key=lambda(x): x[1])
            self._visited_set.append(curr)

        self.path = self.reconstruct_path(start, goal)
        self._effort = goal._tentative_weight
        return True

    def _prepare_cells(self):
        for i in self.graph.cells:
            for j in i:
                if j != None:
                    j._tentative_weight = sys.maxint

    def visited(self):
        return self._visited_set

    def effort(self, node):
        return self._effort


class Grid():
    NEIGHBOUR_OFFSETS = [
            (-1, -1), ( 0, -1), (+1, -1),
            (-1,  0),           (+1,  0),
            (-1, +1), ( 0, +1), (+1, +1)
        ]

    def __init__(self, x = None, y = None):
        self.cells = None
        self._visited_set = []
        #self._check_and_add_neighbour = self._check_link_and_do_action(Cell.add_neighbour)
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

        [self._check_and_add_neighbour(c, x + offset_x, y + offset_y, cost) for offset_x, offset_y in Grid.NEIGHBOUR_OFFSETS]


    def remove_cell(self, x, y):
        try:
            c = self.cells[y][x]
        except Exception:
            raise GridError("Cell does not exists")
        [self._check_and_remove_neighbour(c, x + offset_x, y + offset_y) for offset_x, offset_y in Grid.NEIGHBOUR_OFFSETS]
        self.cells[y][x] = None

        
    def cell_neighbours(self, c):
        #neighbours = c.get_neighbours()
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





