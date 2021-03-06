#!/usr/bin/env python

from Tkinter import *
from grid import *
import warnings

class GridComp(object):
    active_comp = [None]

    @staticmethod
    def next_active_comp():
        for ac in GridComp.active_comp:
            yield ac

    @staticmethod
    def reset_active_comp():
        GridComp.active_comp = []

    active_color = "green"
    active_fill = "green"
    inactive_fill = "black"

    def __init__(self):
        self.idx = None
        self.activate_on_creation = True

    def create(self, view, grid):
        self.grid = grid
        self.idx = self.create_component(view)
        if self.activate_on_creation:
            self.activate()
        self.view.tag_raise("waypoint")  # Make sure that waypoint are always at the top
        return self.idx

    def activate(self, clear=True):
        if clear:
            for ac in GridComp.next_active_comp():
                if ac is not None:
                    ac.inactivate()
            GridComp.active_comp = []
        self.view.logger("[" + str(type(self).__name__) + "] " + str(self))
        self.activate_component(self.idx)
        GridComp.active_comp.append(self)

    def inactivate(self):
        self.inactivate_component(self.idx)
        GridComp.reset_active_comp()

    def delete(self):
        self.inactivate()
        self.delete_component()

    def move(self, view, cell):
        (x, y) = self.view.cell_to_screen(cell)
        (sx, sy) = self.view.cell_to_screen(self.cell)
        view.move(self.idx, x-sx, y-sy)
        self.cell = cell

    def __str__(self):
        return ""

class Waypoint(GridComp):
    def __init__(self, cell):
        super(Waypoint, self).__init__()
        self.cell = cell
        self.view = None
        self.next_wp = None
        self.prev_wp = None
        self.outgoing_paths = []
        self.ingoing_paths = []

    def create_component(self, view):
        (x, y) = view.cell_to_screen(self.cell)
        self.view = view
        for ac in GridComp.next_active_comp():
            if isinstance(ac, Waypoint):
                ac.next_wp = self
                self.prev_wp = ac
                break
        return view.create_rectangle(x-view.cw/2+2, y-view.ch/2+2, x+view.cw/2-2, y+view.ch/2-2, tag="waypoint", fill="red", width=0, activewidth=3, activeoutline="blue")

    def activate_component(self, idx):
        self.view.itemconfig(idx, outline=GridComp.active_fill, width=2)

    def inactivate_component(self, idx):
        self.view.itemconfig(idx, outline=GridComp.inactive_fill, width=0)

    def remove_paths(self, *path_list):
        for p in path_list:
            iter_paths = list(p)
            for op in iter_paths:
                op.delete()

    def delete_component(self):
        (prev_wp, next_wp) = (self.prev_wp, self.next_wp)
        if prev_wp is not None:
            prev_wp.next_wp = next_wp
        if next_wp is not None:
            next_wp.prev_wp = prev_wp
        if self.outgoing_paths and self.ingoing_paths:
            p = Path(self.ingoing_paths[0].start_wp, self.outgoing_paths[0].end_wp)
            self.view.add(p)
        self.remove_paths(self.outgoing_paths, self.ingoing_paths)
        self.view.remove(self)

    def __str__(self):
        s = "{:10s}".format(str(self.cell))
        s += "\n\t->"
        if self.outgoing_paths:
            for path in self.outgoing_paths:
                s += "{:10s}".format(str(path.end_wp.cell))
        else:
            s += "{:10s}".format("None")
        s += "\n\t<-"
        if self.ingoing_paths:
            for path in self.ingoing_paths:
                s += "{:10s}".format(str(path.start_wp.cell))
        else:
            s += "{:10s}".format("None")
        return s

    def remove_path(self, wp):
        try:
            self.outgoing_paths.pop(self.outgoing_paths.index(wp))
        except ValueError:
            pass

        try:
            self.ingoing_paths.pop(self.ingoing_paths.index(wp))
        except ValueError:
            pass

    def find_path(self, wp):
        for po in self.outgoing_paths:
            if po.end_wp == wp:
                return po

        for po in self.ingoing_paths:
            if po.start_wp == wp:
                return po
        return None

    def move(self, view, cell):
        super(Waypoint, self).move(self.view, cell)
        # Update paths connected to this WP
        iter_outgoing = list(self.outgoing_paths)
        for op in iter_outgoing:
            op.delete()
            if op.end_wp.cell is not cell:
                p = Path(self, op.end_wp)
                self.view.add(p)

        iter_ingoing = list(self.ingoing_paths)
        for op in iter_ingoing:
            op.delete()
            if op.start_wp.cell is not cell:
                p = Path(op.start_wp, self)
                self.view.add(p)
        # Make sure that WP is still active
        self.activate()

