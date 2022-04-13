import random
from utils import updateGraph
from graph import Graph
import numpy as np


class ACO:
    def __init__(self, acoParams):
        self.acoParams = acoParams

    def updatePheromone(self, graph, ants):
        for i in range(graph.nrNoduri):
            for j in range(graph.nrNoduri):
                graph.feromon[i][j] = graph.feromon[i][j] * self.acoParams['evaporare']
                for ant in ants:
                    graph.feromon[i][j] = graph.feromon[i][j] + ant.feromonDepus[i][j]

    def solveStatic(self, graph: Graph, startNode):
        bestCost = float('inf')
        bestAnt = []
        for gen in range(self.acoParams['noGen']):
            ants = [Ant(self, graph, startNode) for i in range(self.acoParams['noAnts'])]
            for ant in ants:
                for i in range(graph.nrNoduri - 1):
                    ant.nextNode()
                ant.totalCost += graph.mat[ant.visited[-1]][ant.visited[0]]
                if ant.totalCost < bestCost:
                    bestCost = ant.totalCost
                    bestAnt = [] + ant.visited

                ant.updateFeromonDepus()
            self.updatePheromone(graph, ants)

        return bestAnt, bestCost

    def solveDynamic(self, graph: Graph, startNode):
        count = 1
        bestCost = float('inf')
        bestAnt = []
        for gen in range(self.acoParams['noGen']):
            count += 1

            ants = [Ant(self, graph, startNode) for i in range(self.acoParams['noAnts'])]
            for ant in ants:
                for i in range(graph.nrNoduri - 1):
                    ant.nextNode()
                ant.totalCost += graph.mat[ant.visited[-1]][ant.visited[0]]
                if ant.totalCost < bestCost:
                    bestCost = ant.totalCost
                    bestAnt = [] + ant.visited

                ant.updateFeromonDepus()
            self.updatePheromone(graph, ants)
            graph = updateGraph(graph)
            if count % 10 == 0:
                graph = updateGraph(graph)
        return bestAnt, bestCost


class Ant:
    def __init__(self, aco: ACO, graph: Graph, startNode):
        self.aco = aco
        self.graph = graph
        self.totalCost = 0.0
        self.visited = []
        self.feromonDepus = []
        self.notVisited = [i for i in range(graph.nrNoduri)]
        self.distanta = [[0 if i == j else 1 / graph.mat[i][j] for j in range(graph.nrNoduri)] for i in
                         range(graph.nrNoduri)]

        self.visited.append(startNode)
        self.current = startNode
        self.notVisited.remove(startNode)

    def nextNode(self):
        numitor = 0
        for i in self.notVisited:
            feromon = self.graph.feromon[self.current][i] ** self.aco.acoParams['alpha']
            distanta = self.distanta[self.current][i] ** self.aco.acoParams['beta']
            numitor += feromon * distanta

        probabilitati = [0] * self.graph.nrNoduri
        for i in range(self.graph.nrNoduri):
            if i in self.notVisited:
                feromon = self.graph.feromon[self.current][i] ** self.aco.acoParams['alpha']
                distanta = self.distanta[self.current][i] ** self.aco.acoParams['beta']
                probabilitati[i] = feromon * distanta / numitor

        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilitati):
            rand -= probability
            if rand <= 0:
                selected = i
                break

        self.updateVisited(selected)


    def updateFeromonDepus(self):
        self.feromonDepus = np.zeros((self.graph.nrNoduri, self.graph.nrNoduri))
        for x in range(len(self.visited)-1):
            i = self.visited[x]
            j = self.visited[x + 1]
            self.feromonDepus[i][j] = self.aco.acoParams['feromon']
            self.feromonDepus[j][i] = self.aco.acoParams['feromon']

    def updateVisited(self, index):
        self.notVisited.remove(index)
        self.visited.append(index)
        self.totalCost += self.graph.mat[self.current][index]
        self.current = index