#!/usr/bin/env python

from Tkinter import *
from grid import *
import warnings
from graphen.algorithms.pathfinding import Djikstra as Djikstra
from graphen.algorithms.pathfinding import AStar as AStar

class GridCanvas(Canvas, object):
    def __init__(self, root, grid, width=200, height=200):
        Canvas.__init__(self, root, width=width, height=height)
        self.root = root
        self.grid = grid
        (self.vert_cells, self.hori_cells) = grid.size
        (self.cw, self.ch) = (width*1.0/self.vert_cells, height*1.0/self.hori_cells)
        self._selected_cells = []
        self._edit_mode = False
        self.path_objs = []
        self.draw()

    @property
    def selected_cells(self):
        return self._selected_cells

    @selected_cells.setter
    def selected_cells(self, cells):
        self._selected_cells = cells
        self.draw()

    @property
    def edit_mode(self):
        return self._edit_mode

    @edit_mode.setter
    def edit_mode(self, em):
        self._edit_mode = em
        self.draw()

    @property
    def path_objs(self):
        return self._path_objs

    @path_objs.setter
    def path_objs(self, po):
        self._path_objs = po
        self.draw()

    def draw(self, path_obj=None):
        self.rect_ids = [[None]*self.hori_cells]*self.vert_cells

        for i in range(self.vert_cells):
            for j in range(self.hori_cells):
                cell_fill = "white"
                cell_active_fill = "blue"
                if self.edit_mode:
                    cell_active_fill = "black"
                try:
                    c = g.get_cell(i, j)
                except GraphError:
                    # Cell does not exists
                    cell_fill = "black"
                    cell_active_fill = "black"
                else:
                   if len(list(filter(lambda path_obj: c in path_obj.visited(), self.path_objs))) > 0:
                        cell_fill = "brown"
                   #if len(list(filter(lambda path_obj: c in path_obj.fringe(), self.path_objs))) > 0:
                   #    cell_fill = "gray"
                   if (i, j) in self.selected_cells:
                        cell_fill = "blue"
                id = self.create_rectangle(i * self.cw, j * self.ch, (i + 1) * self.cw, (j + 1) * self.ch, fill = cell_fill, activefill=cell_active_fill)
                self.rect_ids[i][j]= id

        for po in self.path_objs:
            for idx, start in enumerate(po.path):
                try:
                    end = po.path[idx + 1]
                except Exception as e:
                    pass
                else:
                    (sx, sy) = self.grid.cell_coord(start)
                    (ex, ey) = self.grid.cell_coord(end)
                    self.create_line(sx*self.cw + self.cw/2, sy*self.ch + self.ch/2,
                                     ex*self.cw + self.cw/2, ey*self.ch + self.ch/2, width=3)

    def get_rect(self, x, y):
        return self.rect_ids[y][x]

class GridController(object):
    def __init__(self, grid, view):
        self.grid = grid
        self.view = view
        self.view.bind("<Button-1>", self.mouse_click)
        self.view.root.bind("<a>", self.toggle_algo)
        self.view.root.bind("<e>", self.toggle_map_edit)
        self.algo = "Djikstra"
        self.algos = {"Djikstra":"A*", "A*":"Djikstra"}
        self.map_edit = False
        self.set_win_title()
        self.selected_cells = []

    def set_win_title(self):
        self.view.root.wm_title("Algorithm [" + self.algo + "] Map edit [" + str(self.map_edit) + "]")

    def toggle_algo(self, event):
        self.algo = self.algos[self.algo]
        self.set_win_title()

    def toggle_map_edit(self, event):
        self.map_edit = not self.map_edit
        self.view.edit_mode = self.map_edit
        self.set_win_title()

    def create_path_obj(self):
        if self.algo == "Djikstra":
            return Djikstra(self.grid)
        else:
            return AStar(self.grid, self.grid.dist)

    def mouse_click(self, event):
        cell = self.coord_to_cell(event.x, event.y)
        d = self.create_path_obj()
        cell_lbl = Grid.CellCoordLabel(cell[0], cell[1])
        # See if cell is existing
        try:
            c = self.grid.vertex(cell_lbl)
        except:
            print "here", cell_lbl
            self.grid.add_cell(cell[0], cell[1])
            self.view.draw()
            return
        else:
            if self.map_edit:
                self.grid.del_cell(cell)
                # Create all PO's again, world has changed
                new_pos = []
                for po in self.view.path_objs:
                    p = self.create_path_obj()
                    (start, end) = (po.path[0], po.path[-1])
                    p.shortest_path(start, end)
                    new_pos.append(p)
                self.view.path_objs = new_pos
                return

        if cell in self.selected_cells:
            idx = self.selected_cells.index(cell)
            self.selected_cells.remove(cell)

            po_to_be_removed = []
            (new_start, new_end) = (None, None)
            for po in self.view.path_objs:
                (po_start, po_end) = (self.grid.cell_coord(po.path[0]), self.grid.cell_coord(po.path[-1]))
                if po_start == cell:
                    po_to_be_removed.append(po)
                    new_end = po_end
                elif po_end == cell:
                    po_to_be_removed.append(po)
                    new_start = po_start
            [self.view.path_objs.remove(po) for po in po_to_be_removed]
            if new_end != None and new_start != None:
                d.shortest_path(self.grid.get_cell(new_start), self.grid.get_cell(new_end))
                self.view.path_objs.append(d)
        else:
            self.selected_cells.append(cell)
            idx = self.selected_cells.index(cell)
            if idx > 0:
                s = self.grid.get_cell(self.selected_cells[idx-1][0], self.selected_cells[idx-1][1])
                e = self.grid.get_cell(self.selected_cells[idx][0], self.selected_cells[idx][1])
                d.shortest_path(s, e)
                print ("Time", d.time)
                self.view.path_objs.append(d)

        self.view.selected_cells = self.selected_cells

    def coord_to_cell(self, x, y):
        cell_x = int(x / self.view.cw)
        cell_y = int(y / self.view.ch)
        return (cell_x, cell_y)

if __name__ == '__main__':

    (hori_cells, vert_cells) = (40, 40)
    g = Grid(hori_cells, vert_cells)

    # Make some obstacles
    for i in [2, 4]:
        for y in range(5):
            g.del_vertex(Grid.CellCoordLabel(hori_cells/i, vert_cells/i - y))
        for x in range(4):
            g.del_vertex(Grid.CellCoordLabel(hori_cells/i - x - 1, vert_cells/i))

    root = Tk()
    w = GridCanvas(root, g, width=400, height=400)
    c = GridController(g, w)

    w.pack()

    mainloop()
