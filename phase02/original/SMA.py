import numpy as np
import argparse
from os import path
from datetime import datetime
from math import exp

from utils import readPoints


class SlimeMould:
    def __init__(self, points: np.ndarray, startPoint: int, endPoint: int, intialConductivity: float, totalFlux: float) -> None:
        self.points = points
        self.totalPoints = len(points)
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.totalFlux = totalFlux
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
        
        self.pressure = netFlux @ np.linalg.inv(self.pressureCoeff)
    
    
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
            
    
    def simulate(self, maxIterations: int, fluxInfluence: float, minContractionRate: float, maxContractionRate: float, transitionRate: float) -> None:
        T = maxIterations / 3
        for t in range(maxIterations):
            self.calculatePressure()
            self.calculateFlux()
            
            # gamma = a[ 1 - 1/[a/(a-b) + (ce)^(T-t)] ]
            contractionRate = minContractionRate * ( 1 - (minContractionRate/(maxContractionRate-minContractionRate) +  (transitionRate * exp(T - t)))**-1 )
            self.updateConductivity(contractionRate, fluxInfluence)


def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",dest="filename",help="Filepath for the file containing city coordinates",required=True)
    parser.add_argument("--debug",dest="debug",action="store_true",help="Flag to enable print statements")
    # parser.add_argument("--saveplot", dest="saveplot", help="Save plots instead of displaying them")
    # parser.add_argument("--iterationplot",dest="plotIterations",help="Save plot of optimal path length vs iterations")

    args = parser.parse_args()

    if not path.isfile(args.filename):
        print(f"{args.filename}: File Does Not Exist!")

    points = readPoints(args.filename)
    
    sma = SlimeMould(points, 0, len(points)-1, 10.0, 200.0)
    sma.simulate(100, 10.5, 0.2, 0.7, 1.2)
    

if __name__ == "__main__":
    __main__()