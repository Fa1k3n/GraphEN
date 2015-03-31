#!/usr/bin/env python

import unittest
import math
from graphen.algorithms.pathfinding import Djikstra as Djikstra

from grid import *


class test_grid(unittest.TestCase):

    def setUp(self):
        pass

    def testDefaultCreate(self):
        g = Grid()
        self.assertIsNotNone(g.vertex(Grid.CellCoordLabel(0, 0)))

    def testRemoveNode(self):
        g = Grid()
        g.del_vertex(Grid.CellCoordLabel(2, 2))
        with self.assertRaises(GraphError):
            g.vertex(Grid.CellCoordLabel(2, 2))
        
    def testRemoveNonexistingNode(self):
        g = Grid()
        with self.assertRaises(GraphError):
            g.del_vertex(Grid.CellCoordLabel(7, 3))

    def testShortestPath(self):
        g = Grid(5, 1)
        PO = Djikstra(g)
        PO.shortest_path(g.get_cell(0, 0), g.get_cell(4, 0))
        self.assertEquals(PO.effort(), 4)
        answ = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        for idx, p in enumerate(PO.path):
            self.assertEquals(p.label, g.CellCoordLabel(answ[idx][0], answ[idx][1]))

        #g.add_cell(5, 0, Node(), 2)
        #PO = Djikstra(g)
        #PO.shortest_path(g.get_cell(0, 0), g.get_cell(5, 0))
        #self.assertEquals(PO.effort(), 6)
        #answ = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
        #for idx, p in enumerate(PO.path):
        #    self.assertEquals(p.label, answ[idx])
#        self.assertEquals(PO.path, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)])

    def testShortestPathBigGrid(self):
         g = Grid(5, 5)
         PO = Djikstra(g)
         PO.shortest_path(g.get_cell(0, 0), g.get_cell(4, 4))
         self.assertEquals(PO.effort(), math.sqrt(4*4 + 4*4))
         answ = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
         for idx, p in enumerate(PO.path):
             self.assertEquals(p.label, g.CellCoordLabel(answ[idx][0], answ[idx][1]))

    def testNodeCoord(self):
         g = Grid(5, 5)
         c = g.get_cell(3, 2)
         self.assertEquals(g.cell_coord(c), (3,2))

    def testNoPathFound(self):
         g = Grid(3, 3)
         PO = Djikstra(g)
         g.del_cell(1, 1)
         g.del_cell(1, 0)
         g.del_cell(0, 1)
         with self.assertRaises(GraphError):
             PO.shortest_path(g.get_cell(0, 0), g.get_cell(2, 2))


        

if __name__ == '__main__':
    unittest.main()
