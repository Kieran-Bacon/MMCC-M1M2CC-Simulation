from Simulation import MMCC
from Event import Event
from pylab import *
from math import factorial

def blockingProbability(num_servers: int, arrival_rate: float, departure_rate: float) -> float:
    """ Static function to be able to analytical determine the expected blocking
    probability for a simulation of MMCC given its parameters.

    Params:
        - num_servers: The number of clients in the simulation
        - arrival_rate: The exponential mean of arrival for the clients
        - departure_rate: the exponential mean of the departure of the clients

    Return:
        - float: Blocking probability of the system
    """
    numerator = double(((arrival_rate/departure_rate)**num_servers)/double(factorial(num_servers)))
    demoninator = sum( [((arrival_rate/departure_rate)**k)/factorial(k) for k in range(1,num_servers)])
    return numerator/demoninator

def serverUtilisation(arrival_rate: float, departure_rate: float) -> float:
    """ Calculate the expected server Utilisation of the system with the given
    parameters.

    Params:
        - arrival_rate: The exponential mean of arrival for the clients
        - departure_rate: the exponential mean of the departure of the clients

    Returns:
        - float: Value representing the server utilisation value

    """
    return arrival_rate/departure_rate


if __name__ == "__main__":

    matplotlib.pyplot.show() # Allow plotting package to display figures
    machine = MMCC()         # Generate simulation machine

    # Initialise investigation parameters
    servers = 16                        # Number of servers in the simulation
    arrival_range = logspace(-2,-1,50)  # Range or arrival values to test
    departure_rate = 0.01               # Departure rate of simulation events
    clients = 10000                     # Number of client arrivals

    # Data structures to hold obversations
    prob_blocking = [] # Probability of blocking evaluated from the simulation
    pred_blocking = [] # Predicted probability of blocking from an analytical model

    utilisation = []      # Recorded utilisation value from the simulation
    pred_utilisation = [] # Predicted utilisation value from an analytical model

    
    # Begin investigation
    index = 0 
    for i, arrival_rate in enumerate(arrival_range):
        Event.arrivalRate = arrival_rate # Set the arrival rate value

        # run the simulation 
        machine.run( total_servers = servers, total_arrival = clients )        

        # Collect the statistical information from the simulation
        probability = machine.blockingProbability()
        
        # Record simulation that yielded a blocking probability less than 0.01
        if probability < 0.01: index = i

        # Add information into data structures
        prob_blocking.append(probability)
        pred_blocking.append(blockingProbability(servers, arrival_rate, departure_rate))

        utilisation.append(machine.serverUtilisation())
        pred_utilisation.append(serverUtilisation(arrival_rate, departure_rate))

    # Display best simulation values
    print("Values for re-run on best arrival rate:")
    Event.arrivalRate = arrival_range[index]
    machine.run(total_servers = servers, total_arrival = clients)
    machine.report()
    print()

    # Statistical information about the progress of the investigation
    difference = [i-j for i, j in zip(prob_blocking, pred_blocking)]
    print("For blocking rate lower than 0.01:")
    print("\tArrival rate:", arrival_range[index])
    print("\tSimulation blocking probability:", prob_blocking[index])
    print("\tSimulations variance from predictions:", sum(difference)/len(difference) )

    # Plot the findings of the investigation for blocking probability
    figure()
    plot(arrival_range, prob_blocking, "b*", label="Simulation blocking percentage")
    plot(arrival_range, pred_blocking, "r--", label="Analytic blocking percentage")
    plot([0.01, arrival_range[index]], [prob_blocking[index]]*2, "y--", label="Setup with probability under 0.01")
    plot([arrival_range[index]]*2, [-0.0005, prob_blocking[index]], "y--")
    legend()
    ylabel("Blocking Probability")
    xlabel("Arrival rate")
    xlim(0.01, 0.1)
    ylim(-0.0005,0.025)
    show(block=True)

    # Plot the findings of the investigation for server utility
    figure()
    plot(arrival_range, utilisation, "b*", label="Utilisation of servers")
    plot(arrival_range, pred_utilisation, "r--", label="Predicted utilisation of servers")
    ylabel("Server Utility")
    xlabel("Arrival rate")
    legend()
    xlim(0.01, 0.1)
    show(block=True)