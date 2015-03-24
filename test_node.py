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

class test_graph(unittest.TestCase):
    def testGraphCreation(self):
        g = Graph()
        self.assertIsNot(g, None)
        g = Graph("The First Graph")
        self.assertEquals(g.name, "The First Graph")

    def testGraphAddAVertex(self):
        g = Graph()
        n = Node()
        g.add_vertex(n)
        self.assertEquals(g._vertex_count, 1)
        self.assertTrue(n in g._vertices.keys())
        self.assertEquals(len(g._vertices[n]), 0)

    def testAddExistingVertexShouldRaiseGraphError(self):
        g = Graph()
        n = Node()
        g.add_vertex(n)
        with self.assertRaises(GraphError):
            g.add_vertex(n)
        self.assertEquals(g._vertex_count, 1)

    def testGraphRemoveVertex(self):
        g = Graph()
        n = Node()
        g.add_vertex(n)
        g.rem_vertex(n)
        self.assertEquals(g._vertex_count, 0)
        self.assertTrue(n not in g._vertices.keys())
        self.assertEquals(len(g._vertices.keys()), 0)

    def testRemoveNonExistingVertexShouldRaiseGraphError(self):
        g = Graph()
        n = Node()
        g.add_vertex(n)
        g.rem_vertex(n)
        with self.assertRaises(GraphError):
            g.rem_vertex(n)
        self.assertEquals(g._vertex_count, 0)



if __name__ == '__main__':
    unittest.main()
