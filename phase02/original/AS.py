import random, argparse
from datetime import datetime
from sys import platform
from os import path, system
import matplotlib.pyplot as plt

def getRandom(lowerBound: float, upperBound: float) -> float:
    return lowerBound + random.random() * (upperBound - lowerBound)

def clrscr():
    if platform == "win32":
        system("cls")
    else:
        system("clear")


class Ant:
    def __init__(self, startingCity: int, totalCities: int) -> None:
        self.currentCity = startingCity  # the city in which ant currently is
        self.totalCities = totalCities  # total number of cities in the network
        self.route = list[tuple[int, int]]()  # edges the ant visits on its tour
        self.visited = { startingCity }  # the cities ant already visited
        
        
    def pathComplete(self) -> bool:
        return len(self.visited) == self.totalCities
    
    
    def addNextCity(self, city) -> bool:
        if not city in self.visited and not self.pathComplete():
            self.route.append((self.currentCity, city))
            self.currentCity = city
            self.visited.add(city)
            return True
        return False
    
    
    def hasVisited(self, city: int) -> bool:
        return city in self.visited
    
    
    def pathLength(self, distMatrix: list[list[float]]) -> float:
        pathLength = 0
        for path in self.route:
            pathLength += distMatrix[path[0]][path[1]]
        return pathLength
        

class AntSystem:
    def __init__(self, antCount: int, cityCount: int, distMatrix: list[list[float]]) -> None:
        self.antCount = antCount
        self.cityCount = cityCount
        
        if len(distMatrix) == cityCount:
            for distRow in distMatrix:
                if len(distRow) != cityCount:
                    raise ValueError("distMatrix must be of size (cityCount, cityCount)")
        
        self.distMatrix = distMatrix
        self.popSet = False # to check if population is set or not
        
    
    def initializePheromoneTrail(self, initialPheromone: float) -> None:
        if initialPheromone <= 0:
            raise ValueError(f"Initial Pheromone Level must be Positive. {initialPheromone} is invalid")
        self.edgePheromone = [[initialPheromone for _ in range(self.cityCount)] for _ in range(self.cityCount)]
        
    
    def resetAntPop(self) -> None:
        self.population = [Ant(random.randint(0, self.cityCount - 1), self.cityCount) for _ in range(self.antCount)]
        
    
    def constructRoute(self, alpha: float, beta: float) -> None:
        for i in range(1, self.cityCount):
            for j in range(self.antCount):
                notVisited = set(range(self.cityCount)) - self.population[j].visited
                if not notVisited: return
                
                transitionProb = {}
                for city in notVisited:
                    transitionProb[city] = (self.edgePheromone[i][city] ** alpha) * (self.distMatrix[i][city] ** -beta)
                
                tot = sum(transitionProb.values())
                if tot != 0:
                    for key in transitionProb.keys():
                        transitionProb[key] /= tot
                else:
                    for key in transitionProb.keys():
                        transitionProb[key] = 1
                nextCity = random.choices(population=list(transitionProb.keys()), weights=list(transitionProb.values()))
                self.population[i].addNextCity(nextCity[0])
                
    
    def updatePheromone(self, evaporationRate: float) -> None:
        if not 0 < evaporationRate < 1:
            raise FloatingPointError(f"EvaporationRate = {evaporationRate} outside of range (0,1)")
        
        antRouteLength = [ self.population[i].pathLength(self.distMatrix) for i in range(self.antCount) ]
        
        # Performing pheromone evaporation
        self.edgePheromone = [[(1-evaporationRate) * self.edgePheromone[i][j] for j in range(self.cityCount)] for i in range(self.cityCount) ]
        
        # Pheromone released by the ants over the path
        for i in range(self.antCount):
            for path in self.population[i].route:
                self.edgePheromone[path[0]][path[1]] += antRouteLength[i] ** -1
        
    
    def runSimulation(self, initialPheromone: float, alpha: float, beta: float, evaporationRate: float=0.2, Tmax: int=10_000, debug: bool=False) -> None:
        if initialPheromone <= 0:
            raise ValueError(f"Initial Pheromone Level must be Positive. {initialPheromone} is invalid")
        if not 0 < evaporationRate < 1:
            raise FloatingPointError(f"EvaporationRate = {evaporationRate} outside of range (0,1)")
        
        if debug: print("Initializing Pheromone Trail...")
        self.initializePheromoneTrail(initialPheromone)
        
        if debug: print("Running Iterations...")
        
        for t in range(Tmax):
            if debug: print("Iteration:",t)
            
            if debug: print("Setting Ants at starting Position...")
            self.resetAntPop()
            
            if debug: print("Constructing Routes...")
            self.constructRoute(alpha, beta)
            
            if debug: print("Updating Pheromones...")
            self.updatePheromone(evaporationRate)
            if debug: clrscr()
                    
        if debug: print("Simulation Complete")
        