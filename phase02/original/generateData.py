import argparse
import random
from utils import getRandom


def generatePoints(totalPoints: int, lowerBound: float, upperBound: float, filename: str) -> None:
    points = [(getRandom(lowerBound, upperBound), getRandom(lowerBound, upperBound)) for _ in range(totalPoints)]
    
    with open(filename, "w") as file:
        for point in points:
            file.write(f"{point[0]:.3f},{point[1]:.3f}\n")


def generate3dPoints(totalPoints: int, lowerBound: float, upperBound: float, zMin: float, zMax: float, filename: str) -> None:
    points = [(getRandom(lowerBound, upperBound), getRandom(lowerBound, upperBound), getRandom(zMin, zMax)) for _ in range(totalPoints)]
    
    with open(filename, "w") as file:
        for point in points:
            file.write(f"{point[0]:.3f},{point[1]:.3f},{point[2]:.3f}\n")
    

def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", dest="datasetCount", help="Number of dataset to be created", required=True)
    parser.add_argument("-3d", dest="threeDim", action="store_true", help="Set flag to generate 3D dataset points")
    
    args = parser.parse_args()
    
    if args.threeDim:
        for i in range(int(args.datasetCount)):
            # generate 30-50 points located in cuboidal space of side-length 100-200 m at altitude of 100 to 200 m
            zMin, zMax = 100, 200
            zMin, zMax = 100, 200
            generate3dPoints(random.randint(30, 50), 0, random.random() * 100 + 100, zMin, zMax, f"data/points3D_{i:03d}.csv")
    else:
        for i in range(int(args.datasetCount)):
            # generate 30-50 points located in squared area of side-length 100-200 m
            generatePoints(random.randint(30,50), 0, random.random() * 100 + 100, f"data/points2D_{i:03d}.csv")

if __name__ == "__main__":
    __main__()