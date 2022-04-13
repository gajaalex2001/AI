from graph import Graph
import random
import numpy


def updateGraph(g : Graph):
    a = numpy.array(g.mat)
    minval = numpy.min(a[numpy.nonzero(a)])
    maxval = numpy.max(a[numpy.nonzero(a)])
    for i in range((g.nrNoduri ** 2) // 2):
        linie = random.randint(0, g.nrNoduri - 1)
        coloana = random.randint(0, g.nrNoduri - 1)
        while coloana == linie:
            coloana = random.randint(0, g.nrNoduri - 1)
        num = random.randint(minval,maxval)
        g.mat[linie][coloana] = num
        g.mat[coloana][linie] = num
        g.feromon[linie][coloana] = 1 / g.nrNoduri ** 2
        g.feromon[coloana][linie] = 1 / g.nrNoduri ** 2
    return g

def readNet(fileName):
    f = open(fileName, "r")
    net = {}
    n = int(f.readline())
    net['noNodes'] = n
    mat = []
    for i in range(n):
        mat.append([])
        line = f.readline()
        elems = line.split(" ")
        for j in range(n):
            mat[-1].append(int(elems[j]))
    net["mat"] = mat
    degrees = []
    noEdges = 0
    for i in range(n):
        d = 0
        for j in range(n):
            if (mat[i][j] == 1):
                d += 1
            if (j > i):
                noEdges += mat[i][j]
        degrees.append(d)
    net["noEdges"] = noEdges
    net["degrees"] = degrees
    f.close()
    return net