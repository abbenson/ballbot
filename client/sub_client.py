"""Subscribe to data published by the bot."""

import client

class SubClient(client.Client):

    """Use ZMQ SUB socket to get information about the bot."""

    def __init__(self):
        """Get logger and config, build subscribe socket and set topics."""
        super(SubClient, self).__init__("subscribe")
        self.set_topics()
        self.print_msgs()

    def set_topics(self):
        """"""
        self.sock.setsockopt(zmq.SUBSCRIBE, "motors")

    def print_msgs(self):
        """Print all messages from server."""
        while True:
            print self.sock.recv()
