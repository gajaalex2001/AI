import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import warnings
import random
from fcOptimisation.geneticAlgorithm import *
from fcOptimisation.RealChromosome import *

from networkx.algorithms import community

warnings.simplefilter('ignore')


# read the network details
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


# read the network details (from a GML file)
def readGML(fileName):
    net = {}
    G = nx.read_gml(fileName)
    n = len(G.nodes)
    m = len(G.edges)
    net['noNodes'] = n
    net['noEdges'] = m
    mat = np.zeros((n, n))
    for el in (list(G.edges)):
        l = list(G.nodes).index(el[0])
        c = list(G.nodes).index(el[1])
        mat[l][c] = 1
        mat[c][l] = 1

    net['mat'] = mat
    degrees = []
    noEdges = 0
    for i in range(net['noNodes']):
        d = 0
        for j in range(net['noNodes']):
            if (mat[i][j] == 1):
                d += 1
            if (j > i):
                noEdges += mat[i][j]
        degrees.append(d)
    net['degrees'] = degrees
    return net


# plot a network
def plotNetwork(network, communities=[1, 1, 1, 1, 1, 1]):
    np.random.seed(123)  # to freeze the graph's view (networks uses a random view)
    A = np.matrix(network["mat"])
    G = nx.from_numpy_matrix(A)
    pos = nx.spring_layout(G)  # compute graph layout
    plt.figure(figsize=(4, 4))  # image is 8 x 8 inches
    nx.draw_networkx_nodes(G, pos, node_size=600, cmap=plt.cm.RdYlBu, node_color=communities)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.show()


# /////////////////////////////////////////////////////////////////////////////////////


def modularity(chromosome, net):
    noNodes = net['noNodes']
    mat = net['mat']
    degrees = net['degrees']
    noEdges = net['noEdges']
    M = 2 * noEdges
    Q = 0.0
    for i in range(0, noNodes):
        for j in range(0, noNodes):
            if (chromosome[i] == chromosome[j]):
               Q += (mat[i][j] - degrees[i] * degrees[j] / M)
    return Q * 1 / M


# load a network
crtDir = os.getcwd()
filePath = os.path.join(crtDir, 'data', 'dolphins.gml')
network = readGML(filePath)


# initialise de GA parameters
gaParam = {'popSize' : network['noNodes'], 'noGen' : 300}
# problem parameters
problParam = {'min' : 1, 'max' : 3, 'noDim' : network['noNodes'], 'function' : modularity, 'network' : network}

ga = GA(gaParam, problParam)
ga.initialisation()
ga.evaluation()

for g in range (gaParam['noGen']):
    #ga.oneGeneration()
    ga.oneGenerationElitism()
    #ga.oneGenerationSteadyState()

bestChrom = ga.bestChromosome()
print('Best solution in generation ' + str(g) + ' is: x = ' + str(bestChrom.repres) + ' f(x) = ' + str(bestChrom.fitness))

plotNetwork(network, bestChrom.repres)
