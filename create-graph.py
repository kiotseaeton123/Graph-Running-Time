
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

numberVertices = 10000

# 
# complete undirected graph
# 
startTime = time.time()

myGraph = graph.AdjacencyListGraph(numberVertices)

for edge in range(numberVertices):
    i = math.floor(random.random() * 10)
    j = math.floor(random.random() * 10)
    # vertex can't be adjacent to itself
    if(i != j): 
        myGraph.addEdge(i, j)

print('complete graph ------ %s seconds -------' % (time.time() - startTime))
myGraph.print()