import matplotlib.pyplot as plt
import random
from sys import platform
from os import system

def getRandom(lowerBound: float, upperBound: float) -> float:
    return lowerBound + random.random() * (upperBound - lowerBound)

def clrscr():
    if platform == "win32":
        system("cls")
    else:
        system("clear")
        

def readCities(filepath: str) -> list[tuple[float, float]]:
    with open(filepath, "r") as data:
        cities = data.readlines()
        cities = [ tuple(map(float, city.split(","))) for city in cities ]
    
    return cities # type: ignore


def getDistanceMatrix(cities: list[tuple[float, float]]) -> list[list[float]]:
    cityCount = len(cities)
    distMatrix = [[0.0] * cityCount] * cityCount
    for i in range(cityCount):
        for j in range(i+1, cityCount):
            dist = ( (cities[i][0] - cities[j][0])**2 + (cities[i][1] - cities[j][1])**2 )**0.5
            distMatrix[i][j] = distMatrix[j][i] = dist
            
    return distMatrix


def printMatrix(mat: list[list[float]]) -> None:
    for row in mat:
        for val in row:
            print(f"{val:.3f}", end=" ")
        print()
        
        
def plotData(cities: list[tuple[float, float]], edgeWeight: list[list[float]], widthFactor:int) -> None:
    # plt.scatter([city[0] for city in cities], [city[1] for city in cities])
    cityCount = len(cities)
    for i in range(cityCount):
        for j in range(cityCount):
            if float(f"{edgeWeight[i][j]:.4f}") != 0:
                plt.plot([cities[i][0], cities[j][0]], [cities[i][1], cities[j][1]], linewidth=widthFactor*edgeWeight[i][j])
    
    plt.grid(visible=True)
    plt.show()
    