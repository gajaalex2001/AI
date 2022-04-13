from random import randint
from fcOptimisation.utils import generateARandomPermutation
import numpy as np
import collections

class Chromosome:
    def __init__(self, problParam=None):
        self.__problParam = problParam
        self.__repres = generateARandomPermutation(problParam['noDim'], problParam['start'])
        self.__fitness = 0.0

    @property
    def repres(self):
        return self.__repres

    @property
    def fitness(self):
        return self.__fitness

    @repres.setter
    def repres(self, l=[]):
        self.__repres = l

    @fitness.setter
    def fitness(self, fit=0.0):
        self.__fitness = fit

    def crossover(self, c):
        newrepres = []
        a1 = np.array(c.__repres)
        a2 = np.array(self.repres)
        newrepres = list(a1[a2])

        for i in range(len(newrepres)):
            if newrepres[i] == self.__problParam['start']:
                newrepres[0], newrepres[i] = newrepres[i], newrepres[0]
                break

        duplicate = [item for item, count in collections.Counter(newrepres).items() if count > 1][0]

        for j in range(len(newrepres)):
            if newrepres[j] == duplicate:
                newrepres[j] = self.__problParam['start']
                newrepres[j], newrepres[len(newrepres)-1] = newrepres[len(newrepres)-1], newrepres[j]
                break

        offspring = Chromosome(c.__problParam)
        offspring.repres = list(newrepres)
        return offspring

    def mutation(self):
        pos1 = randint(1, len(self.__repres) - 2)
        pos2 = randint(1, len(self.__repres) - 2)
        while pos2 == pos1:
            pos2 = randint(1, len(self.__repres) - 2)
        self.__repres[pos1], self.__repres[pos2] = self.__repres[pos2], self.__repres[pos1]

    def __str__(self):
        return '\nChromo: ' + str(self.__repres) + ' has fit: ' + str(self.__fitness)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, c):
        return self.__repres == c.__repres and self.__fitness == c.__fitness