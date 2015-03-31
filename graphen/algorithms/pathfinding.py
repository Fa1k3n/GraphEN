import Queue
import time

class AlgObj(object):

    def __init__(self, graph):
        self._graph = graph
        self._came_from = {}
        self.closedset = []
        self.openset = Queue.PriorityQueue()
        self.path = []

    def shortest_path(self, start, goal): pass

    def visited(self):
        return self.closedset

    def fringe(self):
        return self.openset.queue

    def effort(self, n): pass

    def reconstruct_path(self, start, goal):
        curr = goal
        shortest_path = []

        while curr != start:
            shortest_path.append(curr)
            curr = self._came_from[curr]

        shortest_path.append(start)
        return list(reversed(shortest_path))


class Djikstra(AlgObj):
    def __init__(self, graph):
        super(Djikstra, self).__init__(graph)
        self.g_score = {}
        self.f_score = {}
        self.dist = lambda x,y : 0
        self.time = 0

    def shortest_path(self, start, goal):
        t1 = time.clock()
        r = self._shortest_path(start, goal)
        self.time = time.clock() - t1

    def _shortest_path(self, start, goal):
        self.openset.put((0, start))
        self.f_score = {}
        self.g_score[start] = 0
        self.f_score[start] = self.g_score[start] + self.dist(start, goal)

        while not self.openset.empty():

            (score, current) = self.openset.get()

            if current == goal:
                # Found path
                self.path = self.reconstruct_path(start, goal)
                return True

            self.closedset.append(current)

            for (vert, edge) in self._graph.neighbours(current):
                if vert in self.closedset:
                    continue
                tentative_g_score = self.g_score[current] + edge.cost

                in_open_set = False
                for (cost, node) in self.openset.queue:
                    if vert == node:
                        in_open_set = True
                        break

                if not in_open_set or tentative_g_score < self.g_score[vert]:
                    #edge.end_node._parent_cell = current
                    self._came_from[vert] = current
                    self.g_score[vert] = tentative_g_score
                    self.f_score[vert] = self.g_score[vert] + self.dist(vert, goal)
                    if not in_open_set:
                        self.openset.put((self.f_score[vert], vert))
        # No path
        raise graphen.GraphError("No path found")

    def effort(self, node=None):
        if node == None:
            node = self._graph.get_cell(self.path[-1])
        return self.g_score[node]

# AStar is a Djikstra with a distance function
class AStar(Djikstra):
    def __init__(self, graph, dist):
        super(AStar, self).__init__(graph)
        self.dist = self.cached_dist
        self.dist_cache = {}

    """
    A very simple distance caching mechanism so that each node only need to
    do an expencive sqrt calculation onece

    Early measurements:
        0.0561 - vert, not cached
        0.0787 - hori, not cached
        0.7050 - diag, not cached

        0.0606 - vert, cached
        0.0745 - hori, cached
        0.4604 - diag, cached
    """
    def cached_dist(self, start, end):
        if start not in self.dist_cache:
            self.dist_cache[start] = self._graph.dist(start, end)
        return self.dist_cache[start]