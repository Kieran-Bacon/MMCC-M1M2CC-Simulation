from numpy import *

from EventHandler import EventHandler, M1M2EventHandler
from Servers import Servers
from Event import Event, M1M2Event

class MMCC:
    """ Simulation object tasked with conducting the MMCC system """

    def run(self, total_servers: int, total_arrival :int) -> None:
        """ Begin the simulation of a MMCC system. Process the information until
        termination criteria is meet.

        Params:
            - total_servers :: The number of servers that can handle clients at 
                               any one instance.
            - total_arrival :: The total number of clients that can be handled
                               within the simulation.
        """

        # Initialise the beginning parameters of the simulation
        self.servers = Servers(total_servers) # Set up server handler
        self.events = EventHandler()          # Set up the event handler

        startingEvent = Event("arrival", 0)   # Construct the first event object
        startingEvent.departure_time -= startingEvent.arrival_time # Reset times
        startingEvent.arrival_time = 0        # Reset times

        self.events.add(startingEvent)        # Create the first event

        # Begin iteration of events, record arrivals for checking
        self.num_arrival = 0
        while(self.num_arrival < total_arrival):

            # Collect next event from the event handler
            currentEvent = self.events.next()
            # Update simulation time
            self.sim_time = currentEvent.time()

            if currentEvent.type == "arrival":
                # Arrival event received
                self.num_arrival += 1 # Record number of arrivals

                # Create new arrival event
                self.events.add(Event("arrival", currentEvent.time()))

                # Check if any server is available
                if not self.servers.isFree():
                    self.events.block(currentEvent) # Arriving client is blocked
                    continue
                
                # Begin serving the client.
                currentEvent.servedBy(self.servers.allocate())

                # All event handler to manage departure
                self.events.add(currentEvent)

            else:
                # Departure event received
                self.servers.deallocate(currentEvent.servedBy()) # Free the server
                self.events.depart(currentEvent)                 # Record departure

    def blockingProbability(self) -> float:
        """ Calculate the blocking probability for the previous simulation run.
        
        Returns:
            - float :: Probability of blocking 
        """
        return len(self.events.blocked)/self.num_arrival
 
    def serverUtilisation(self) -> float:
        """ Calculate the server utilisation for the previous simulation run.
        
        Returns:
            - float :: Server utilisation value
        """
        return sum([e.serviceTime() for e in self.events.departed])/self.sim_time

    def report(self) -> None:
        """ Display the results of the simulation is a readible fashion. """
        
        print("\tEvents Handled ::") 
        print("\t\tArrival:", self.num_arrival)
        incomplete = self.num_arrival - (len(self.events.departed) + len(self.events.blocked))
        print("\t\tIncomplete events:", incomplete)
        print("\t\tDeparture:", len(self.events.departed))
        print("\t\tBlocked:", len(self.events.blocked))

        print("\tBlocking rate:", self.blockingProbability())
        print("\tServer Utilisation:", self.serverUtilisation())            

class M1M2CC(MMCC):

    def run(self, total_servers: int, total_arrival :int, threshold: int) -> None:
        """ Begin the simulation and record the system variables during execution.

        Params:
            - total_servers :: The number of servers that can handle clients at 
                               any one instance.
            - total_arrival :: The total number of clients that can be handled 
                               within the simulation.
            - threshold :: The number of servers that must remain open for top 
                           priority callers.
        """

        # Initialise the beginning parameters of the simulation
        self.servers = Servers(total_servers) # Set up server handler
        self.events = M1M2EventHandler()      # Set up the event handler
        self.events.start()                   # Create the first event

        # Begin iteration of events, record arrivals for checking
        self.num_arrival = 0
        self.arrival = {"handover": 0, "newcall": 0}
        while(sum(self.num_arrival) < total_arrival):

            # Collect next event from the event handler
            currentEvent = self.events.next()
            # Update simulation time
            self.sim_time = currentEvent.time()

            if currentEvent.type == "arrival":
                # Arrival event received
                priority = currentEvent.path
                self.num_arrival += 1
                self.arrival[priority] += 1

                # Create new arrival event
                self.events.add(M1M2Event(priority, "arrival", currentEvent.time()))

                # Check server availablity
                if (len(self.servers) > threshold) or \
                   (priority == "handover" and self.servers.isFree()) :
                    
                    # Begin serving the client.
                    currentEvent.servedBy(self.servers.allocate())

                    # All event handler to manage departure
                    self.events.add(currentEvent)
                    continue
                
                # No servers were available therefore the event is blocked
                self.events.block(currentEvent) # Arriving client has been blocked

            else:
                # Departure event received
                self.servers.deallocate(currentEvent.servedBy()) # Free the server
                self.events.depart(currentEvent)                 # Event recorded as departed.

    def blockingProbability(self):
        """ Calculate the blocking probability for the previous simulation run.
        
        Returns:
            - float :: Probability of blocking 
        """

        HFP = len(self.events.hblocked)/self.arrival["handover"] \
              if self.arrival["handover"] else 0
        CBP = len(self.events.nblocked)/self.arrival["newcall"] \
              if self.arrival["newcall"] else 0
        return CBP + (10 * HFP)

    def report(self) -> None:
        """ Display the results of the simulation is a readible fashion. """
        
        print("\tEvents Handled ::") 
        print("\t\tArrival:", self.num_arrival)
        print("\t\tHandover:", self.arrival["handover"])
        print("\t\tNew call:", self.arrival["newcall"])
        incomplete = self.num_arrival - \
            (len(self.events.departed) + len(self.events.hblocked) + len(self.events.nblocked))
        print("\t\tIncomplete events:", incomplete)
        print("\t\tDeparture:", len(self.events.departed))
        print("\t\tBlocked:", len(self.events.hblocked) + len(self.events.nblocked))
        print("\t\tHandover blocked:", len(self.events.hblocked))
        print("\t\tNew call blocked:", len(self.events.nblocked))

        print("\tBlocking rate:", self.blockingProbability())
        print("\tServer Utilisation:", self.serverUtilisation())  


