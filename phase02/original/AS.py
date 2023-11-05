import random
from datetime import datetime
from sys import argv
from os import path
import matplotlib.pyplot as plt

from utils import clrscr, readCities, printMatrix, getDistanceMatrix


INFINITY = 1E32


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
        
        self.bestRoute = []
        self.bestRouteLength = INFINITY
        
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
        self.popSet = True
        self.population = [Ant(random.randint(0, self.cityCount - 1), self.cityCount) for _ in range(self.antCount)]
        
    
    def constructRoute(self, alpha: float, beta: float) -> None:
        if not self.popSet: 
            return
        
        for ant in range(self.antCount):
            notVisited = set(range(self.cityCount)) - self.population[ant].visited
            currentCity = self.population[ant].currentCity
            
            while not self.population[ant].pathComplete():
                transitionProb = {}
                for city in notVisited:
                    transitionProb[city] = (self.edgePheromone[currentCity][city] ** alpha) * (self.distMatrix[currentCity][city] ** -beta)
                
                tot = sum(transitionProb.values())
                # if tot != 0:
                #     for key in transitionProb.keys():
                #         transitionProb[key] /= tot
                if tot == 0:
                    for key in transitionProb.keys():
                        transitionProb[key] = 1.0
                
                nextCity = random.choices(population=list(transitionProb.keys()), weights=list(transitionProb.values()))[0]
                if self.population[ant].addNextCity(nextCity):
                    currentCity = nextCity
                    notVisited.remove(nextCity)
        
            
        self.antRouteLength = [ self.population[i].pathLength(self.distMatrix) for i in range(self.antCount) ]
        
        
    def updateBestPath(self) -> None:
        for i in range(self.antCount):
            if self.antRouteLength[i] < self.bestRouteLength:
                self.bestRoute = self.population[i].route
                self.bestRouteLength = self.antRouteLength[i]
                
    
    def updatePheromone(self, evaporationRate: float, scaleFactor:float) -> None:
        if not 0 < evaporationRate < 1:
            raise FloatingPointError(f"EvaporationRate = {evaporationRate} outside of range (0,1)")
        
        # Performing pheromone evaporation
        self.edgePheromone = [[(1-evaporationRate) * self.edgePheromone[i][j] for j in range(self.cityCount)] for i in range(self.cityCount) ]
        
        # Pheromone released by the ants over the path
        for i in range(self.antCount):
            for path in self.population[i].route:
                self.edgePheromone[path[0]][path[1]] += scaleFactor * (self.antRouteLength[i] ** -1)
        
    
    def runSimulation(self, initialPheromone: float, alpha: float, beta: float, evaporationRate: float=0.2, Tmax: int=10_000, pheromonScaleFactor:float=50, debug: bool=False) -> None:
        if initialPheromone <= 0:
            raise ValueError(f"Initial Pheromone Level must be Positive. {initialPheromone} is invalid")
        if not 0 < evaporationRate < 1:
            raise FloatingPointError(f"EvaporationRate = {evaporationRate} outside of range (0,1)")
        
        if debug: print("Initializing Pheromone Trail...")
        self.initializePheromoneTrail(initialPheromone)
        
        if debug: print("Running Iterations...")
        
        for t in range(Tmax):
            if debug: print("Iteration:", t)
            
            if debug: print("Setting Ants at starting Position...")
            self.resetAntPop()
            
            if debug: print("Constructing Routes...")
            self.constructRoute(alpha, beta)
            
            if debug: 
                print("Smallest Route Created:", min(self.antRouteLength))
                print("Updating Best Path...")
            self.updateBestPath()
            
            if debug: 
                print(f"Shortes Length: {self.bestRouteLength}")
                print(self.bestRoute)
                print("Updating Pheromones...")
            self.updatePheromone(evaporationRate, pheromonScaleFactor)
            if debug: clrscr()
                    
        if debug: print("Simulation Complete")
     


def plotPathPoints(cities: list[tuple[float, float]], path: list[tuple[int, int]]) -> None:
    citiesX, citiesY = [cities[path[0][0]][0]], [cities[path[0][0]][1]]
    for edge in path:
        citiesX.append(cities[edge[1]][0])
        citiesY.append(cities[edge[1]][1])
    
    plt.title("Shortest Path by A.S. Algorithm")
    plt.xlabel("X co-ordinate")
    plt.ylabel("Y co-ordinate")
    plt.scatter([city[0] for city in cities], [city[1] for city in cities])
    plt.plot(citiesX, citiesY)
    # for i in range(len(cities)):
    #     plt.annotate(f"{i}", cities[i])
    
    plt.show()


def __main__():
    if len(argv) < 2 or len(argv) > 4:
        print(f"usage: f{argv[0]} <filepath> [debug]\n<filepath>: filepath for the city coordinates\n[debug]: constant to enable debugging statements")
        exit(1)
    
    if not path.isfile(argv[1]):
        print(f"{argv[1]}: Not A File")
    
    cities = readCities(argv[1])
    distanceMatrix = getDistanceMatrix(cities)
    
    debug = len(argv) == 3 and argv[2] == "debug"
    AS = AntSystem(100, len(cities), distanceMatrix)
    
    start = datetime.now()
    try:
        AS.runSimulation(initialPheromone=10, alpha=1, beta=5, evaporationRate=0.1, Tmax=10_000, pheromonScaleFactor=50, debug=debug)
    except Exception as eobj:
        print(eobj)
    end = datetime.now()
    
    with open(argv[1] + ".output", "w") as outputFile:
        for edge in AS.bestRoute:
            outputFile.write(f"{edge[0]},{edge[1]}\n")
            
    delta = end - start
    print(AS.bestRoute)
    print(AS.bestRouteLength)
    print(delta)
    
    # plotPathPoints(cities, AS.bestRoute)  
    
    
if __name__ == "__main__":
    __main__()