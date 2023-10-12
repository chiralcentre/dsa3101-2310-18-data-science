from collections import deque

#preconditions:
#1) graph must be directed acyclic
#2) adjList is a list of lists representing the graph in adjaceny list form
#3) indeg is a list of length V where indeg[v] represents the indegree of vertex v
#postconditions:
#1) indeg array is modified such that every entry is now 0
#2) returns an list of vertices in topological order
def kahnsAlgorithm(adjList,indeg):
    frontier = deque([])
    for v in range(len(indeg)):
        if indeg[v] == 0:
            frontier.append(v)
    toposort = []
    while frontier:
        u = frontier.popleft()
        toposort.append(u)
        for v in adjList[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                frontier.append(v)
    return toposort    