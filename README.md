# BMPCode

## Phase 01

Contains the python code for the modified NSGA-II and related intermediate algorithms

- `utils.py` contains the code for the supporting classes used in the main algorithm and the sample data generation functions.
- `objectiveFunc.py` defines objective functions to be minimized.
- `nsga2.py` contains the main NSGA-II algorithm applied to find optimal UHP for a cluster.

### Classes

#### Chromosome

- A Chromosome class instance denotes an individual of the population of the possible UHPs.
- It contains the corresponding genes or location co-ordinates for UHP, and the corresponding fitness value for each objective function.

#### Node

- Node class instance is for the IoT devices on the ground, i.e., ground nodes (GNs).
- It stores the number of bits in the GN's data packet, GN location, and its transmission frequency in MHz.

#### Cluster

- Contains a list of Node representing the IoT Devices belonging to that cluster

#### NSGA2

- The main class containing various steps of the NSGA-II algorithm as class instance functions.
- The class uses all of the above defined classes to implement the logic of the algorithm.

### Extra Functions

| Functions | Description |
| --------- | ----------- |
| utils.generateSampleCluster | generates a sample cluster according to the given paramaters, stores it in a CSV file and returns the file path. |
| objectFunc.changeParameter | Change constant parameters used in the algorithm. |
| objectiveFunc.uavEnergyConsumption | calculates the energy consumed by the UAV in moving from one location to another in three dimensions. |
| objectiveFunc.clusterEnergyConsumption | calculates the total energy expended by all nodes in a cluster in transmitting the data to the UAV sink hovering at a particular location |
| objectiveFunc.receivedSignalStrengthLoss | the average signal strength lost when a cluster node transmits the data to the UAV sink hovering at a particular location |

## Phase 02

Contains the python code for SSMFAS altered for UAV tour and related intermediate algorithms

- The folder `original` contains the original algorithms implemented directly from the papers.
- `ssmfas.py` contains the SSMFAS algorithm implementation.

### "Original" folder

- `AS.py` contains the code for Ant System Algorithm to solve Travelling Salesman Problem.
- `generateData.py` generates sample city data.
