from cell import *

class GridError(Exception):
     def __init__(self, value):
         self.error = value

     def __str__(self):
         return repr(self.error)

class Grid():
    NEIGHBOUR_OFFSETS = [
            (-1, -1), ( 0, -1), (+1, -1),
            (-1,  0),           (+1,  0),
            (-1, +1), ( 0, +1), (+1, +1)
        ]

    def __init__(self, x = None, y = None):
        self.cells = None
        #self._check_and_add_neighbour = self._check_link_and_do_action(Cell.add_neighbour)
        if x != None and y != None:
            for i in range(y):
                for j in range(x):
                    self.add_cell(j, i, Cell())

    def get_cell(self, x, y):
        if self.cells == None:
            return None
        try:
            if self.cells[y][x] == None:
                raise GridError("Cell does not exists")
        except IndexError:
            raise GridError("Trying to get cell outside Grid")
        return self.cells[y][x]

    def _check_and_add_neighbour(self, c, x, y):
        if x < 0 or y < 0:
            return
        try:
            n = self.get_cell(x, y)
            c.add_neighbour(n)
            n.add_neighbour(c)
        except Exception:
            pass

    def _check_and_remove_neighbour(self, c, x, y):
        try:
            n = self.get_cell(x, y)
            c.remove_neighbour(n)
            n.remove_neighbour(c)
        except Exception:
            pass

    def add_cell(self, x, y, c):
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

        [self._check_and_add_neighbour(c, x + offset_x, y + offset_y) for offset_x, offset_y in Grid.NEIGHBOUR_OFFSETS]


    def remove_cell(self, x, y):
         # Check and add the neighbours (both directions)
        try:
            c = self.cells[y][x]
        except Exception:
            raise GridError("Cell does not exists")
        [self._check_and_remove_neighbour(c, x + offset_x, y + offset_y) for offset_x, offset_y in Grid.NEIGHBOUR_OFFSETS]
        self.cells[y][x] = None

        
    def cell_neighbours(self, c):
        neighbours = c.get_neighbours()
        ret_list = []
        for n in neighbours:
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

    def _prepare_cells(self):
        for i in self.cells:
            for j in i:
                if j != None:
                    j._tentative_weight = 10000
                    j._status = "NOT VISITED"

    # Djikstras shortest path algorithm
    # Refactor this!
    def get_shortest_path(self, start, end):
        self._prepare_cells()
        curr = start
        curr._tentative_weight = 0
        pending_exploration = [start]    # Make this into a set
        visited_set = []

        while curr != end:
            try:
                curr = pending_exploration.pop(0)
            except IndexError:  # pending_exploration is empty, no path found
                raise GridError("No path found")

            visited_set.append(curr)

            for cell in curr.get_neighbours():
                if cell in visited_set:
                    next
                possible_cost = curr._tentative_weight + cell.get_cost()
                if cell._tentative_weight > possible_cost:
                    cell._tentative_weight = possible_cost
                    cell._parent_cell = curr
                    if cell not in pending_exploration:   # If peding_exploration is a set then this is not needed 
                        pending_exploration.append(cell)
            pending_exploration = sorted(pending_exploration, key=lambda(x): x._tentative_weight)

        # Find the path taken
        curr = end
        shortest_path = []

        while curr != start:
            shortest_path.append(self.cell_coord(curr))
            curr = curr._parent_cell
    
        shortest_path.append(self.cell_coord(start))

        return (end._tentative_weight, list(reversed(shortest_path)))
