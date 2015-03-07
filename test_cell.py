#!/usr/bin/env python

import unittest
from cell import *

class test_cell(unittest.TestCase):

    def setUp(self):
        pass

    def testDefaultCreate(self):
        c = Cell()
        self.assertEquals(c.get_cost(), 1)

    def testOverriddenCreate(self):
        c = Cell(2)
        self.assertEquals(c.get_cost(), 2)

    def testChangeCost(self):
        c = Cell(1)
        c.set_cost(3)
        self.assertEquals(c.get_cost(), 3)

    def testAddNeighbourCell(self):
        c1 = Cell()
        c2 = Cell()
        c1.add_neighbour(c2)
        neighbours = c1.get_neighbours()
        assert(c2 in neighbours)

    def testRemoveNeigbourCell(self):
        c1 = Cell()
        c2 = Cell()
        c3 = Cell()
        c1.add_neighbour(c2)
        c1.add_neighbour(c3)
        c1.remove_neighbour(c2)
        neighbours = c1.get_neighbours()
        assert(c2 not in neighbours)
        assert(c3 in neighbours)

    def testRemoveAlreadyRemovedCell(self):
        c1 = Cell()
        c2 = Cell()
        c1.add_neighbour(c2)
        c1.remove_neighbour(c2)
        with self.assertRaises(CellError): 
            c1.remove_neighbour(c2)

if __name__ == '__main__':
    unittest.main()
