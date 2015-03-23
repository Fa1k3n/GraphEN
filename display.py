#!/usr/bin/env python

from Tkinter import *
from grid import *

import time
import itertools

class GridCanvas(Canvas, object):
    def __init__(self, root, grid, width=200, height=200):
        Canvas.__init__(self, root, width=width, height=height)
        self.root = root
        self.grid = grid
        (self.vert_cells, self.hori_cells) = grid.size
        (self.cw, self.ch) = (width*1.0/self.vert_cells, height*1.0/self.hori_cells)
        self.cell_active_fill = "red"
        self._selected_cells = []
        self.path_objs = []
        self.draw()

    @property
    def selected_cells(self):
        return self._selected_cells

    @selected_cells.setter
    def selected_cells(self, cells):
        self._selected_cells = cells
        self.draw()

    def draw(self, path_obj=None):
        self.rect_ids = [[None]*self.hori_cells]*self.vert_cells

        for i in range(self.vert_cells):
            for j in range(self.hori_cells):
                cell_fill = "white"
                cell_active_fill = self.cell_active_fill
                try:
                    c = g.get_cell(i, j)
                except GridError:
                    # Cell does not exists
                    cell_fill = "black"
                    cell_active_fill = "black"
                else:
                    if filter(lambda path_obj: c in path_obj.visited(), self.path_objs):
                        cell_fill = "brown"
                    if (i, j) in self.selected_cells:
                        cell_fill = "blue"
                id = self.create_rectangle(i * self.cw, j * self.ch, (i + 1) * self.cw, (j + 1) * self.ch, fill = cell_fill, activefill=cell_active_fill)
                self.rect_ids[i][j]= id

        for path_obj in self.path_objs:
            for idx, start in path_obj.path:
                print path_obj.path
                try:
                    end = path_obj.path[idx + 1]
                except Exception as e:
                    print "Exception", e
                    pass
                else:
                    #pass
                    print "Start:", start
                    #(sx, sy) = (start[0], start[1])
                    #(ex, ey) = (end[0], end[1])
                    #self.create_line(sx*self.cw + self.cw/2, sy*self.ch + self.ch/2,
                    #self.cw + self.cw/2, ey*self.ch + self.ch/2, width=3)
            #old_cell = None
            #for cell in path_obj.path:
            #    if old_cell is None:
            #        old_cell = cell
            #        continue
            #    self.create_line(old_cell[0]*self.cw + self.cw/2, old_cell[1]*self.ch + self.ch/2,
            #    cell[0]*self.cw + self.cw/2, cell[1]*self.ch + self.ch/2, width=3)
            #    old_cell = cell

    def get_rect(self, x, y):
        return self.rect_ids[y][x]

class GridController(object):
    def __init__(self, grid, view):
        self.grid = grid
        self.view = view
        #self.toggle_algo = itertools.cycle(['Djikstra', 'AStar']).next
        self.view.bind("<Button-1>", self.mouse_click)
        self.view.root.bind("<a>", self.toggle_algo)
        self.algo = "Djikstra"
        self.algos = {"Djikstra":"AStar", "AStar":"Djikstra"}
        self.selected_cells = []


    def toggle_algo(self, event):
        self.algo = self.algos[self.algo]

    def mouse_click(self, event):
        cell = self.coord_to_cell(event.x, event.y)
        if self.algo == "Djikstra":
            d = Djikstra(self.grid)
        else:
            d = AStar(self.grid, self.grid.dist)

        (s, e) = (None, None)
        if cell in self.selected_cells:
            idx = self.selected_cells.index(cell)
            self.selected_cells.remove(cell)
            # Create a new Path object between the cells
            try:
                s = self.grid.get_cell(self.selected_cells[idx-1])
                e = self.grid.get_cell(self.selected_cells[idx+1])
            except:
                print "Problem removing checkpoint", e
        else:
            self.selected_cells.append(cell)
            idx = self.selected_cells.index(cell)
            try:
                s = self.grid.get_cell(self.selected_cells[idx-1])
                e = self.grid.get_cell(self.selected_cells[idx])
            except Exception as e:
                print "Problem adding checkpoint", e

        d.shortest_path(s, e)
        print d.path
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
            g.remove_cell(hori_cells/i, vert_cells/i - y)
        for x in range(5):
            g.remove_cell(hori_cells/i - x, vert_cells/i)

    root = Tk()
    w = GridCanvas(root, g, width=400, height=400)
    c = GridController(g, w)

    w.pack()

    mainloop()
