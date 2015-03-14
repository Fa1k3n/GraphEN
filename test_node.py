#!/usr/bin/env python

import unittest
from node import *

class test_edge(unittest.TestCase):
    def testDefaultCreate(self):
        e = Edge(None, None, 3)
        self.assertEqual(e.cost, 3)

    def testCostProperty(self):
        e = Edge(None, None, 3)
        e.cost = 2
        self.assertEqual(e.cost, 2)
        with self.assertRaises(EdgeError):
            e.cost = -1



class test_cell(unittest.TestCase):

    def setUp(self):
        pass

    def testBasicSetuo(self):
        c1 = Node()
        self.assertIsNotNone(c1)

    def testAddDefaultNeighbourCostNode(self):
        c1 = Node()
        c2 = Node()
        c1.add_neighbour(c2)
        assert(c2 in c1.neighbours())
        self.assertEquals(c1.edge_list[0].cost, 1)

    def testAddNeighbourNode(self):
        c1 = Node()
        c2 = Node()
        c1.add_neighbour(c2, 2)
        assert(c2 in c1.neighbours())

    def testRemoveNeigbourNode(self):
         c1 = Node()
         c2 = Node()
         c3 = Node()
         c1.add_neighbour(c2)
         c1.add_neighbour(c3)
         c1.remove_neighbour(c2)
         assert(c2 not in c1.neighbours())
         assert(c3 in c1.neighbours())
         assert(c1 not in c2.neighbours())

    def testRemoveAlreadyRemovedNode(self):
         c1 = Node()
         c2 = Node()
         c1.add_neighbour(c2)
         c1.remove_neighbour(c2)
         with self.assertRaises(NodeError):
             c1.remove_neighbour(c2)

    def testCellNeighbourGenerator(self):
         c1 = Node()
         neighbour_nodes = []
         for _ in range(10):
             c = Node()
             neighbour_nodes.append(c)
             c1.add_neighbour(c)

         for idx, neigbour in enumerate(c1.neighbours()):
             self.assertEquals(neigbour, neighbour_nodes[idx])




if __name__ == '__main__':
    unittest.main()
