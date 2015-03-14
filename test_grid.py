#!/usr/bin/env python

import unittest
from node import *
from grid import *

class test_grid(unittest.TestCase):

    def setUp(self):
        pass

    def testDefaultCreate(self):
        g = Grid()
        self.assertEquals(g.get_cell(0, 0), None)

    def testAddNode(self):
        g = Grid()
        c = Node()
        g.add_cell(0, 0, c, 1)
        self.assertEquals(g.get_cell(0, 0), c)

    def testAddNodeOutside(self):
        g = Grid()
        c = Node()
        g.add_cell(1, 1, c, 1)
        self.assertEquals(g.get_cell(1, 1), c)

    def testRemoveNode(self):
        g = Grid()
        c = Node()
        g.add_cell(2, 3, c, 1)
        g.remove_cell(2, 3)
        with self.assertRaises(GridError): 
            g.get_cell(2, 3)
        
    def testRemoveNonexistingNode(self):
        g = Grid()
        with self.assertRaises(GridError):
            g.remove_cell(2, 3)

    def testNodeNeighbours(self):
         g = Grid()
         c1 = Node()
         c2 = Node()
         g.add_cell(0, 0, c1)
         g.add_cell(0, 1, c2)
         assert(c2 in c1.neighbours())
         assert(c1 in c2.neighbours())
         self.assertEquals(len(list(c1.neighbours())), 1)

    def testNodeNeighboursAfterRemove(self):
         g = Grid()
         c1 = Node()
         c2 = Node()
         g.add_cell(0, 0, c1)
         g.add_cell(1, 0, c2)
         assert(c2 in c1.neighbours())
         g.remove_cell(1, 0)
         assert(c2 not in c1.neighbours())
         self.assertEquals(len(list(c1.neighbours())), 0)

    def testOverloadedConstrucor(self):
         g = Grid(10, 10)
         assert(g.get_cell(3, 4) in g.get_cell(3, 5).neighbours())
         assert(g.get_cell(2, 3) not in g.get_cell(3, 5).neighbours())

    def testRemoveNodeInUniformGrid(self):
         g = Grid(10, 10)
         assert(g.get_cell(5, 5) in g.get_cell(4, 5).neighbours())
         self.assertEquals(len(list(g.get_cell(4, 5).neighbours())), 8)
         g.remove_cell(5, 5)
         self.assertEquals(len(list(g.get_cell(4, 5).neighbours())), 7)
         self.assertEquals(len(list(g.get_cell(6, 5).neighbours())), 7)

    def testGetNodeNeighbours(self):
        g = Grid(5, 5)
        n = g.cell_neighbours(g.get_cell(2, 2))
        assert((2, 3) in n)
        assert((2, 1) in n)

    def testShortestPath(self):
        g = Grid(5, 1)
        (effort, path) = g.get_shortest_path(g.get_cell(0, 0), g.get_cell(4, 0))
        self.assertEquals(effort, 4)
        self.assertEquals(path, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)])
        g.add_cell(5, 0, Node(), 2)
        (effort, path) = g.get_shortest_path(g.get_cell(0, 0), g.get_cell(5, 0))
        self.assertEquals(effort, 6)
        self.assertEquals(path, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)])

    def testShortestPathBigGrid(self):
         g = Grid(5, 5)
         (effort, path) = g.get_shortest_path(g.get_cell(0, 0), g.get_cell(4, 4))
         self.assertEquals(effort, 4)
         self.assertEquals(path, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])

    def testNodeCoord(self):
         g = Grid(5, 5)
         c = g.get_cell(3, 2)
         self.assertEquals(g.cell_coord(c), (3,2))

    def testNodeCoordDeletedNode(self):
         g = Grid(5, 5)
         c = g.get_cell(3, 2)
         g.remove_cell(3, 2)
         with self.assertRaises(GridError):
             g.cell_coord(c)

    def testShortestPathDifficult(self):
         g = Grid(3, 3)
         g.remove_cell(1, 1)
         c = g.get_cell(1, 2)
         c.change_edge_costs(30)
         (effort, path) = g.get_shortest_path(g.get_cell(0, 0), g.get_cell(2, 2))
         self.assertEqual(effort, 3)
         self.assertEquals(path, [(0, 0), (1, 0), (2, 1), (2, 2)])

    def testNoPathFound(self):
         g = Grid(3, 3)
         g.remove_cell(1, 1)
         g.remove_cell(1, 0)
         g.remove_cell(0, 1)
         with self.assertRaises(GridError):
             (effort, path) = g.get_shortest_path(g.get_cell(0, 0), g.get_cell(2, 2))


        

if __name__ == '__main__':
    unittest.main()
