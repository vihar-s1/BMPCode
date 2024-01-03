import numpy as np
import argparse
from os import path
from datetime import datetime
from math import exp

from utils import readPoints, plotweights, printMatrix


def gammaFunc(a: float, b: float, c: float, T: int, t: int) -> float:
    return a * (1 - ( a/(a-b) + (c*exp(1))**(T-t) )**-1)

def getRowToDelete(matrix: np.ndarray, startPoint: int, endPoint: int) -> int:
    totalPoints = np.size(matrix, 1)
    
    for deleteRow in range(totalPoints):
        if deleteRow in [startPoint, endPoint]: continue
        newMat = np.delete(matrix, deleteRow, 0)
        if np.linalg.det(newMat) != 0:
            return deleteRow
    
    return startPoint

class PressureCoeffSingular(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class SlimeMould:
    def __init__(self, points: np.ndarray, startPoint: int, endPoint: int, intialConductivity: float, totalFlux: float, distanceMatrix: np.ndarray=None) -> None:
        self.points = points
        self.totalPoints = len(points)
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.totalFlux = totalFlux
        self.distance = distanceMatrix
        if distanceMatrix is None:
            self.distance = np.ones((self.totalPoints, self.totalPoints), dtype=np.float64)
            self.distance = np.ones((self.totalPoints, self.totalPoints), dtype=np.float64)
        
            self.distance = np.ones((self.totalPoints, self.totalPoints), dtype=np.float64)
        
            for i in range(self.totalPoints):
                for j in range(self.totalPoints):
                    self.distance[i, j] = np.sqrt(np.sum((points[i] - points[j]) ** 2))
        
        self.conductivity = np.ones((self.totalPoints, self.totalPoints), dtype=np.float64) * intialConductivity
        
    
    def calculatePressure(self) -> None:
        # Calculating Pressure at each Node
        for i in range(self.totalPoints): self.distance[i][i] = 1
        
        # Element-wise division to obtain Dij/Lij
        self.pressureCoeff = self.conductivity / self.distance
        
        for i in range(self.totalPoints):
            self.distance[i][i] = 0
            self.pressureCoeff[i][i] = 0
        
        for i in range(self.totalPoints):
            self.pressureCoeff[i][i] -= sum(self.pressureCoeff[i])
        
        netFlux = np.zeros(self.totalPoints)
        netFlux[self.startPoint] = -self.totalFlux
        netFlux[self.endPoint] = self.totalFlux
    
        self.pressure = np.linalg.lstsq(self.pressureCoeff, netFlux, rcond=None)[0]
            
    
    def calculateFlux(self) -> None:
        # Qij = (Dij/Lij) * (pi - pj) 
        self.flux = np.zeros((self.totalPoints, self.totalPoints))
        for i in range(self.totalPoints):
            for j in range(self.totalPoints):
                if i == j: continue
                self.flux[i][j] = self.conductivity[i][j] * (self.pressure[i] - self.pressure[j]) / self.distance[i][j]
        
        
    def updateConductivity(self, contractionRate: float, fluxInfluence: float) -> None:
        # Dij = mu * Qij + (1 - gamma) * Dij
        self.conductivity = fluxInfluence * self.flux + (1 - contractionRate) * self.conductivity
            
    
    def simulate(self, maxIterations: int, fluxInfluence: float, minContractionRate: float, maxContractionRate: float, transitionRate: float, debug: bool=False) -> None:
        T = maxIterations / 3
        if debug: print("Initiating Simulation...")
        for t in range(maxIterations):
            if debug: print(f"Iteration No. {t}")
            self.calculatePressure()
            self.calculateFlux()
            
            # gamma = a[ 1 - 1/[a/(a-b) + (ce)^(T-t)] ]
            contractionRate = gammaFunc(minContractionRate, maxContractionRate, transitionRate, T, t)
            self.updateConductivity(contractionRate, fluxInfluence)
            print(f"Total Node Flux: {self.flux.sum()}")
                


class MultiStateSlimeMould:
    def __init__(self, points: np.ndarray) -> None:
        self.points = points
        self.totalPoints = len(points)
        self.distance = np.ones((self.totalPoints, self.totalPoints), dtype=np.float64)
        
        # Pre-calculating distance matrix
        for i in range(self.totalPoints):
            for j in range(self.totalPoints):
                self.distance[i, j] = np.sqrt(np.sum((points[i] - points[j]) ** 2))
        
                
    def setupSimulation(self, maxIterations: int, initialConductivity: float, totalFlux: float, fluxInfluence: float, minContractionRate: float, maxContractionRate: float, transitionRate: float):
        self.maxIterations, self.iterationCleared = maxIterations, 0
        self.initialConductivity = initialConductivity
        self.totalFlux, self.fluxInfluence = totalFlux, fluxInfluence
        self.minContractionRate, self.maxContractionRate = minContractionRate, maxContractionRate
        self.transitionRate = transitionRate
        
        self.subSystems = list[SlimeMould]()
        for i in range(self.totalPoints):
            for j in range(self.totalPoints):
                if i == j: continue
                self.subSystems.append(SlimeMould(self.points, i, j, initialConductivity, totalFlux, self.distance))
        
        # Qij(t) = sum^{N(N-1)/2}_{k=1} (Qij^m(t))
        self.netEdgeFlux = np.zeros((self.totalPoints, self.totalPoints), dtype=np.float64)
    
    
    def nextIteration(self, debug:bool=False) -> bool:
        # Simulate next Slime Mold Iteration for all subsystems
        if self.iterationCleared >= self.maxIterations: return False
        
        self.netEdgeFlux = np.zeros((self.totalPoints, self.totalPoints))
        for i in range(len(self.subSystems)):
            self.subSystems[i].calculatePressure()
            self.subSystems[i].calculateFlux()
            
            # gamma =  a[1 - 1/[a/(a-b) + (ce^(T-t))]]
            contractionRate = gammaFunc(self.minContractionRate, self.maxContractionRate, self.transitionRate, self.maxIterations/3, self.iterationCleared)
            self.subSystems[i].updateConductivity(contractionRate, self.fluxInfluence)
        
            # Update the netEdgeFlux
            # Qij(t) = sum^{N(N-1)/2}_{k=1} (Qij^m(t))
            self.netEdgeFlux += self.subSystems[i].flux
            if self.subSystems[i].flux.shape != (self.totalPoints, self.totalPoints):
                print(f"({self.subSystems[i].startPoint}, {self.subSystems[i].endPoint}): Size note matching: size = {self.subSystems[i].flux.shape}, expected = ({self.totalPoints}, {self.totalPoints})")
        
        self.iterationCleared += 1
        return True
    
    
    def simulate(self, maxIterations: int, initialConductivity: float, totalFlux: float, fluxInfluence: float, minContractionRate: float, maxContractionRate: float, transitionRate: float, debug: bool):
        if debug: print("Initiating Simulation Setup...")
        self.setupSimulation(maxIterations, initialConductivity, totalFlux, fluxInfluence, minContractionRate, maxContractionRate, transitionRate)
        T = maxIterations / 3
        
        if debug: print("Initiating Simulation...")
        while self.nextIteration(debug):
            if debug: print("Iterations Cleared:", self.iterationCleared)


def __SlimeMoldSim__():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",dest="filename",help="Filepath for the file containing city coordinates",required=True)
    parser.add_argument("--debug",dest="debug",action="store_true",help="Flag to enable print statements")
    # parser.add_argument("--saveplot", dest="saveplot", help="Save plots instead of displaying them")
    # parser.add_argument("--iterationplot",dest="plotIterations",help="Save plot of optimal path length vs iterations")

    args = parser.parse_args()

    if not path.isfile(args.filename):
        print(f"{args.filename}: File Does Not Exist!")

    points = readPoints(args.filename)
    
    start = datetime.now()
    sma = SlimeMould(points, 0, len(points)-1, 100.0, 200.0)
    sma.simulate(1000, 10.5, 0.2, 0.7, 1.2, args.debug)
    end = datetime.now()
    print(end - start)
    
    flux = sma.flux
    print(flux.sum())
    plotweights(points, sma.flux, 10, sma.startPoint, sma.endPoint)


def __SSMSim__():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",dest="filename",help="Filepath for the file containing city coordinates",required=True)
    parser.add_argument("--debug",dest="debug",action="store_true",help="Flag to enable print statements")
    # parser.add_argument("--saveplot", dest="saveplot", help="Save plots instead of displaying them")
    # parser.add_argument("--iterationplot",dest="plotIterations",help="Save plot of optimal path length vs iterations")

    args = parser.parse_args()

    if not path.isfile(args.filename):
        print(f"{args.filename}: File Does Not Exist!")

    points = readPoints(args.filename)
    
    start = datetime.now()
    mssm = MultiStateSlimeMould(points)
    mssm.simulate(100, 100.0, 200.0, 10.5, 0.2, 0.7, 1.2, args.debug)
    end = datetime.now()
    print(end - start)
    
    print(mssm.netEdgeFlux.sum())
    plotweights(points, mssm.netEdgeFlux, 10, 0, 0)
    

if __name__ == "__main__":
    __SlimeMoldSim__()
    # __SSMSim__()