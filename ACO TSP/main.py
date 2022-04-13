import os
from aco import ACO, Graph
from utils import readNet

crtDir = os.getcwd()
filePath = os.path.join(crtDir, 'data', 'ha30.txt')
network = readNet(filePath)

adiacenta = network['mat']
n = network['noNodes']

acoParams = {'noAnts': 20, 'noGen': 100, 'alpha': 1.0, 'beta': 5.0, 'evaporare': 0.4, 'feromon': 8}

aco = ACO(acoParams)

graph = Graph(adiacenta, n)
startNode = 2
path, cost = aco.solveDynamic(graph, startNode)
path.append(startNode)
print('cost: {}, path: {}'.format(cost, path))
