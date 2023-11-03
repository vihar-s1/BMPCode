import random
import numpy as np

def getEntryExitLoc(n, N):
    totPairs = N * (N-1) / 2
    possiblities = N-1
    n_copy = n
    while possiblities <= n:
        n -= possiblities
        possiblities -= 1
    
    indexI = N-1-possiblities
    return indexI, indexI + n + 1
    
    

def calculatePressure(D: list[list[float]], L: list[list[float]], I0: float, n: int):
    N = len(D)
    entryExitPairs = N * (N-1) / 2
    netFlux = [[0]] * N
    
    x = [[-D[i][j]/L[i][j] for j in range(N)] for i in range(N)]
    for i in range(N):
        x[i][i] = -1 * sum(x[i])
    
    entry, exit = getEntryExitLoc(n, N)
    netFlux[entry][0], netFlux[exit][0] = I0, -I0
    
    pressure = np.linalg.inv(x) @ np.array(netFlux)
    return pressure.T.tolist()[0]
        

def ssm(L: list[list[float]], Tmax: int, N: int):
    entryExitPairs = N * (N-1) / 2
    
    # D[n][i][j] = conductivity for tube (i,j) in the nth subsystem
    D = [[[random.random() for i in range(N)] for j in range(N)] for n in range(entryExitPairs)]
    I0 = 5.0
    
    # Q[t][i][j] = net flux for tube (i,j) at t^th iteration
    Q = [[[0 for i in range(N)] for j in range(N)] for n in range(entryExitPairs)]
    
    for t in range (Tmax):
        for n in range(entryExitPairs):
            # calculate p^n(t) at each node
            pn = calculatePressure(D[n], L, I0, n)
            # obtain q^n_ij(t)
            # update conductivity D^n_ij
            pass
        # calculate Q_ij(t)
        
                