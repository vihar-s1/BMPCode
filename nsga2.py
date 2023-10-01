import random
from objectiveFunc import objFunc1, objFunc2, objFunc3, parameters

INFINITY = 1e20
#! ASSUMING ALL THE OPTIMIZATION OBJECTIVES ARE OF MAXIMIZATION

def initializePopulation(populationSize: int, geneCount: int, lowerBound: float, upperBound: float) -> list[list[float]]:
	"""Randomly initialize the population space of chromosomes inside given lower-bound and upper-bound

	Args:
		populationSize (int): number of chromosomes in population
		geneCount (int): number of genes in a population chromosome
		lowerBound (float): lower-bound on the chromosome values
		upperBound (float): upper-bound on the chromosome values

	Returns:
		list[list[float]]: `populationSize` no. of chromosomes each containing `geneCount` no of genes
	"""
	population = [[-1] * geneCount] * populationSize
	for i in range(populationSize):
		for j in range(geneCount):
			population[i][j] = lowerBound + random.random() * (upperBound - lowerBound)
	
	return population


def nonDominationSorting(population: list[list[float]], populationSize: int, geneCount: int) -> list[list[float]]:
	"""Selects the non-dominated (dominating) chromosomes from the given population

	Args:
		population (list[list[float]]): the list of chromosomes
		populationSize (int): count of chromosomes
		geneCount (int): no. of genes in each chromosome

	Returns:
		list[list[float]]: returns the list of non-dominated (dominating) chromosomes from the population
	"""
	def anySuperior(j, i):
		for g in range(geneCount):
			if population[j][g] > population[i][g]:
				return True
		return False

	def anyInferior(j, i):
		for g in range(geneCount):
			if population[j][g] < population[i][g]:
				return True
		return False


	dominated = [False] * populationSize
	for i in range(populationSize):
		for j in range(populationSize):
			if population[i] == population[j]: continue
			if anySuperior(j, i) and not anyInferior(j, i):
				dominated[i] = True

	nonDominated = []
	for i in range(populationSize):
		if not dominated[i]: nonDominated.append(population[i])
	
	return nonDominated


def SORT(paretoFront: list[list[float]], objFunc, k: int) -> list[list[float]]:
    return paretoFront


def calculateObjFuncVal(objFunc: int, paretoFront: list[list[float]], referencePoint: list[float]) -> float | dict[tuple, float]:
	"""Calculating objective function values for each of the 3D points in the paretoFront

	Args:
		objFunc (int): 1, 2, or 3 to determine the function to use
		paretoFront (list[list[float]]): the set of points forming the pareto Front
		referencePoint (list[float]): the sink location or the previous point

	Returns:
		float | dict[tuple, float]: returns dictionary of distance to reach each node if objFunc = 1,
  	sum of node transmission energy if objFunc = 2, and average RSSI value if objFunc = 3
	"""
	values = {}
	if objFunc == 1:
		for chromosome in paretoFront:
			values[tuple(chromosome)] = objFunc1(referencePoint, chromosome)
	elif objFunc == 2:
		values = 0.0
		for chromosome in paretoFront:
			values += objFunc2(chromosome, referencePoint)

	elif objFunc == 3:
		values = 0.0
		for chromosome in paretoFront:
			values += objFunc3(chromosome, referencePoint)
		values /= parameters["m"]
	else:
		return None


def getCrowdingDistance(objFunc, paretoFront: list[list[float]], populationSize: int, geneCount: int) -> dict[tuple, float]:
	crowdingDist = [0] * populationSize
	objFuncVal = calculateObjFuncVal(objFunc, paretoFront)

	objFuncVal_min, objFuncVal_max = min(objFuncVal.values()), max(objFuncVal.values())
 
	for k in range(len(objFunc)):
		paretoFront = SORT(paretoFront, objFunc, k)
  
		crowdingDist[tuple(paretoFront[0])] = crowdingDist[tuple(paretoFront[-1])] = INFINITY
  
		for i in range(2, populationSize):
			# crowdingDist[i] = crowdingDist[i] + (fk_(i+1) - fk_(i-1)) / (fk_max - fk_min)
			prev = objFuncVal[ tuple(paretoFront[i-1]) ]
			next = objFuncVal[ tuple(paretoFront[i+1]) ]
			crowdingDist[tuple(paretoFront[i])] += (next - prev) / (objFuncVal_max - objFuncVal_min)

	return crowdingDist


if __name__ == "__main__":
	pass