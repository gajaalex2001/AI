class Graph:
    def __init__(self, adiacenta, n):
        self.mat = adiacenta
        self.nrNoduri = n
        self.feromon = [[1 / (n * n) for j in range(n)] for i in range(n)]