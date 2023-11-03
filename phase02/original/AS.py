import random
from sys import argv
import matplotlib.pyplot as plt

def getRandom(lowerBound: float, upperBound: float) -> float:
    return lowerBound + random.random() * (upperBound - lowerBound)


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
        self.population = [Ant(random.randint(0, self.cityCount - 1)) for _ in range(self.antCount)]
        
    
    def constructRoute(self, alpha: float, beta: float) -> None:
        for _ in range(1, self.cityCount):
            for i in range(self.antCount):
                notVisited = set(range(self.cityCount)) - self.population[i].visited
                transitionProb = {}
                for city in notVisited:
                    transitionProb[city] = (self.edgePheromone[i][city] ** alpha) * (self.distMatrix[i][city] ** -beta)
                
                tot = sum(transitionProb.values())
                for key in transitionProb.keys():
                    transitionProb[key] /= tot
                
                nextCity = random.choices(population=transitionProb.keys(), weights=transitionProb.values())
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
                self.edgePheromone[path[0]][[path[1]]] += antRouteLength[i] ** -1
        
    
    def runSimulation(self, initialPheromone: float, alpha: float, beta: float, evaporationRate: float, Tmax: int) -> None:
        if initialPheromone <= 0:
            raise ValueError(f"Initial Pheromone Level must be Positive. {initialPheromone} is invalid")
        if not 0 < evaporationRate < 1:
            raise FloatingPointError(f"EvaporationRate = {evaporationRate} outside of range (0,1)")
        
        self.initializePheromoneTrail(initialPheromone)
        for _ in range(Tmax):
            self.resetAntPop()
            self.constructRoute(alpha, beta)
            self.updatePheromone(evaporationRate)
        

def readCities(filepath: str) -> list[tuple[float, float]]:
    with open(filepath, "r") as data:
        cities = data.readlines()
        cities = [ tuple(map(float, city.split())) for city in cities ]
    
    return cities


def getDistanceMatrix(cities: list[tuple[float, float]]) -> list[list[float]]:
    cityCount = len(cities)
    distMatrix = [[0] ** cityCount] ** cityCount
    for i in range(cities):
        for j in range(i+1, cities):
            dist = ( (cities[i][0] - cities[j][0])**2 + (cities[i][1] - cities[j][1])**2 )**0.5
            distMatrix[i][j] = distMatrix[j][i] = dist
            
    return distMatrix

 
def __main__():
    if len(argv) != 2:
        print(f"usage: {argv[0]} <filepath>\n<filepath>: file containing city co-ordinates")
        exit(1)
    
    cities = readCities(argv[1])
    # distMatrix = getDistanceMatrix(cities)
    cities.sort()
    plt.scatter([city[0] for city in cities], [city[1] for city in cities])
    # plt.plot([city[0] for city in cities], [city[1] for city in cities])
    plt.grid(visible=True)
    plt.show()
    

if __name__ == "__main__":
    __main__()
    