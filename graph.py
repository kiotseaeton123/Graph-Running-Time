import abc
import time
import random
import math

#########################################################
# 
# base Graph class will have all interface methods
# 
#########################################################

class Graph(abc.ABC):
    def __init__(self, numberVertices, isDirected = False) -> None:
        self.numberVertices = numberVertices
        self.isDirected = isDirected

    @abc.abstractmethod
    def addEdge(self, v1, v2):
        pass

    @abc.abstractmethod
    def getAdjacentVertices(self, v):
        pass

    @abc.abstractmethod
    def getIndegree(self, v):
        pass

    @abc.abstractmethod
    def print(self):
        pass

#########################################################
# 
# Node class contains list of adjacent vertices
# Using adjacency 'set' allows one single representation for a particular graph
# 
#########################################################
class Node:
    def __init__(self, vertexId) -> None:
        self.vertexId = vertexId
        self.adjacencyList = set()

    def addEdge(self, v):
        if self.vertexId == v:
            raise ValueError('vertex %d can not be adjacent to itself' % v)
            return
        
        self.adjacencyList.add(v)

    def getAdjacentVertices(self):
        return sorted(self.adjacencyList)

#########################################################
# 
# AdjacencyList(set) representation of graph 
# 
#########################################################
class AdjacencyListGraph(Graph):
    def __init__(self, numberVertices, isDirected=False) -> None:
        super(AdjacencyListGraph, self).__init__(numberVertices, isDirected)

        # set up all vertices as a Node
        self.vertexList = []
        for i in range(numberVertices):
            self.vertexList.append(Node(i))

    def addEdge(self, v1, v2):
        if v1 < 0 or v2 < 0 or v1 >= self.numberVertices or v2 >= self.numberVertices:
            raise ValueError('vertices %d and %d out of bound' % (v1, v2))

        # if edge doesn't exist already
        self.vertexList[v1].addEdge(v2)
        # undirected graph, add edge the other way as well
        self.vertexList[v2].addEdge(v1)

    def getAdjacentVertices(self, v):
        if v < 0 or v >= self.numberVertices:
            raise ValueError('vertex %d is out of bounds' % v)

        return self.vertexList[v].getAdjacentVertices()

    def getIndegree(self, v):
        if v < 0 or v >= self.numberVertices:
            raise ValueError('vertex %d is out of bounds' % v)

        indegree = 0
        for i in range(self.numberVertices):
            if v in self.getAdjacentVertices(i):
                indegree = indegree + 1

        return indegree

    def print(self):
        outputFile = open('outputFile.txt', 'w')
        outputFile.write("%d = number of vertices\n" % len(self.vertexList))

        for i in range(self.numberVertices):
            outputFile.write("%d = starting index for vertex %d\n" % (i, i))

        for i in range(self.numberVertices):
            for j in self.getAdjacentVertices(i):
                outputFile.write("%d is adjacent to %d\n" % (i, j))

        outputFile.close()

#########################################################
# 
# main
# uniform distribution for choosing graphs with conflicts/edges, using random() for pseudo random number generation
# 
#########################################################
# Note: timing data only works when doing one graph at a time despite using different variables for time(). Before running code, comment out one of the graphs inside of main

numberVertices = 10000

# 
# complete undirected graph
# 
startTime = time.time()

myGraph = AdjacencyListGraph(numberVertices)

for edge in range(numberVertices):
    i = math.floor(random.random() * 10)
    j = math.floor(random.random() * 10)
    # vertex can't be adjacent to itself
    if(i != j): 
        myGraph.addEdge(i, j)

print('complete graph ------ %s seconds -------' % (time.time() - startTime))

myGraph.print()
