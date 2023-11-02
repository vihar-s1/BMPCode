from utils import Chromosome, Cluster
from utils import generateSampleCluster
from objectiveFunc import uavEnergyConsumption, nodeEnergyConsumption, receivedSignalStrengthLoss


INFINITY = 1e20
#! ASSUMING ALL THE OPTIMIZATION OBJECTIVES ARE OF MINIMIZATION


class nsga2:
	def __init__(self, currentLoc: Chromosome, cluster: Cluster, population: list[Chromosome] | None) -> None:
		self.currentLoc = currentLoc
		self.cluster = cluster
		self.population = population
		if population:
			self.popSize = len(population)
			self.genCount  = population[0].geneCount()
			self.set = True  # to keep track of whether population is initialized or not
		else: 
			self.popSize, self.genCount = 0, 0
			self.set = False
        
        
	def initializePopulation(self, popSize:int, geneCount:int, LB:float, UB:float) -> None:
		self.population = [Chromosome(geneCount, LB, UB) for _ in popSize]
		self.popSize, self.genCount = popSize, geneCount
		self.set = True

 
	def estimateFitness(self) -> None:
		"""Set fitness of each individual of the population"""
		if not self.set:
			return 

		for i in range(self.popSize):
			fitness = [
				uavEnergyConsumption(self.population[i], self.currentLoc),
				nodeEnergyConsumption(self.cluster, self.population[i]),
				receivedSignalStrengthLoss(self.cluster, self.population[i])
			]
			self.population[i].setFitness(fitness)
	
 		
def __main__():
    pass
        


if __name__ == "__main__":
    __main__()