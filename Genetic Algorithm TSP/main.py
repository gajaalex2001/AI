import os
import numpy as np
import networkx as nx
from fcOptimisation.geneticAlgorithm import *
from fcOptimisation.RealChromosome import *
from fcOptimisation.utils import generateARandomPermutation

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

def modularity(chromosome, net):
    noNodes = net['noNodes']
    mat = net['mat']
    degrees = net['degrees']
    noEdges = net['noEdges']
    M = 0
    for i in range(len(chromosome)-1):
        M = M + mat[chromosome[i]][chromosome[i+1]]
    return M


# load a network
crtDir = os.getcwd()
filePath = os.path.join(crtDir, 'data', 'p01.txt')
network = readNet(filePath)

# initialise de GA parameters
gaParam = {'popSize' : 200, 'noGen' : 300}
# problem parameters
problParam = {'start' : 2, 'noDim' : network['noNodes'], 'function' : modularity, 'network' : network}

ga = GA(gaParam, problParam)
ga.initialisation()
ga.evaluation()


for g in range (gaParam['noGen']):
    #ga.oneGeneration()
    ga.oneGenerationElitism()
    #ga.oneGenerationSteadyState()

bestChrom = ga.bestChromosome()
bestFitness = bestChrom.fitness

solutions = []
for sol in ga.population:
    if sol.fitness == bestFitness and sol not in solutions:
        solutions.append(sol)

print('Best solutions in generation ' + str(g) + ' are : ')

for sol in solutions:
    print(str(sol.repres) + ' f(x) = ' + str(sol.fitness))

