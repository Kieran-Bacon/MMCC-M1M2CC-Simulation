class Servers:
    """ A collect of server ID, provides a collection of convient functions to 
    interact with a server item. The servers are represented by an integer, 
    these server ids move back and forth from a free and busy list to keep
    track.
    """

    def __init__(self, num_servers: int):
        """ Initialise the server list. Server Ids fall in range 1 - the number
        of servers.
        
        Params:
            - num_servers :: The total number of servers in for the system.
        """
        self.free = list(range(1,num_servers+1))
        self.busy = []

    def __len__(self) -> int:
        """ Protected function allowing len() to determine the number of free
        servers.

        Returns:
            - int :: Number of free servers.abs
        """
        return len(self.free)

    def isFree(self) -> bool:
        """ Query if any servers are free.

        Returns:
            - bool :: True if server free, False if server not free.
        """
        return len(self) > 0

    def allocate(self) -> int:
        """ Remove next freely available server for allocation, record server is
        now busy.

        Returns:
            - int :: ServerID of the now allocated server.
        """
        server, self.free = self.free[0], self.free[1:]
        self.busy.append(server)
        return server

    def deallocate(self, server: int) -> None:
        """ Remove the server from the busy collection and ensure it is ready to
        be accessible for the next arrival event.

        Params:
            - server :: a serverID of a busy server
        """
        self.busy.remove(server)
        self.free.append(server)

