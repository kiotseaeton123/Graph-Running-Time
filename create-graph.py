
#########################################################
# 
# PART 1: CREATE CONFLICT GRAPHS
# uniform distribution for choosing graphs with conflicts/edges, using random() for pseudo-random number generation
# 
#########################################################

import graph
import time
import math
import random

numberVertices = 100
startTime = time.time()

myGraph = graph.AdjacencyListGraph(numberVertices)

# the number of edges is double that of vertices
for edge in range(numberVertices * 2):
    i = math.floor(random.random() * 100 % numberVertices)
    j = math.floor(random.random() * 100 % numberVertices)
    # vertex can't be adjacent to itself
    if(i != j): 
        myGraph.addEdge(i, j)

print('create graph ------ %s seconds -------' % (time.time() - startTime))
myGraph.printOutput()