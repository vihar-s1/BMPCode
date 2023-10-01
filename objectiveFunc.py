from math import sqrt, log10, pi

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
    "G_sigma": 2, # Gaussian arbitary variable of zero mean and `sigma` standard deviation
    "m": 50, # Number of nodes in cluster
    "Pt": 1, # Signal Transmit Power (in dBm) on nodes
}


def changeParameter(parameter: str, value: float) -> None:
    global parameters
    if parameter in parameters.keys():
        parameters[parameter] = value


def objFunc1(chromosome_start: list[float], chromosome_final: list[float]) -> float:
    """Energy expended by UAV in flying from start position to end position

    Args:
        chromosome_start (list[float]): The co-ordinates of the UAV's starting position
        chromosome_final (list[float]): The co-ordinates of the UAV's ending position

    Returns:
        float: The amount of energy expended from start to end
    """
    value = 0.0
    if chromosome_final[2] > chromosome_start[2]:
        value += 315.0 * (chromosome_final[2] - chromosome_start[2]) - 0.852
    if chromosome_start[2] > chromosome_final[2]:
        value += 68.956 * (chromosome_start[2] - chromosome_final[2]) - 65.183
    
    horizontalDist = sqrt( (chromosome_final[0] - chromosome_start[0])**2 + (chromosome_final[1] - chromosome_start[1])**2 )
    value += 308.709 * (horizontalDist / parameters["horinzontalVelocity"]) - 0.852
    
    return value


def objFunc2(chromosome_node: list[float], chromosome_sink: list[float]) -> float:
    """Calculate node energy consumption in data transmission to UAV from node

    Args:
        chromosome_node (list[float]): Location of IoT node sending the data
        chromosome_sink (list[float]): Location of the UAV receiving the data

    Returns:
        float: Node energy consumed in the data transmission by an IoT device
    """
    value = 0.0
    dist = sqrt( ( chromosome_node[0] - chromosome_sink[0] )**2 + ( chromosome_node[1] - chromosome_sink[1] )**2 + ( chromosome_node[2] - chromosome_sink[2] )**2 )
    d0 = sqrt( parameters["e_fs"] / parameters["e_mp"] )
    
    if dist < d0:
        value = parameters["k"] * ( parameters["E_elec"] + parameters["e_fs"] * (dist ** 2) )
    else:
        value = parameters["k"] * ( parameters["E_elec"] + parameters["e_mp"] * (dist ** 4) )
    
    return value


def objFunc3(chromosome_node: list[float], chromosome_sink: list[float]) -> float:
    """Calculating RSSI between IoT node and UAV

    Args:
        chromosome_node (list[float]): The IoT node position
        chromosome_sink (list[float]): The position of the UAV (data sink)

    Returns:
        float: RSSI value of between the IoT node and UAV
    """
    dist = sqrt( (chromosome_node[0] - chromosome_sink[0])**2 + (chromosome_node[1] - chromosome_sink[1])**2 + (chromosome_node[2] - chromosome_sink[2])**2 )
    value = 0.0
    value += parameters["Pt"] - 20 * log10(4 * pi * parameters["D0"] * parameters["f"] / parameters["C"]) 
    value -= 10 * parameters["eta"] * log10(dist / parameters["D0"])
    value += parameters["G_sigma"]
    
    return value


if __name__ == "__main__":
    print(parameters["horizontalVelocity"])
    changeParameter("horizontalVelocity", 10.4)
    print(parameters["horizontalVelocity"])