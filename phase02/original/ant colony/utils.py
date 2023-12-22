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


def readPoints(filepath: str) -> np.ndarray[np.dtype[np.float64]]:  # type: ignore
    with open(filepath, "r") as data:
        points = data.readlines()
        points = [tuple(map(float, city.split(","))) for city in points]

    return np.array(points)


def plotPath(points: np.ndarray, path: list[int]) -> None:
    fig = plt.figure()
    
    axes = plt.axes(projection="3d")
    fig.add_axes(axes)
    axes.plot(points[path][:,0], points[path][:,1], points[path][:,2])
    axes.set_xlabel("X-Coordinate")
    axes.set_ylabel("Y-Coordinate")
    axes.set_zlabel("Z-Coordinate")
    
    plt.show()


def savePlot(points: np.ndarray, path: list[int], filename: str) -> None:
    fig = plt.figure()
    axes = plt.axes(projection="3d")
    fig.add_axes(axes)
    axes.plot(points[path][:,0], points[path][:,1], points[path][:,2])
    axes.set_xlabel("X-Coordinate")
    axes.set_ylabel("Y-Coordinate")
    axes.set_zlabel("Z-Coordinate")
    fig.savefig(filename)


def saveIterationPlot(data: list, dataLabel: str, filename) -> None:
    plt.close()
    plt.grid()
    plt.plot(data)
    plt.xlabel("Iterations")
    plt.ylabel(dataLabel)
    plt.savefig(filename)
    

def printMatrix(mat: list[list[float]]) -> None:
    for row in mat:
        for val in row:
            print(f"{val:.3f}", end=" ")
        print()


def plotweights(data: np.ndarray, weights: np.ndarray, widthFactor: int) -> None:
    plt.close()
    plt.scatter(data[:,0],data[:,1])
    totalPoints = len(data)
    for i in range(totalPoints):
        for j in range(totalPoints):
            if float(f"{weights[i][j]:.4f}") != 0:
                plt.plot([data[i,0], data[j,0]], [data[i,1], data[j,1]])
    plt.grid()
    plt.show()
    