class Path(GridComp):
    def __init__(self, start_wp, end_wp):
        super(Path, self).__init__()
        self.start_wp = start_wp
        self.end_wp = end_wp
        start_wp.outgoing_paths.append(self)
        end_wp.ingoing_paths.append(self)
        self.view = None
        self.po = None
        self.activate_on_creation = False
        self.markers = []

    def create_component(self, view):
        self.view = view
        (x, y) = view.cell_to_screen(self.start_wp.cell)
        self.po = self.grid.create_path_obj()
        self.po.shortest_path(self.grid.get_cell(self.start_wp.cell), self.grid.get_cell(self.end_wp.cell))
        coords = [(x*self.view.cw + self.view.cw/2, y*self.view.ch+self.view.ch/2) for x,y in [self.view.grid.cell_coord(seg) for seg in self.po.path]]
        coords = list(sum(coords, ()))
        if len(coords) == 2:  # This is for when the start and end cells are the same
            [coords.append(c) for c in list(coords)]
        return view.create_line(*coords, width=2, smooth=True, activefill="blue", tag="path")

    def activate_component(self, idx):
        for vert in self.po.closedset:
            (x, y) = self.view.cell_to_screen(self.grid.cell_coord(vert))
            self.markers.append(self.view.create_oval(x-2, y-2, x+2, y+2, fill="red"))
        for (score, vert) in self.po.openset.queue:
            (x, y) = self.view.cell_to_screen(self.grid.cell_coord(vert))
            self.markers.append(self.view.create_oval(x-2, y-2, x+2, y+2, fill="green"))
        self.view.itemconfig(idx, fill=GridComp.active_fill, width=3)


    def inactivate_component(self, idx):
        self.view.logger("")
        self.view.itemconfig(idx, fill=GridComp.inactive_fill, width=2)
        for marker in self.markers:
            self.view.delete(marker)

    def delete_component(self):
        self.start_wp.remove_path(self)
        self.end_wp.remove_path(self)
        self.view.remove(self)

    def __str__(self):
        s = "No path selected"
        if self.po is not None:
            s = "Time: " + str(self.po.time) + " s"
        return s

class Cell(GridComp):
    def __init__(self, cell):
        super(Cell, self).__init__()
        self.cell = cell
        self.view = None

    def create_component(self, view):
        self.view = view
        (x, y) = self.cell
        return view.create_rectangle(x * view.cw, y * view.ch, (x + 1) * view.cw, (y + 1) * view.ch,
                                    fill="white", activewidth=3, activeoutline="blue", tag="Cell")

    def activate_component(self, idx):
        self.view.itemconfig(idx, outline=GridComp.active_fill, width=3)

    def inactivate_component(self, idx):
        self.view.itemconfig(idx, outline=GridComp.inactive_fill, width=1)

    def delete_component(self):
        self.view.remove(self)

    def __str__(self):
        return str(self.cell)

class GridCanvas(Canvas, object):

    def __init__(self, root, grid, width=200, height=200):
        Canvas.__init__(self, root, width=width, height=height, background="black")
        self.root = root
        self.grid = grid
        (self.vert_cells, self.hori_cells) = grid.size
        (self.cw, self.ch) = (width*1.0/self.vert_cells, height*1.0/self.hori_cells)
        self.rect_ids = [[None]*self.hori_cells]*self.vert_cells
        self.objects = {}
        self.logger = lambda x: x

        for i in range(self.vert_cells):
            for j in range(self.hori_cells):
                c = Cell((j, i))
                self.add(c)
                try:
                    c = g.get_cell(i, j)
                except GraphError:
                    self.remove(c)

    def cell_to_screen(self, cell):
        return (cell[0]*self.cw+self.cw/2, cell[1]*self.ch+self.ch/2)

    def screen_to_cell(self, x, y):
        cell_x = int(x / self.cw)
        cell_y = int(y / self.ch)
        return (cell_x, cell_y)

    def add(self, obj):
        idx = obj.create(self, self.grid)
        self.objects[obj] = idx
        self.tag_raise("waypoint")  # Make sure waypoints are on top

    def remove(self, object):
        self.delete(self.objects[object])
        self.objects.pop(object)
        if isinstance(object, Cell):
            # World has changed, recalculate all paths
            self.recalculate_paths()

    def recalculate_paths(self):
        for obj in filter(lambda x: isinstance(x, Path), self.objects):
            obj.delete()

            ## FIX THIS!!! creation of object should add it to the view
            p = Path(obj.start_wp, obj.end_wp)
            self.add(p)

    def get_current_obj(self):
        try:
            idx = self.find_withtag(CURRENT)[0]
        except IndexError:
            # Object does not exist
            return None
        else:
            for obj in self.objects:
                if self.objects[obj] == idx:
                    return obj
        return None

    def find_enclosed_objs(self, x0, y0, x1, y1):
        ei = self.find_enclosed(x0,y0, x1, y1)
        eo = []
        for idx in ei:
            eo.append(self.find_obj(idx))
        return eo

    def find_obj(self, idx):
        for obj in self.objects:
            if self.objects[obj] == idx:
                return obj
        return None

    def iterate_objs(self):
        for obj in self.objects:
            yield obj

