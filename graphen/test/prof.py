from grid import *
import cProfile
import timeit
from graphen.algorithms.pathfinding import Djikstra as Djikstra

if __name__ == '__main__':

    (hori_cells, vert_cells) = (5, 5)
    cProfile.run("g = Grid(hori_cells, vert_cells)")

    # Make some obstacles
    #for i in [2, 4]:
    #    for y in range(5):
    #        g.del_cell(hori_cells/i, vert_cells/i - y)
    #    for x in range(5):
    #        g.del_cell(hori_cells/i - x, vert_cells/i)

    #PO = AStar(g, g.dist)

    #PO = Djikstra(g)
    #cProfile.run("PO.shortest_path(g.get_cell(0, 0), g.get_cell(39, 39))")
    #timeit.timeit("PO.shortest_path(g.get_cell(0, 0), g.get_cell(39, 39))")
    #print (PO.time)
