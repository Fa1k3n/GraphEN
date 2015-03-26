#!/usr/bin/env python

import unittest
from node import *

class test_graph(unittest.TestCase):
    def testGraphCreation(self):
        g = Graph()
        self.assertIsNot(g, None)
        g = Graph("The First Graph")
        self.assertEquals(g.name, "The First Graph")

    def testGraphAddAVertex(self):
        g = Graph()
        n = Vertex()
        g.add_vertex(n)
        self.assertEquals(g._vertex_count, 1)
        self.assertTrue(n in g._vertices.keys())
        self.assertEquals(len(g._vertices[n]), 0)

    def testAddExistingVertexShouldRaiseGraphError(self):
        g = Graph()
        n = Vertex()
        g.add_vertex(n)
        with self.assertRaises(GraphError):
            g.add_vertex(n)
        self.assertEquals(g._vertex_count, 1)

    def testGraphRemoveVertex(self):
        g = Graph()
        n = Vertex()
        g.add_vertex(n)
        g.rem_vertex(n)
        self.assertEquals(g._vertex_count, 0)
        self.assertTrue(n not in g._vertices.keys())
        self.assertEquals(len(g._vertices.keys()), 0)

    def testRemoveNonExistingVertexShouldRaiseGraphError(self):
        g = Graph()
        n = Vertex()
        g.add_vertex(n)
        g.rem_vertex(n)
        with self.assertRaises(GraphError):
            g.rem_vertex(n)
        self.assertEquals(g._vertex_count, 0)

    def testAddSeveralVerticesAndEdges(self):
        g = Graph()
        n1 = Vertex("Node 1")
        n2 = Vertex("Node 2")
        g.add_vertex(n1, n2)
        g.add_edge(n1, n2, Edge(2, "Test edge"))
        self.assertEquals(g._vertex_count, 2)
        self.assertEquals(g._edge_count, 1)
        self.assertTrue("Node 1" in g._vertices.keys())
        self.assertTrue("Node 2" in g._vertices.keys())
        self.assertTrue("Node 1" in g._vertices["Node 2"])
        self.assertTrue("Node 2" in g._vertices["Node 1"])


if __name__ == '__main__':
    unittest.main()
