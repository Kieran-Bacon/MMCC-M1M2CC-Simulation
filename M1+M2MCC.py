from Simulation import M1M2CC
from Event import M1M2Event as Event
from pylab import *
from math import factorial

def blockingProbability(num_clients: int, threshold: int, ho_rate: float, \
                        c_rate: float, d_rate: float) -> float:
    """ Blocking probability function for a m1/m2/m/c/c type simulation, it 
    gives consideration to both paths of arrival and the priority aspects of
    each path. This function unfortunately did not provide reasonable results 
    for the validity checking but I have left is in as a work in progress.

    Params:
        - num_clients: The number of arrivals the system is to experience from 
                       both paths.
        - threshold: The number of reserved servers in the system for the hand 
                     over path.
        - ho_rate: The hand over arrival rate.
        - c_rate: The new call arrival rate.
        - d_rate: The departure rate for a given arrival.

    Returns:
        - float: Blocking probability of the simulation set up.
    """

    diff = num_clients - threshold

    a = sum([(factorial(k)**-1)*(((ho_rate+c_rate)/d_rate)**k) for k in range(diff)])
    b = 0
    for k in range(diff + 1, num_clients):
        x = (((num_clients-factorial(threshold))*factorial(k-(diff)))**-1)
        y = (((ho_rate+c_rate)/d_rate)**(diff))
        z = ((ho_rate/d_rate)**(k-num_clients+threshold))
        b += x*y*z

    p0 = a + b

    a = ((num_clients-factorial(threshold))*factorial(threshold))**-1
    b = ((ho_rate + c_rate)/d_rate)**(diff)
    c = (ho_rate/d_rate)**num_clients

    return a*b*c*(p0**-1)

if __name__ == "__main__":

    matplotlib.pyplot.show() # Prepare python for plotting
    machine = M1M2CC()       # Construct a simulation object
    
    # Initialise investigation parameters
    handover_range = logspace(-6, -1, 50) # Range of hand over arrival rate
    Event.priorities["newcall"] = 0.1             # Set new call arrival rate
    Event.departure_rate = 0.01

    prob_blocking = []

    for p in handover_range:
        Event.priorities["handover"] = p
        machine.run(16,10000,2)
        prob_blocking.append(machine.blockingProbability())

    figure()
    plot(handover_range, prob_blocking, "b*", label="ABP blocking percentage")
    plot([handover_range[0], handover_range[-1]], [0.02]*2, \
        'r--', label="Target probability of 0.02")
    ylabel("ABP blocking probability")
    xlabel("Handover arrival rate")
    legend()
    xlim(handover_range[0], handover_range[-1])
    xscale("log")
    show(block=True)

    call_range = linspace(0.01, 0.08, 50)
    Event.priorities["handover"] = 0.03
    Event.departure_rate = 0.01

    prob_blocking = []
    index, best_prob = 0 , 0

    for i, c in enumerate(call_range):
        Event.priorities["newcall"] = c
        machine.run(16,10000,2)
        prob = machine.blockingProbability()
        if prob < 0.02: index, best_prob = i, prob
        prob_blocking.append(prob)

    print("Report from rerun on best proposed call arrival rate:")
    Event.priorities["newcall"] = call_range[index]
    machine.run(16,10000,2)
    machine.report()
    print("")
    
    print("For Aggregated blocking rate below 0.02:")
    print("\tCall arrival value:", call_range[index])
    print("\tBlocking value:", best_prob)

    figure()
    plot(call_range, prob_blocking, "b*", label="ABP blocking percentage")
    plot([0.01, call_range[index]], [prob_blocking[index]]*2, "r--", \
        label="Setup with probability under 0.02")
    plot([call_range[index]]*2, [-0.0005, prob_blocking[index]], "r--")
    ylabel("ABP blocking probability")
    xlabel("New call arrival rate")
    xlim(0.01,0.08)
    ylim(-0.005, 0.2)
    legend()
    show(block=True)