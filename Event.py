from numpy import log
import random

class Event:
    """ Class object to represent an event that occurs during the simulation """

    arrivalRate = 0.1     # Static arrival rate of all events
    departureRate = 0.01  # Static departure rate of all events

    def expon(mean_rate: float) -> float:
        """ Calculate a random value from a exponential distribution around a
        specified mean.

        Params:
            - mean_rate :: the mean of the exponential distribution.

        Returns:
            - float :: the randomly generated value for time.
        """
        return - (log(random.random())/mean_rate)

    def __init__(self, type: str, time: float):
        """ Initialise the event. Calculate the arrival time and departure time 
        of the event, from a given time instance.

        Params:
            - type :: Identification of state of event.(start/arrival/departure)
            - time :: A time setting, expected to be the simulation time at the 
                      point of creation.
        """

        # Record type
        self.type = type
        # Calculate the arrival time using an exponential distribution
        self.arrival_time = time + Event.expon(Event.arrivalRate)
        # Calculate the departure time using an exponential distribution 
        self.departure_time = self.arrival_time + Event.expon(Event.departureRate)

    def __str__(self) -> str:
        """ Protected function to allow str() to display an object 
        
        Returns:
            - str :: A string representation of the event.
        """
        return self.type + " event at time: " + str(self.time())

    def time(self) -> float:
        """ Returns the time of the event depending on its type.
        
        Returns:
            - float :: The time of the event depending on the type.
        """
        if self.type == "arrival":
            return self.arrival_time
        return self.departure_time

    def serviceTime(self) -> float:
        """ Return the service time of the event. 
        
        Returns:
            - float :: Difference in time between the arrival and departure of 
                       the event.
        """
        return self.departure_time - self.arrival_time

    def servedBy(self, serverID = None):
        """ Overloaded function to set the server that has been allocated to the
        event, or to return the server ID. As a server can only be allocated to 
        an event that must then depart, the event type is also changed.

        Params :
            - serverID :: The id that represents a server

        Returns:
            - None :: In the event that a server is being set, None is returned.
            - int  :: In the event that no parameter is given, the id of the
                      server of this event is given.
        """

        if serverID:
            self.type = "Departure"   # Change event type
            self.serverID = serverID  # Record server ID
            return

        return self.serverID

class M1M2Event(Event):
    """ Event object responsible for recording the time for the event and the 
    type of event. The path on which the event affects the mean of the times
    exponential distribution.
    """
    # Static arrival rates for the hand over and new call paths
    priorities = {"handover":0.1, "newcall": 0.1}  
    departureRate = 0.01   # Static departure rates for events

    def __init__(self,path, type, time):
        """ Initialise the values for the event """
        self.path = path
        self.type = type
        self.arrival_time = time + Event.expon(M1M2Event.priorities[path])
        self.departure_time = self.arrival_time + Event.expon(M1M2Event.departureRate)
