import random, datetime

class Chromosome:
    def __init__(self, geneCount:int, LB:float, UB:float) -> None:
        self.genes = [random.random() * (UB-LB) + LB for _ in geneCount]
        self.fitness = []

    def geneCount(self) -> int:
        return len(self.genes)
    
    def setFitness(self, fitness: tuple[float]) -> None:
        self.fitness = fitness
    

class Node:
    def __init__(self, k: int, loc: tuple[float, float, float], frequency: float) -> None:
        """
        k   : data packet bit count
        loc : Node location
        frequency: Node Transmission Frequency (in MHz)
        """
        self.k = k # data packet bit count
        self.location = loc # node location
        self.freq = frequency
        
        
class Cluster:
    def __init__(self, IoTDevices: list[Node]) -> None:
        self.IoTDevices = IoTDevices
        
    def size(self):
        return len(self.IoTDevices)


def generateSampleCluster(LB: float, UB: float, hasZ: bool=False) -> str:
	file = "./clusters/sampleCluster_" + str(datetime.datetime.now().timestamp()).replace(".", "") + ".csv"
	with open(file, "w") as sampleCluster:
		for _ in range(100):
			x, y, z = LB + random.random() * (UB-LB), LB + random.random() * (UB-LB), 0
			if hasZ:
				z = LB + random.random() * (UB-LB)
			sampleCluster.write(f"{x:.3f}, {y:.3f}, {z:.3f}\n")
	
	return file