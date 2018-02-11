from Event import Event, M1M2Event

class EventHandler:
    """ Event handler is tasked with managing a collection of events. The events
    that are to be enacted in the future are stored in order of execution
    separately from the blocked or departed events.
    """

    def __init__(self):
        """ Initialise the object variables """
        self.container = []  # Event list of future events
        self.departed = []   # Events that have been resolved
        self.blocked = []    # Arrivals that have been blocked from entry

    def add(self, event: Event) -> None:
        """ Add a new event into the handler correctly into the sorted event
        list.

        Params:
            - event :: Event to be stored in the list
        """

        # Look for index of correct insertation of event
        for i, e in enumerate(self.container):
            if e.time() > event.time():
                self.container.insert(i, event)
                return
        
        # No events in the list or event correctly placed at end of event list.
        self.container.append(event)
    
    def depart(self, event: Event) -> None:
        """ Store the departed event """
        self.departed.append(event)

    def block(self, event: Event) -> None:
        """ Store the blocked event """
        self.blocked.append(event)

    def next(self) -> Event:
        """ Remove the next event from the event list and return the event.

        Returns:
            - Event :: The next event to be enacted in the simulation
        """
        e = self.container[0]
        self.container = self.container[1:]
        return e

class M1M2EventHandler(EventHandler):
    """ Adaptation of the event handler object to have separate collections for
    the hand over rate, new call rate blocked events. Additionally functionality
    to ensure non bias creation of the initial arrival events is introduced
    """

    def __init__(self):
        """ Initialising the data structures for the object """
        self.container = [] # Event list of future events
        self.departed = []  # Events that have departed from the simulation
        self.hblocked = []  # Hand over events that were blocked
        self.nblocked = []  # New call events that were blocked

    def start(self) -> None:
        """ Generate both event types and introduce them into the event list,
        ensuring the no warm up period is included to prevent statistical skew.
        """

        # Create both event types objects
        arrivals = [M1M2Event("handover", "arrival", 0), M1M2Event("newcall", "arrival", 0)]

        # Identify which of the two occur first
        startTime = min([arrivals[0].time(), arrivals[1].time()])

        for e in arrivals:
            # Remove the warm up time from event times
            e.arrival_time = e.arrival_time - startTime
            e.depature_time = e.departure_time - startTime

            # Store the events
            self.add(e)

    def block(self, event: M1M2Event) -> None:
        """ Overwriting Event block function, to include functionality of two 
        different blocked collections

        Params:
            - event: Event to be blocked
        """
        if event.path == "handover":
            self.hblocked.append(event)
        else:
            self.nblocked.append(event)

