import numpy as np
import argparse
from os import path
from datetime import datetime

from utils import readCities, plotPath, savePlot

class Ant:
    def __init__(self, startPoint: int, totalPoints: int) -> None:
        self.currentPoint = startPoint
        self.visited = [False] * totalPoints
        self.visited[startPoint] = True
        self.path = [ startPoint ]
        # self.pathLength = 0.0
        self.totalPoints = totalPoints
        
    def istourCompleted(self) -> bool:
        return len(self.path) == self.totalPoints
    
    def nextPoint(self, newPoint: int) -> bool:
        if self.visited[newPoint] or self.istourCompleted():
            return False
        self.path.append(newPoint)
        self.visited[newPoint] = True
        self.currentPoint = newPoint
        return True
    
    def returnHome(self) -> bool:
        if self.istourCompleted():
            self.path.append(self.path[0])
            return True
        return False
    
    def calculatePathLength(self, distance: np.ndarray[np.float64]) -> float: # type: ignore
        self.pathLength = 0.0
        
        for i in range(1, len(self.path)):
            self.pathLength += distance[self.path[i-1], self.path[i]]
        
        return self.pathLength
    
    
class AntSystem:
    def __init__(self, antCount: int, points: np.ndarray, initialPheromones: float=1.0) -> None:
        self.totalPoints = len(points)
        self.antCount = antCount
        self.points = points
        
        self.pheromones = np.ones((self.totalPoints, self.totalPoints), dtype=np.float64) * initialPheromones
        self.distance = np.ones((self.totalPoints, self.totalPoints), dtype=np.float64)
        for i in range(self.totalPoints):
            for j in range(self.totalPoints):
                self.distance[i,j] = np.sqrt( np.sum( (points[i] - points[j])**2 ) )
        
        self.bestPath = None
        self.bestPathLength = np.inf
        
    def initializeAntPopulation(self) -> None:
        self.population = [Ant(np.random.randint(self.totalPoints), self.totalPoints) for _ in range(self.antCount)]
        
    def constructRoutes(self, alpha: float, beta: float):
        for ant in range(self.antCount):
            while not self.population[ant].istourCompleted():
                unvisited = np.where(np.logical_not(self.population[ant].visited))[0]
                currentPoint = self.population[ant].currentPoint
                
                transitionProb = np.zeros(len(unvisited), dtype=np.float64)
                for i, point in enumerate(unvisited):
                    transitionProb[i] = ( self.pheromones[currentPoint, point] ** alpha ) / ( self.distance[currentPoint, point] ** beta )
                
                transitionProb /= np.sum(transitionProb)
                nextPoint = np.random.choice(unvisited, p=transitionProb)
                self.population[ant].nextPoint(nextPoint)
            
            # returning home/starting-point
            self.population[ant].returnHome()
            
            pathLength = self.population[ant].calculatePathLength(self.distance)
            if pathLength < self.bestPathLength:
                self.bestPathLength = pathLength
                self.bestPath = self.population[ant].path
                
    def updatePheromones(self, evaporationRate: float, pheromoneScaleFactor: float) -> None:
        self.pheromones *= (1 - evaporationRate)
        for ant in range(self.antCount):
            path = self.population[ant].path
            
            pathLength = self.population[ant].pathLength
            for i in range(1,self.totalPoints):
                self.pheromones[path[i-1], path[i]] += pheromoneScaleFactor/pathLength
            # Back to home
            self.pheromones[path[-1], path[0]] += pheromoneScaleFactor/pathLength
        
    def simulate(self, maxIterations:int, alpha:float, beta:float, evaporationRate: float, pheromoneScaleFactor:float, debug:bool=False) -> None:
        for i in range(maxIterations):
            if debug: print("Iteration:", i)
            
            if debug: print("Initializing Ant Population...")
            self.initializeAntPopulation()
            if debug: print("Constructing Routes...")
            self.constructRoutes(alpha, beta)
            if debug:
                print("Best Path Length:", self.bestPathLength)
                print("Updating Pheromones...")
            self.updatePheromones(evaporationRate, pheromoneScaleFactor)


def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="filename", help="Filepath for the file containing city coordinates", required=True)
    parser.add_argument("--debug", dest="debug", action="store_true", help="Flag to enable print statements")
    parser.add_argument("--saveplot", dest="saveplot", help="Save plots instead of displaying them")

    args = parser.parse_args()
    
    if not path.isfile(args.filename):
        print(f"{args.filename}: File Does Not Exist!")
    
    points = readCities(args.filename)
    
    start = datetime.now()
    AS = AntSystem(antCount=10, points=points, initialPheromones=10.0)
    AS.simulate(maxIterations=100, alpha=1, beta=1, evaporationRate=0.36, pheromoneScaleFactor=200.0, debug=args.debug)
    end = datetime.now()
    print("run-time:", end - start)
    
    bestPath = AS.bestPath
    bestPathLength = AS.bestPathLength
    print("Best Path:", bestPath)
    print("Best Path Length:", bestPathLength)
    
    if bestPath:
        if args.saveplot:
            savePlot(points, bestPath, args.saveplot)
        else:
            plotPath(points, bestPath)


if __name__ == "__main__":
    __main__()