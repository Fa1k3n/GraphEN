#!/usr/bin/env python

import unittest
from node import *

class test_edge(unittest.TestCase):
    def testDefaultCreate(self):
        e = Edge(3, None, None)
        self.assertEqual(e.cost, 3)

    def testCostProperty(self):
        e = Edge(3, None, None)
        e.cost = 2
        self.assertEqual(e.cost, 2)
        with self.assertRaises(EdgeError):
            e.cost = -1

class test_cell(unittest.TestCase):

    def setUp(self):
        pass

    def testDefaultCreate(self):
        c = Node()
        self.assertEquals(c.get_cost(), 1)

    def testOverriddenCreate(self):
        c = Node(2)
        self.assertEquals(c.get_cost(), 2)

    def testChangeCost(self):
        c = Node(1)
        c.set_cost(3)
        self.assertEquals(c.get_cost(), 3)

    def testAddNeighbourNode(self):
        c1 = Node()
        c2 = Node()
        c1.add_neighbour(c2)
        neighbours = c1.get_neighbours()
        assert(c2 in neighbours)

    def testRemoveNeigbourNode(self):
        c1 = Node()
        c2 = Node()
        c3 = Node()
        c1.add_neighbour(c2)
        c1.add_neighbour(c3)
        c1.remove_neighbour(c2)
        neighbours = c1.get_neighbours()
        assert(c2 not in neighbours)
        assert(c3 in neighbours)

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
