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
        n = g.add_vertex()
        self.assertEquals(g._vertex_count, 1)
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
        g.del_vertex(n)
        self.assertEquals(g._vertex_count, 0)
        self.assertTrue(n not in g._vertices.keys())
        self.assertEquals(len(g._vertices.keys()), 0)

    def testRemoveVertexShouldRemoveAllEdgesToIt(self):
        g = Graph()
        for i in range(3):
            g.add_vertex(Vertex(str(i+1)))
        g.add_edge("1", "2")
        g.add_edge("2", "3")
        g.add_edge("3", "1")
        self.assertTrue(("1", "2") in g)
        g.del_vertex("2")
        self.assertFalse(("1", "2") in g)
        self.assertFalse(("2", "1") in g)
        self.assertFalse(("3", "2") in g)
        self.assertTrue(("1", "3") in g)
        self.assertEqual(g._edge_count, 1)


    def testAddExistingVertexShouldRaiseGraphError(self):
        g = Graph()
        v = Vertex()
        g.add_vertex(v)
        with self.assertRaises(GraphError):
            g.add_vertex(v)

    def testRemoveNonExistingVertexShouldRaiseGraphError(self):
        g = Graph()
        n = Vertex()
        g.add_vertex(n)
        g.del_vertex(n)
        with self.assertRaises(GraphError):
            g.del_vertex(n)
        self.assertEquals(g._vertex_count, 0)

    def testAddSeveralVerticesAndEdges(self):
        g = Graph()
        v1 = Vertex("Vert 1")
        v2 = Vertex("Vert 2")
        g.add_vertex(v1, v2)
        e1 = Edge("Edge 1", 2)
        g.add_edge("Vert 1", v2, e1)
        self.assertEquals(g._vertex_count, 2)
        self.assertEquals(g._edge_count, 1)
        # Check both ways to adress a vertex, both via reference and via name
        self.assertTrue(v1 in g)
        self.assertTrue("Vert 2" in g)
        # Chaeck that they have been added to the graph correctly
        self.assertTrue((v1, e1) in g._vertices[v2])
        self.assertTrue((v2, e1) in g._vertices[v1])
        # Check that the cost between the nodes are correct, test that the different
        # test that the different adressing modes id/label works
        self.assertTrue(g.edge("Edge 1").cost == 2)

    def testAddSeveralVerticeasAndEdgesAgain(self):
        g = Graph("My Graph")
        g.add_vertex(Vertex("V1"), Vertex("V2"), Vertex("V3"))
        g.add_edge("V1", "V4", Edge("V1<->V4", 2))
        g.add_edge("V1", "V3", Edge("V1<->V3", 2))
        g.add_edge("V2", "V3", Edge("V2<->V3", 4))

        self.assertTrue(g.edge("V2<->V3").cost == 4)


if __name__ == '__main__':
    unittest.main()
