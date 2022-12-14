#########################################################
# 
# PART 2: COLOR GRAPHS
# 1. read from input file and create graph
# 2. color graphs
# 
#########################################################

from os import terminal_size
from pickle import FALSE
import graph
import re
import time

# read file and create graph
startTime = time.time()
inputFile = open('outputFile.txt', 'r')
inputFile.seek(0)

# get number vertices 
numberVertices = int(re.findall('\d+', inputFile.readline()).pop())
myGraph = graph.AdjacencyListGraph(numberVertices)

for i in range(numberVertices):
    inputFile.readline()

# fill in adjacent list for vertices
for i in range(numberVertices * 2):
    info = inputFile.readline()
    vertices = re.findall('\d+', info)
    vertex1 = int(vertices.pop())
    vertex2 = int(vertices.pop())
    myGraph.addEdge(vertex1, vertex2)

# verify graph output in outputfile2.txt
myGraph.printOutput2()
print('read and create graph ------ %s seconds -------' % (time.time() - startTime))


#########################################################
# 
# slvo coloring
# 
#########################################################

vertexDegrees = []
vertexDegreeWhenRemoved = []
unremovedVertices = []
vertexColors = []
colors = []
# push smallest degree vertex to this stack
smallestDegreeOrdering = []
terminalCliqueSize = 0
terminalCliqueElements = []
anArbitrayBigNumber = 99999 * numberVertices

# populate vertexDegrees
for i in range(numberVertices):
    vertexDegrees.append(myGraph.getOutdegree(i))
    # currently all vertices are unremoved, append vertex index
    unremovedVertices.append(i)
    # initialize with arbitrary value
    vertexDegreeWhenRemoved.append(-1)
    vertexColors.append(-1)

# populate smallest degree ordering
for i in range(numberVertices):
    # check if current graph is terminal clique
    # for computation speed, first check if vertex degrees are identical: highly increases likelihood of being terminal clique
    if(len(set(vertexDegrees)) == 1 + i): 
        # check if current graph is complete
        isCompleteGraph = False
        # get remaining vertices that have not been removed
        for unremovedVertex in unremovedVertices:
            for adjacentVertex in myGraph.getAdjacentVertices(unremovedVertex):
                if unremovedVertex in myGraph.getAdjacentVertices(adjacentVertex):
                    isCompleteGraph = True
                else:
                    isCompleteGraph = False
        # current graph is terminal clique, get clique size
        if(isCompleteGraph):
            terminalCliqueElements = unremovedVertices.copy()
            terminalCliqueSize = numberVertices - i

    # get smallest degree vertex
    smallestDegreeVertex = vertexDegrees.index(min(vertexDegrees))
    # push smallest degree vertex into stack, update unremovedVertices[]
    smallestDegreeOrdering.append(smallestDegreeVertex)
    unremovedVertices.remove(smallestDegreeVertex)
    # update vertex degrees
    for connectedVertex in myGraph.getAdjacentVertices(smallestDegreeVertex):
        vertexDegrees[connectedVertex] = vertexDegrees[connectedVertex] - 1
    # store info: vertex degree when removed
    vertexDegreeWhenRemoved[smallestDegreeVertex] = vertexDegrees[smallestDegreeVertex]
    # vertex in stack, remove from list; make processed vertex some big, arbitrary number
    vertexDegrees[smallestDegreeVertex] = anArbitrayBigNumber


# first color terminal clique elements
for i in range(terminalCliqueSize):
    # color vertices according to smallestDegreeOrdering
    vertexGettingColored = smallestDegreeOrdering.pop()
    vertexColors[vertexGettingColored] = i
    colors.append(i)

# color remaining elements
for i in range(numberVertices - terminalCliqueSize):
    # color vertices according to smallestDegreeOrdering
    vertexGettingColored = smallestDegreeOrdering.pop()
    vertexIsColored = False
    colorAvailable = False
    currentColor = -1

    for color in colors:
        if colorAvailable:
            vertexColors[vertexGettingColored] = currentColor
            vertexIsColored = True
            break
        # check if color is already taken by adjacent vertices
        for adjacentVertex in myGraph.getAdjacentVertices(vertexGettingColored):                
            if(vertexColors[adjacentVertex] == color):
                colorAvailable = False
                break
            else:
                colorAvailable = True
                currentColor = color                

    # color unavailable, create new color
    if (vertexIsColored == False):
        colors.append(len(colors))
        vertexColors[vertexGettingColored] = len(colors)
    
outputFile = open('coloringResults.txt', 'w')

outputFile.write("%d = number of vertices\n" % numberVertices)
outputFile.write("%d = number of colors used\n" % len(colors))
outputFile.write("%d = maximum degree when deleted\n" % max(vertexDegreeWhenRemoved))
outputFile.write("%d = size of terminal clique\n" % terminalCliqueSize)

for vertex in range(numberVertices):
    # this argument can't convert during formatting, so I convert it here
    outputFile.write("vertex %d: color %d, degree %d, degree when deleted %d\n" % (vertex, vertexColors[vertex], myGraph.getOutdegree(vertex), vertexDegreeWhenRemoved[vertex]))

outputFile.close()
