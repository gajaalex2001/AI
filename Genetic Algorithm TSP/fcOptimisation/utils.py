from random import randint, seed

def generateARandomPermutation(n, start):
    perm = [i for i in range(n)]
    pos1 = randint(0, n - 1)
    pos2 = randint(0, n - 1)
    perm[pos1], perm[pos2] = perm[pos2], perm[pos1]
    for i in range(n):
        if perm[i] == start:
            perm[0], perm[i] = perm[i], perm[0]
    perm.append(start)
    return perm