import random

from math import sqrt, log10, pi
from utils import Chromosome, Node, Cluster

parameters = {
    "horizontalVelocity" : 1, # meter/second --> UAV horizontal-velocity
    "verticalVelocity" : 1,   # meter/second --> UAV vertical-velocity
    
    "e_fs" : 1, # Amplifier coefficients of free space
    "e_mp" : 1, # Amplifier coefficients of multipath communication
    "E_elec": 1, # Transceiver energy consumption (J per bit)
    "d": 500, # Transimission distance (metre)
    "k": 16, # Data packet bit count
    
    "f": 2400, # Transmission Frequency in MHz
    "D0": 1, # Reference distance in meters
    "C": 5, #. WHAT IS IT ?? 
    "eta": 1.0, # Path Loss Index
    "signma": 2, # S.D. of Gaussian Arbitary Variable G_signma of zero mean
    "m": 50, # Number of nodes in cluster
    "Pt": 1, # Signal Transmit Power (in dBm) on nodes
}


def changeParameter(parameter: str, value: float) -> None:
    global parameters
    if parameter in parameters.keys():
        parameters[parameter] = value


def uavEnergyConsumption(target: Chromosome, current: Chromosome) -> float | None:
    """
    returns (float) Energy Expanded by UAV in moving from "current" position to "target" position in 3D Space.
    "target" and "current" chromosomes must have exactly 3 genes. If not, returns None
    """
    if target.geneCount() != 3 or current.geneCount() != 3:
        return None
    
    xt, yt, zt = target.genes
    xc, yc, zc = current.genes
    
    # horizontal movement
    horizontalDist = sqrt( (xt-xc)**2 + (yt-yc)**2 )
    consumption = 308.709 * (horizontalDist / parameters["horizontalVelocity"]) - 0.852
    
    if zt > zc:  # moving up
        consumption += 315 * (zt - zc) - 0.852
    elif zt < zc:  # moving down
        consumption += 68.956 * (zc - zt) - 65.183
        
    return consumption
        

def nodeEnergyConsumption(cluster: Cluster, sink: Chromosome) -> float:
    """Calculate total energy consumed by all nodes of the cluster "cluster" in transmitting the data to UAV at location "sink"."""
    consumption = 0.0
    d0 = sqrt(parameters["e_fs"] / parameters["e_mp"])
    
    # transceiverEnergy = data packet bits * energy per bit
    # consumption = sum {
    #       k * E_elec + k * e_fs * dist^2 if dist < d0
    #       k * E_elec + k * e_mp * dist^4 if dist >= d0
    # }
    for node in cluster.IoTDevices:
        dist = sqrt( (sink.genes[0] - node.location[0])**2 + (sink.genes[1] - node.location[1])**2 + (sink.genes[2] - node.location[2])**2 )
        consumption += node.k * parameters["E_elec"]
        if dist < d0:
            consumption += node.k * parameters["e_fs"] * (dist ** 2)
        else:
            consumption += node.k * parameters["e_mp"] * (dist ** 4)
        
    return consumption


# to make all objective functions a minimization problem, 
# focus is maintained on path loss of transmitted signal instead of 
# RSSI at UAV. 
# The difference is that instead of focusing on average signal strength recieved
# at UAV, the average signal strength lost at UAV is calculated.

def receivedSignalStrengthLoss(cluster: Cluster, sink: Chromosome):
    """average Received Signal Strength loss at UAV located at "Sink"."""
    # RSSI = sum ( P_t - 20log10(4pi*D0*f/C) - 10eta*log10(dist/D0) - G_signma ) / m
    # RSSI = sum (P_t - loss) / m
    m = cluster.size()
    
    loss = 0.0
    for node in cluster.IoTDevices:
        dist = sqrt( (sink.genes[0] - node.location[0])**2 + (sink.genes[1] - node.location[1])**2 + (sink.genes[2] - node.location[2])**2 )
        # calculating Gaussian Noise
        G_sigma = random.gauss(0, parameters["signma"])
        
        loss += 20 * log10(4 * pi * parameters["D0"] * node.freq / parameters["C"]) + 10 * parameters["eta"] * log10(dist / parameters["D0"]) + G_sigma
        
    loss /= m
    return loss


if __name__ == "__main__":
    print(parameters["horizontalVelocity"])
    changeParameter("horizontalVelocity", 10.4)
    print(parameters["horizontalVelocity"])