#!/usr/bin/env python

from Tkinter import *
from grid import *
import warnings
from graphen.algorithms.pathfinding import Djikstra as Djikstra
from graphen.algorithms.pathfinding import AStar as AStar

class Waypoint(object):
    def __init__(self, cell):
        self.cell = cell
        self.next_wp = None
        self.prev_wp = None

    def create(self, view):
        (x, y) = view.cell_to_screen(self.cell)
        idx = view.create_rectangle(x-view.cw/2+2, y-view.ch/2+2, x+view.cw/2-2, y+view.ch/2-2, fill="red", activeoutline="yellow")
        return idx

class Path(object):
    def __init__(self, PO, start, end):
        self.start_wp = start
        self.end_wp = end
        self.start_vertex = PO._graph.get_cell(start.cell)
        self.end_vertex = PO._graph.get_cell(end.cell)
        self.po = PO
        self.po.shortest_path(self.start_vertex, self.end_vertex)
        print ("Time", self.po.time)

    def create(self, view):
        print "Create PATH", self, [view.grid.cell_coord(seg) for seg in self.po.path]
        coords = [(x*view.cw + view.cw/2, y*view.ch+view.ch/2) for x,y in [view.grid.cell_coord(seg) for seg in self.po.path]]
        coords = list(sum(coords, ()))
        idx = view.create_line(*coords, width=3, smooth=True)
        return idx

class GridCanvas(Canvas, object):
    def __init__(self, root, grid, width=200, height=200):
        Canvas.__init__(self, root, width=width, height=height, background="black")
        self.root = root
        self.grid = grid
        (self.vert_cells, self.hori_cells) = grid.size
        (self.cw, self.ch) = (width*1.0/self.vert_cells, height*1.0/self.hori_cells)
        self._edit_mode = False
        self.rect_ids = [[None]*self.hori_cells]*self.vert_cells
        self.objects = {}
        for i in range(self.vert_cells):
            for j in range(self.hori_cells):
                idx = self.create_rectangle(i * self.cw, j * self.ch, (i + 1) * self.cw, (j + 1) * self.ch,
                                            fill = "white", activewidth=3, activeoutline="blue")
                self.rect_ids[i][j]= idx
                try:
                    c = g.get_cell(i, j)
                except GraphError:
                    self.itemconfig(idx, fill="black")

    def cell_to_screen(self, cell):
        return (cell[0]*self.cw+self.cw/2, cell[1]*self.ch+self.ch/2)

    def add(self, object):
        idx = object.create(self)
        self.objects[object] = idx
        print "Created:", object

    def remove(self, object):
        print "Remove", object
        self.delete(self.objects[object])
        self.objects.pop(object)


    def process_click(self, x, y):
        colors = {"black" : "white", "white" : "black"}
        idx = self.find_closest(x, y)
        fill = self.itemcget(idx, "fill")
        self.itemconfig(idx, fill=colors[fill])

class GridController(object):
    def __init__(self, grid, view):
        self.grid = grid
        self.view = view
        self.objects = {}
        self.waypoints = {"last_added_wp": None}
        self.paths = {}
        self.view.bind("<Button-1>", self.mouse_click)
        self.view.root.bind("<a>", self.toggle_algo)
        self.view.root.bind("<e>", self.toggle_map_edit)
        self.algo = "Djikstra"
        self.algos = {"Djikstra":"A*", "A*":"Djikstra"}
        self.map_edit = False
        self.set_win_title()


    def set_win_title(self):
        self.view.root.wm_title("Algorithm [" + self.algo + "] Map edit [" + str(self.map_edit) + "]")

    def toggle_algo(self, event):
        self.algo = self.algos[self.algo]
        self.set_win_title()

    def toggle_map_edit(self, event):
        self.map_edit = not self.map_edit
        self.view.edit_mode = self.map_edit
        self.set_win_title()

    def toggle_waypoint(self, cell):
        try:
            self.view.remove(self.objects[cell])
            wp = self.objects.pop(cell)
        except KeyError:
            wp = Waypoint(cell)
            self.objects[cell] = wp
            self.view.add(wp)
            self.waypoints[wp] = {"prev":None, "next":None, "paths":[]}
            return (True, wp)
        return (False, wp)

    def create_path_obj(self):
        if self.algo == "Djikstra":
            return Djikstra(self.grid)
        else:
            return AStar(self.grid, self.grid.dist)

    def update_paths(self):
        for wp, p in self.paths.items():
            print wp, p
            self.view.remove(p)
            p.po = self.create_path_obj()
            p.po.shortest_path(p.start_vertex, p.end_vertex)
            self.view.add(p)

    def mouse_click(self, event):
        cell = (rect_x, rect_y) = self.coord_to_cell(event.x, event.y)
        d = self.create_path_obj()
        cell_lbl = Grid.CellCoordLabel(cell[0], cell[1])
        # See if cell is existing
        try:
            c = self.grid.vertex(cell_lbl)
        except:
            if self.map_edit:
                self.view.process_click(event.x, event.y)
                self.grid.add_cell(cell[0], cell[1])
                self.update_paths()
                return
        else:
            if self.map_edit:
                self.view.process_click(event.x, event.y)
                self.grid.del_cell(cell)
                self.update_paths()
                return

        (wp_added, wp) = self.toggle_waypoint(cell)
        if wp_added:
            try:
                last_added = self.waypoints["last_added_wp"]
                self.waypoints[last_added]["next"] = wp
                self.waypoints[wp]["prev"] = last_added
            except KeyError as e:
                pass
            else:
                prev_wp = self.waypoints[wp]["prev"]
                p = Path(d, prev_wp, wp)
                self.view.add(p)
                self.paths[wp] = p
                if p not in self.waypoints[wp]["paths"]:
                    self.waypoints[wp]["paths"].append(p)
                if p not in self.waypoints[prev_wp]["paths"]:
                    self.waypoints[prev_wp]["paths"].append(p)
            self.waypoints["last_added_wp"] = wp
        else:
            prev_wp = self.waypoints[wp]["prev"]
            next_wp = self.waypoints[wp]["next"]
            for path in self.waypoints[wp]["paths"]:
                self.view.remove(path)
            #print "Remove from paths", wp, self.paths
            #self.paths.pop(wp)
            self.waypoints.pop(wp)
            self.view.remove(wp)
            try:
                self.waypoints[prev_wp]["next"] = next_wp
            except:
                return
            try:
                self.waypoints[next_wp]["prev"] = prev_wp
            except:
                self.waypoints["last_added_wp"] = prev_wp
                return
            p = Path(d, prev_wp, next_wp)
            self.add_path_to_wp(p, prev_wp)
            self.add_path_to_wp(p, next_wp)
            self.view.add(p)
            self.paths[wp] = p

    def add_path_to_wp(self, path, waypoint):
        if path not in self.waypoints[waypoint]["paths"]:
            self.waypoints[waypoint]["paths"].append(path)

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
    w = GridCanvas(root, g, width=600, height=600)
    c = GridController(g, w)

    w.pack()

    mainloop()
