import client

class MyApp(object):
    def __init__(self, client):
        self.client = client
        self.running = True

    def is_running(self):
        return self.running

    def loop(self):
        self.client.helper.dispatch("test?")
        self.running = raw_input("->")

c = client.Client(MyApp)
c.connect()
