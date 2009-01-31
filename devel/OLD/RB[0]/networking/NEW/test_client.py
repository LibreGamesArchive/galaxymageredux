import newnet
from twisted.internet import reactor, threads

class TestClient(newnet.Client):
    def __init__(self, host, port, username):
        newnet.Client.__init__(self, host, port, username)
        self.get_input = True

    def input_received(self, line):
        """Callback for to send out a finished line of input."""
        if line == "q":
            c.close()
        elif len(line) > 0:
            c.avatar.callRemote("sendMessage", line)
        self.get_input = True

    def update(self):
        # Only run this code once at a time!
        if self.get_input:
            # Thread this blocking call, which immediately returns a deferred
            d = threads.deferToThread(raw_input, ":->")

            # Execute function as soon as input is available
            d.addCallback(self.input_received)
            self.get_input = False

c = TestClient("localhost", 44444, "test!")
c.connect()
