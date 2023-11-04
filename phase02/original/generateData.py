from sys import argv
import random


def getRandom(lowerBound: float, upperBound: float) -> float:
    return lowerBound + random.random() * (upperBound - lowerBound)


def generatePoints(cityCount: int, lowerBound: float, upperBound: float, filename: str) -> None:
    cities = [(getRandom(lowerBound, upperBound), getRandom(lowerBound, upperBound)) for _ in range(cityCount)]
    
    with open(filename, "w") as file:
        for city in cities:
            file.write(f"{city[0]:.3f},{city[1]:.3f}\n")
    

def __main__():
    dataset_count = int(argv[1])
    for i in range(dataset_count):
        # generate 15-25 cities located in squared area of side-length 100-200 m
        generatePoints(random.randint(15, 25), 0, random.random() * 100 + 100, f"data/cities_{i:02d}.csv")


if __name__ == "__main__":
    __main__()