class GridController(object):
    def __init__(self, grid, view):
        self.grid = grid
        self.view = view
        self.key_down = None
        self.last_mouse = (None, None)
        self.view.bind("<Button-1>", self.mouse_leftclick)
        self.view.bind("<Button-3>", self.mouse_rightclick)
        self.view.bind("<ButtonRelease-1>", lambda event: setattr(self, "last_mouse", (None, None)))
        self.view.bind("<B1-Motion>", self.mouse_motion)
        self.view.root.bind("<a>", self.toggle_algo)
        self.view.root.bind("<BackSpace>", self.delete_comp)
        self.view.root.bind("<Any-KeyPress>", lambda event: setattr(self, "key_down", event.char))
        self.view.root.bind("<Any-KeyRelease>", lambda event: setattr(self, "key_down", None))
        self.logger = lambda s, x: x

    def toggle_algo(self, event):
        self.grid.algo = self.grid.algos[self.grid.algo]
        self.logger("Algorithm [" + self.grid.algo + "]")

    def delete_comp(self, event):
        to_be_deleted = list(GridComp.active_comp)
        for ac in to_be_deleted:
            if isinstance(ac, Cell):
                self.grid.del_cell(ac.cell)
            ac.delete()
        GridComp.active_comp = []

    def check_and_create_wp(self, cell):
        if len(GridComp.active_comp) > 0:
            last_obj = GridComp.active_comp[0]
        else:
            last_obj = None

        new_obj = self.view.get_current_obj()
        if isinstance(new_obj, Cell):
            wp = Waypoint(cell)
            self.view.add(wp)
            if isinstance(last_obj, Waypoint):
                p = Path(last_obj, wp)
                self.view.add(p)
            return wp
        return None

    def mouse_motion(self, event):
        new_cell = self.view.screen_to_cell(event.x, event.y)
        if self.grid.has_cell(new_cell) and len(GridComp.active_comp) and isinstance(GridComp.active_comp[0], Waypoint):
            for ac in filter(lambda x: isinstance(x, Waypoint), list(GridComp.next_active_comp())):
                if ac.cell is not new_cell:
                    ac.move(self.view, new_cell)
        elif self.grid.has_cell(new_cell):
            for obj in filter(lambda x: isinstance(x, Cell), GridComp.active_comp):
                obj.inactivate()
            enclosed_obj = self.view.find_enclosed_objs(event.x, event.y, self.last_mouse[0], self.last_mouse[1])
            for obj in filter(lambda x: isinstance(x, Cell), enclosed_obj):
                obj.activate(False)

    def mouse_rightclick(self, event):
        cell = (rect_x, rect_y) = self.view.screen_to_cell(event.x, event.y)
        if self.grid.has_cell(cell):
            self.check_and_create_wp(cell)

    def mouse_leftclick(self, event):
        cell = (rect_x, rect_y) = self.view.screen_to_cell(event.x, event.y)
        if not self.grid.has_cell(cell):
            c = Cell(cell)
            self.view.add(c)
            self.grid.add_cell(cell[0], cell[1])
            self.view.recalculate_paths()
        last_obj = GridComp.next_active_comp()
        if self.key_down == "w":
            new_obj = self.check_and_create_wp(cell)
        else:
            new_obj = self.view.get_current_obj()
        # Lets activate the new object if possible
        try:
            new_obj.activate()
        except AttributeError:
            pass

        if isinstance(last_obj, Waypoint) and isinstance(new_obj, Waypoint) and last_obj is not new_obj:
            # User has selected two different waypoints, lets create a path between them
            # unless there already is a path between them
            if not last_obj.find_path(new_obj):
                p = Path(last_obj, new_obj)
                self.view.add(p)
        else:
            # Possible drag select action, lets set last known pos
            self.last_mouse = (event.x, event.y)

def view_msg_hndlr(msg):
    view_message.set(msg)

def ctrl_msg_hndlr(msg):
    ctrl_message.set(msg)

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
    root.wm_title("Pathfinding experiments")
    w = GridCanvas(root, g, width=600, height=600)
    c = GridController(g, w)
    view_message = StringVar()
    ctrl_message = StringVar()
    c.logger = ctrl_msg_hndlr
    c.toggle_algo(None)
    w.logger = view_msg_hndlr


    view_lbl = Label(root, textvariable=view_message, bd=3)
    ctrl_lbl = Label(root, textvariable=ctrl_message, bd=3)

    w.pack()
    ctrl_lbl.pack(side="left")
    view_lbl.pack(side="left", after=ctrl_lbl, padx=30)


    mainloop()
