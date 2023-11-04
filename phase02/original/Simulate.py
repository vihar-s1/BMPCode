import matplotlib.pyplot as plt
from sys import argv
from AS import AntSystem
from os import path
from datetime import datetime


def readCities(filepath: str) -> list[tuple[float, float]]:
    with open(filepath, "r") as data:
        cities = data.readlines()
        cities = [ tuple(map(float, city.split(","))) for city in cities ]
    
    return cities


def getDistanceMatrix(cities: list[tuple[float, float]]) -> list[list[float]]:
    cityCount = len(cities)
    distMatrix = [[0] * cityCount] * cityCount
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
        
 
 
def __main__():
    if len(argv) < 2 or len(argv) > 4:
        print(f"usage: f{argv[0]} <filepath> [debug]\n<filepath>: filepath for the city coordinates\n[debug]: constant to enable debugging statements")
        exit(1)
    
    if not path.isfile(argv[1]):
        print(f"{argv[1]}: Not A File")
    
    cities = readCities(argv[1])
    distanceMatrix = getDistanceMatrix(cities)
    
    AS = AntSystem(100, len(cities), distanceMatrix)
    start = datetime.now()
    try:
        debug = len(argv) == 3 and argv[3] == "debug"
        AS.runSimulation(initialPheromone=10, alpha=3, beta=2, evaporationRate=0.3, Tmax=10_000, debug=debug)
    except Exception as eobj:
        print(eobj)
    end = datetime.now()
    
    with open(argv[1] + ".output", "w") as outputFile:
        for row in AS.edgePheromone:
            for value in row:
                outputFile.write(f"{value:.3f},")
            outputFile.write("\n")
            
    printMatrix(AS.edgePheromone)
    plotData(cities, AS.edgePheromone, 25)
    delta = end - start
    print(delta)
    

if __name__ == "__main__":
    __main__()
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-f", dest="filename", help="Filepath containing the city coordinates", required=True)
    # args = parser.parse_args()
    # cities = readCities(args.filename)
    # with open(args.filename + ".output", "r") as outputFile:
    #     edgePheromones = outputFile.readlines()
    
    # edgePheromones = [list(map(float, row.split(","))) for row in edgePheromones]
    # printMatrix(edgePheromones)
    # plotData(cities, edgePheromones, 50)