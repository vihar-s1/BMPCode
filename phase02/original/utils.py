import matplotlib.pyplot as plt
import numpy as np
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
       

def readCities(filepath: str) -> np.ndarray[np.dtype[np.float64]]: #type: ignore
    with open(filepath, "r") as data:
        cities = data.readlines()
        cities = [ tuple(map(float, city.split(","))) for city in cities ]
    
    return np.array(cities)


def plotPath(points: np.ndarray, path: list[int]) -> None:
    plt.grid(visible=True)
    plt.scatter(points[path][:,0], points[path][:,1])
    plt.plot(points[path][:,0], points[path][:,1])
    plt.xlabel("x coordinates")
    plt.ylabel("y coordinates")
    plt.show()


def savePlot(points: np.ndarray, path: list[int], filename: str) -> None:
    plt.grid(visible=True)
    pointpath = points[path]
    plt.scatter(pointpath[:,0], pointpath[:,1])
    plt.plot(pointpath[:,0], pointpath[:,1])
    plt.xlabel("x coordinates")
    plt.ylabel("y coordinates")
    plt.savefig(filename)
    