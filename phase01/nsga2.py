from utils import Chromosome, Cluster
from utils import generateSampleCluster
from objectiveFunc import uavEnergyConsumption, nodeEnergyConsumption, receivedSignalStrengthLoss


INFINITY = 1e20
#! ASSUMING ALL THE OPTIMIZATION OBJECTIVES ARE OF MINIMIZATION


class nsga2:
	def __init__(self, currentLoc: Chromosome, cluster: Cluster) -> None:
		self.currentLoc = currentLoc
		self.cluster = cluster
		lowerBoundX = min([ device.location[0] for device in cluster.IoTDevices ])
		lowerBoundY = min([ device.location[1] for device in cluster.IoTDevices ])
		lowerBoundZ = min([ device.location[2] for device in cluster.IoTDevices ])
		upperBoundX = max([ device.location[0] for device in cluster.IoTDevices ])
		upperBoundY = max([ device.location[1] for device in cluster.IoTDevices ])
		upperBoundZ = max([ device.location[2] for device in cluster.IoTDevices ])

		if lowerBoundZ == upperBoundZ == 0:
			lowerBoundZ = INFINITY
			upperBoundZ = -INFINITY
   
		self.lowerBound = min([lowerBoundX, lowerBoundY, lowerBoundZ])
		self.upperBound = max([upperBoundX, upperBoundY, upperBoundZ])
		self.set = False # used to check if population is set or not
        
        
	def initializePopulation(self, popSize:int, geneCount:int, LB:float, UB:float) -> None:
		self.population = [Chromosome(geneCount, LB, UB) for _ in popSize]
		self.popSize, self.genCount = popSize, geneCount
		self.lowerBound, self.upperBound = LB, UB
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
   
	
	def nonDominationSorting(self) -> None:
		#!----------- INCOMPLETE -----------!#
		def anySuperior(j, i):
			jFitness, iFitness = self.population[j].fitness, self.population[i].fitness
			for pair in zip(jFitness, iFitness):
				if pair[0] > pair[1]:
					return True
			return False

		def anyInferior(j, i):
			jFitness, iFitness = self.population[j].fitness, self.population[i].fitness
			for pair in zip(jFitness, iFitness):
				if pair[0] < pair[1]:
					return True
			return False

		if not self.set: return

		for i in range(self.popSize):
			for j in range(self.popSize):
				if i == j: continue
				if anySuperior(j, i) and not anyInferior(j, i):
					pass # mark x_i as dominated
	
 
	def run(self, Tmax: int, popSize:int=None, geneCount:int=None):
		if not self.set and (not popSize or not geneCount):
			return
		if not self.set:
			self.initializePopulation(popSize, geneCount, self.lowerBound, self.upperBound)
		self.estimateFitness()


		
	
 		
def __main__():
    pass
        


if __name__ == "__main__":
    __main__()